#Card class
class Card:
    def __init__(self, number: str, suit: str):
        self.suit = suit
        self.number = number
        self.card = [self.number, self.suit]

#class Balance:
#    def __init__(self):
#        pass