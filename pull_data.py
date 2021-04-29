from pull_ranked_API import find_match
import time

def pull_data(summoner_name, cycle):
    # 100 Default per summoner
    defaul_per_summoner = 100
    random_summoner = find_match(summoner_name, defaul_per_summoner)
    print("---------- Random cummoner is " + random_summoner + ". ----------")
    ctr = 0
    print('Run %s complete' % ctr)

    for i in range(0, cycle - 1):
        random_summoner = find_match(random_summoner, defaul_per_summoner)
        print("---------- Random cummoner is " + random_summoner + ". ----------")
        print('Run %s complete' % ctr)
        ctr += 1
        time.sleep(3)


test_summoner = 'Rito Torchic'
pull_data(test_summoner, 2)
