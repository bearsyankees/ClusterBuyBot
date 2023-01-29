import re

s = "Tip('<img src=\\\\'https://www.profitspi.com/stock/stock-charts.ashx?chart=LOB&v=stock-chart&vs=637453390322078326\\\\' alt=\\\\'\\\\' width=\\\\'360px\\\\' height=\\\\'280px\\\\'>', DELAY, 1)"
print(s)
reg_exp = "https:\/\/www\.profitspi\.com\/stock\/stock-charts\.ashx\?chart=.{0,5}&v=stock-chart&vs=.{18}\\\\"

new_s = re.search(reg_exp,s)
print (new_s)

