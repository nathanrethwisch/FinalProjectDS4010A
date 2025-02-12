library(dplyr)

#################
#Data processing#
#################

#Initial importing and selecting rows
occur <- read.csv("C:/Users/colin/Downloads/National_USFS_Fire_Occurrence_Point_(Feature_Layer) (1).csv")
occurDF <- fire %>%
  select(UNIQFIREID, FIREYEAR, DISCOVERYDATETIME, FIREOUTDATETIME, SIZECLASS, TOTALACRES, STATCAUSE,
         LATDD83, LONGDD83)
occurDF <- na.omit(occurDF)

min <- min(occurDF$FIREYEAR, na.rm=FALSE)
max <- max(occurDF$FIREYEAR, na.rm=FALSE)


#Checking the size class vs total acres.
set.seed(1000)
rows <- sample(nrow(occurDF), 5)
class <- occurDF$SIZECLASS[rows]
acres <- occurDF$TOTALACRES[rows]



#Cleaning Fire Years
validYears <- 1900:2023
invalid <- which(!(occurDF$FIREYEAR %in% validYears))
occurDF <- occurDF[-invalid, ]


#Checking Longitude and Latitude values
set.seed(100)
lon <- sample(occurDF$LONGDD83, 5, replace=FALSE)
lat <- sample(occurDF$LATDD83, 5, replace=FALSE)



#NA Values?
sum(occurDF$UNIQFIREID == "", na.rm=TRUE) #200476
sum(occurDF$FIRENAME == "", na.rm=TRUE) #26925
sum(occurDF$FIREYEAR == "", na.rm=TRUE) #0 
sum(occurDF$DISCOVERYDATETIME == "", na.rm=TRUE) #47147
sum(occurDF$SIZECLASS == "", na.rm=TRUE) #452
sum(occurDF$TOTALACRES == "", na.rm=TRUE) #0
sum(occurDF$STATCAUSE == "", na.rm=TRUE) #552
sum(occurDF$FIREOUTDATETIME == "", na.rm=TRUE) #412582
sum(occurDF$LATDD83 == "", na.rm=TRUE) #0
sum(occurDF$LONGDD83 == "", na.rm=TRUE) #0



###########################
# Fire Perimiter Cleaning #
###########################
#perim <- read.csv("C:/Users/colin/Downloads/National_USFS_Final_Fire_Perimeter_(Feature_Layer).csv")
#perim <- na.omit(perim)
#perimDF <- perim %>%
#  select(UNIQFIREID, FIREYEAR, SHAPEAREA, )


#min <- min(perim$FIREYEAR, na.rm=FALSE)
#max <- max(perim$FIREYEAR, na.rm=FALSE)

#join <- inner_join(occurDF, perimDF, by="UNIQFIREID")





####################
#Exploring the data#
####################

#samp <- occurDF[sample(nrow(occurDF), 10, replace=FALSE), ]

