from riotwatcher import LolWatcher, ApiError
import pandas as pd
import numpy as np
import csv

# golbal variables
api_key = 'RGAPI-8a76ca9c-5e29-42ac-9198-634d0af8843e'
watcher = LolWatcher(api_key)

# Find player rank
def find_player_info(my_region, me):
	my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])
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
	me = watcher.summoner.by_name(my_region, summoner_name)

	my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])

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
  
	for i, match in enumerate(my_matches['matches']):
		with open('data.csv', 'a', newline='') as csvfile:
			#fieldnames = ['champion', 'win', 'playerID', 'summonerName', 'tier', 'rank', 'matchID']
			fieldnames = ['tier', 'rank', 'win', 'champion1', 'champion2', 'champion3', 'champion4', 'champion5', 'champion6' ,'champion7' ,'champion8' ,'champion9' ,'champion10', 'matchID']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			#writer.writeheader()
			if i in ranked_games:
				match_detail = watcher.match.by_id(my_region, match['gameId'])
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
					found = True
				writer.writerow(game_data)
				games.append(game_data)
				'''ctr = 0

				for data in match_detail['participants']:
					participants_row = {}
					participants_row['champion'] = data['championId']
					participants_row['win'] = data['stats']['win']
					participants_row['playerID'] = match_detail['participantIdentities'][ctr]['player']['accountId']
					participants_row['summonerName'] = match_detail['participantIdentities'][ctr]['player']['summonerName']
					participants_row['tier'] = game_rank['tier']
					participants_row['rank'] = game_rank['rank']
					# player = watcher.summoner.by_name(my_region, participants_row['summonerName'])
					# player_rank = find_player_info('na1', player)
					# participants_row['tier'] = player_rank['tier']
					# participants_row['rank'] = player_rank['rank']
					# participants_row['lp'] = player_rank['lp']
					participants_row['matchID'] = matchID
					#participants.append(participants_row)
					writer.writerow(participants_row)
					if ctr == 0 and participants_row['summonerName'] != summoner_name and found == False:
						random_summoner += participants_row['summonerName']
						found = True

					ctr += 1'''
	return random_summoner

  #df = pd.DataFrame(participants)
  #pd.set_option("display.max_rows", None, "display.max_columns", None)
  #print(df)

my_region = 'na1'  # Always na1 for north america 1 servers
test_summoner = 'rito torchic'
a = find_match(test_summoner, 3)
