from pathlib import Path

import pandas as pd
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import geopandas as gpd

dataset = ds.dataset(Path('../model_output'))

tab = dataset.to_table()

pq.write_table(tab, Path('../assets/model_output.parquet'))
