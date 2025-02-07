# National USFS Final Fire Perimeter Dataset

## Overview
This dataset contains the **final perimeter shapes** of wildfires in the United States, as recorded by the **U.S. Forest Service (USFS)**. It provides spatial boundaries of fires, helping in fire impact assessment and risk analysis.

## Source
- **Agency:** U.S. Forest Service (USFS)
- **Dataset Catalog:** [Data.gov - Fire Perimeters](https://catalog.data.gov/dataset/national-usfs-final-fire-perimeter-feature-layer-80014)
- **Access Method:** Download as GeoJSON, SHP (Shapefile), or access via API.

## File Details
- **Filename:** `usfs_fire_perimeters.geojson` (or `.shp` for GIS use)
- **Format:** GeoJSON / Shapefile (SHP) / Feature Layer
- **Size:** Varies based on the dataset subset

## Data Dictionary
| Column Name          | Description |
|----------------------|-------------|
| `fire_id`           | Unique identifier for each fire |
| `fire_name`         | Name of the fire |
| `discovery_date`    | Date the fire was first discovered |
| `containment_date`  | Date the fire was fully contained |
| `fire_size`         | Fire size in acres |
| `fire_cause`        | Cause of the fire (Lightning, Human, Unknown, etc.) |
| `geometry`          | Fire perimeter polygon in GeoJSON or SHP format |

## Usage in This Project
- **Fire Spread Analysis:** Used to study how fires expand over time.
- **GIS Mapping:** Integrated with ArcGIS or QGIS to visualize fire boundaries.
- **Correlation with Weather & Wind Data:** Helps analyze how conditions impact fire perimeters.
- **Historical Fire Impact Assessment:** Assists in studying vegetation loss and urban impact.

## Notes
- **Missing Data Handling:** Some fires may lack `fire_cause` or `containment_date` details.
- **Projection:** Ensure the dataset's **spatial reference system (CRS)** matches other layers (e.g., WGS84 for global or NAD83 for the U.S.).
- **Data Updates:** The dataset is periodically updated by USFS.

## How to Access
1. Visit [USFS Fire Perimeter Data](https://catalog.data.gov/dataset/national-usfs-final-fire-perimeter-feature-layer-80014).
2. Download the dataset in **GeoJSON, SHP, or API access**.
3. Load into a GIS tool or a data processing script.

## How to Use in Python
### **Example: Load GeoJSON File and Convert to Pandas DataFrame**
```python
import geopandas as gpd

# Load fire perimeter dataset
fire_perimeters = gpd.read_file("usfs_fire_perimeters.geojson")

# Display first 5 rows
print(fire_perimeters.head())
