#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Author: Albert Hoo
Date: 2018-02-10
Version: v1.0
Show 12306 tickets.

Usage:
	ticketshow [-gdtkz] <from> <to> <date> [--nextdays=<nextdays>] [--trains=<trains>]

Options:
	-h,--help	显示帮助菜单
	--nextdays=<nd>	Search for how many days after the designed date [default: 0].
	--trains=<trains>	Which train needs to be attentioned!

Example:
	ticketshow 上海 北京 2018-02-14
	ticketshow -dg 青岛 上海 2018-02-14 --days=3
	ticketshow -dg 青岛 上海 2018-02-14 --trains=G222
	ticketshow -dg 青岛 上海 2018-02-14 --days=3 --trains=G222
"""

from docopt import docopt
from stationlist import stationlist
import requests
from prettytable import PrettyTable
import warnings
import time
import datetime
import random

class Ticketshow():
	def findTicket(self):
		arguments = docopt(__doc__)
		from_station = stationlist.get(arguments['<from>'])
		to_station = stationlist.get(arguments['<to>'])
		date = arguments['<date>']
		nextdays = arguments['--nextdays']
		trains = arguments['--trains']
		#预处理参数
		if type(nextdays) is type('a'):
			days = int(nextdays)
		else:
			days = 0
		if type(trains) is type('a'):
			attention = True
		else:
			attention = False
		newdate = datetime.datetime.strptime(date,'%Y-%m-%d')
		#开始查找余票
		i = 0
		print( time.ctime() )
		while i <= days:
			i = i + 1
			url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT'.format(newdate.strftime('%Y-%m-%d'),from_station, to_station)
			req = requests.get(url, verify=True)
			#If access failed, retrying endless until success.
			while req.url=='http://www.12306.cn/mormhweb/logFiles/error.html':
				print("waiting for a moment...   ",end=''), print( time.ctime() )
				time.sleep(10*random.random())
				req = requests.get(url, verify=True)
			rows = req.json()['data']['result']
			headers = '日期 车次 出发站 到达站 出发时间 到达时间 历时 商务 一等 二等 高软 软卧 硬卧 软座 硬座 无座 其他'.split()
			pt = PrettyTable()
			pt._set_field_names(headers)
			#对返回的json数据中每一条记录做格式化解析和输出
			for row in rows:
				list = row.split('|')
				items = []
				for item in (newdate.strftime('%Y-%m-%d'),list[3],arguments['<from>'],arguments['<to>'],list[8],list[9],list[10],list[32],list[31],list[30],list[29],list[28],list[27],list[26],list[25],list[24],list[23]):
					items.append(item)
				pt.add_row(items)
				if attention and (list[3]==trains) and ( list[32]!='无' or list[31]!='无' or list[30]!='无' ):
					print("#######################################注意 {} 有票############################################################".format(trains))
					time.sleep(1)
			print(pt)
			newdate = newdate + datetime.timedelta(days=1)

if __name__ == '__main__':
	warnings.filterwarnings("ignore")
	ticket = Ticketshow()
	# 持续的监视余票情况,免去手工操作时不停点击页面的烦恼
	while True:
		ticket.findTicket()
		print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
		print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
		time.sleep(6)
