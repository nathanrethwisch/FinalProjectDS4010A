## 2-14-2025
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

## 2-21-2025
### Project Goals
- Target audience – Ultimately, our target audience would be homeowners, real estate investors, and those planning trips to areas of high wildfire risk. However, given the scope of  

- Response variable -  Our response is the probability of a fire occurring in a given area. Then, if we can predict that data, we can also try to predict the severity (size & damage) of the fire. 

- Dashboard Usefulness - This dashboard is useful for predicting the probability of a wildfire occurring in a given area. This is important for homeowners, backpackers, and real estate investors.  

- Similar dashboards - We’ve found some similar maps in ArcGIS - https://isugisf.maps.arcgis.com/apps/mapviewer/index.html?webmap=336503af2034455b8ba03e8972ec252f. This map does a good job of visualizing where wildfires have occurred in the past. There are also dashboarding tools in ArcGIS which seem straightforward, such as the one implemented here: https://isugisf.maps.arcgis.com/apps/dashboards/3c160943b14c40bb88ca2d7b108da72d 

### Modeling Plan
- With a response variable of probability of fire occurrence, a logistic regression or somewhat similar prediction model would be appropriate.  

- Weather/Environmental variables are our main variables that will be used to predict the probability of ignition. This includes precipitation, temperature, snowfall, humidity, wind speed, etc. 

- Severity/Duration will be dealt with at a later date as another potential response variable. 

- These types of models would be fairly easy to implement in the dashboarding plan, as we can use ArcGIS to visualize our prediction scores by geographic location. 

- Assumptions of independence between locations are met. Multicollinearity may be present between certain predictors and will need to be analyzed when we get to the modeling phase of the project.

### Exploratory Analysis
- So far, we have been plotting the wildfire data using R’s leaflet package. Here’s an example of the plotting of some wildfire location
![wildfire locations](https://github.com/user-attachments/assets/b7140fe6-b3e6-416f-b2a3-90fbd20693a8)
- However, going forward, we probably want to move towards using geopandas in Python and more ArcGIS tools, as that is what we want our dashboard to run on. Therefore, this specific plot will probably not be included in our final dashboard, but we will have very similar plots that overlay predictions and/or past data. 

- Next week, we will focus on summary statistics for the weather data as we were able to pull that data in this week. 

- We’ve also taken out outliers from the wildfire data of points that were not within the US or data that did not make logical sense. Colin has worked on cleaning the data by removing variables that aren’t necessary and removing some NA values. 

### Project Progress 
- Dhruv has written scripts to download and process NOAA weather data. Colin has written scripts for cleaning wildfire ignition point data. Nathan has been experimenting with plotting gis data in R, Thanh has been experimenting with a few weather API’s to be used for real-time data acquisition. 

- Everyone knows how to set up the tech stack: R, Python, venv, renv 

- Next steps: We are still having issues with the size of the weather data. We expect these will be sorted out by early next week. After that we will have to write a script to transform the weather data into a format acceptable for modeling. Then we can begin to experiment with modeling.  

  - We have a lot of research ahead of us in modeling GIS data. 

  - The team is communicating very well and everyone knows what they need to do for the next week or so. 
