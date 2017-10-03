processed_ez <- function(x){
  error <- c()
  for (i in seq(1, length(x[,1]) - 1, by = 2)){
    a <- as.vector(unlist(x[i,]))
    b <- as.vector(unlist(x[i+1,]))
    tmp <- 0
    for (j in 1: (length(x)-2)){
      if (b[j] < 0){
        b[j] <- 0
      }
      tmp = tmp + (a[j] - b[j]) ** 2
    }
    error[length(error) + 1] <- tmp
  }
  return(error)
}

experiment_data_0.8 = read.csv("result_0.8.csv",header = TRUE)
result_0.8 <- mean_for_error(experiment_data_0.8$error, experiment_data_0.8$max_error)
experiment_data_0.6 = read.csv("result_0.6.csv",header = TRUE)
result_0.6 <- mean_for_error(experiment_data_0.6$error, experiment_data_0.6$max_error)
experiment_data_0.5 = read.csv("result_0.5.csv",header = TRUE)
result_0.5 <- mean_for_error(experiment_data_0.5$error, experiment_data_0.5$max_error)
experiment_data_0.4 = read.csv("result_0.4.csv",header = TRUE)
result_0.4 <- mean_for_error(experiment_data_0.4$error, experiment_data_0.4$max_error)
experiment_data_0.3 = read.csv("result_0.3.csv",header = TRUE)
result_0.3 <- mean_for_error(experiment_data_0.3$error, experiment_data_0.3$max_error)
experiment_data_0.2 = read.csv("result_0.2.csv",header = TRUE)
result_0.2 <- mean_for_error(experiment_data_0.2$error, experiment_data_0.2$max_error)
experiment_data_0.1 = read.csv("result_0.1.csv",header = TRUE)
result_0.1 <- mean_for_error(experiment_data_0.1$error, experiment_data_0.1$max_error)

mean_ez_processed_0.1 <- mean(processed_ez(experiment_data_0.1))
mean_ez_processed_0.2 <- mean(processed_ez(experiment_data_0.2))
mean_ez_processed_0.3 <- mean(processed_ez(experiment_data_0.3))
mean_ez_processed_0.4 <- mean(processed_ez(experiment_data_0.4))
mean_ez_processed_0.5 <- mean(processed_ez(experiment_data_0.5))
mean_ez_processed_0.6 <- mean(processed_ez(experiment_data_0.6))
mean_ez_processed_0.8 <- mean(processed_ez(experiment_data_0.8))

 
mean_ez_error <- c(mean_ez_processed_0.2, mean_ez_processed_0.3 ,mean_ez_processed_0.4, mean_ez_processed_0.5, mean_ez_processed_0.6, mean_ez_processed_0.8)

processed_data_0.8 = read.csv("result_consistency_0.8.csv",header = TRUE)
result_p_0.8 <- mean_for_error(processed_data_0.8$error, experiment_data_0.8$max_error)
processed_data_0.6 = read.csv("result_consistency_0.6.csv",header = TRUE)
result_p_0.6 <- mean_for_error(processed_data_0.6$error, experiment_data_0.6$max_error)
processed_data_0.5 = read.csv("result_consistency_0.5.csv",header = TRUE)
result_p_0.5 <- mean_for_error(processed_data_0.5$error, experiment_data_0.5$max_error)
processed_data_0.4 = read.csv("result_consistency_0.4.csv",header = TRUE)
result_p_0.4 <- mean_for_error(processed_data_0.4$error, experiment_data_0.4$max_error)
processed_data_0.3 = read.csv("result_consistency_0.3.csv",header = TRUE)
result_p_0.3 <- mean_for_error(processed_data_0.3$error, experiment_data_0.3$max_error)
processed_data_0.2 = read.csv("result_consistency_0.2.csv",header = TRUE)
result_p_0.2 <- mean_for_error(processed_data_0.2$error, experiment_data_0.2$max_error)
processed_data_0.1 = read.csv("result_consistency_0.1.csv",header = TRUE)
result_p_0.1 <- mean_for_error(processed_data_0.1$error, experiment_data_0.1$max_error)

mean_p_error <- c(result_p_0.2[1], result_p_0.3[1], result_p_0.4[1], result_p_0.5[1], result_p_0.6[1], result_p_0.8[1])
mean_error_small <- c(result_0.2[1], result_0.3[1], result_0.4[1], result_0.5[1], result_0.6[1], result_0.8[1])

eps2 <- c("0.2", "0.3", "0.4", "0.5", "0.6", "0.8")
x_3 = rep(eps2, each=3)
y_3 = rep(c("error", "sp_error", "p_error"), time=6)
c_3 = as.vector(rbind(mean_error_small, mean_ez_error, mean_p_error))
df_3 = data.frame(x=x_3, y=y_3, z=c_3)
df_3$order <- factor(df_3$x, rep(eps2, each=3))
df_3$order2 <- factor(df_3$y, rep(c("error", "sp_error", "p_error"), time=7))
p3 = ggplot(data = df_3, mapping = aes(x = x, y = z, fill = y)) + geom_bar(stat = 'identity', aes(x = order, fill = order2), data = df_3, position = position_dodge(0.2), width = 0.15)
p3 + labs(title = "error comprison", x = "epsilon", y = "error") + theme(panel.grid =element_blank(), legend.title=element_blank())
