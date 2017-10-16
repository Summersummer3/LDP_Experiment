experiment_data_2.5 = read.csv("result_2.5.csv",header = TRUE)
result_2.5 <- mean_for_error(experiment_data_2.5$error, experiment_data_2.5$max_error)
experiment_data_2.0 = read.csv("result_2.0.csv",header = TRUE)
result_2.0 <- mean_for_error(experiment_data_2.0$error, experiment_data_2.0$max_error)
experiment_data_1.5 = read.csv("result_1.5.csv",header = TRUE)
result_1.5 <- mean_for_error(experiment_data_1.5$error, experiment_data_1.5$max_error)
experiment_data_1.0 = read.csv("result_1.csv",header = TRUE)
result_1.0 <- mean_for_error(experiment_data_1.0$error, experiment_data_1.0$max_error)
experiment_data_0.5 = read.csv("result_0.5.csv",header = TRUE)
result_0.5 <- mean_for_error(experiment_data_0.5$error, experiment_data_0.5$max_error)

mean_error <- c(result_0.5[1], result_1.0[1], result_1.5[1], result_2.0[1], result_2.5[1])
mean_max_error <- c(result_0.5[2], result_1.0[2], result_1.5[2], result_2.0[2], result_2.5[2])
epsilon <- c(0.5, 1.0, 1.5, 2.0, 2.5)

opar <- par(no.readonly = TRUE)
par(lwd=3, cex=1.2)
plot(y.1, type="b", pch=15, lty=1, lwd=3, col="red", main = "Error and Max Error", xlab = "Epsilon", ylab = "Error")
lines(y.2, type ="b", pch=16, lty=2, lwd=3, col="blue")

library(Hmisc)
minor.tick(nx=3, ny=3, tick.ratio = 0.5)

legend("topright", inset = .05, title = "Error Type", c("Error", "Max error"), lty=c(1, 2), pch = c(15, 16), col = c("red", "blue"))

par(opar)


