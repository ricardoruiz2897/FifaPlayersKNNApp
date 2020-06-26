get.player.name <- function(key, ids, complete) {
  
  key <- dplyr::filter(key, id %in% ids) %>%
    dplyr::left_join(complete, by = "id")
  
}

library(tidyverse)

key <- read_csv("names_key.csv") %>%
  dplyr::select(-X1)

complete <- read_csv("processed_data.csv") %>%
  dplyr::select(-X1)

ids <- c(188545.0, 182521.0)

get.player.name(key, ids, complete) %>%
  View()
