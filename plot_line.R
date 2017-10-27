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

var_error <- function(error, max_error){
  log_var_e <- log(var(error, na.rm = T), base = 10)
  log_var_me <- log(var(max_error, na.rm = T), base = 10)
  c(log_var_e, log_var_me)
}

var_0.5 <- var_error(experiment_data_0.5$error, experiment_data_0.5$max_error)
var_1.0 <- var_error(experiment_data_1.0$error, experiment_data_1.0$max_error)
var_1.5 <- var_error(experiment_data_1.5$error, experiment_data_1.5$max_error)
var_2.0 <- var_error(experiment_data_2.0$error, experiment_data_2.0$max_error)
var_2.5 <- var_error(experiment_data_2.5$error, experiment_data_2.5$max_error)

var_errors <- c(var_0.5[1], var_1.0[1], var_1.5[1], var_2.0[1], var_2.5[1])
var_max_errors <- c(var_0.5[2], var_1.0[2], var_1.5[2], var_2.0[2], var_2.5[2])

opar <- par(no.readonly = TRUE)
dev.off()
par(lwd=2, cex=0.6)
plot(x=epsilon,y=mean_error, type="b", pch=15, lty=1, lwd=2, col="red", xlab = "epsilon", ylab = "mean(error)", ylim = c(0, 0.1))
lines(x=epsilon, y=mean_max_error, type ="b", pch=10, lty=3, lwd=2, col="blue")

library(Hmisc)
minor.tick(nx=3, ny=3, tick.ratio = 0.5)

legend("topright", inset = .05, title = "", c("error", "max_error"), lty=c(1, 3), pch = c(15, 10), col = c("red", "blue"),bty = "n", cex = 1.3)

plot(x=epsilon,y=var_errors, type="b", pch=15, lty=1, lwd=2, col="red", xlab = "epsilon", ylab = "log(var(error))", ylim = c(-7, -3))
lines(x=epsilon, y=var_max_errors, type ="b", pch=10, lty=3, lwd=2, col="blue")

legend("topright", inset = .05, title = "", c("error", "max_error"), lty=c(1, 3), pch = c(15, 10), col = c("red", "blue"),bty = "n", cex = 1.3)

par(opar)


