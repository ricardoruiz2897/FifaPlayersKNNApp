#Load libraries
library(tidyverse)
library(wangr)

full_dataset <- readr::read_csv("complete_dataset.csv") %>%
  select(-c(X1,`Club Logo`, Flag, Photo))

library(snakecase)
#change to a usefull naming convection convention.
names(full_dataset) <- snakecase::to_lower_camel_case(names(full_dataset))
write_csv(full_dataset, "Data/full_dataset.csv")

#variables that we are going to pass to the front-end app
front_end_data_set <- full_dataset %>%
  select(id, name, name, age, nationality, overall, club)

write_csv(front_end_data_set, "Data/front_end_data_set.csv")
