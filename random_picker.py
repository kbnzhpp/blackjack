import random as rd
from cards import Card

def pick_random():
    number, suit = rd.choice(ranks), rd.choice(suits)
    card = Card(number, suit)
    return card

ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
suits =  ['♦', '♣', '♥', '♠']