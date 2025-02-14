#install.packages(c("leaflet", "sp"))
fireDataMap <- function(fireData){
  df <- data.frame(fireData$LONGDD83, fireData$LATDD83)
  df2  <- df %>% tail(10000)
  coordinates(df2) <- ~fireData.LONGDD83 + fireData.LATDD83
  leaflet(df2) %>%
    addTiles() %>%
    addCircleMarkers(radius = 2, color = "red", fillColor = "red")
}






