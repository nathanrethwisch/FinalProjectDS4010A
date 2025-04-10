from datetime import date
from pathlib import Path

import geopandas as gpd
import dash_leaflet as dl

import matplotlib.colors as mcolors
from dash import html, dcc

from .utils import *

PLOT_DATA_ROOT = Path(__file__).resolve().parents[2] / "model_output"
print(PLOT_DATA_ROOT.absolute())
# Field Selection Component
field_selection = dcc.RadioItems(
    id="field-checklist",
    options=[
        {"label": "Fire Probability", "value": "normalized_probabilities"},
        {"label": "Precipitation", "value": "prcp_avg"},
        {"label": "Max Temperature", "value": "tmax_avg"},
        {"label": "Min Temperature", "value": "tmin_avg"},
        {"label": "Snowfall", "value": "snow_avg"},
        # {"label": "Wind", "value": "snwd"}
    ],
    value="normalized_probabilities"
)

# Date Picker Component
date_picker = dcc.DatePickerSingle(
    id="date-picker",
    min_date_allowed=date(2000, 1, 1),
    max_date_allowed=date(2025, 2, 28),
    initial_visible_month=date(2020, 1, 1),
    date=date(2020, 7, 1),
)


def read_data(dt):
    """
    read the plot_{date}.parquet for the correct date, return a colorized gdf
    :rtype: gpd.GeoDataFrame
    """
    file_path = PLOT_DATA_ROOT / f"Model_Output_{dt}.parquet"
    print(f"READING DATA FROM {file_path}")
    return gpd.read_parquet(file_path, )
    # columns=["Hexagon_ID", "geometry", field])


def generate_polys(gdf, field):
    """
    return a list of polys to be passed into a layergroup
    """
    print(f"GENERATING POLYGONS FOR {field}")
    cmap = get_colormap_choice(field)

    # print(gdf[field])
    polygons = []
    for _, row in gdf.iterrows():
        polygon = row["geometry"]
        coordinates = [[lat, lon] for lat, lon in polygon.exterior.coords]  # TODO is this necessary
        color = mcolors.to_hex(cmap(row[field]))
        # color = mcolors.to_hex(cmap(row["tmax_avg"]))
        polygons.append(dl.Polygon(positions=coordinates, color=color, fillColor=color, fillOpacity=0.6, weight=1))
    return polygons


def generate_layers(dt, field):
    gdf = read_data(dt)
    min_val = gdf[field].min()
    max_val = gdf[field].max()
    gdf = normalize_to_field_range(gdf, field)
    polys = generate_polys(gdf, field)
    poly_layer = dl.LayerGroup(polys)
    overlay = dl.BaseLayer(poly_layer, name=field, checked=True)
    # return value range to support colorbar
    return [overlay], float(min_val), float(max_val)


def generate_colorbar(field, min_val, max_val):
    cmap = get_colormap_choice(field)

    steps = [cmap(i / 10) for i in range(11)]
    hex_colors = [mcolors.to_hex(c) for c in steps]

    gradient = f'linear-gradient(to right, {", ".join(hex_colors)})'

    gradient_style = {
        'height': '20px',
        'background': gradient,
        'marginBottom': '4px',
        'width': '100%',
        'border': '1px solid #ccc',
        'borderRadius': '4px'
    }

    ticks = html.Div([
        html.Div(f"{min_val:.2f}", style={'width': '33%', 'textAlign': 'left'}),
        html.Div(f"{(min_val + max_val) / 2:.2f}", style={'width': '34%', 'textAlign': 'center'}),
        html.Div(f"{max_val:.2f}", style={'width': '33%', 'textAlign': 'right'})
    ], style={'display': 'flex', 'width': '100%', 'fontSize': '12px'})

    return html.Div([
        ticks,
        html.Div(style=gradient_style)
    ])
