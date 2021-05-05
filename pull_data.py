from pull_ranked_API import find_match
import time

def pull_data(summoner_name, cycle):
    # 100 Default per summoner
    total_games_pulled = 0
    defaul_per_summoner = 100
    random_summoner, num_games = find_match(summoner_name, defaul_per_summoner)
    total_games_pulled += num_games
    print("---------- Random cummoner is " + random_summoner + ". ----------")
    ctr = 0
    print('Run %s complete. %s total games pulled.' % (ctr, total_games_pulled))

    for i in range(0, cycle - 1):
        ctr += 1
        random_summoner, num_games = find_match(random_summoner, defaul_per_summoner)
        total_games_pulled += num_games
        print("---------- Random cummoner is " + random_summoner + ". ----------")
        print('Run %s complete. %s total games pulled.' % (ctr, total_games_pulled))
        time.sleep(3)


test_summoner = 'Dark King Shea'
pull_data(test_summoner, 10000)
