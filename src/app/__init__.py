from datetime import date
import geopandas as gpd
import dash_leaflet as dl


from dash import dcc

field_selection = dcc.RadioItems(
    id='field-checklist',
    options=[
        {'label': 'Precipitation', 'value': 'prcp'},
        {'label': 'Max Temperature', 'value': 'tmax'},
        {'label': 'Min Temperature', 'value': 'tmin'},
        {'label': 'Snowfall', 'value': 'snow'},
        {'label': 'Wind', 'value': 'snwd'}
    ],
    value=None
)

date_picker = dcc.DatePickerSingle(
    id='date-picker',
    min_date_allowed=date(2000, 1, 1),
    max_date_allowed=date(2025, 2, 28),
    initial_visible_month=date(2020, 1, 1),
    date=date(2020, 1, 1),
)

def get_layer(selected_field, date):
    def gdf_to_geojson(gdf):
        return {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": shapely.geometry.mapping(row.geometry),
                    "properties": {}
                } for _, row in gdf.iterrows()
            ]
        }
    
    output_data = read.parquet(gpd.read_parquet("../data/curated/hexagon_data.parquet"))

    geojson_data = gdf_to_geojson(output_data)
    return dl.GeoJSON(data=geojson_data, style={"color": "blue", "weight": 2, "fillOpacity": 0.4}, id="hexagons-layer")

