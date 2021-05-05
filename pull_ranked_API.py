from riotwatcher import LolWatcher, ApiError
import pandas as pd
import numpy as np
import time
import csv

# golbal variables
api_key = 'RGAPI-38db3aee-36e7-4add-bd2b-623d80923aef'
watcher = LolWatcher(api_key)

# Find player rank
def find_player_info(my_region, me):
	my_ranked_stats = None
	tier = '-'
	rank = '-'
	lp = '-'
	while(my_ranked_stats == None):
		try:
			my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
		except:
			print("Error occured @ stats.waiting")
			time.sleep(20)
	for row in my_ranked_stats:
		if row['queueType'] == 'RANKED_SOLO_5x5':
			tier = row['tier']
			rank = row['rank']
			lp = row['leaguePoints']
			break
		else:
			tier = '-'
			rank = '-'
			lp = '-'

	ret = {'tier': tier,
		 'rank': rank,
		 'lp': lp}
	return(ret)

# Find most recent match history
def find_match(summoner_name, itrs, my_region='na1'):
	num_games = 0
	me = None
	while(me == None):
		try:
			me = watcher.summoner.by_name(my_region, summoner_name)
		except:
			print("Error occured @ match.waiting")
			time.sleep(20)

	my_matches = None
	while(my_matches == None):
		try:
			my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])
		except:
			print("Error occured @ match2.waiting")
			time.sleep(20)

	ranked_games = []

	random_summoner = ''
	found = False

  # fetch last match detail
	ctr = 0
	for match in my_matches['matches']:
		# Find indices for ranked matches
		if match['queue'] == 420:  # 420 is id for ranked 5x5 matches
			ranked_games.append(ctr)
		if len(ranked_games) == itrs:
			break
		ctr += 1

	ranked_games[:itrs]
	#participants = []
	games = []
	count = 0
	for i, match in enumerate(my_matches['matches']):
		with open('jdata2.csv', 'a', newline='') as csvfile:
			fieldnames = ['tier', 'rank', 'win', 'champion1', 'champion2', 'champion3', 'champion4', 'champion5', 'champion6' ,'champion7' ,'champion8' ,'champion9' ,'champion10', 'matchID']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			if i in ranked_games:
				time.sleep(1.5)
				match_detail = None
				errcount = 0
				while(match_detail == None):
					try:
						match_detail = watcher.match.by_id(my_region, match['gameId'])
					except:
						print("Error occured @ game.waiting")
						time.sleep(20)
						errcount += 1
						if errcount == 2:
							continue
				game_rank = find_player_info(my_region, me)
				matchID = match_detail['gameId']
				game_data={}
				game_data['rank'] = game_rank['rank']
				game_data['tier'] = game_rank['tier']
				game_data['matchID'] = matchID
				usernames=[]
				ctr = 1
				for data in match_detail['participants']:
					if ctr == 1:
						game_data['win'] = data['stats']['win']
					game_data['champion' + str(ctr)] = data['championId']
					usernames.append(match_detail['participantIdentities'][ctr-1]['player']['summonerName'])
					ctr = ctr + 1
				if(found == False):
					num = np.random.randint(9)#scuffed
					if(usernames[num] == summoner_name):
						num += 1
					random_summoner = usernames[num]
					try:
						watcher.summoner.by_name('na1', random_summoner)
						if(count!=0):
							found = True
					except:
						print('Invalid summoner found. looking for other summoner')
				writer.writerow(game_data)
				num_games += 1
				games.append(game_data)
				count += 1
	return random_summoner, num_games
