import json
import os
import tempfile
import zipfile
from io import StringIO
from pathlib import Path

import geopandas as gpd
import pandas as pd
import pyarrow.dataset as ds
import pyarrow.parquet as pq
import requests
from shapely.geometry import shape, Polygon, mapping, Point
from shapely.validation import make_valid

import h3


class Datalake:

    def __init__(self, root_path):

        self.datalake_root = Path(root_path)
        self.paths = {"ghcnd_raw_stations": "raw/ghcnd/stations.txt", "ghcnd_raw_daily": "raw/ghcnd/daily/",
                      "ghcnd_clean_stations": "clean/ghcnd/stations.parquet",
                      "ghcnd_metadata": "clean/ghcnd/metadata.html", "ghcnd_clean_daily": "clean/ghcnd/daily/",
                      "ghcnd_statistics": "curated/ghcnd/statistics.parquet",
                      "fire_point_raw": "raw/fire_occurrence_point/National_USFS_Fire_Occurrence_Point_(Feature_Layer).geojson",
                      "fire_point_clean": "clean/fire_occurrence_point/Fire_Occurence.parquet",
                      "fire_perimeter_raw": "raw/fire_perimeter/National_USFS_Fire_Perimeter_(Feature_Layer).geojson",
                      "fire_perimeter_cleaned": "clean/fire_perimeter/National_USFS_Fire_Perimeter_(Feature_Layer).parquet",
                      "states_raw": "raw/maps/cb_2023_us_all_500k.zip",
                      "states_clean": "clean/maps/cb_2023_us_states_500k.parquet", }
        self.ghcnd_elements = ['PRCP', 'SNOW', 'SNWD', 'TMAX', 'TMIN', 'AWND', 'AWDR', 'EVAP']
        self.ghcnd_sources = {"readme": "https://docs.opendata.aws/noaa-ghcn-pds/readme.html",
                              "stations": "https://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-stations.txt",
                              "inventory": "https://noaa-ghcn-pds.s3.amazonaws.com/ghcnd-inventory.txt",
                              "bucket": "https://noaa-ghcn-pds.s3.amazonaws.com"}
        self.years = (2000, 2025)

    def initialize(self):
        self._create_subdirectory('raw')
        self._create_subdirectory('raw/ghcnd')
        self._create_subdirectory('raw/ghcnd/daily')
        self._create_subdirectory('clean')
        self._create_subdirectory('clean/ghcnd')
        self._create_subdirectory('clean/ghcnd/daily')
        self._create_subdirectory('raw/fire_occurrence_point')
        self._create_subdirectory('raw/fire_perimeter')
        self._create_subdirectory('clean/fire_occurrence_point')
        self._create_subdirectory('clean/fire_perimeter')

    def query_ghcnd(self, pyarrow_query, columns=None):
        if columns and 'geometry' not in columns:
            return ValueError("Columns list is provided but does not contain 'geometry'!")
        else:
            dataset = ds.dataset(self.datalake_root / self.paths["ghcnd_clean_daily"])
            return gpd.GeoDataFrame.from_arrow(dataset.filter(pyarrow_query).to_table(columns=columns)).set_crs(
                epsg=4326)

    def query_states(self):
        return gpd.read_parquet(self.datalake_root / self.paths["states_clean"])

    def query_fire_perimeter(self, pyarrow_query=None, columns=None):
        if columns and 'geometry' not in columns:
            return ValueError("Columns list is provided but does not contain 'geometry'!")
        elif pyarrow_query:
            table = pq.read_table(self.datalake_root / self.paths["fire_perimeter_cleaned"], columns=columns).filter(
                pyarrow_query)
            return gpd.GeoDataFrame.from_arrow(table).to_crs(epsg=4326)
        else:
            table = pq.read_table(self.datalake_root / self.paths["fire_perimeter_cleaned"], columns=columns)
            return gpd.GeoDataFrame.from_arrow(table).to_crs(epsg=4326)

    def query_fire_point(self, pyarrow_query=None, columns=None):
        if columns and 'geometry' not in columns:
            return ValueError("Columns list is provided but does not contain 'geometry'!")
        elif pyarrow_query:
            table = pq.read_table(self.datalake_root / self.paths["fire_point_clean"], columns=columns).filter(
                pyarrow_query)
            return gpd.GeoDataFrame.from_arrow(table).to_crs(epsg=4326)
        else:
            table = pq.read_table(self.datalake_root / self.paths["fire_point_clean"], columns=columns)
            return gpd.GeoDataFrame.from_arrow(table).to_crs(epsg=4326)

    def query_stations(self) -> gpd.GeoDataFrame:
        stations = pd.read_parquet(self.datalake_root / self.paths["ghcnd_clean_stations"])
        us_stations = stations[stations['station_id'].str.startswith('US')]
        ca_stations = stations[stations['station_id'].str.startswith('CA')]
        mx_stations = stations[stations['station_id'].str.startswith('MX')]
        result = pd.concat([us_stations, ca_stations, mx_stations])

        # Encode as shapely point object
        result["geometry"] = result.apply(lambda row: Point(row["longitude"], row["latitude"]), axis=1)

        return gpd.GeoDataFrame(result, geometry="geometry", crs="EPSG:4326")

    def process_ghcnd_stations(self):
        print('CLEANING GHCND STATIONS')
        self.clean_stations_file(self.datalake_root / self.paths["ghcnd_raw_stations"],
                                 self.datalake_root / self.paths["ghcnd_clean_stations"])

    def process_ghcnd_daily(self):
        for year in range(self.years[0], self.years[1] + 1):
            print(f'CLEANING DAILY: {year}')
            self.clean_daily_file(self.datalake_root / self.paths["ghcnd_raw_daily"] / f'{year}.csv.gz',
                                  self.datalake_root / self.paths["ghcnd_clean_daily"] / f'{year}.parquet')

    def process_states(self):
        raw_path = self.datalake_root / self.paths["states_raw"]
        clean_path = self.datalake_root / self.paths["states_clean"]
        states = None
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(raw_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            files = os.listdir(temp_dir)
            states = gpd.read_file(os.path.join(temp_dir, files[0]), layer='cb_2023_us_state_500k')
        not_conus = ['District of Columbia', 'American Samoa', 'United States Virgin Islands',
                     'Commonwealth of the Northern Mariana Islands', 'Puerto Rico', 'Guam', 'Hawaii', 'Alaska']
        states = states[~states['NAME'].isin(not_conus)]
        states = states[['NAME', "geometry"]]
        states.columns = ['name', 'geometry']
        states = states.to_crs(epsg=4326)
        states = states.reset_index(drop=True)
        states['code'] = [
            'NM', 'SD', 'CA', 'KY', 'AL', 'GA', 'AR', 'PA', 'MO', 'CO', 'UT', 'OK', 'TN', 'WY', 'NY', 'IN', 'KS', 'ID', 'NV', 'IL',
            'VT', 'MN', 'IA', 'SC', 'NH', 'DE', 'CT', 'MI', 'MA', 'FL', 'NJ', 'ND', 'MD', 'ME', 'RI', 'MT', 'AZ', 'NE', 'WA', 'TX',
            'OH', 'WI', 'OR', 'MS', 'NC', 'VA', 'WV', 'LA'
        ]
        states = states[['name', 'code', 'geometry']]
        states.to_parquet(clean_path)

    def process_fire_point(self):
        gdf = gpd.read_file(self.datalake_root / self.paths["fire_point_raw"])
        # gdf = self.drop_not_conus(gdf) # TODO THIS TAKES YEARS
        gdf = self._clean_fire_point(gdf)
        gdf.to_parquet(self.datalake_root / self.paths["fire_point_clean"])

    def process_fire_perimeter(self):
        gdf = self._repair_geojson(self.datalake_root / self.paths["fire_perimeter_raw"])
        gdf = self.drop_not_conus(gdf)
        gdf = self._clean_fire_perimeter(gdf)
        gdf.to_parquet(self.datalake_root / self.paths["fire_perimeter_cleaned"])

    def drop_not_conus(self, gdf):
        states = self.query_states()
        union = states.geometry.union_all()
        gdf = gdf[gdf.geometry.within(union)]
        return gdf

    def erase(self):
        pass

    def download_ghcnd(self):
        self._download_file(self.ghcnd_sources["readme"], self.datalake_root / self.paths["ghcnd_metadata"])
        # download stations
        self._download_file(self.ghcnd_sources['stations'], self.datalake_root / self.paths["ghcnd_raw_stations"])
        # download daily
        for year in range(self.years[0], self.years[1] + 1):
            file_url = f'{self.ghcnd_sources["bucket"]}/csv.gz/by_year/{year}.csv.gz'
            dest_path = self.datalake_root / self.paths['ghcnd_raw_daily'] / f'{year}.csv.gz'
            self._download_file(file_url, dest_path)

    @staticmethod
    def _download_file(file_url, dest_path):
        """
        Downloads a file from a url to a filesystem path.
        If file is less than 1GiB then direct download and save to disk.
        If file is larger than 1GiB stream download to disk.
        """
        print(f'Downloading {file_url}')
        response = requests.head(file_url)
        file_size = int(response.headers.get('content-length', 0))
        one_gib = 1 * 1024 * 1024 * 1024

        if file_size < one_gib:
            response = requests.get(file_url)
            with open(dest_path, 'wb') as file:
                file.write(response.content)
        else:
            response = requests.get(file_url, stream=True)
            with open(dest_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
        pass

    def _create_subdirectory(self, relative_path):
        """
        Creates a directory using paths relative to the datalake root
        :param relative_path:
        """
        path = self.datalake_root / relative_path
        if not os.path.exists(path):
            os.makedirs(path)
            print(f'{relative_path} folder created')
        else:
            print(f'{relative_path} folder already exists')

    @staticmethod
    def _repair_geojson(path):
        print("READING/REPAIRING GEOJSON ")
        with open(path, 'r') as f:
            data = json.load(f)
        for feature in data['features']:
            try:
                geometry = shape(feature['geometry'])
                if not geometry.is_valid:
                    geometry = make_valid(geometry)
                feature['geometry'] = mapping(geometry)
            except Exception as e:
                print(f"Error processing geometry: {e}")
                feature['geometry'] = mapping(Polygon())  # Replace with an empty polygon
        geojson_str = json.dumps(data)
        geojson_file = StringIO(geojson_str)
        gdf = gpd.read_file(geojson_file).to_crs(epsg=4326)
        return gdf

    @staticmethod
    def _clean_fire_perimeter(gdf):
        gdf = gdf.to_crs(epsg=4326)
        # TODO DROP UNWANTED COLS
        # drop = [
        #     'SHAPE', 'GLOBALID', 'REVDATE',
        #     'COMPLEXNAME', 'SOFIRENUM', 'LOCALFIRENUM',
        #     'SECURITYID', 'DATASOURCE', 'OWNERAGENCY',
        #     'UNITIDOWNER', 'PROTECTIONAGENCY', 'UNITIDPROTECT',
        #     'POINTTYPE', 'FIRERPTQC', 'DBSOURCEID',
        #     'DBSOURCEDATE', 'ACCURACY', 'SHAPE'
        # ]
        # gdf.drop(columns=drop, inplace=True)
        # TODO CREATE YEAR MONTH DAY COLS
        # TODO RENAME COLUMN NAMES
        return gdf

    @staticmethod
    def _clean_fire_point(gdf):
        gdf.to_crs(epsg=4326)
        # TODO DROP UNWANTED COLS
        drop = ['SHAPE', 'GLOBALID', 'REVDATE', 'COMPLEXNAME', 'SOFIRENUM', 'LOCALFIRENUM', 'SECURITYID', 'DATASOURCE',
                'OWNERAGENCY', 'UNITIDOWNER', 'PROTECTIONAGENCY', 'UNITIDPROTECT', 'POINTTYPE', 'FIRERPTQC',
                'DBSOURCEID',
                'DBSOURCEDATE', 'ACCURACY', 'SHAPE', 'FIREOUTDATETIME', 'FIREYEAR']
        gdf = gdf.drop(columns=drop)

        # TODO PROCESS DATES
        gdf = gdf.dropna(subset=['DISCOVERYDATETIME'])
        dates = gdf['DISCOVERYDATETIME'].str.split(" ", expand=True)[0].str.split('/', expand=True)
        dates.columns = ['year', 'month', 'day']
        gdf = pd.concat([gdf, dates], axis=1)
        gdf = gdf.drop(columns=['DISCOVERYDATETIME'])

        # TODO REPAIR POINTS
        gdf['geometry'] = gdf.apply(
            lambda row: Point(row['LONGDD83'], row['LATDD83']) if pd.isnull(row['geometry']) and pd.notnull(
                row['LATDD83']) and pd.notnull(row['LONGDD83']) else row['geometry'], axis=1)
        gdf = gdf.drop(columns=['LATDD83', 'LONGDD83'])

        # TODO RENAME COLUMN NAMES

        return gdf

    @staticmethod
    def clean_stations_file(raw_path, clean_path):
        """
        Clean a single stations file
        :param raw_path:
        :param clean_path:
        """
        """
            Reads the ghcnd-stations fixed-width file, sets datatypes, and saves it as a parquet file.
            """
        stations = pd.read_fwf(raw_path, header=None,
                               colspecs=[(0, 11), (12, 20), (21, 30), (31, 37), (38, 40), (41, 71), (72, 75), (76, 79),
                                         (80, 85)])
        stations.columns = ['station_id', 'latitude', 'longitude', 'elevation', 'state', 'name', 'gsn_flag',
                            'hcn_crn_flag', 'wmo_id']
        stations['station_id'] = stations['station_id'].astype(str)
        stations['latitude'] = stations['latitude'].astype(float)
        stations['longitude'] = stations['longitude'].astype(float)
        stations['elevation'] = stations['elevation'].astype(float)
        stations['name'] = stations['name'].astype(str)
        stations.drop(columns=['gsn_flag', 'hcn_crn_flag', 'wmo_id'], inplace=True)

        stations.to_parquet(clean_path)

    @staticmethod
    def process_dates(df):
        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['day'] = df['date'].dt.day
        return df

    @staticmethod
    def drop_daily_columns(df):
        df.drop(columns=['time', 'date', 'm_flag', 'q_flag', 's_flag'], inplace=True)
        return df

    def create_element_tables(self, df):
        element_tables = []
        for element in self.ghcnd_elements:
            element_df = df[df['element'] == element].drop(columns=['element'])
            element_df = element_df[['station_id', 'year', 'month', 'day', 'value']]
            element_df.columns = ['station_id', 'year', 'month', 'day', element.lower()]
            element_tables.append(element_df)
        return element_tables

    @staticmethod
    def join_element_tables(element_tables):
        left = element_tables[0]
        for i in range(1, len(element_tables)):
            right = element_tables[i]
            left = pd.merge(left, right, on=['station_id', 'year', 'month', 'day'], how='outer')
        return left

    @staticmethod
    def join_stations_elements(df, stations):
        df = pd.merge(df, stations, how='inner', on='station_id')
        return df


    @staticmethod
    def drop_station_columns(df):
        df.drop(columns=['name'], inplace=True)
        return df

    @staticmethod
    def generate_geometries(df):
        gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude), crs='EPSG:4326')
        #gdf.drop(columns=['longitude', 'latitude'], inplace=True)
        return gdf

    @staticmethod
    def generate_hexes(gdf):
        # Creation of the hexagonal grid
        #The input lat and lng are where the grid is centered - this can be moved to any lat, long - for example, over Califonia (lng = -119.45, lat = 37.17)
        input_lng = -103
        input_lat = 44

        # Generate H3 hexagons at a specified resolution - a larger resolution means smaller cell size
        resolution = 3

        # Indicate the number of rings around the central hexagon - larger ring size means more area of the map will be covered
        ring_size = 25

        # Get the H3 hexagon for the center point
        center_h3 = h3.latlng_to_cell(input_lat, input_lng, resolution)

        # Generate hexagons within a disk around the center (instead of just rings)
        hexagons = list(h3.grid_disk(center_h3, ring_size))  # All hexagons within the distance

        # Create a GeoDataFrame with hexagons and their corresponding geometries
        hexagon_geometries = [Polygon(h3.cell_to_boundary(hexagon)) for hexagon in hexagons]

        # Create the GeoDataFrame
        hexagon_df = gpd.GeoDataFrame({'Hexagon_ID': hexagons, 'geometry': hexagon_geometries},  crs="EPSG:4326")

        gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf['latitude'], gdf['longitude']),  crs="EPSG:4326")

        if gdf.crs != hexagon_df.crs:
            gdf = gdf.to_crs(hexagon_df.crs)
        # Perform spatial join
        joined = gpd.sjoin(gdf, hexagon_df, how='left', predicate='intersects')

        # Return only the original DataFrame with the new Hexagon_ID column
        gdf['Hexagon_ID'] = joined['Hexagon_ID'].values

        return gdf

    def clean_daily_file(self, raw_path, clean_path):
        """
        Clean a single daily file. each cleaning step should be a sub function
        :param raw_path:
        :param clean_path:
        """
        daily_dtypes = {'station_id': 'str', 'element': pd.CategoricalDtype(), 'm_flag': pd.CategoricalDtype(),
                        'q_flag': pd.CategoricalDtype(), 's_flag': pd.CategoricalDtype(), 'date': str, 'time': str,
                        'value': 'float'}
        df = pd.read_csv(raw_path, header=None,
                         names=['station_id', 'date', 'element', 'value', 'm_flag', 'q_flag', 's_flag', 'time'],
                         dtype=daily_dtypes, engine='pyarrow')
        # daily file cleaning steps:
        # 4. process dates
        df = self.process_dates(df)
        # 2. drop unwanted columns
        df = self.drop_daily_columns(df)
        # 5. create element table
        df = self.create_element_tables(df)
        # 6. join elements into single table
        df = self.join_element_tables(df)
        # 7. join with stations
        df = self.join_stations_elements(df, self.query_stations())
        # 8. drop unwanted columns
        df = self.drop_station_columns(df)
        # 9. generate geometries
        gdf = self.generate_geometries(df)
        #10. Generate h3 cells
        gdf = self.generate_hexes(gdf)
        gdf.to_parquet(clean_path)
