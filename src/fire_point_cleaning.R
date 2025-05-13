library(dplyr)
library(stringr)
library(ggplot2)

#################
#Data processing#
#################

#Initial importing and selecting rows
occur <- read.csv("C:/Users/colin/Downloads/National_USFS_Fire_Occurrence_Point_(Feature_Layer) (1).csv")
occurDF <- occur %>%
  select(UNIQFIREID, FIREYEAR, DISCOVERYDATETIME, FIREOUTDATETIME, SIZECLASS, TOTALACRES, STATCAUSE,
         LATDD83, LONGDD83)
occurDF <- na.omit(occurDF)


#Cleaning NA/null values
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

occurDF <- occurDF %>%
  mutate(across(where(is.character), ~na_if(.x, "null"))) %>%
  mutate(across(where(is.character), ~na_if(.x, "")))

occurDF <- occurDF %>%
  na.omit()

#Cleaning Fire Years
table(sort(occurDF$FIREYEAR))

occurDF$FIREYEAR <- as.numeric(occurDF$FIREYEAR)

validYears <- 1900:2023
invalid <- which(!(occurDF$FIREYEAR %in% validYears))
occurDF <- occurDF[-invalid, ]


#Checking the size class vs total acres.
set.seed(1000)
rows <- sample(nrow(occurDF), 5)
class <- occurDF$SIZECLASS[rows]
acres <- occurDF$TOTALACRES[rows]



#Checking Longitude and Latitude values
set.seed(100)
lon <- sample(occurDF$LONGDD83, 5, replace=FALSE)
lat <- sample(occurDF$LATDD83, 5, replace=FALSE)


#Cleaning StatCause
sort(unique(occurDF$STATCAUSE_CLEAN)) #42

occurDF <- occurDF %>% 
  mutate(
    STATCAUSE_CLEAN = str_to_lower(str_trim(STATCAUSE)),  # Normalize text
    STATCAUSE_CLEAN = case_when(
      str_detect(STATCAUSE_CLEAN, "lightning|1") ~ "Lightning",
      str_detect(STATCAUSE_CLEAN, "camp") ~ "Campfire",
      str_detect(STATCAUSE_CLEAN, "debris|burning|5") ~ "Debris Burning",
      str_detect(STATCAUSE_CLEAN, "equip|vehicle|machinery|power|utilities|trans") ~ "Equipment/Utility Use",
      str_detect(STATCAUSE_CLEAN, "arson|7") ~ "Arson",
      str_detect(STATCAUSE_CLEAN, "smok") ~ "Smoking",
      str_detect(STATCAUSE_CLEAN, "child") ~ "Children",
      str_detect(STATCAUSE_CLEAN, "firearm|weapon") ~ "Firearms/Weapons",
      str_detect(STATCAUSE_CLEAN, "misc|9") ~ "Miscellaneous",
      str_detect(STATCAUSE_CLEAN, "railroad") ~ "Railroad",
      str_detect(STATCAUSE_CLEAN, "natural") ~ "Natural",
      str_detect(STATCAUSE_CLEAN, "undetermined|undertermined|cause not|investigated|unknown|^$|0") ~ "Unknown",
      TRUE ~ "Other"
    )
  )

occurDF$STATCAUSE <- NULL
occurDF

#StatCause Barplot
stat_sum <- occurDF %>%
  group_by(STATCAUSE_CLEAN) %>%
  summarise(count=n()) %>%
  arrange(desc(count))

ggplot(data=stat_sum, aes(x=STATCAUSE_CLEAN, y=count)) +
  geom_bar(stat="identity") +
  xlab("Stat Cause") +
  ylab("Cause of Fire") +
  theme_minimal()



####################
#Exploring the data#
####################
test <- occur %>%
  group_by(FIREYEAR) %>%
  summarise(count=n())

ggplot(occur, x=FIREYEAR) +
  geom_bar()

sort(unique(occur$FIREYEAR))

