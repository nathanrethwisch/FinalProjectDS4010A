from datetime import date

import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
import dash_leaflet as dl

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

app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])

theme = {
    # Define colorscheme here: https://coolors.co/07020d-5db7de-f25757-f1e9db-716a5c
    "Black": "07020d",
    "Aero": "5db7de",
    "Bittersweet": "f25757",
    "Alabaster": "f1e9db",
    "Dim gray": "716a5c"
}

app.layout = html.Div([
    # Top Navigation Bar
    html.Div([
        html.H2("Wildfire"),
        # Add navigation links or components here
    ], style={'width': '100%', 'display': 'block', 'backgroundColor': '#f8f9fa', 'padding': '10px',
              'textAlign': 'center'}
    ),
    # Primary Content Area
    html.Div([
        # Left Sidebar
        html.Div([
            # Add components for the left sidebar here
            html.H3("Data"),
            field_selection,
            date_picker
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'backgroundColor': '#e9ecef',
                  'padding': '10px'}
        ),

        # Center Content Area
        html.Div([
            html.H3("Map"),
            # Add main content components and plots here
            dl.Map(children=[
                dl.TileLayer(),
                dl.LayerGroup(id='hexes', interactive=True),
            ], center=[40, -95], zoom=4, style={'height': '50vh'}, id="map"),
            html.Button("Recenter", id="recenter")
        ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}
        ),

        # Right Sidebar
        html.Div([
            # Add components for the right sidebar here
            html.H3("Model"),
            # TODO HEX DETAILED TABLE
        ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top', 'backgroundColor': '#e9ecef', 'padding': '10px'}
        ),
    ], style={'width': '100%', 'display': 'block'}),
    html.Div([
        html.H3('Bottom Panel'),
        html.Div(id='diagnostics')  # Displays Diagnostics on field/date selection
    ], style={'padding': '10px'})
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
@app.callback(Output('hexes', 'children'),
              Input('date-picker', 'date'),
              Input('field-checklist', 'value'),
               )
def update_map(date, field):
    gdf = read_data(date, field)
    gdf = normalize(gdf, field)
    polys = generate_polys(gdf, field)
    # print(polys[5])
    return polys

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
