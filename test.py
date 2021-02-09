import datetime
import time
import random

import requests
from bs4 import BeautifulSoup
import re

url = 'https://na.op.gg/summoner/userName=rito+torchic'

r = requests.get(url).text
soup = BeautifulSoup(r, 'html.parser')
# mydivs = soup.findAll("div", {"class": "Team"})
#
win_loss = soup.findAll("div", {"class": "GameResult"})

teams = [a.get_text() for a in soup.find_all("div", {"class": "Team"})]

a = teams[0].replace('\n','|')
a = a.split('|')
for player in a:
    teams[0].replace('|','')

a = list(filter(None, a))

arr = []

for foo in range(0,len(a), 3):
    new_intry = (a[foo], a[foo+2], 'https://na.op.gg/summoner/userName=' + a[foo+2].replace(' ','+'))
    arr.append(new_intry)



print(arr)
