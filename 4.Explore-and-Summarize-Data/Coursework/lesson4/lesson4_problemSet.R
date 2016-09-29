data("diamonds")

ggplot(aes(x, price), data = diamonds) +
  geom_point()

cor.test(diamonds$z, diamonds$price)

ggplot(aes(depth, price), data = diamonds) +
  geom_point(alpha = 1/100)

cor.test(diamonds$depth, diamonds$price)

ggplot(aes(carat, price), data = diamonds) +
  xlim(0, quantile(diamonds$carat, 0.99)) +
  ylim(0, quantile(diamonds$price, 0.99)) +
  geom_point()

diamonds$volume <- diamonds$x * diamonds$y * diamonds$z
ggplot(aes(volume, price), data = diamonds) +
  geom_point()

with(subset(diamonds, diamonds$volume > 0 & diamonds$volume <= 800), cor.test(volume, price))

ggplot(aes(volume, price), data = subset(diamonds, diamonds$volume > 0 & diamonds$volume <= 800)) +
  geom_point(alpha = 1/100) + geom_smooth()

clarity_groups <- group_by(diamonds, clarity)
diamondsByClarity <- summarise(clarity_groups,
                               mean_price = mean(price),
                               median_price = median(price),
                               min_price = min(price),
                               max_price = max(price),
                               n = n())
head(diamondsByClarity)
