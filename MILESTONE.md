## Team Formation Milestone
To pick our team name, we used chatGPT to come up with a list of “funny” team names that we liked. We hadn’t picked a group project at the time yet, but “P-value posse” was the only thing that made us laugh, so that’s what we decided to go with. We haven’t been using the team name very much and typically refer to ourselves as team A. 

## 2-14-2025: Acquire Data Milestone
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

## 2-21-2025: Project Goals Milestone
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

## 2025-03-03: Exploratory Analysis Milestone
### Project Progress
Individual Progress: 

- Nathan – This week, I worked on learning ArcGIS. I created a sample dashboard for use going forward and created some summary statistics using the software. 
- Dhruv – This week, I have been working on reducing the size of the NOAA weather data by removing unneeded variables and records. I want to have finalized read-only tables uploaded to onedrive and github by 2025/03/04 
- Colin - This week, I finalized the Fire Occurrence data by cleaning the cause of fires and adjusting the lon/lat of origin. I also have done some exploratory analysis in R using the packages ‘sp’ (which is compatible with ArcGIS) and ‘leaflet’. 
- Thanh - This week, I worked on exploratory data analysis for the USFS fire occurrence and perimeter datasets. I created several preliminary visualizations to examine the climate conditions around when wildfires begin to spread. 
 
Every team member has access to the ArcGIS dashboard and will have access to the weather data by the end of this weekend. Going forward, we are going to try to load the weather data in ArcGIS to be sure that ArcGIS can handle this large dataset and create visualizations around them. We will also start running simple models in Python to see what kinds of predictions we get. In terms of roadblocks, we are going pretty smoothly. There may be some anticipated roadblocks with the size of the data, but we’re prepared to face these by reducing the size of the data, and using libraries which lazy-load data. Going forward, each member has a role – Dhruv is exploring the weather data in ArcGIS, Nathan is doing some simple dashboarding, Colin is cleaning the weather data and looking into models, and Thanh is pulling soil data via an API. 

We have also switched from a sms group chat to MS Teams to avoid some communication issues. 

