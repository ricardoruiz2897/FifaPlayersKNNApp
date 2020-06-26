#Load libraries
library(tidyverse)
library(wangr)
library(psych)

normalize.vector <- function(nums) {
  
  #Get mean.
  average <- mean(nums)
  
  #Get std.
  std <- sd(nums)
  
  normalize.number <- function(num, avg, std) {
    return( (num-avg) / std )
  } 
  
  #Get variance.
  unlist(purrr::map(nums, normalize.number, avg = average, std = std))
  
}

#Load data
original.data <- read_csv("fifa-18-demo-player-dataset/CompleteDataset.csv") %>%
  dplyr::mutate(id = as.numeric(ID)) %>%
  dplyr::select(-X1, -ID) 

write.csv(original.data, file = "complete_dataset.csv")

data <- original.data %>%
  wangr::wang.naming()

#Create key...
name.key <- data %>%
  dplyr::select(name, id)

write.csv(name.key, file = "names_key.csv")

#Helpers...
handle.currencies <- Vectorize(function(currency){
  
  currency <- stringr::str_remove_all(currency, "\\.")
  currency <- stringr::str_remove_all(currency, "€")
  currency <- stringr::str_replace_all(currency, pattern = "M", replacement = "000000")
  currency <- stringr::str_replace_all(currency, pattern = "K", replacement = "000")
  as.numeric(currency)
  
}) 

handle.sign <- function(attribute){
  
  #Summation of splitted with "+"
  splits.operation <- function(att, operand, type = "sum") {
    
    splits <- as.numeric(unlist(stringr::str_split(att, pattern = operand)))
    
    if(type == "sum") {
      
      att = splits[1] + splits[2]
      
    } else if (type == "substraction") {
      
      att = abs(splits[2] - splits[1])
      
    }
    
    att
    
  }
  
  atts <- c()
  for(i in 1:length(attribute)) {
    
    current <- attribute[i]
    
    if(grepl(pattern = "\\+", current)) {
      
      atts <- append(atts, splits.operation(current, operand = "\\+", type = "sum"))
    
    } else if (grepl(pattern = "-", current)) {
    
      atts <- append(atts, splits.operation(current, operand = "-", type = "substraction"))
        
    } else {
      
      atts <- append(atts, as.numeric(current))
      
    }
    
  }
  
  atts
  
}

get.first.position <- Vectorize(function(positions) {
  
  positions <- unlist(stringr::str_split(positions, " "))
  positions[1]
    
})

#Naming convetion, select columns needed...
data <- data %>%
  dplyr::select(-c(photo, flag, club.logo, name, club)) %>% #We dont care or need this vars..
  dplyr::mutate(wage = handle.currencies(wage), 
                value = handle.currencies(value))

#Select the ones to tranform...
attributes <- data %>%
  dplyr::select(acceleration:st, -preferred.positions) %>%
  colnames()

#Transform for + and minus....
data[attributes] <- purrr::map(data[attributes], handle.sign)

#Get only first preffered position.
data$preferred.positions <- get.first.position(data$preferred.positions)

#Dummy codess...
dummy.code.vars <- data %>%
  dplyr::select(nationality) %>%
  colnames()

for(dummy in dummy.code.vars) {
  
  temp <- psych::dummy.code(data[[dummy]])
  temp <- as.data.frame(temp)
  data <- cbind(data, temp)
  
}

rm(temp)

#separate goalkeepers and players. Then drop nationality and preffered positions.
gk.data <- data %>%
  dplyr::filter(preferred.positions == "GK") %>%
  dplyr::select_if((~sum(!is.na(.)) > 0)) %>%
  dplyr::select(-c(preferred.positions, nationality)) %>%
  wangr::wang.naming() 

players.data <- data %>%
  dplyr::filter(preferred.positions != "GK") %>%
  select_if(~sum(!is.na(.)) > 0) %>%
  dplyr::select(-c(preferred.positions, nationality)) %>%
  wangr::wang.naming()

data <- data %>%
  dplyr::select(-c(preferred.positions, nationality)) %>%
  wangr::wang.naming()

#Make sure all are numeric...
data <- as.data.frame(sapply(data, as.numeric))
gk.data <- as.data.frame(sapply(gk.data, as.numeric))
players.data <- as.data.frame(sapply(players.data, as.numeric))

#Goal keeper positioning has NAs so make it zero...
gk.data[is.na(gk.data)] <- 0

#Both should have zero NAs..
sum(sapply(gk.data, function(x) sum(is.na(x))))
sum(sapply(players.data, function(x) sum(is.na(x))))

players.data <- normalize.data.set(players.data, "id")
gk.data <- normalize.data.set(gk.data, "id")

#Nas to 0...
players.data[is.na(players.data)] <- 0
gk.data[is.na(gk.data)] <- 0

#Save csv...
write.csv(gk.data, file = "gk_data.csv")
write.csv(players.data, file = "players_data.csv")
write.csv(data, file = "processed_data.csv")

players.data <- left_join(players.data, name.key, by = "id")


#To get all countries as a string
countries <- levels(as.factor(data$nationality))

countries.string <- ""

for(c in countries){
  c <- paste("'", c, sep = "")
  c <- paste(c, "'", sep = "")
  
  countries.string <- paste(countries.string, c, sep = ", ")
}



