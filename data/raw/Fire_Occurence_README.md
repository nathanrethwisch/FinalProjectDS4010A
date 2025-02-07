# National USFS Fire Occurrence Dataset

## Overview
This dataset contains **fire occurrence point data** from the **U.S. Forest Service (USFS)**, representing individual fire incidents across the United States. It includes details such as fire location, cause, size, and date.

## Source
- **Agency:** U.S. Forest Service (USFS)
- **Dataset Catalog:** [Data.gov - Fire Occurrence](https://catalog.data.gov/dataset/national-usfs-fire-occurrence-point-feature-layer-d3233)
- **Access Method:** Download as CSV, SHP, or access via API.

## File Details
- **Filename:** `usfs_fire_occurrence.csv`
- **Format:** CSV / Shapefile (SHP) / Feature Layer
- **Size:** Approx. (Varies based on download filters)

## Data Dictionary
| Column Name          | Description |
|----------------------|-------------|
| `fire_id`           | Unique identifier for each fire |
| `fire_name`         | Name of the fire |
| `latitude`          | Latitude coordinate of fire occurrence |
| `longitude`         | Longitude coordinate of fire occurrence |
| `discovery_date`    | Date the fire was first discovered |
| `containment_date`  | Date the fire was fully contained |
| `fire_size`         | Fire size in acres |
| `fire_cause`        | Cause of the fire (Lightning, Human, Unknown, etc.) |
| `fire_class`        | Fire classification based on size |

## Usage in This Project
- **Fire Risk Modeling:** Used to identify fire-prone regions.
- **Correlation with Weather Data:** Combined with historical weather (wind speed, humidity, temperature).
- **Fire Spread Analysis:** Helps in predicting wildfire behavior.

## Notes
- **Missing Data Handling:** Some entries have `null` values for `fire_cause` or `containment_date`.
- **Update Frequency:** Dataset is updated periodically by USFS.
- **Projection:** If using GIS software, check the coordinate reference system (CRS).

## How to Access
1. Visit [USFS Fire Occurrence Data](https://catalog.data.gov/dataset/national-usfs-fire-occurrence-point-feature-layer-d3233).
2. Download the dataset in CSV, SHP, or access via API.
3. Load the data into your analysis pipeline.

## Contact & Support
- **Data Provider:** U.S. Forest Service
- **Support Email:** [support@usfs.gov](mailto:support@usfs.gov)

