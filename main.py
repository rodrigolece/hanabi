
from game import Hanabi

nb_players = 4
hanabi = Hanabi(nb_players)
print(hanabi)


# Here we test discard
p = hanabi.current_player
print(p)

print('\nPassing hand')
hanabi.next_player()
p = hanabi.current_player

_ = hanabi.player_played('discard', card=p.hand[-1])
print(p)

# Here we test passing hands
for i in range(2):
    print('\nPassing hand')
    hanabi.next_player()

    p = hanabi.current_player
    print(p)


# We test playing a card
pass_hand = hanabi.player_played('play', card=p.hand[1])

hanabi.table.print_stacks()

if pass_hand:
    hanabi.next_player()
    p = hanabi.current_player

# We test giving both types of hints
to_player = hanabi.players[2]
_ = hanabi.player_played('hint', to_player=to_player, info='white')
_ = hanabi.player_played('hint', to_player=to_player, info=2)

print(f"\nPlayer {to_player.index}'s hand info:")
for i, (card, colour) in enumerate(to_player.hand_colour_info.items()):
    print("card",i,":", card,"--Info: ", colour, to_player.hand_number_info[card])

# test discard piles

hanabi.table.print_discard_piles()

print("\ncurrent hands:")
for i in hanabi.players: print(i)
hanabi.current_player = hanabi.players[2]
p = hanabi.current_player
hanabi.player_played('discard', card = p.hand[-1])

hanabi.table.print_discard_piles()
print("\ncurrent hands:")
for i in hanabi.players: print(i)

hanabi.current_player = hanabi.players[3]
p = hanabi.current_player
hanabi.player_played('play', card = p.hand[2])

hanabi.table.print_stacks()

hanabi.table.print_discard_piles()



# Basic interactive loop:

hanabi.next_player()

while True:
    #print game state
    print(hanabi)
    hanabi.table.print_stacks()
    for i in hanabi.players: print(i)
    p = hanabi.current_player

    # need to control for invalid responses with try except or some other way

    action = input("Do you want to play, discard, or give a hint? (options: 'play', 'discard', 'hint')\n")
    if action == "exit": exit()
    elif action == 'play' or action == 'discard':
        card_num = int(input("which card?\n"))
        next = hanabi.player_played(action, card = p.hand[card_num])
        if next: hanabi.next_player()
    elif action == 'hint':
        to_player = int(input("To which player?\n"))
        info = input("Insert the colour or number of the hint:\n")
        if info in ['red', 'blue', 'green', 'yellow', 'white']:
            next = hanabi.player_played(action, to_player = hanabi.players[to_player], info = info)
        else:
            next = hanabi.player_played(action, to_player = hanabi.players[to_player], info = int(info))
        if next: hanabi.next_player()
