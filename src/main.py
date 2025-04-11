from datetime import date

import sys
from pathlib import Path
import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
import dash_leaflet as dl

sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / 'app'))
from app import *

from datalake import Datalake

# TODO
# 1. Define Base Layout
# 2. Add Checkboxes for Field Selection
# 3. Add Date selection( Pick a resolution)
# 5. Generate a callback function which generates a new map_context for each change

# TODO Workflow
# 1. User selects date and field
# 2. User clicks Render button(or auto render)
# 3. Callback function takes inputs, creates query/loads data
# 4. Map Updates

# Initialization
lake = Datalake('../data')

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True) #suppress_callback_exceptions=True is needed
server = app.server 

app.layout = html.Div([
    html.H2("Wildfire Dashboard", style={'textAlign': 'center'}),

    dcc.Tabs(id = 'tabs', value='map-tab', children = [
        dcc.Tab(label = 'Map View', value = 'map-tab'),
        dcc.Tab(label = "Time Series Plot", value = 'plot-tab')
    ]),

    html.Div(id='tabs-content')  # content filled dynamically
])

theme = {
    # Define colorscheme here: https://coolors.co/07020d-5db7de-f25757-f1e9db-716a5c
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
                    html.H3("Data"),
                    field_selection,
                    date_picker
                ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top',
                          'backgroundColor': '#e9ecef', 'padding': '10px'}),

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
                    # Optionally add more output here
                ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top',
                          'backgroundColor': '#e9ecef', 'padding': '10px'})
            ], style={'width': '100%', 'display': 'block'}),

            html.Div([
                html.H3('Bottom Panel'),
                html.Div(id='diagnostics')
            ], style={'padding': '10px'})
        ])

    elif tab == 'plot-tab':
        return html.Div([
            html.H3("Fire Occurrence Over Time"),
            html.Iframe(
                src="/assets/fire_timeseries.html",  # Puts the file inside an `assets/` folder
                style={"width": "100%", "height": "600px", "border": "none"}
            )
        ])





# updates bottom panel's diagnostics
@app.callback(Output('diagnostics', 'children'),
              Input('field-checklist', 'value'),
              Input('date-picker', 'date'), )
def update_diagnostics(selected_fields, date):
    return f"Selected Fields: {selected_fields} on {date} "

# Reenters Map
@app.callback(Output("map", "viewport"),
              Input("recenter", "n_clicks"),
              prevent_initial_call=True)
def recenter(_):
    return dict(center=[40, -95], zoom=4, transition="flyTo")

# updates the map
@app.callback(Output('lc', 'children'),
              Input('date-picker', 'date'),
              # Input('field-checklist', 'value'),
               )
def update_map(date):
    # gdf = read_data(date, field)
    # gdf = normalize(gdf, field)
    # polys = generate_polys(gdf, field)
    return generate_layers(date)

# @app.callback(
#     [Output('hexes', 'children'),
#      Output("map", "viewport"),
#      Output('diagnostics', 'children')],
#     [Input('field-checklist', 'value'),
#      Input('date-picker', 'date'),
#      Input("recenter", "n_clicks")]
# )
# def update_map(field, date, n_clicks):
#     gdf = read_data(date)
#     gdf = normalize(gdf, field)
#     polys = generate_polys(gdf, field)
#
#     diagnostics = f"Selected Fields: {field} on {date}"
#
#     if n_clicks:
#         viewport = dict(center=[40, -95], zoom=4, transition="flyTo")
#     else:
#         viewport = dash.no_update
#
#     return polys, viewport, diagnostics

if __name__ == "__main__":
    app.run(debug=True, dev_tools_hot_reload=True)
