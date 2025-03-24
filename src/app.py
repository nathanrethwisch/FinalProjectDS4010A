import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_leaflet as dl
import h3

app = dash.Dash(__name__)

# Sample GIS data
data = [
    {"name": "Location A", "lat": 37.7749, "lon": -122.4194},  # San Francisco
    {"name": "Location B", "lat": 34.0522, "lon": -118.2437},  # Los Angeles
    {"name": "Location C", "lat": 40.7128, "lon": -74.0060},   # New York
]

# Function to generate H3 grid
def generate_h3_grid(resolution):
    hexagons = []
    for loc in data:
        hex_id = h3.geo_to_h3(loc["lat"], loc["lon"], resolution)
        hex_boundary = h3.h3_to_geo_boundary(hex_id, geo_json=True)
        hexagons.append(dl.Polygon(positions=hex_boundary, color="blue", fillOpacity=0.2))
    return hexagons

app.layout = html.Div([
    dl.Map(center=[37.7749, -122.4194], zoom=4, children=[
        dl.TileLayer(),
        dl.LayerGroup(id="layer"),
        dl.LayerGroup(id="h3-layer", children=generate_h3_grid(3)),
    ], style={'width': '100%', 'height': '50vh'}),
    html.Div([
        html.Label("Select Locations:"),
        dcc.Checklist(
            id="location-checklist",
            options=[{"label": loc["name"], "value": loc["name"]} for loc in data],
            value=[loc["name"] for loc in data]
        ),
    ], style={'padding': '20px'})
])

@app.callback(
    Output("layer", "children"),
    [Input("location-checklist", "value")]
)
def update_map(selected_locations):
    markers = [
        dl.Marker(position=[loc["lat"], loc["lon"]], children=[
            dl.Tooltip(loc["name"]),
            dl.Popup(loc["name"])
        ]) for loc in data if loc["name"] in selected_locations
    ]
    return markers

if __name__ == '__main__':
    app.run_server(debug=True)
