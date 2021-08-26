import random

class Card:
    def __init__(self, suit, strength):
        self.suit = suit
        self.strength = strength
        
    def isStronger(self, card):
        return self.strength > card.strength
        
    def isEqual(self, card):
        return self.strength == card.strength
        
class Player:
    def __init__(self, deck):
        self.deck = deck
        
    def getNextCard(self):
        return self.deck.pop(0)
        
    def addCard(self, card):
        self.deck.append(card)
        
    def won(self):
        return len(self.deck) == 52
    
    def lost(self):
        return len(self.deck) == 0
    
    
class Game:
    def __init__(self):
        self.deck = []
        suits = ["spades", "hearts", "clubs", "diamonds"]
        for i in range(2, 15):
            for suit in suits:
                self.deck.append(Card(suit, i))
                
    def start_game(self):
        random.shuffle(self.deck)
        print("len of deck: " + str(len(self.deck)))
        self.player1 = Player(self.deck[0:26].copy())
        self.player2 = Player(self.deck[26:52].copy())
        print(len(self.player1.deck))
        print(len(self.player2.deck))
        self.moves = 0
        
    def playMove(self):
        self.moves = self.moves + 1
        card1 = self.player1.getNextCard()
        card2 = self.player2.getNextCard()
        
        cards = [card1, card2]
        
        while not self.player1.lost() and not self.player2.lost() and card1.isEqual(card2):
            card1 = self.player1.getNextCard()
            card2 = self.player2.getNextCard()
            cards.append(card1)
            cards.append(card2)
            
        random.shuffle(cards)
        if card1.isStronger(card2):
            for card in cards:
                self.player1.addCard(card)
        else:
            for card in cards:
                self.player2.addCard(card)
            
        if self.player1.won():
            print("player 1 won")
            return True
        elif self.player2.won():
            print("player 2 won")
            return True
        else:
            return False
        
game = Game()
game.start_game()
gameWon = False

while not gameWon and game.moves < 100000:
    gameWon = game.playMove()
    
if len(game.player1.deck) > len(game.player2.deck):
    print("player1 wins the game in " + str(game.moves) + " moves with " + str(len(game.player1.deck)) + " cards")
    print("player2 has: " +str(len(game.player2.deck)) + " cards" )
else:
    print("player2 wins the game in " + str(game.moves) + " moves with " + str(len(game.player2.deck)) + " cards")
    print("player1 has: " +str(len(game.player1.deck)) + " cards" )