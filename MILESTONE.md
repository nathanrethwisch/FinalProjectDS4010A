### Project Goals
The primary research goals of this project currently includes identifying and analyzing environmental, meteorological, and geographical factors that have the potential to influence the risk and severity of wildfires. We also aim to develop a live monitoring system of risk factors to assess and predict the likelihood of wildfire threats.  

### Technology Plan
Our current technology plan involves both the use of R and Python for cleaning. We’ve been using R to clean more of the wildfire data and Python for some of the weather data. As we continue to progress to more predictive models, we likely will combine all of the data and work exclusively in Python. Python has a GIS library called geopandas that will be useful for working with this geospatial data. We plan on using a standardized dataset framework (Apache Arrow) and storing in Apache Parquet format so that it is easy to work with across multiple software. For dashboarding, we are looking into using ArcGIS. We have looked at other dashboards in ArcGIS, and it seems reasonable as a software to learn. However, if this doesn’t work, we will likely turn to Python’s dash framework. 

### Data Wrangling
At this point in the semester, we have written an R script which pulls csv files on fire locations from the United States Fire Service and cleans it by removing missing values and making sure coordinates are reasonable. We have also mapped the coordinates of historical fires on a map of the US using the dataVisualization.R file. For NOAA weather data, a python script to download, clean, and partition the dataset is being written.  

### Team Evaluation
So far, we are progressing nicely towards our project goals – we have started cleaning and visualizing some of the data, and weather data is almost pulled. There are a couple of obstacles we are watching out for: 

- The size of the weather data may be difficult to work with – we may need to limit the amount of data we are using to make the dashboard usable or rethink how we are processing/storing the data. 

- We don’t have a ton of experience using ArcGIS for dashboarding, so we will need to learn this tool. 

- Our current wildfire data contains a base longitude/latitude as well as fire size but does not include a geospatial perimeter around the whole fire. This may limit our analysis in some ways unless we can find this data. 
