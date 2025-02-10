# FinalProjectDS4010A
This repository stores Team P-Value Posse's work for our data science capstone at Iowa State University (DS4010). The goal of this project is to create a usable dashboard that predicts wildfire occurrence, spread, and severity. 

To achieve this, we are pulling data from the United States Forest Service (USFS) on historical wildfire location and severity. We also have pulled data from NOAA (National Oceanic and Atmospheric Administration) on historical weather patterns. By combining this data, we aim to build a predictive model that provides valuable information on wildfire risk.

## Team Members
- Dhruv Dole  - @dsdole
- Thanh Mai - @tanh-x
- Nathan Rethwisch - @nathanrethwisch
- Colin Russell - @colinrussell5
  
## Folders
The current folder structure contains a `/data` folder where our raw data and descriptions of the data are being housed. Future folders will be added to house the dashboard and data processing code.
Certain data sets involve API calls, such as the Open-Meteo Historical Weather data. The Python code for these API calls are located in `/py-notebooks` 

## Data Processing
The following steps highlight how we are planning to process the data used for this project:
1. Add raw data to `/data/raw` using LFS if necessary
2. Read data into pandas and set datatypes
3. Export pandas dataframes as parquet to preserve data.


