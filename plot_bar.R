x_1 = rep(epsilon, each=2)
y_1 = rep(c("error", "processed_error"), time=5)
c_1 = as.vector(rbind(mean_error, mean_p_error))
df = data.frame(x=x_1, y=y_1, z=c_1)
p = ggplot(data = df, mapping = aes(x = x,y = z, fill = y)) + geom_bar(stat = 'identity', position = position_dodge(0.2), width = 0.15)
p + scale_x_continuous(breaks = seq(0, 3, 0.5)) + labs(title = "error comprison", x = "epsilon", y = "error") + theme(panel.grid =element_blank(),legend.title = element_blank())
