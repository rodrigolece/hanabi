
from game import Hanabi


def simulated_game(nb_players=2):
    hanabi = Hanabi(nb_players)
    p = hanabi.current_player

    # We test giving both types of hints
    to_player = hanabi.players[1]
    pass_hand = hanabi.player_played('hint', to_player=to_player, info='white')

    if pass_hand:
        hanabi.next_player()
        p = hanabi.current_player

    pass_hand = hanabi.player_played('hint', to_player=to_player, info=2)

    if pass_hand:
        hanabi.next_player()
        p = hanabi.current_player

    for _ in range(2):
        pass_hand = hanabi.player_played('discard', card=p.hand[-1])
        if pass_hand:
            hanabi.next_player()
            p = hanabi.current_player

    for _ in range(3):
        pass_hand = hanabi.player_played('play', card=p.hand[2])

        if pass_hand:
            hanabi.next_player()
            p = hanabi.current_player

    return hanabi

# hanabi.table.print_stacks()

# hanabi.table.print_discard_piles()

# with open('tmp_output.json', 'w') as f:
#     f.write(hanabi.serialise())

# Basic interactive loop:


# while True:
#     #print game state
#     print(hanabi)
#     # hanabi.table.print_stacks()
#     for i in hanabi.players: print(i)
#     p = hanabi.current_player
#
#     # need to control for invalid responses with try except or some other way
#
#     action = input("Do you want to play, discard, or give a hint? (options: 'play', 'discard', 'hint')\n")
#     if action == "exit": exit()
#     elif action == 'play' or action == 'discard':
#         card_num = int(input("which card?\n"))
#         next = hanabi.player_played(action, card = p.hand[card_num])
#         if next: hanabi.next_player()
#     elif action == 'hint':
#         to_player = int(input("To which player?\n"))
#         info = input("Insert the colour or number of the hint:\n")
#         if info in ['red', 'blue', 'green', 'yellow', 'white']:
#             next = hanabi.player_played(action, to_player = hanabi.players[to_player], info = info)
#         else:
#             next = hanabi.player_played(action, to_player = hanabi.players[to_player], info = int(info))
#         if next: hanabi.next_player()
