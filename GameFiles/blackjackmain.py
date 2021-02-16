import random
from os import system, name

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear')
        
class card: 
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
    
    def __repr__(self):
        return self.value + " of " + self.suit

class deck:
    def __init__(self):
        self.cards = [card(suit, value) 
                      for suit in ["Spades", "Clubs", "Hearts", "Diamonds"]
                        for value in ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]]
                        # for value in ["A", "K"]]
    
    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)
    
    def deal(self):
        if len(self.cards) > 1:
            return self.cards.pop(0)

class hand:
    def __init__(self, dealer=False):
        self.dealer = dealer
        self.cards = []
        self.value = 0
        
    def add_card(self, card):
        self.cards.append(card)
        
    def calculate_value(self):
        self.value = 0
        
        for card in self.cards:
            has_ace = False
            if card.value == "A":
                has_ace = True

            if card.value.isnumeric():
                self.value += int(card.value)
            elif has_ace and (self.value > 21):
                self.value -= 10
                break
            elif has_ace and (self.value >= 11):
                self.value += 1
            else:
                if card.value == "A":
                    has_ace = True
                    self.value += 11
                else: 
                    self.value += 10
            
    def get_value(self):
        self.calculate_value()
        return self.value
    
    def display(self):
        if self.dealer:
            print("hidden")
            print(self.cards[1])
        else:
            for card in self.cards:
                print(card)
            print("Value:", self.get_value())
            
    def reveal(self):
        if self.dealer:
            for card in self.cards:
                print(card)
            
class Gameloop:
    def __init__(self):
        pass
    
    def dealer_draw(self):
        dealer_hand_value = self.dealer_hand.get_value()
        print("Dealer's hand is:")
        if dealer_hand_value < 17:
            while dealer_hand_value < 17:
                self.dealer_hand.add_card(self.deck.deal())
                dealer_hand_value = self.dealer_hand.get_value()
                if dealer_hand_value >= 17:
                    break
        self.dealer_hand.reveal()
    
    def final_results(self):
        dealer_hand_value = self.dealer_hand.get_value()
        player_hand_value = self.player_hand.get_value()
        print('****************************************************')
        print("Final Results")
        print("Your hand:", player_hand_value)
        print("Dealer's hand:", dealer_hand_value)
        
        if dealer_hand_value > 21 or player_hand_value > dealer_hand_value:
            print("You Win!")
        elif player_hand_value == dealer_hand_value:
            print("Tie!")    
        else:
            print("Dealer Wins!")
        # game_over = True            
                
    def play(self):
        playing = True
        
        while playing:
            clear()
            self.deck = deck()
            self.deck.shuffle()
        
            self.player_hand = hand()
            self.dealer_hand = hand(dealer=True)
            
            for _ in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())

            print("Dealer hand is:")
            self.dealer_hand.display()
            print()
            print("Your hand is:")
            self.player_hand.display()
            
            game_over = False
            
            while not game_over:
                player_has_blackjack = self.check_for_blackjack()
                dealer_has_blackjack = self.check_for_blackjack()
                
                if player_has_blackjack == True or dealer_has_blackjack == True:
                    game_over = True
                    
                    self.show_blackjack_results(player_has_blackjack, dealer_has_blackjack)
                    self.final_results()  
                else:
                    break

            if game_over == True:
                again = input("Play again? [y/n]\n")
                while again.lower() not in ["y", "n"]:
                    again = input("Play again? [y/n]\n")
                if again.lower() in ['n', 'no']:
                    print("GG!")
                    playing = False
                else:
                    game_over = False
            
            else:
                choice = input("Hit/Stay![h/s]\n").lower()
                while choice not in ["h", "s", "hit", "stay"]:
                    choice = input("Hit/Stay![h/s]\n").lower()

                if choice in ['hit', 'h']:
                    while choice in ['hit', 'h']:
                        self.player_hand.add_card(self.deck.deal())
                        self.player_hand.display()

                        if self.player_is_over():
                            print("You have lost.")
                            game_over = True
                            break
                        
                        choice = input("Hit/Stay!\n").lower()
                        if choice in ['stay', 's']:
                            self.dealer_draw()
                            self.final_results()

                            again = input("Play again? [y/n]\n")
                            while again.lower() not in ["y", "n"]:
                                again = input("Play again? [y/n]\n")
                            if again.lower() in ['n', 'no']:
                                print("GG!")
                                playing = False
                            else:
                                game_over = False

                else:
                    self.dealer_draw()
                    self.final_results()
                    
                    again = input("Play again? [y/n]\n")
                    while again.lower() not in ["y", "n"]:
                        again = input("Play again? [y/n]\n")
                    if again.lower() in ['n', 'no']:
                        print("GG!")
                        playing = False
                    else:
                        game_over = False
                    
    def check_for_blackjack(self):
        player_has_blackjack = False
        dealer_has_blackjack = False
        if self.player_hand.get_value() == 21:
            player_has_blackjack = True
        if self.dealer_hand.get_value() == 21:
            dealer_has_blackjack = True

        return player_has_blackjack, dealer_has_blackjack
    
    def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack):
        if player_has_blackjack == (True, True) and dealer_has_blackjack == (True, True):
            print("Both players have blackjack! It is a draw!")
        
        elif player_has_blackjack == (True, False):
            print("You have blackjack! You win!")
        
        elif dealer_has_blackjack == (False, True):
            print("Dealer has blackjack! Dealer wins!")
    
    def player_is_over(self):
        return self.player_hand.get_value() > 21   
    
if __name__ == "__main__":
    game = Gameloop()
    game.play()
