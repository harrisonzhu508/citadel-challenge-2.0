W <- runif(1000, -1, 1)
y <- 3 + 2 * W + 10 * (W>=0.5) + rnorm(1000)

# load the package 'rddtools'
library(rddtools)

# construct rdd_data 
data <- rdd_data(y, W, cutpoint = 0.5)

# plot the sample data
plot(data,
     col = "steelblue",
     cex = 0.35, 
     xlab = "W", 
     ylab = "Y")
# estimate the sharp RDD model
rdd_mod <- rdd_reg_lm(rdd_object = data, 
                      slope = "same")
summary(rdd_mod)

# plot the RDD model along with binned observations
plot(rdd_mod,
     cex = 0.35, 
     col = "steelblue", 
     xlab = "W", 
     ylab = "Y")

