from datetime import date
from pathlib import Path

import geopandas as gpd
import dash_leaflet as dl
import matplotlib.colors as mcolors
import numpy as np
from dash import html, dcc
import os

PLOT_DATA_ROOT = Path(__file__).resolve().parents[2] / 'model_output'
print(PLOT_DATA_ROOT.absolute())
# Field Selection Component
field_selection = dcc.RadioItems(
    id='field-checklist',
    options=[
        {'label': 'Fire Probability', 'value': 'normalized_probabilities'},
        {'label': 'Precipitation', 'value': 'prcp_avg'},
        {'label': 'Max Temperature', 'value': 'tmax_avg'},
        {'label': 'Min Temperature', 'value': 'tmin_avg'},
        {'label': 'Snowfall', 'value': 'snow_avg'},
        # {'label': 'Wind', 'value': 'snwd'}
    ],
    value='normalized_probabilities'
)


# Date Picker Component
date_picker = dcc.DatePickerSingle(
    id='date-picker',
    min_date_allowed=date(2000, 1, 1),
    max_date_allowed=date(2025, 2, 28),
    initial_visible_month=date(2020, 1, 1),
    date=date(2020, 7, 1),
)

def normalize(gdf, field):
    """
    Assign Colors to values
    """
    min_val = gdf[field].min()
    max_val = gdf[field].max()
    gdf[field] = (gdf[field] - min_val) / (max_val - min_val)
    #mean_shift = 0.5 - gdf[field].mean()
    #gdf[field] += mean_shift
    gdf[field] = np.clip(gdf[field], 0, 1)
    return gdf

def read_data(date):
    """
    read the plot_{date}.parquet for the correct date, return a colorized gdf
    :rtype: gpd.GeoDataFrame
    """
    file_path = PLOT_DATA_ROOT / f'Model_Output_{date}.parquet'
    print(f'READING DATA FROM {file_path}')
    return gpd.read_parquet(file_path,)
                            # columns=["Hexagon_ID", 'geometry', field])



def generate_polys(gdf, field):
    """
    return a list of polys to be passed into a layergroup
    """
    print(f"GENERATING POLYGONS FOR {field}")
    cmap = mcolors.LinearSegmentedColormap.from_list("green_red", ["green", "yellow", "red"])
    # print(gdf[field])
    polygons = []
    for _, row in gdf.iterrows():
        polygon = row['geometry']
        coordinates = [[lat,lon] for lat, lon in polygon.exterior.coords] # TODO is this necessary
        color = mcolors.to_hex(cmap(row[field]))
        # color = mcolors.to_hex(cmap(row['tmax_avg']))
        polygons.append(dl.Polygon(positions=coordinates, color=color, fillColor=color, fillOpacity=0.6, weight=1))
    return polygons

def generate_layers(date, field):
    gdf = read_data(date)
    min_val = gdf[field].min()
    max_val = gdf[field].max()
    gdf = normalize(gdf, field)
    polys = generate_polys(gdf, field)
    poly_layer = dl.LayerGroup(polys)
    overlay = dl.BaseLayer(poly_layer, name=field, checked=True)
    # return value range to support colorbar
    return [overlay], float(min_val), float(max_val)


def generate_colorbar(field, min_val, max_val):
    colormap = {
        'normalized_probabilities': ['green', 'yellow', 'red'],
        'prcp_avg': ['white', 'blue'],
        'tmax_avg': ['blue', 'red'],
        'tmin_avg': ['purple', 'lightblue'],
        'snow_avg': ['white', 'gray']
    }

    colors = colormap.get(field, ['white', 'black'])

    style = {
        'height': '20px',
        'background': f'linear-gradient(to right, {", ".join(colors)})',
        'marginBottom': '5px',
        'width': '100%'
    }

    print("dssd", max_val, min_val)
    ticks = html.Div([
        html.Span(f"a{min_val:.2f}", style={'float': 'left'}),
        html.Span(f"b{(min_val + max_val)/2:.2f}", style={'textAlign': 'center'}),
        html.Span(f"c{max_val:.2f}", style={'float': 'right'})
    ], style={'fontSize': '12px', 'width': '100%', 'display': 'flex', 'justifyContent': 'space-between'})

    return html.Div([
        html.Div(style=style),
        ticks
    ])
