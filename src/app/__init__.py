from datetime import date
from pathlib import Path

import geopandas as gpd
import dash_leaflet as dl
import matplotlib.colors as mcolors
import numpy as np
from dash import dcc

PLOT_DATA_ROOT = Path('C:/Users/dhruv/IdeaProjects/capstone/data') # READ FROM ENV VAR

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
    mean_shift = 0.5 - gdf[field].mean()
    gdf[field] += mean_shift
    gdf[field] = np.clip(gdf[field], 0, 1)
    return gdf

def read_data(date, field):
    """
    read the plot_{date}.parquet for the correct date, return a colorized gdf
    :rtype: gpd.GeoDataFrame
    """
    file_path = PLOT_DATA_ROOT / 'curated' / f'Model_Output_{date}.parquet'
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
