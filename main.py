
from game import Hanabi

nb_players = 4
hanabi = Hanabi(nb_players)
print(hanabi)

p = hanabi.current_player

print('\nhand of first player')
for c in p.hand:
    print(c.colour, c.number)

for i in range(3):
    print('\npassing hand')
    hanabi.next_player()
    p = hanabi.current_player

    print(f'\nhand of player {p.index}')
    for c in p.hand:
        print(c.colour, c.number)
