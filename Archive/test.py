from parsing import two_matches

def test():
    target = 'Rito Torchic'
    matches = two_matches(target)
    print("First match's first team's players:")
    matches[0].print_team(0)
test()
