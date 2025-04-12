import json
import os
import sys
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import Output, Input, html, dcc
import dash_leaflet as dl

sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / 'app'))
from app import date_picker, generate_layers

from datalake import Datalake

# Initialization
lake = Datalake('../data')

_, hex_ids = generate_layers("2020-06-03")
del (_)
print(hex_ids)

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

theme = {
    "Black": "07020d",
    "Aero": "5db7de",
    "Bittersweet": "f25757",
    "Alabaster": "f1e9db",
    "Dim gray": "716a5c"
}


@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_tab_content(tab):
    if tab == 'map-tab':
        return html.Div([
            html.Div([
                html.Div([
                    html.H3("Map"),
                    dl.Map(children=[
                        dl.TileLayer(),
                        dl.LayersControl([], id="lc", collapsed=False, position="bottomright")
                    ], center=[40, -95], zoom=4, style={'height': '50vh'}, id="map"),
                    html.Button("Recenter", id="recenter")
                ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

                html.Div([
                    html.H3("Model"),
                    html.Div(id='output-container'),
                ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top',
                          'backgroundColor': '#e9ecef', 'padding': '10px'})
            ], style={'width': '100%', 'display': 'block'}),

            html.Div([
                html.H3('Date'),
                date_picker,
                dcc.Store(id='hex_ids', storage_type='session'),
            ], style={'padding': '10px'})
        ])

    elif tab == 'plot-tab':
        return html.Div([
            html.H3("Fire Occurrence Over Time"),
            html.Iframe(
                src="/assets/fire_timeseries.html",
                style={"width": "100%", "height": "600px", "border": "none"}
            )
        ])

    elif tab == 'info-tab':  
        return html.Div([
            html.H3("Dashboard Information"),
            html.Iframe(
                src="/assets/model-info.html", 
                style={"width": "100%", "height": "600px", "border": "none"}
            )
        ])


@app.callback(Output("map", "viewport"),
              Input("recenter", "n_clicks"),
              prevent_initial_call=True)
def recenter(_):
    return dict(center=[40, -95], zoom=4, transition="flyTo")


@app.callback(Output('lc', 'children'),
              Output('hex_ids', 'data'),
              Input('date-picker', 'date'),
              )
def update_map(date):
    return generate_layers(date)


@app.callback(Output('output-container', 'children'),
              Input('layer', 'clickData'),
              Input('map', 'clickData'),
              )
def show_click_data(lclickData, mclickData):
    result = f"""
    layer: {json.dumps(lclickData)}
    map: {json.dumps(mclickData)}
    """
    return result


if __name__ == "__main__":
    if os.getenv("ENVIRONMENT", "dev") == "prod":
        app.run_server(host="0.0.0.0", port=8080, debug=False)
    else:
        app.run(debug=True, dev_tools_hot_reload=True)
