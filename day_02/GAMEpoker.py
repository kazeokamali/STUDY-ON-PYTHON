from enum import Enum

class fourSUITE(Enum):
    Spade,Heart,Club,Diamond,Joker = range(5)

'''
for i in fourSUITE:
    print(f'{i}:{i.value}')
'''

class Card:

    def __init__(self,suite,score):
        self.suite = suite
        self.score = score

    def getCard(self):
        all_suites = '♠♥♣♦🃏'
        all_scores = ['','2','3','4','5','6','7','8','9','10','J','Q','K','A','小王','大王']
        '''
        if self.suite == fourSUITE.Joker:
            return f'' 
        '''
        return f'{all_suites[self.suite.value]}{all_scores[self.score]}'

    def __lt__(self, other):
        if self.score == other.score:
            return self.suite.value < other.suite.value
        return self.score < other.score
    '''
    def __lt__(self, other):
        if self.suite == other.suite:
            return self.score < other.score
        return self.suite.value < other.suite.value'''

    def __eq__(self, other):
        return self.suite == other.suite and self.score == other.score
'''
testCard = Card(fourSUITE.Heart,12)
print( testCard.getCard() )
'''

import random

class OPtoPOKER:
    def __init__(self):
        self.allCRADS =  [Card(fourSUITE.Joker, 14), Card(fourSUITE.Joker, 15)]
        for i in range(1, 14):
            for suite in list(fourSUITE)[:-1]:  # 不包括 Joker
                self.allCRADS.append(Card(suite, i))

        self.current = 0

    def shuffle(self):
        self.current = 0
        random.shuffle( self.allCRADS )
        print('succeed')

    def deal(self):
        thecard = self.allCRADS[self.current]
        self.current += 1
        return thecard

    @property
    def hasleft(self):
        return self.current < len(self.allCRADS)

'''
poke = OPtoPOKER()
for k in poke.allCRADS:
    print( k.getCard() )

poke.shuffle()
for k in poke.allCRADS:
    print( k.getCard() )
'''

class Player:

    def __init__(self,name):
        self.name = name
        self.hands = []

    def hand_card(self,onecard):
        self.hands.append(onecard)


    def arrange(self):
        self.hands.sort()



poke = OPtoPOKER()
poke.shuffle()

players = [Player('p1'),Player('p2'),Player('p3')]

tobuy = []
for t in range(3):
    tobuy.append(poke.allCRADS.pop())
    print(tobuy[t].getCard())


for _ in range(17):
    for i in players:
        i.hand_card( poke.deal() )



for i in players:
    print(f'\033[034m{i.name}\033[0m:\n',end= '')
    i.arrange()
    for j in range(17):
        # print( i.hands[j].getCard() )
        if i.hands[j].suite.value == 1 or i.hands[j].suite.value ==3:
            print(f'\033[031m{i.hands[j].getCard()}\033[0m')
        else:
            print(f'{i.hands[j].getCard()}')

