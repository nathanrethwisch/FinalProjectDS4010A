library(leaflet)
library(dplyr)
library(arrow)
library(ggplot2)

#######
#Notes#
#######

#See if you can overlay fire intesity ratings over the fire occurence time series.


fire <- read_parquet("C:/Users/colin/OneDrive/Documents/Fire_Occurence.parquet")

#Interactive map of ISU
leaflet() %>%
  addTiles() %>%
  addMarkers(lng = -93.65, lat = 42.03, popup = "Iowa State University")


#General Map
leaflet(data = fire %>% filter(STATE %in% c("OR"))) %>%
  addTiles() %>%
  addCircleMarkers(
    lng = ~LONGDD83,
    lat = ~LATDD83,
    radius = 2,
    color = "red",
    popup = ~paste("Cause:", STATCAUSE, "<br>", "Acres:", TOTALACRES)
  )



#########################
#Bar Chart of Stat Cause#
#########################

stat_sum <- fire %>%
  group_by(STATCAUSE) %>%
  summarise(count=n()) %>%
  arrange(desc(count))

ggplot(data=stat_sum, aes(x=STATCAUSE, y=count)) +
  geom_bar(stat="identity") +
  xlab("Stat Cause") +
  ylab("Cause of Fire") +
  theme_minimal()




#############
#Time Series#
#############
library(plotly)
library(dplyr)
library(lubridate)
library(htmlwidgets)
library(zoo)

#Group fires by week
fires_week <- fire %>%
  mutate(date = as.Date(DISCOVERYDATE),
         week = floor_date(date, "week")) %>%
  group_by(week) %>%
  summarise(fire_count = n(),
            avg_acres = mean(TOTALACRES))


#Creates the plotly plot
plot <- plot_ly(fires_week, x = ~week) %>%
  add_trace(
    y = ~fire_count,
    type = 'scatter',
    mode = 'lines+markers',
    name = "Fires per Week",
    line = list(color = 'red', width = 2),
    marker = list(size = 4),
    fill = "tozerox",
    fillcolor = "red"
  ) %>%
  add_trace(
    y = ~avg_acres,
    type = 'scatter',
    mode = 'lines+markers',
    name = "Avg Acres Burned",
    line = list(color = 'green', width = 2),
    marker = list(size = 4),
    yaxis = "y2",
    fill = "tozeroy",
    fillcolor = "green"
  ) %>%
  layout(
    paper_bgcolor = 'black',
    plot_bgcolor = 'black',
    font = list(color = 'white'),
    title = "Weekly Fire Count and Avg Acres Burned",
    xaxis = list(
      title = "Date",
      rangeselector = list(
        buttons = list(
          list(count = 6, label = "6m", step = "month", stepmode = "backward"),
          list(count = 1, label = "1y", step = "year", stepmode = "backward"),
          list(count = 2, label = "2y", step = "year", stepmode = "backward"),
          list(step = "all")
        ),
        font = list(color='black')
      ),
      rangeslider = list(visible = TRUE),
      type = "date"
    ),
    yaxis = list(title = "Number of Fires"),
    yaxis2 = list(
      title = "Avg Acres Burned",
      overlaying = "y",
      side = "right"
    ),
    hovermode = "x unified"
  )


plot

saveWidget(plot, "final_fire_timeseries.html", selfcontained = TRUE)












