import json
import os
import sys
from datetime import date
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from dash import Output, Input, html, dcc

from h3 import latlng_to_cell

# sys.path.append(str(Path(__file__).parent))
# sys.path.append(str(Path(__file__).parent / 'app'))

from app import generate_layers, generate_colorbar
from app.utils import *
import geopandas as gpd
import pandas as pd

# Initialization

#ASSETS_ROOT = Path("C:/FinalProjectDS4010A - repair/data/assets")

ASSETS_ROOT = Path(os.getenv('ASSETS_ROOT'))
CELL_RESOLUTION = 3
data = gpd.read_parquet(ASSETS_ROOT / 'model_output.parquet')

#Gets min and max date from the data
min_date = data['date'].min().date()
max_date = data['date'].max().date()

#Generates Date Range
date_range = pd.date_range(start=min_date, end=max_date, freq="D")

#Labels the slider every 6 months
date_marks = {
    i: d.strftime("%b %Y")
    for i, d in enumerate(date_range)
    if d.day == 1 and d.month in [1, 7]  # Jan and July
}

#Maps the date and index to each other
date_to_index = {d.date(): i for i, d in enumerate(date_range)}
index_to_date = {i: d.date() for i, d in enumerate(date_range)}

#Gets all available dates instead of timestamps
available_dates = list(date_range.date)


# hex_ids = data['Hexagon_ID'].unique().tolist()  # TODO DON'T THINK THIS IS NEEDED ANYMORE

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY],
                suppress_callback_exceptions=True)
server = app.server

app.layout = html.Div([
    html.H2("Wildfire Dashboard", style={'textAlign': 'center'}),
    dcc.Tabs(id='tabs', value='map-tab', children=[
        dcc.Tab(label='Map View', value='map-tab'),
        dcc.Tab(label="Time Series Plot", value='plot-tab'),
        dcc.Tab(label="Dashboard Info", value='info-tab')
    ]),

    html.Div(id='tabs-content')
    
    
])


