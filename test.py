import datetime
import time
import random

import requests
from bs4 import BeautifulSoup
import re
import html

class Summoner:
    def __init__(self, summoner_name):
        self.name = summoner_name

        self.id = None
        self.url = None
        self.rank = None
        self.id_url_rank()

    def __str__(self):
        return (self.name, self.rank, self.id)

    def id_url_rank(self):
        url = 'https://na.op.gg/summoner/userName=' + self.name.replace(' ','+')
        data = requests.get(url).text
        soup = BeautifulSoup(data, 'html.parser')
        mydiv = soup.find("div", {"class": "MostChampionContent"})
        child_div = mydiv.find("div", {"class": "MostChampionContent"})
        summ_id = child_div['data-summoner-id']

        self.url = url
        self.id = summ_id

        rank = soup.find("div", {"class": "TierRank"}).string

        self.rank = rank


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
        match = []
        for t in range(2):  # Pull both teams for each math
            team_list = []
            team = teams[itr].split('\n')
            for i in range(len(team)):
                team[i] = team[i].strip()

            team = list(filter(None, team))  # Get rid of empty indexes

            for index in range(0,len(team), 3):
                champion = team[index]
                summoner_name = team[index+2]
                summoner = Summoner(summoner_name)

                new_entry = (champion, summoner)

                team_list.append(new_entry)
            match.append([team_list])
            itr += 1

        matches.append([match])

    return matches

def test():
    target = 'Rito Torchic'
    matches = two_matches(target)
    for i in matches:
        print("MATCH")
        for j in i:
            print("TEAM")
            print(j)

test()
