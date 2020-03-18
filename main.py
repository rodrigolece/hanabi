
from game import Hanabi

nb_players = 4
hanabi = Hanabi(nb_players)
print(hanabi)

p = hanabi.current_player

print('\nhand of first player')
for c in p.hand:
    print(c.colour, c.number)

hanabi.discard_card(p, 1)  # card_num

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

hanabi.play_card(p, 1)  # card_num

print("\ncurrent red stack:")
for c in hanabi.table.red_stack:
    print(c)

hanabi.next_player()

p = hanabi.players[2]
hanabi.give_hint(p, p.hand[0], "white")  # card instead of card_num
hanabi.give_hint(p, p.hand[1], 2)

print("\n player 2's hand info:")
for i, (card, colour) in enumerate(p.hand_colour_info.items()):
    print(i, colour, p.hand_number_info[card])
