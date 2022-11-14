# A quick guide on how to open shape file in R

library(dplyr)
library(sf)

# setwd("RWorkshop-at-UF/Hurricane_Crop_Acreage/Code") # Change your path

# Original Shape data source: https://www2.census.gov/geo/tiger/GENZ2018/shp/
df = sf::st_read("../Data/cb_2018_us_county_500k.shp") # Change path if necessary
# Check the columns and their type
str(df)

# Note you are only interested in FL. 
# So, filter by state code. 
# Look up State code for FL... 
# https://www.census.gov/library/reference/code-lists/ansi.html#state
# https://www.census.gov/geographies/reference-files.html
# State code for FL: 12
df %>%
  dplyr::filter(STATEFP == "12") -> dff # dff as in Dataframe Florida

# You now have polygons for plotting counties in FL
plot(dff)

# Use the State and County code as a key fields to merge with other files