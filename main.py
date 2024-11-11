import random_picker as r_p
from cards import Card

"""
    !!! 28.10.24 - 30.10.24 --- TRY CODE THIS STATEMENTS !!!
                             |
                             |
                             |
                             V           
    func to show balance(done), to do bids, to count balance; count cards ranks(dealer and player)(done), dealer or player win/lose func, restart game func(done)
"""
#30.10 rework system of validation moves, loop of games added, count bids func added, small changes due to rules of blackjack
#31.10 finished logic of split(close to finish, had bugs(so tired today, need lil break)) tomorrow just need to debug code, think this would help to find mitekes in code structure
#01.11 did start_game's functions global, finished working split, kinda working hit and stand, on this time bugs werent found by me, current_hand added, returned to split functions of showing dealer and players cards. tomorrow need to write double function, insurance function, if possible start to write count bids 


#Start screen
def start_game():
    global player_hand
    global dealer_hand
    global current_bid
    global dealer_card2_disclosed
    global current_hand
    player_card1 = r_p.pick_random()
    player_card2 = r_p.pick_random()
    player_hand = [player_card1, player_card2]
    dealer_card1 = r_p.pick_random()
    dealer_card2 = Card('Hidden card', '')
    dealer_card2_disclosed = r_p.pick_random()
    if dealer_card1.number == 'A':
        dealer_hand = [dealer_card1, dealer_card2_disclosed]
    else:
        dealer_hand = [dealer_card1, dealer_card2]
    current_hand = player_hand
    
    print(f'You started new game\nYour balance: {balance_player}.')
    bid = do_bid()
    while bid > balance_player:
        print('Make smaller bid, your current bid bigger than your balance')
        bid = do_bid()
    current_bid = bid
    
    cards_show(current_hand)
    cards_show_dealer()

    check_available_moves(current_hand)
    moves()
    print(dealer_moves())

    player_value = count_values(current_hand)
    dealer_value = count_values(dealer_hand)
    if player_value > 21:
        result = "lose"
    elif dealer_value > 21 or player_value > dealer_value:
        result = "win"
    elif player_value < dealer_value:
        result = "lose"
    else:
        result = "draw"

    print_result(current_bid, result)
    
def check_available_moves(hand):
    for key in available_moves_hashmap.keys():
        match key:
            case "SPL":
                    if (hand[0].number == hand[-1].number):
                        available_moves_hashmap[key] = True
            case "DB":
                if len(hand) == 2:
                    available_moves_hashmap[key] = True
            case "HIT":
                if hand:
                    available_moves_hashmap[key] = True
            case "STAND":
                if hand:
                    available_moves_hashmap[key] = True
            case _:
                continue

#Game moves function
def moves():
    global current_hand
    global current_bid
    while True and count_values(current_hand) <= 21:
        yes_or_no = input("What's your next move? Print SUR if you want to surrend, DB if double, SPL if split, INS if you want insurance, HIT if +card, STAND if you dont need new card\n")
        match yes_or_no:
            case "SPL":
                if available_moves_hashmap['SPL'] == True:
                    current_bid *= 2
                    available_moves_hashmap['SPL'] = False
                    split1, split2 = [player_hand[0], r_p.pick_random()], [player_hand[-1], r_p.pick_random()]
                    player_hand1 = split1
                    player_hand2 = split2
                    current_hand = player_hand1
                    cards_show(current_hand)
                    moves()
                    current_hand = player_hand2
                    check_available_moves(current_hand)
                    available_moves_hashmap['SPL'] = False
                    cards_show(current_hand)
                    moves()
                    break
                else: print('Cannot split there')
            case 'DB':
                if available_moves_hashmap['DB'] == True:
                    current_bid *= 2
                    current_hand.append(r_p.pick_random())
                    cards_show(current_hand)
                    available_moves_hashmap['DB'] = False
                    break
                else:
                    print('Double can be made only when you have 2 cards in hand')
            case 'HIT':
                current_hand.append(r_p.pick_random())
                cards_show(current_hand)
            case "STAND":
                break
            case 'SUR':
                global balance_player
                current_bid /= 2
                balance_player -= current_bid
                print(f"You surrendered! You lose half your bet: {current_bid}. Current balance: {balance_player}")
                start_game()
            case _:
                print('Move is not allowed or not recognized')

#Cards show
def cards_show(hand):
    print("Player's cards")
    for i in hand:
        print(f"| {' '.join(i.card)} |")
    print('\n')

def cards_show_dealer():
    print("Dealer's cards")
    for i in dealer_hand:
        print(f"| {' '.join(i.card)} |")
    print('\n')

def count_values(hand):
    total_value = 0
    num_aces = 0

    for card in hand:
            value = numbers[card.number]
            if card.number == 'A':
                num_aces += 1
            total_value += value
        
    while total_value > 21 and num_aces > 0:
        total_value -= 10
        num_aces -= 1

    return total_value

def dealer_moves():
    while True:
        dealer_hand[1] = dealer_card2_disclosed
        x = count_values(dealer_hand)
        cards_show_dealer()
        print(x)
        if x > 17:
            break
        dealer_hand.append(r_p.pick_random())
    return x

def do_bid():
    try:
        bid = int(input('How much would you like to bet?\n'))
    except ValueError:
        print('Do bid in number')
        bid = int(input('How much would you like to bet?\n'))
    return bid

def print_result(bid, result):
    global balance_player
    if result == "win":
        balance_player += bid  # Player wins, add the bid as profit
        print(f"You won! Current balance: {balance_player}")
    elif result == "lose":
        balance_player -= bid  # Player loses, subtract the bid from balance
        print(f"You lost! Current balance: {balance_player}")
    elif result == "draw":
        print(f"It's a draw! Balance remains the same: {balance_player}")
    else:
        print("Invalid result")
    

numbers = {
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8,
        '9' : 9,
        '10' : 10,
        'J' : 10,
        'Q' : 10,
        'K' : 10,
        'A' : 11
    }

available_moves_hashmap = {
        "SPL" : False,
        "DB" : False,
        "HIT" : False,
        "STAND" : True,
        "SUR" : True,
    }

balance_player = 1000

while balance_player > 0 :
    start_game()
    if input('Wanna play another? Y or N\n') != 'Y':
        break

