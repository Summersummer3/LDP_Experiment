processed_data_2.5 = read.csv("result_consistency_2.5.csv",header = TRUE)
result_p_2.5 <- mean_for_error(processed_data_2.5$error, experiment_data_2.5$max_error)
processed_data_2.0 = read.csv("result_consistency_2.0.csv",header = TRUE)
result_p_2.0 <- mean_for_error(processed_data_2.0$error, experiment_data_2.0$max_error)
processed_data_1.5 = read.csv("result_consistency_1.5.csv",header = TRUE)
result_p_1.5 <- mean_for_error(processed_data_1.5$error, experiment_data_1.5$max_error)
processed_data_1.0 = read.csv("result_consistency_1.csv",header = TRUE)
result_p_1.0 <- mean_for_error(processed_data_1.0$error, experiment_data_1.0$max_error)
processed_data_0.5 = read.csv("result_consistency_0.5.csv",header = TRUE)
result_p_0.5 <- mean_for_error(processed_data_0.5$error, experiment_data_0.5$max_error)

mean_p_error <- c(result_p_0.5[1], result_p_1.0[1], result_p_1.5[1], result_p_2.0[1], result_p_2.5[1])
mean_p_max_error <- c(result_p_0.5[2], result_p_1.0[2], result_p_1.5[2], result_p_2.0[2], result_p_2.5[2])

