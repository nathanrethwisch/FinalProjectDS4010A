from datetime import date
from pathlib import Path

import geopandas as gpd
import dash_leaflet as dl

import matplotlib.colors as mcolors
import numpy as np
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


def generate_layers(date):
    gdf = read_data(date)
    overlays = []
    for field in field_identifiers:
        gdf = normalize_to_field_range(gdf, field)
        polys = generate_polys(gdf, field)
        poly_layer = dl.LayerGroup(polys)
        over = dl.BaseLayer(poly_layer, name=field, checked=False)
        overlays.append(over)
    return overlays


def generate_colorbar(field, n_ticks):
    cmap = get_colormap_choice(field)
    min_val, max_val = get_field_range(field)

    # Build a linear gradient with discrete steps
    n_grad_steps = 24
    steps = [cmap(i / (n_grad_steps - 1)) for i in range(n_grad_steps)]
    hex_colors = [mcolors.to_hex(c) for c in steps]
    gradient = f'linear-gradient(to right, {", ".join(hex_colors)})'

    # The gradient bar with relative positioning
    gradient_style = {
        'height': '20px',
        'width': '100%',
        'background': gradient,
        'border': '1px solid #ccc',
        'borderRadius': '4px',
        'position': 'relative'
    }

    # Container for tick marks and labels (absolute positioning relative to its own container)
    tick_elements = []
    for i, val in enumerate(np.linspace(min_val, max_val, n_ticks)):
        # Compute left position as a percentage along the bar.
        left_percent = (i / (n_ticks - 1)) * 100
        # Tick mark: a short vertical line on the colorbar.
        tick_mark_style = {
            'position': 'absolute',
            'top': '0px',
            'left': f'{left_percent}%',
            'width': '1px',
            'height': '8px',
            'background': 'black',
            'transform': 'translateX(-50%)'
        }
        # Tick label: positioned below the colorbar.
        tick_label_style = {
            'position': 'absolute',
            'top': '12px',
            'left': f'{left_percent}%',
            'transform': 'translateX(-50%)',
            'fontSize': '12px',
            'textAlign': 'center'
        }
        tick_elements.append(html.Div([], style=tick_mark_style))
        tick_elements.append(html.Div(format_field_values(val, field), style=tick_label_style))

    ticks_container_style = {
        'position': 'relative',
        'width': '100%',
        'height': '40px'
    }

    ticks_container = html.Div(tick_elements, style=ticks_container_style)

    # Assemble the colorbar with ticks below the gradient bar.
    return html.Div([
        html.Div(style=gradient_style),
        ticks_container
    ])
