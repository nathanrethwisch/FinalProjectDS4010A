from pathlib import Path

import pandas as pd
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import geopandas as gpd
from shapely.geometry.polygon import Polygon

dataset = ds.dataset(Path('../model_output'))

tab = dataset.to_table()

pq.write_table(tab, Path('../data/assets/model_output.parquet'))

gdf = gpd.read_parquet(Path('../data/assets/model_output.parquet'))

gdf['date'] = pd.to_datetime(gdf[['year', 'month', 'day']])

# tmin = gdf[['date', 'Temperature Minimum (3-Day Average)','Temperature Maximum (3-Day Average)',  'geometry']]

# tmin.columns = ['date', 'tmin','tmax', 'geometry']

gdf.columns = ['HEX_ID',
               'YEAR',
               'MONTH',
               'DAY',
               'T-MAX',
               'T-MIN',
               'PRCP',
               'SNOW',
               'WIND',
               'FIRE',
               'DATE',
               'ELEV',
               'PROB-PRED',
               'geometry',
               'PROB-NORM2',
               'PROB-NORM']

gdf = gdf[gdf['YEAR'] == 2024]

gdf.drop(columns=['YEAR', 'MONTH', 'DAY'], inplace=True)

def swap_coords(geom):
    if geom.geom_type == 'Polygon':
        return Polygon([(y,x) for x, y in geom.exterior.coords])

gdf['geometry'] = gdf['geometry'].apply(swap_coords)

def transform(gdf):
    #TODO PUT TRANSFORMATION LOGIC HERE
    return gdf

gdf = transform(gdf)


gdf.to_file(Path('../data/assets/combined/combined.shp'))
