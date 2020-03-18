
from game import Hanabi

nb_players = 4
hanabi = Hanabi(nb_players)
print(hanabi)


# Here we test discard
p = hanabi.current_player
print(p)

_ = hanabi.player_played(p, 'discard', card=p.hand[1])
print(p)

# Here we test passing hands
for i in range(3):
    print('\nPassing hand')
    hanabi.next_player()

    p = hanabi.current_player
    print(p)


# We test playing a card
pass_hand = hanabi.player_played(p, 'play', card=p.hand[1])

print("\nCurrent red stack:")
for c in hanabi.table.red_stack:
    print('', c)

if pass_hand:
    hanabi.next_player()
    p = hanabi.current_player

# We test giving both types of hints
to_player = hanabi.players[2]
_ = hanabi.player_played(p, 'hint', to_player=to_player, info='white')
_ = hanabi.player_played(p, 'hint', to_player=to_player, info=2)

print(f"\nPlayer {to_player.index}'s hand info:")
for i, (card, colour) in enumerate(to_player.hand_colour_info.items()):
    print(i, colour, to_player.hand_number_info[card])

print(hanabi)
