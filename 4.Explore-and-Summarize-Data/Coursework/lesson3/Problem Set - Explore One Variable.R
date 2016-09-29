library(ggplot2)
data(diamonds)
summary(diamonds)
length(diamonds)
?diamonds

qplot(x=price, data=diamonds)
summary(diamonds$price)

summary(diamonds$price >= 15000)

qplot(x=log10(price), data=diamonds, binwidth = .1)

qplot(x = price, data = diamonds) + facet_wrap(~cut, scales = 'free_y')

by(diamonds$price, diamonds$cut, summary, digits = max(getOption('digits')))

?facet_wrap

diamonds$price_per_carat <- diamonds$price / diamonds$carat
qplot(x = log10(price/carat), data = diamonds, binwidth = 0.1) + facet_wrap(~cut)

by(diamonds$price, diamonds$color, summary)

qplot(x = carat,
      data = diamonds,
      geom = 'freqpoly',
      binwidth = 0.01) + coord_cartesian(ylim = c(2000,10000))
table(diamonds$carat)
