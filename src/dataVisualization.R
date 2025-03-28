#install.packages(c("leaflet", "sp"))
fireDataMap <- function(fireData){
  df <- data.frame(fireData$X, fireData$Y)
  df2  <- df #%>% head(10000)
  coordinates(df2) <- ~fireData.X + fireData.Y
  leaflet(df2) %>%
    addTiles() %>%
    addCircleMarkers(radius = 2, color = "red", fillColor = "red")
}






