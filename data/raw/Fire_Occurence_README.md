# Fire Occurrence Data Processing and Mapping

## Overview
This project focuses on processing and analyzing fire occurrence data from the U.S. National Forest Service (USFS). It includes data cleaning, filtering, and visualization using R. The script loads and processes a CSV dataset containing fire occurrences, extracts relevant information, and maps fire locations using the `leaflet` package.

## Requirements
Ensure you have R and the required packages installed before running the script.

### Required R Packages
The script uses the following R packages:
- `dplyr`
- `ggplot2`
- `sp`
- `leaflet`

To install missing packages, run:
```r
install.packages(c("dplyr", "ggplot2", "sp", "leaflet"))
```

## Data Processing Steps

### 1. Importing Data
- The script reads fire occurrence data from a CSV file located at:
  ```
  C:/Users/colin/Downloads/National_USFS_Fire_Occurrence_Point_(Feature_Layer).csv
  ```
- The dataset is filtered to select relevant columns: `OBJECTID`, `DISCOVERYDATETIME`, `SIZECLASS`, `TOTALACRES`, `STATCAUSE`, `LATDD83`, `LONGDD83`.

### 2. Cleaning and Preprocessing
- Extracts the discovery date from `DISCOVERYDATETIME` and removes unnecessary columns.
- Removes empty values and ensures all data is valid.
- Standardizes and groups similar causes under `STATCAUSE`.
- Filters latitude and longitude values to include only U.S. locations.
- Outputs the cleaned dataset as `Fire_Occurence.csv`.

### 3. Data Verification
- Counts unique values in key columns to ensure data consistency.
- Checks for missing values and removes them.

### 4. Data Visualization
- Creates a bar plot of fire occurrence causes using `ggplot2`.
- Maps sampled fire locations using the `leaflet` package.

## Running the Script
1. Ensure all required packages are installed.
2. Update the file paths in the script to match your local directory structure.
3. Run the script in an R environment such as RStudio.

## Output
- A cleaned dataset saved as `Fire_Occurence.csv`.
- A bar plot of fire causes.
- An interactive map of sampled fire locations.

## To-Do
- Create a README file for this script ✅
- Look at NOAA pipeline and run it
- Analyze dataset comparing 'Start -> Fire Out' times

## Author
Colin Russell

## License
This project is open-source. Feel free to modify and distribute it as needed.

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

