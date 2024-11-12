import random as rd

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

#Card class
class Card:
    def __init__(self, number: str, suit: str):
        self.suit = suit
        self.number = number
        self.card = [self.number, self.suit]

#Start screen
def start_game():
    global player_hand
    global dealer_hand
    global current_bid
    global dealer_card2_disclosed
    global current_hand
    player_card1 = Card('2', '')
    player_card2 = Card('2', '')
    player_hand = [player_card1, player_card2]
    dealer_card1 = pick_random()
    dealer_card2 = Card('Hidden card', '')
    dealer_card2_disclosed = pick_random()
    if dealer_card1.number == 'A':
        dealer_hand = [dealer_card1, dealer_card2_disclosed]
    else:
        dealer_hand = [dealer_card1, dealer_card2]
    current_hand = player_hand
    
    print(f'Your balance: {balance_player}.')
    bid = do_bid()
    while bid > balance_player:
        print('Make smaller bid, your current bid bigger than your balance')
        bid = do_bid()
    current_bid = bid
    
    cards_show(current_hand)
    cards_show_dealer()

    check_available_moves(current_hand)
    moves()
    print(f'Your final score: {count_values(current_hand)}')
    print(f'Dealer final score: {dealer_moves()}')

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
    
#Available moves check
def check_available_moves(hand):
    for key in available_moves_hashmap.keys():
        match key:
            case "SPL":
                if (hand[0].number == hand[-1].number) and len(hand) == 2:
                    available_moves_hashmap[key] = True
                else:
                    available_moves_hashmap[key] = False
            case "DB":
                if len(hand) == 2:
                    available_moves_hashmap[key] = True
                else:
                    available_moves_hashmap[key] = False
            case "HIT":
                if hand:
                    available_moves_hashmap[key] = True
                else:
                    available_moves_hashmap[key] = False
            case "STAND":
                if hand:
                    available_moves_hashmap[key] = True
                else:
                    available_moves_hashmap[key] = False
            case _:
                continue

#Game moves function
def moves():
    global current_hand
    global current_bid
    while True and count_values(current_hand) <= 21:
        yes_or_no = input("What's your next move? SUR(to surrender), HIT(to hit), STAND(to stand), DB(to double), SPL(to split)\n")
        match yes_or_no.lower():
            case "spl":
                if available_moves_hashmap['SPL'] == True:
                    available_moves_hashmap['SPL'] = False
                    split1, split2 = [player_hand[0], pick_random()], [player_hand[-1], pick_random()]
                    player_hand1 = split1
                    player_hand2 = split2
                    current_hand = player_hand1
                    bid1 = bid2 = current_bid
                    cards_show(current_hand)
                    moves()
                    bid1 = current_bid
                    print(f'Your final score: {count_values(current_hand)}')
                    current_hand = player_hand2
                    current_bid = bid2
                    check_available_moves(current_hand)
                    available_moves_hashmap['SPL'] = False
                    cards_show(current_hand)
                    moves()
                    bid2 = current_bid
                    print(bid1, bid2)
                    current_bid = bid1 + bid2
                    print(current_bid)
                    break
                else: print('Cannot split there')
            case 'db':
                if available_moves_hashmap['DB'] == True:
                    current_bid *= 2
                    current_hand.append(pick_random())
                    cards_show(current_hand)
                    break
                else:
                    print('Double can be made only when you have 2 cards in hand')
            case 'hit':
                current_hand.append(pick_random())
                cards_show(current_hand)
            case "stand":
                break
            case 'sur':
                global balance_player
                current_bid /= 2
                balance_player -= current_bid
                print(f"You surrendered! You lose half your bet: {current_bid}. Current balance: {balance_player}")
                start_game()
                break
            case _:
                print('Move is not allowed or not recognized')
        check_available_moves(current_hand)

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

#Count hand
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

#Dealer's moves after player's
def dealer_moves():
    while True:
        dealer_hand[1] = dealer_card2_disclosed
        x = count_values(dealer_hand)
        
        if x > 17:
            break
        dealer_hand.append(pick_random())
    cards_show_dealer()
    return x

#Making bid and chekicng validation of it
def do_bid():
    while True:
        try:
            bid = float(input('How much would you like to bet?\n'))
            assert bid > 0 
            return bid
        except ValueError:
            print('Please enter a number.')
        except AssertionError:
            print('Bid cannot be lower or equal to zero.')

#Show final result function
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

#Random card picker
def pick_random():
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    suits =  ['♦', '♣', '♥', '♠']

    number, suit = rd.choice(ranks), rd.choice(suits)
    card = Card(number, suit)
    return card

    
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

#Game would be infitity, while player have money or player himself wouldnt
print('------------------  | BLACKJACK |   ------------------')
while balance_player > 0 :
    start_game()
    inp = input('Wanna play another? Y or N\n').lower()
    if inp != 'y':
        print('Thanks for playing!')
        break