### Exploratory Analysis 
We’ve had to do some cleaning with the wildfire data. Specifically, we’ve had to remove outliers for the longitude and latitude coordinates that were inaccurate or outside of the United States. We’ve visualized historical wildfires, and this will likely be added as a final layer to our dashboard. Other summary statistics, such as the total number of acres burned, wildfires by year, and wildfires by cause, were also graphed. We were surprised to find less wildfires in recent years, as well as not many fires caused by arson (only 23 in the dataset). The two exploratory plots shown are examples of some of the cleaning that we did for wildfire causes.
![Exploratory Analysis 1](https://github.com/user-attachments/assets/4badd6f6-23f9-4a76-aa71-625d828941d5) ![Exploratory Analysis 2](https://github.com/user-attachments/assets/103cc9f5-f510-4308-a687-d55c2b954350)

### Brainstorm Dashboard
Our dashboard is trying to identify areas where wildfires are predicted to happen and potentially the severity of such wildfires. We are looking at using heatmaps within ArcGIS to achieve this goal. Ideally, a user could select an area on the map and pull up summary statistics for that area from weather patterns, soil, and historical wildfires. It will also give a number or summary statistic from our machine-learning model summarizing the likelihood of a fire. We have started to play with the dashboarding tool in ArcGIS, which also has been nice for creating summary statistics. The attached image shows an example of what the dashboard could look like. Right now, it just shows summaries of historical wildfires, but our goal would be to have it show future wildfire predictions. There are also filtering tools that we may want to include, like filtering by areas of high/low precipitation, high/low wind, etc. 
![example dashboard](https://github.com/user-attachments/assets/2d4e5ee8-7a55-4a81-92a4-cb4bae34ee75)

### Data Report 
One struggle that we’ve been facing is that the data we have, specifically the weather data is very large. However, we’ve been able to load this data and get it in a somewhat manageable format.  

NOAA Global Historical Climatology Network daily(GHCNd) data: 
The raw data has been downloaded and processed into a typed format. We have also filtered weather station location for US, Canadian, and Mexican stations. The final 2 steps are to join the North American stations with the weather records, and to filter nulls and convert value units to US Imperial Units 
Sources/tables: 
Stations.txt: fixed-width file processed by pandas and stored as parquet 
Superghcnd: a directory of csv.gz files, each representing a single year of observations. Has been processed into parquets, and transformed to include each type of observation as a separate variable. 
Finalized data: drop all superghcnd records not from North America  
Once completed, a final metadata/codebook will be placed in the repo. 

USFS Wildfire data:  The data has been downloaded as a csv and cleaned. We have plotted it via ArcGIS, and it is in a usable format for further work/predictions. 

## 2025-03-09: Brainstorm Dashboard Milestone

### Project Progress
This week, we worked on getting ready to run some models. Although we don’t have a model picked out, we wanted to get to a point where we could start thinking about what types of models we want to use. First, all of the weather and fire data is cleaned and pushed, and we have been able to query both by year and location. One idea that we had was to use a box around fire locations and create summary statistics within that box to predict whether or not a fire would occur.

![ProjectProgress3-9](https://github.com/user-attachments/assets/645a4470-cc9d-4410-a36b-c6f605427c3a)

In this upcoming week, we hope to have a model picked out and run to analyze the results and see what changes we need to make. We also have talked about limiting our data to a specific area such as California, so we may start with modeling that small area to see what results we get. Overall, the team is communicating well when moving to Teams. Everyone has put in good work this week and understands what they need to do to keep moving forward. We have all been researching models to use and hope to start running in the next few weeks.

### Brainstorm Dashboard
A few things have changed on our dashboard, but it remains relatively similar. We have updated the sample dashboard with the cleaned fire data, and this can be seen below:

![ExampleDashboard3-9](https://github.com/user-attachments/assets/30a18b5c-7de3-441a-b268-1741c5710399)

We’re interested in using ArcGIS Pro for dashboarding as this will have better functionality for loading in this large dataset. Because the large size of our data, we are likely going to have to use Geopandas or an R alternative to plot locally. We then will be creating models and plotting the output of our predictions using ArcGIS. This will limit the amount of data that will needed to be pushed to ArcGIS while still allowing us to use its dashboard functionality. 

### Finalize Data Models
-	We have not yet begun modelling, so we have nothing to say yet on model types or hyperparameters.
-	The response is numeric: either the size of the fire or the probability of a fire occurring.
-	There are many predictors: at least 5 different weather measurements including precipitation, temperatures, and humidity. We also have variables for soil moisture content.
-	Our biggest issue right now is finding a way to relate our predictor and response datasets together. We need to spatially join records. This is complicated due to the fact that many different dates’ weather records will be directly related to a single fire occurrence.
-	We are considering two questions(we will choose based on which one is more achievable): What is the probability of a fire occurring at a given point and time? What is the predicted severity of a fire?
- Sketch:

![SketchModel3-9](https://github.com/user-attachments/assets/80711d96-e966-4b19-9b99-56b915ddb10a)
 
### Team Mini Milestone - Finalize Data
MILESTONE: Finalize all data access: make sure variable datatypes are set. All datasets should be stored as parquet (preserves types). Data(except for ghcnd) should be uploaded to Github. NOAA GHCND pipeline scripts should be working for all team members and helper functions for querying should be tested and uploaded to github.

PROGRESS: The NOAA GHCND dataset’s pipelines and helpers are working. As we write reports and test models, we will upload the subset of data used for that report into the github repo. The fire data has been cleaned and saved as a parquet file as well. We have successfully been able to query both datasets, and data types seem to be set. We are now ready to start running models and see how our data responds.

## 2025-03-15: Finalize Data Models

### Project Progress
We have decided to split our data into two separate models and made progress on both aspects: 
-	For the fire severity model, Thanh worked on looking at the geographic boundaries of fires and pulling data from the fire stations that lie within those boundaries. For fires that were too small, he extended the boundary so that every fire had at least one weather station.
-	For the fire prediction model, Nathan worked on overlaying cells on a map of the US and assigning both fires and weather stations in the US to a respective cell. Based on the cell, we can then aggregate weather data to predict whether or not a fire occurred in the cell at a given point.
This week, we also had trouble running out of space with Git LFS. Dhruv set up a Symlink to OneDrive that allows us to access data outside of the repo without having to use LFS space every time we pull the files. Dhruv also was able to get geometries for each state, meaning that we are able to limit our predictions to California to start with, giving us less data as we begin to train models.
In addition, Collin has worked on cleaning the fire data as a parquet shape file and pushing that back to the repo.
The team is working together very well, we’ve managed to organically work on multiple portions of the project at once instead of fixating on a single part and neglecting others.

### Dashboard Sketch
Because a majority of our data exists in Python, as well as our models, we are moving towards Dash instead of ArcGIS. The main goals and sketches from ArcGIS are still what we want to represent, but we will use Dash instead. Dhruv has done some exploratory work in Dash and has shown that it will work for our purposes. In terms of our dashboard, we want to display two maps – one that has a heatmap with the probability of a fire occuring, and the other that has a prediction of fire severity. We could also have overlaying maps that could be filtered by weather patterns, soil, etc. 
Our current thinking is to have a full page interactive map, with a sidebar that allows selecting the elements to view. There should also be zoom/scale map controls, and a detail view for specific hex cells. 

### Finalize Data Models
At this point, we are splitting into two separate models – one that predicts fire severity and the other that predicts whether or not a fire will occur in a given area. Both are based on historical weather and soil patterns. 

_Fire Severity Model_: This model is meant to grade fire severity. We are planning on a clustering algorithm. Using the H3 hex cells, we will aggregate weather data for 3 or so days around a fire. Then given the size of the fire, and how long it took to extinguish, we will cluster the fires and assign severity grades. 

_Fire Prediction Model_: For this model, we are planning on doing a random forest/xgboost or a logistic regression – type model. We have created a geofence around the US using Uber’s H3 cells. Then, using these cells, we can aggregate weather data for the 3 or so days before a fire from all weather stations in a cell. This also gives us negative data, as places were fires did not occur are input with a 0, whereas a fire occurring will be a 1. By the end of spring break, we hope to have those aggregate statistics so we can actually run some of these models.

![Picture1](https://github.com/user-attachments/assets/61c18b3e-db29-42e2-b123-de83a1f9ae13)


### Spring Break Plans
Over spring break, we will continue to work individually and share our progress on teams. The following is each person’s plans:
-	Nathan: I am going to be out of the country over most of Spring Break. I have pushed the file that creates H3 cells for each geolocation of the United States for both the fire and weather data, allowing us to join the data easily and calculate aggregate statistics needed for modeling
-	Dhruv: I plan on using the H3 grid to begin aggregating the data, creating hex plots, and viewing them in dash. 


## 2025-03-30: Finalize Dashboard Sketch
Below is an example sketch of our Dashboard in Dash. The main focus of the dashboard will be the map in the middle. Different checkboxes can be used to see map layers and statistics about temperature, snowfall, precipitation, etc. Clicking on a specific hex in the map will then bring up model output and historical weather data for that region in the right-hand sidebar.. A slider or date field below the map can be used to change the dates in which the weather information is shown. The bottom Panel will include any other options.  

If we have time, we may add a 2nd tab to the app to view weather and wildfire trends over time(not mapped).  
![image](https://github.com/user-attachments/assets/7e668dc3-10fc-4b9e-b2f8-cbc5d3950d2b)

 ![image](https://github.com/user-attachments/assets/12f3361d-17cb-41cf-8e74-8890822bbb1f)

For each date, our random forest model currently outputs a probability of a fire occurring. We then normalized that score from 0 to 1. Each hex is plotted on a map of the US, with the idea that a slider can be used to change the prediction date.

## 2025-04-06: Minimum Viable Dashboard
Our current dashboard is in a working state but allows the user to select different summary statistics and see the output change on a map of the US divided by hexes. Currently, the user can see model predictions, as well as 3-day output for precipitation, snowfall, minimum temperature, and maximum temperature. We are still working on things like making the dashboard look better, updating null values (which are the black hexes), etc. Furthermore, we are also fine-tuning the model and testing other modeling methods, so right now we just have example output from June 1, 2020, to June 10, 2020, that the user can select from. Going forward, we are going to finalize model output and push files for a larger number of years. We will also work on displaying summary statistics for each hex based on the hex that a user selects. Here is a link to the dashboard, which is now hosted on Render: 
https://wildfire-predictions-finalprojectds4010a.onrender.com/ 
NOTE: YOU MUST SELECT MAP OVERLAYS FOR VIEWING IN THE MENU WHICH IS OVERLAYED ON THE MAP, NOT THE “DATA” MENU IN THE LEFT SIDEBAR. DATES CAN BE SELECTED FROM THE LEFT SIDEBAR. 

Note that sometimes, switching between dates can be somewhat slow. Our plan to fix this is to precompute dataframes for each date. This dataframe can be loaded dynamically using the date field. Dash Leaflet will handle selection and display of different kinds of map layers. 
 We are currently working on getting a heatmap from our model output into Dash. Here is an example of what our model will output:  


## 2025-04-13: Add Models to Dashboard
The model on the dashboard is a random forest model. The explanatory variables we chose to use in the model were Hexagon location, average elevation, month, and three-day averages of snowfall, precipitation, temperature maximum, and temperature minimum. We did not use evaporation due to the number of missing values it had. The output of the random forest model shows a 0-1 probability of the chance of a fire occurring in each hexagon location on a given day. Other missing values for our predicted were inputed by looking at the neighboring hexes for that particular date and taking an average of their values. If 1 hex was not enough, we moved 2 rings out. Although this may not be the most statistically accurate approach, due to the small number of missing values and relative geographical similarity between hexes, we felt that it was appropriate to use for missing value imputation. The model was trained on data from 2000-2019 and tested on data from 2020-2025. 
We tested out many different models, including xgboost, logistic regresion, and naive bayes. We optimized the threshold for prediction by selecting the optimal F1 score among all models (which is the average of precision and recall), trying thresholds from 0-1 at a 0.01 interval. In the end, we selected a random forest model because it had the highest F1 score and recall, and because it is more interpretable than similar models. 
 ![image](https://github.com/user-attachments/assets/b3502f2a-eb4f-47ff-9339-f671c7255c10)
![image](https://github.com/user-attachments/assets/70349a3f-5052-4b68-bc2a-317d122eab4a)

 
Once we decided on a random forest model, a randomized grid search was performed. We fit random forests with different hyperparameters, including different max depth, number of trees in the forest, and number of features needed to split a node. Overall, the optimal parameters were found to be 200 estimators with a depth of 30 and 3 features per split. We then retrained using this model, improving F1 score to 0.197029, which is still admittably not great, but given the volatile nature of wildfires and the fact that overall model accuracy is still 0.963756, we felt it was an acceptable threshold.

Our model is shown on the dashboard by clicking on the “Normalized Probabilities” section of the map. We are planning to change this heading to “Relative Fire Risk” to prevent confusion as the values are currently normalized to range from 0-1, but the probability of a fire occurring is never 100%. The goal is to be able to click on an individual hex and have the probability from the random forest model as well as weather information be displayed on a table in the right sidebar. Right now, however, model output is just displayed by color on a hex map for dates from 2020-2025. 

The dashboard is currently hosted at: https://wildfire-predictions-finalprojectds4010a.onrender.com
This is what it currently looks like: 
 
 ![image](https://github.com/user-attachments/assets/693ebed9-c2ae-44f5-acb6-6f9f2adb0a7b)
![image](https://github.com/user-attachments/assets/996232d3-187b-4a3d-bb36-56ef317d0b31)

## 2025-04-20: Dashboard Peer Review
Our dashboard is mostly complete – three are just a few minor things we want to implement. Right now, the main tab shows a map of the US. Depending on what the user selects, there is a hex of heatmaps that shows predicted fire probability, snowfall, precipitation, etc. The user can then select a hex and get information about each of these variables on a given date. There is also a date slider at the bottom of the screen to control what date is selected. Other tabs include a time series plot of fire count over time and a model info tab that gives information about the dashboard and model.  

For future steps, we want to make the dashboard more appealing based on peer feedback. We also want to comment and clean some of the code. The docker file is ready to go, so these changes should be easy to implement, and then we are done! 

Because the dashboard uses so much memory, we could not use onRender. However, we will host it using Dhruv's computer for peer review. Here's a video link of a demo of the dashboard: https://iowastate-my.sharepoint.com/:v:/g/personal/dsdole_iastate_edu/EUgxpFD1u8pJoRd9fWlRq70BANWB52Itajhrhf8ZwlaSSw?e=IC33sr

## 2025-04-27: Finalize Dashboard 
To finalize the dashboard, we made some minor adjustments, including adding a title and cleaning some of the files. We made a docker file, so we are ready to send out the dashboard and host it. Right now, it is being hosted at https://wildfire.ddole.net/. Over the last week, we added a copy to clipboard button for the model output. There are some minor changes we are considering making. One thing that we want to do is make a css style file that allows us to make dashboard features look better. We also want to add a few graphs that show how certain weather variables – precipitation, snowfall, temperature, etc. have changed over time. There are also a few changes we want to make to the info tab to make it more informative based on peer feedback. Other than that, we feel pretty good with where we’re at, and any additional changes will be if we have any extra time. 





