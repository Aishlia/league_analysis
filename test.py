import datetime
import time
import random

import requests
from bs4 import BeautifulSoup
import re
import html

url = 'https://na.op.gg/summoner/matches/ajax/averageAndList/startInfo=0&summonerId=47601640&type=soloranked'

data = requests.get(url).json()
soup = BeautifulSoup(data['html'], 'html.parser').decode('unicode_escape')
soup = BeautifulSoup(soup, 'html.parser')


mydivs = soup.findAll("div", {"class": "Team"})

win_loss = soup.findAll("div", {"class": "GameResult"})

teams = [a.get_text() for a in soup.find_all("div", {"class": "Team"})]
t1 = teams[0].split('\n')

for i in range(len(t1)):
    t1[i] = t1[i].strip()

t1 = list(filter(None, t1))

arr = []
for foo in range(0,len(t1), 3):
    new_entry = (t1[foo], t1[foo+2], 'https://na.op.gg/summoner/userName=' + t1[foo+2].replace(' ','+'))
    arr.append(new_entry)


print(arr)
