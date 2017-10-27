basic_rappor_ln9 <- read.csv("result_basic_rappor_2.19722457734.csv")
basic_rappor_ln49 <- read.csv("result_basic_rappor_3.89182029811.csv")
experiment_data_ln9 <- read.csv("result_2.19722457734.csv")
experiment_data_ln49 <- read.csv("result_3.89182029811.csv")
sampling_rappor_ln9 <- read.csv("result_sampling_rappor_2.19722457734.csv")
sampling_rappor_ln49 <- read.csv("result_sampling_rappor_3.89182029811.csv")

error_mean_ln9 <- mean_for_error(experiment_data_ln9$error, experiment_data_ln9$max_error) 
error_mean_ln49 <- mean_for_error(experiment_data_ln49$error, experiment_data_ln49$max_error) 
error_mean_br_ln9 <- mean_for_error(basic_rappor_ln9$error, basic_rappor_ln9$max_error)
error_mean_br_ln49 <- mean_for_error(basic_rappor_ln49$error, basic_rappor_ln49$max_error)
error_mean_sr_ln9 <- mean_for_error(sampling_rappor_ln9$error, sampling_rappor_ln9$max_error)
error_mean_sr_ln49 <- mean_for_error(sampling_rappor_ln49$error, sampling_rappor_ln49$max_error)

eps <- c("log(9)", "log(49)")
x = factor(rep(eps, each = 3), eps)
y = factor(rep(c("sr", "br", "ours"), time=2), c("sr", "br", "ours"))

error_mean_cmp <- c(error_mean_ln9[1], error_mean_ln49[1])
error_mean_br_cmp <- c(error_mean_br_ln9[1], error_mean_br_ln49[1])
error_mean_sr_cmp <- c(error_mean_sr_ln9[1], error_mean_sr_ln49[1])

error_max_mean_cmp <- c(error_mean_ln9[2], error_mean_ln49[2])
error_max_mean_br_cmp <- c(error_mean_br_ln9[2], error_mean_br_ln49[2])
error_max_mean_sr_cmp <- c(error_mean_sr_ln9[2], error_mean_sr_ln49[2])

c.cmp1 = as.vector(rbind(error_mean_sr_cmp, error_mean_br_cmp, error_mean_cmp))
c.cmp2 = as.vector(rbind(error_max_mean_sr_cmp, error_max_mean_br_cmp, error_max_mean_cmp))

df_1 = data.frame(x=x, y=y, z=c.cmp1)
p1 = ggplot(data = df_1, mapping = aes(x = x, y = z, fill = y)) + geom_bar(stat = 'identity', aes(x = x, fill = y), data = df_1, position = position_dodge(0.2), width = 0.15)
p1 + labs(x = "epsilon", y = "error") + theme(panel.grid =element_blank(), legend.title=element_blank(), legend.text = element_text(size = 6), axis.text.x = element_text(size = 6), 
                                              axis.title.x = element_text(size = 6), axis.text.y = element_text(size = 6), axis.title.y = element_text(size = 6))

df_2 = data.frame(x=x, y=y, z=c.cmp2)
p2 = ggplot(data = df_2, mapping = aes(x = x,y = z, fill = y)) + geom_bar(stat = 'identity', aes(x = x, fill = y), data = df_2, position = position_dodge(0.2), width = 0.15)
p2 + labs(x = "epsilon", y = "max error") +  theme(panel.grid =element_blank(), legend.title=element_blank(), legend.text = element_text(size = 6), axis.text.x = element_text(size = 6), 
                                                        axis.title.x = element_text(size = 6), axis.text.y = element_text(size = 6), axis.title.y = element_text(size = 6))

