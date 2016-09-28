library(ggplot2)
data("diamonds")

qplot(x = price, data = diamonds, binwidth = 10, color = 'orange')

ggplot(aes(table, price), data = diamonds) + geom_point(aes(color = cut)) +
  scale_color_brewer(type = 'qual')

ggplot(aes(cut, table), data = diamonds) + geom_boxplot()

summary(subset(diamonds, diamonds$cut == 'Ideal')$table)
summary(subset(diamonds, diamonds$cut == 'Premium')$table)

diamonds$volume <- diamonds$x * diamonds$y * diamonds$z

ggplot(aes(volume, price), data = diamonds) + 
  geom_point(aes(color = clarity)) +
  ylim(0, quantile(diamonds$volume, 0.99)) +
  scale_y_log10() +
  xlim(c(0,1000))

pf = read.csv('pseudo_facebook.tsv', sep = '\t')

pf$prop_initiated <- with(pf, 
                          ifelse(friend_count == 0, 0, friendships_initiated/friend_count))

ggplot(aes(tenure, prop_initiated), data = pf) + 
  geom_line(aes(color = year_joined.bucket), stat = 'summary', fun.y = median) +
  geom_smooth()

summary(subset(pf, pf$year_joined.bucket == "(2012,2014]")$prop_initiated)

ggplot(aes(cut, price/carat), data = diamonds) + 
  geom_jitter(aes(color = color), alpha = 0.25) + 
  facet_wrap( ~ clarity) +
  scale_color_brewer(type = 'div')
