from riotwatcher import LolWatcher, ApiError
# golbal variables
api_key = 'RGAPI-8a76ca9c-5e29-42ac-9198-634d0af8843e'
watcher = LolWatcher(api_key)

match_detail = watcher.match.by_id('na1', 3880352071)
ctr = 1
for data in match_detail['participants']:
	print(data['stats']['win'])
	print(data['championId'])
	print(match_detail['participantIdentities'][ctr-1]['player']['summonerName'])
	ctr += 1

