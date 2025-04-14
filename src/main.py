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

# Initialization
ASSETS_ROOT = Path(os.getenv('ASSETS_ROOT'))
CELL_RESOLUTION = None
data = gpd.read_parquet(ASSETS_ROOT / 'model_output.parquet')
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
                        dl.LayersControl([], id="lc", collapsed=False, position="bottomright")
                    ], center=[40, -95], zoom=4, style={'height': '50vh'}, id="map"),
                    html.Div(id="colorbar", style={"height": "30px", "margin": "10px 0px"}),
                    html.Button("Recenter", id="recenter"),
                ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),
                html.Div([
                    html.H3("Model"),
                    html.Div(id='output-container'),
                ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top',
                          'backgroundColor': '#e9ecef', 'padding': '10px'})
            ], style={'width': '100%', 'display': 'block'}),

            html.Div([
                html.H3('Select Date'),
                dcc.DatePickerSingle(
                    id="date-picker",
                    min_date_allowed=date(2000, 1, 1),
                    max_date_allowed=date(2025, 2, 28),
                    initial_visible_month=date(2020, 1, 1),
                    date=date(2020, 1, 1),
                )
            ], style={'padding': '10px'})
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
                src="/assets/model-info.html",  # TODO MOVE THIS TO ENV ROOT
                style={"width": "100%", "height": "600px", "border": "none"}
            )
        ])


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


# Loads a new day into the map
@app.callback(Output('lc', 'children'),
              Input('date-picker', 'date'),
              )
def update_map(date_str: str):
    """
    Queries the data by date, calls generate layers, then updates the map
    :param date_str:
    :return:
    """
    year, month, day = date_str.split('-')
    condition_year = data['year'] == int(year)
    condition_month = data['month'] == int(month)
    condition_day = data['day'] == int(day)
    subset = data[condition_year & condition_month & condition_day]
    return generate_layers(subset)


@app.callback(Output('output-container', 'children'),
              Input('map', 'clickData'),
              )
def show_click_data(clickData):
    result = f"""
    map: {json.dumps(clickData)}
    """
    lat = clickData['latlng']['lat']
    lon = clickData['latlng']['lng']
    cell = latlng_to_cell(lat, lon, CELL_RESOLUTION)
    return result


@app.callback(
    Output("colorbar", "children"),
    Input("lc", "baseLayer"),
    Input("lc", "overlays"),
    prevent_initial_call=True
)
def update_colorbar(base, overlays):
    if base not in field_identifiers: return None
    return generate_colorbar(base, n_ticks=11)


if __name__ == "__main__":
    if os.getenv("ENVIRONMENT", "dev") == "prod":
        app.run_server(host="0.0.0.0", port=8080, debug=False)
    else:
        app.run(debug=True, dev_tools_hot_reload=True)
