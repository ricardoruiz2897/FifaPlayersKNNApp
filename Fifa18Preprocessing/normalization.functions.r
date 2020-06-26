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

normalize.data.set <- function(data, id){
  
  cols <- names(players.data)[-which(names(players.data) == id)]
  
  for(col in cols) {
    data[[col]] <- normalize.vector(data[[col]]) 
  }
  
  data
  
}



normalize.vector(c(0,1,1,0,0,1))
