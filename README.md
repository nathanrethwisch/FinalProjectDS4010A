# FinalProjectDS4010A
This repository stores Team P-Value Posse's work for our data science capstone at Iowa State University (DS4010). The goal of this project is to create a usable dashboard that predicts wildfire occurrence, spread, and severity. 

To achieve this, we are pulling data from the United States Forest Service (USFS) on historical wildfire location and severity. We also have pulled data from NOAA (National Oceanic and Atmospheric Administration) and other sources on historical weather patterns. By combining this data, we aim to build a predictive model that provides valuable information on wildfire risk.

## Team Members
- Dhruv Dole  - @dsdole
- Thanh Mai - @tanh-x
- Nathan Rethwisch - @nathanrethwisch
- Colin Russell - @colinrussell5
  
## Folders
- The current folder structure contains a `/data` folder where our raw data and descriptions of the data are being housed.
- Certain data sets involve API calls, such as the Open-Meteo Historical Weather data. The Python code for these API calls are located in `/py-notebooks`
- Source code for cleaning and processing the data can be found under the `/src` folder.
  .
  └── root/
  ├── .venv/
  ├── data/
  │   ├── raw/
  │   │   ├── ghcnd/
  │   │   │   ├── metadata.html
  │   │   │   ├── daily/
  │   │   │   │   ├── 1900.csv.gz
  │   │   │   │   ├── ...
  │   │   │   │   └── 2025.csv.gz
  │   │   │   └── stations.txt
  │   │   └── fire_point/
  │   │       ├── raw.zip
  │   │       └── "METADATA HERE!"
  │   ├── curated/
  │   │   ├── ghcnd/
  │   │   │   ├── daily/
  │   │   │   │   ├── 1900.parquet
  │   │   │   │   ├── ...
  │   │   │   │   └── 2025.parquet
  │   │   │   ├── stations.parquet
  │   │   │   └── METADATA.md
  │   │   └── fire_point/
  │   │       ├── fire_point.parquet
  │   │       └── METADATA.md
  │   └── tmp/
  ├── py-notebooks/
  ├── src/
  │   ├── README.md
  │   ├── ghcnd/
  │   │   ├── README.md
  │   │   ├── clean.py
  │   │   ├── download.py
  │   │   ├── transform.py
  │   │   └── utils.py
  │   └── fire-point/
  │       └── ...
  ├── MILESTONE.md
  ├── README.md
  ├── requirements.txt
  ├── .gitignore
  └── .gitattributes

## Data Processing
The following steps highlight how we are planning to process the data used for this project:
1. Add raw data to `/data/raw` using LFS if necessary
2. Read data into pandas and set datatypes
3. Export pandas dataframes as parquet to preserve datatypes in `/data/raw`.


## Deployment
All commands are run from the repo root

### Configuration
- Port Mappings: inside `docker-compose.yml`, set the port mapping to match your environment(https://docs.docker.com/get-started/docker-concepts/running-containers/publishing-ports/)

- Gunicorn Workers: the number of threads used by the dashboard

### Recommended deployment
For public deployments, the dashboard container should listen be placed behind a reverse proxy such as nginx or caddy.
This app can be deployed using the given docker compose file, or it can be deployed via Azure Container Apps or AWS Elastic Container Service.

A docker compose deployment allows it to run on any machine with docker engine installed. Azure Container Apps is also nice because it can scale automatically scale from 0 instances(cheap or free) when there are no users, up to as many as needed to maintain quick responses. Azure Container Apps will also handle ingress, log management, and TLS termination. 

### Docker Compose
Clone this repository to a machine with [docker engine](https://docs.docker.com/engine/install/) installed.

```bash
git clone --depth 1 https://github.com/nathanrethwisch/FinalProjectDS4010A.git wildfire-dashboard
cd wildfire-dashboard
```

#### build
```bash
docker compose build
```

#### Start Dashboard
```bash
docker compose up -d 
```

#### Build and Start Dashboard
```bash
docker compose up -d --build
```

#### View Logs
```bash
docker compose logs # print to stdout

docker compose logs -f # watch logs (like tail -f)
```

### Stop Dashboard
```bash
docker compose down
```