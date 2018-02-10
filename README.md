# 12306
Show or Buy 12306 tickets, by Python.
Python version 3.5.2

Dependency:
  docopt 0.6.2
  requests 2.9.1
  prettytable 
  warnings
  time
  
Recommend:
  Ubuntu
  virtualenv
  
Usage example:
	ticketshow.py 上海 北京 2018-02-14
	ticketshow.py -dg 青岛 上海 2018-02-14 --days=3
	ticketshow.py -dg 青岛 上海 2018-02-14 --trains=G222
	ticketshow.py -dg 青岛 上海 2018-02-14 --days=3 --trains=G222
