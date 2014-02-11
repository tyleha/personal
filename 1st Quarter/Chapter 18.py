# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

class Card(object):
    """represents a standard playing card."""

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank
        
    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, 'Ace', '2', '3', '4', '5', '6', '7', 
              '8', '9', '10', 'Jack', 'Queen', 'King']

    def __str__(self):
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])
    
    def __cmp__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return cmp(t1, t2)

# <codecell>

import random
class Deck(object):

    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)
                
    def __str__(self):
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)
    
    def deal_card(self):
        return self.cards.pop()
    
    def add_card(self, card):
        self.cards.append(card)
        
    def shuffle(self):
        random.shuffle(self.cards)
        
    def sort(self):
        self.cards.sort(key=lambda c: (c.suit, c.rank) )

    def move_cards(self, hand, num):
        for i in range(num):
            hand.add_card(self.pop_card())
            
            
            

# <codecell>

class Hand(Deck):
    """represents a hand of playing cards"""
    def __init__(self, label=''):
        self.cards = []
        self.label = label

# <codecell>

t1 =  Card(2,3)
t2 = Card(2,1)

mydeck = Deck()
mydeck.shuffle()
#print mydeck

mydeck.sort()
print mydeck

# <codecell>

L = [['a',1], ['a',2], ['a',3], ['b',1], ['b',2], ['b',3]]

L.sort(key=lambda k: (k[0], -k[1]), reverse=True)

# <codecell>

class B:
    pass
class C(B):
    pass
class D(C):
    pass

for c in [B, C, D]:
    try:
        raise c()
    except D:
        print "D"
    except C:
        print "C"
    except B:
        print "B"

# <codecell>


# <codecell>


