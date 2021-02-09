import datetime
import time
import random

import requests
from bs4 import BeautifulSoup
import re
import html

url = 'https://na.op.gg/summoner/matches/ajax/averageAndList/startInfo=0&summonerId=47601640&type=soloranked'

# r = requests.get(url).text
# print(r)

# url = 'https://na.op.gg/summoner/userName=rito+torchic'

data = requests.get(url).json()
soup = BeautifulSoup(data['html'], 'html.parser').decode('unicode_escape')
soup = BeautifulSoup(soup, 'html.parser')


mydivs = soup.findAll("div", {"class": "Team"})

win_loss = soup.findAll("div", {"class": "GameResult"})

teams = [a.get_text() for a in soup.find_all("div", {"class": "Team"})]

print(teams)

for team in teams:
    players = team.split('\n')
    print(players)

new_arr = 

a = list(filter(None, a))

# a = teams[0].replace('\n','|')
# a = a.split('|')
# for player in a:
#     teams[0].replace('|','')
#
# a = list(filter(None, a))
#
# arr = []
#
# for foo in range(0,len(a), 3):
#     new_intry = (a[foo], a[foo+2], 'https://na.op.gg/summoner/userName=' + a[foo+2].replace(' ','+'))
#     arr.append(new_intry)
#
#
#
# print(arr)
