import datetime
import time
import random

import requests
from bs4 import BeautifulSoup
import re
import html

class Summoner:
    def summoner_id(self):
        url = 'https://na.op.gg/summoner/userName=' + self.name.replace(' ','+')
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'html.parser')
        mydivs = soup.find("div", {"class": "MostChampionContent"})
        mydivs = mydivs.find("div", {"class": "MostChampionContent"})
        summ_id = mydivs['data-summoner-id']
        return summ_id

    def __init__(self, summoner_name):
        self.name = summoner_name
        self.id = summoner_id(summoner_name)
        self.url = 'https://na.op.gg/summoner/userName=' + summoner_name.replace(' ','+')

mbo = Summoner("Rito Torchic")
print(mbo)


def summ_id(summ_name):
    url = 'https://na.op.gg/summoner/userName=' + summ_name.replace(' ','+')
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    mydivs = soup.find("div", {"class": "MostChampionContent"})
    mydivs = mydivs.find("div", {"class": "MostChampionContent"})
    summ_id = mydivs['data-summoner-id']
    return summ_id

def two_matches(summ_name):
    """
    Pulls game info for a player's most recent two ranked matches.

    Return: List of most recent 2 matches
    """
    summoner_id = summ_id(summ_name)
    url = 'https://na.op.gg/summoner/matches/ajax/averageAndList/startInfo=0&summonerId=' + str(summoner_id) + '&type=soloranked'

    data = requests.get(url).json()
    soup = BeautifulSoup(data['html'], 'html.parser').decode('unicode_escape')
    soup = BeautifulSoup(soup, 'html.parser')
    win_loss = soup.findAll("div", {"class": "GameResult"})
    teams = [a.get_text() for a in soup.find_all("div", {"class": "Team"})]

    matches = []

    itr = 0
    for m in range(2):  # Pull 2 matches
        team_list = []
        for t in range(2):  # Pull both teams for each math
            team = teams[itr].split('\n')
            for i in range(len(team)):
                team[i] = team[i].strip()

            team = list(filter(None, team))  # Get rid of empty indexes

            for index in range(0,len(team), 3):
                champion = team[index]
                summoner_name = team[index+2]
                opgg_url = 'https://na.op.gg/summoner/userName=' + team[index+2].replace(' ','+')
                summoner_id = summ_id(team[index+2])

                new_entry = (champion, summoner_name, summoner_id, opgg_url)

                team_list.append(new_entry)
            itr += 1

        matches.append([team_list])

    return matches

# def test():
#     target = 'Rito Torchic'
#     print(two_matches(target))
#
# test()
