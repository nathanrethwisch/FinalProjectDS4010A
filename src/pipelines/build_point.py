from pathlib import Path

import geopandas as gpd
import pandas as pd

df = pd.read_parquet(Path('../data/clean/fire_occurrence_point/Fire_Occurence.parquet'))

print(df.columns)

gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.LONGDD83, df.LATDD83), crs='EPSG:4326')

gdf.to_parquet(Path('../data/clean/fire_occurrence_point/Fire_Occurence.parquet'))
