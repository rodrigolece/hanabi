
from game import Hanabi

nb_players = 4
hanabi = Hanabi(nb_players)
print(hanabi)

p = hanabi.current_player

print('\nhand of first player')
for c in p.hand:
    print(c.colour, c.number)

hanabi.discard_card(p,1)

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

hanabi.play_card(p,1)

print("\ncurrent red stack:")
for c in hanabi.table.red_stack:
    c.print_card()

hanabi.next_player()

hanabi.give_hint(hanabi.players[2], 0, "white")

print("\n player 2's hand info:")
print(hanabi.players[2].hand_info)