@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    """
    Generates and returns Tabs
    :param tab:
    :return:
    """
    if tab == 'map-tab':
        return html.Div([
            html.Div([
                html.Div([
                     html.H3("Map"),
                     dl.Map(children=[
                     dl.TileLayer(),
                     dl.LayersControl(id="lc", collapsed=False, position="bottomright", children=[
                    ])
                ], center=[40, -95], zoom=4, style={'height': '50vh'}, id="map"),

                    html.Div(id="colorbar", style={"height": "30px", "margin": "20px 20px"}),
                    html.Button("Recenter", id="recenter"),
                ], style={'width': '75%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '20px'}),
                html.Div([
                    html.H3("Model"),
                    html.Div(id='output-container'),
                ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top',
                          'backgroundColor': '#e9ecef', 'padding': '10px'})
            ], style={'width': '100%', 'display': 'block'}),
            #Tells selected date based on the slider
             html.Div([
                html.Div([
                    html.H3('Selected Date: ', style={'display': 'inline-block', 'marginRight': '20px'}),
                    html.Span(id='selected-date-label', style={'fontSize': '30px'})
                ], style={'marginBottom': '10px'}),
            #Adding in the date slider
            dcc.Slider(
                id='date-slider',
                min=0,
                max=len(date_range) - 1,
                step=1,
                value=date_to_index[date(2020, 1, 1)],
                marks=date_marks,
                tooltip={"always_visible": False, "transform": "numberToDate"},
                ),
        ], style={'padding': '10px', 'marginBottom': '20px'})
    ])

    elif tab == 'plot-tab':
        return html.Div([
            html.H3("Fire Occurrence Over Time"),
            html.Iframe(
                src="/assets/fire_timeseries.html",  # TODO MOVE THIS TO ENV ROOT
                style={"width": "100%", "height": "600px", "border": "none"}
            )
        ])

    elif tab == 'info-tab':
        return html.Div([
            html.H3("Dashboard Information"),
            html.Iframe(
                src= "/assets/model-info.html",  # TODO MOVE THIS TO ENV ROOT
                style={"width": "100%", "height": "600px", "border": "none"}
            )
        ])


#Updates the label of the selected date
@app.callback(
    Output('selected-date-label', 'children'),
    Input('date-slider', 'value')
)
def update_date_label(date_index):
    return available_dates[date_index].strftime('%Y-%m-%d')


# Recenters Map
@app.callback(Output("map", "viewport"),
              Input("recenter", "n_clicks"),
              prevent_initial_call=True)
def recenter(_):
    """
    Recenters the Map
    :param _:
    :return:
    """
    return dict(center=[40, -95], zoom=4, transition="flyTo")


@app.callback(
    Output('lc', 'children'),
    Input('date-slider', 'value'),
)
def update_layers_control(date_index):
    if date_index is None:
        return []
    selected_date = available_dates[date_index]
    year, month, day = selected_date.year, selected_date.month, selected_date.day
    subset = data[(data['year'] == year) & (data['month'] == month) & (data['day'] == day)]
    return generate_layers(subset, selected_date.strftime('%Y-%m-%d'))



@app.callback(
    Output('output-container', 'children'),
    Input('map', 'clickData'),
    Input('date-slider', 'value'),
)
def show_click_data(clickData, date_index):
    if not clickData or date_index is None:
        readable_date = available_dates[date_index].strftime('%Y-%m-%d') 
        return f"Click on a hexagon to view model predictions for {readable_date}."

    lat = clickData['latlng']['lat']
    lon = clickData['latlng']['lng']
    cell = latlng_to_cell(lat, lon, CELL_RESOLUTION)

    selected_date = available_dates[date_index]
    year, month, day = selected_date.year, selected_date.month, selected_date.day    

   # year, month, day = map(int, date_str.split('-'))
    filtered = data[
        (data['year'] == year) &
        (data['month'] == month) &
        (data['day'] == day) &
        (data['Hexagon_ID'] == cell)
    ]
    
    columns_to_keep = [
            'Predicted Fire Probability',
            'Temperature Maximum (3-Day Average)',
            'Temperature Minimum (3-Day Average)',
            'Precipitation (3-Day Average)',
            'Snowfall (3-Day Average)',
            'Daily Average Wind (3-Day Average)',
            'Average Elevation',
            'Fire Occurred?',            
            'geometry'
        ]
        
    filtered = filtered[columns_to_keep]  
    filtered['Fire Occurred?'] = filtered['Fire Occurred?'].map({0: "No", 1: "Yes"})
    filtered['Temperature Maximum (3-Day Average)'] = filtered['Temperature Maximum (3-Day Average)'].apply(lambda s: f"{s * 0.18 + 32:.2f}°F")
    filtered['Temperature Minimum (3-Day Average)'] = filtered['Temperature Minimum (3-Day Average)'].apply(lambda s: f"{s * 0.18 + 32:.2f}°F")
    filtered['Snowfall (3-Day Average)'] = filtered['Snowfall (3-Day Average)'].apply(lambda s: f"{s / 10:.4f}mm")
    filtered['Precipitation (3-Day Average)'] = filtered['Precipitation (3-Day Average)'].apply(lambda s: f"{s / 10:.4f}mm")
    filtered['Predicted Fire Probability'] = filtered['Predicted Fire Probability'].apply(lambda s: f"{s:.5f}")
    filtered["Average Elevation"] = filtered["Average Elevation"].apply(lambda s: f"{(s * 3.28084):,.0f} ft",   )
    filtered["Daily Average Wind (3-Day Average)"] = filtered["Daily Average Wind (3-Day Average)"].apply(lambda s: f"{(s * 0.1 * 2.23694):,.2f} mph")
    

    
    
    filtered = filtered.round(5)
    
        
    transposed = filtered.drop(columns='geometry').T
    transposed.columns = ['Value']
    transposed.reset_index(inplace=True)
    transposed.columns = ['Variable', 'Value']
    
    table = dbc.Table.from_dataframe(transposed, striped=True, bordered=True, hover=True)    
    #table = dbc.Table.from_dataframe(filtered.drop(columns='geometry'), striped=True, bordered=True, hover=True)

    return html.Div([
        html.Div(table, style={"font-size": "12px"})
    ])



@app.callback(
    Output("colorbar", "children"),
    Input("lc", "baseLayer"),
    Input("lc", "overlays"),
    prevent_initial_call=True
)
def update_colorbar(base, overlays):  
    if not base:
        #Set the default state
        base = "Predicted Fire Probability"
        
        #Have to re-add the word Normalized so it works within the _viz_helpers.py framework
    return generate_colorbar("Normalized " + base, n_ticks=11)


if __name__ == "__main__":
    if os.getenv("ENVIRONMENT", "dev") == "prod":
        app.run(host="0.0.0.0", port=8080, debug=False)
    else:
        app.run(debug=True, dev_tools_hot_reload=True)
