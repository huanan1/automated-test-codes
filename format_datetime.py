# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 14:10:19 2018

@author: Tea
"""
import datetime

now = datetime.datetime.now()
s = now.strftime("%d %B %Y, %H:%M:%S")
# customised based on documentation
# https://docs.python.org/3/library/datetime.html#datetime.datetime

print(s)  # 12 July 2018, 17:25:50
