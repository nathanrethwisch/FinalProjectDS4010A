import gzip
from io import StringIO

import pandas as pd
import requests


class GHCND():
    def __init__(self):

    def load_metadata(self):
        pass



    def download_stations(self, stations_url):
        """
        download stations, combine date and time columns,
        set types, and return a dataframe/pyarrow table
        :param stations_url:
        :return:
        """
        station_response = requests.get(stations_url)
        df = pd.read_fwf(StringIO(station_response.content.decode()),
                         header=None,
                         colspecs=[
                             (0, 11),
                             (12, 20),
                             (21, 30),
                             (31, 37),
                             (38, 40),
                             (41, 71),
                             (72, 75),
                             (76, 79),
                             (80, 85)
                         ]
                         )
        df.columns = [
            'station_id',
            'latitude',
            'longitude',
            'elevation',
            'state',
            'name',
            'gsn_flag',
            'hcn_crn_flag',
            'wmo_id'
        ]
        return df

    def get_yearly_filepaths(self):
        pass

    def download_yearly_csv(self, key):
        url = f"{self.data_source_url}/{key}"
        response = requests.get(url)

        filename = key.split("/")[-1]
        csv_content = gzip.decompress(response.content)
        memfile = StringIO(csv_content.decode())
        df = pd.read_csv(memfile, sep=",", header=None)
        return df


# do stations first
# do yearly after

# 1. load metadata
# 2. download and save stations
# 3. get list of yearly files
# 4. for each year's file:
#       1. download and save raw files in base_path/ghcnd_raw/
#       2. create pyarrow schema from metadata
#       3. read csv as pyarrow table using schema.
#       4. fix nulls and missing values
#       5. Create Partitioned Dataset
#           .
#           └── ghcnd/
#               ├── README.md
#               ├── metadata.json
#               ├── raw/
#               │   ├── 1780.csv.gz
#               │   ├── ...
#               │   └── 2025.csv.gz
#               ├── cleaned/
#               │   ├── 1780.parquet
#               │   ├── ...
#               │   └── 2025.parquet
#               └── curated/
#                   ├── nation_wide_rainfall.parquet
#                   ├── ...
#                   └── station_101.parquet


# Metadata:
# each table has a pyarrow.Schema
# each schema is made up of pyarrow.Field
# each field is a datatype + variable name
# datatype and variable name should be read from json.
