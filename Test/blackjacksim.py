import random
import numpy as np
import time

start_time = time.time()

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

class Gameloop:
    def __init__(self):
        pass
    
    def dealer_draw(self):
        dealer_hand_value = self.dealer_hand.get_value()
        if dealer_hand_value < 17:
            while dealer_hand_value < 17:
                self.dealer_hand.add_card(self.deck.deal())
                dealer_hand_value = self.dealer_hand.get_value()
                if dealer_hand_value >= 17:
                    break          

    def hit_or_stay(self):
        dealer_hand_value = self.dealer_hand.get_value()
        player_hand_value = self.player_hand.get_value()

        stay = False

        while stay == False:
            if (dealer_hand_value == 2 or dealer_hand_value == 3) and (player_hand_value < 13):
                self.player_hand.add_card(self.deck.deal())
                player_hand_value = self.player_hand.get_value()

            elif (dealer_hand_value == 4 or dealer_hand_value == 5 or dealer_hand_value == 6) and (player_hand_value < 12):
                self.player_hand.add_card(self.deck.deal())
                player_hand_value = self.player_hand.get_value()

            elif (dealer_hand_value >= 7 and dealer_hand_value <= 11) and (player_hand_value < 17):
                self.player_hand.add_card(self.deck.deal())
                player_hand_value = self.player_hand.get_value()

            else:
                stay = True
    
    # def check_for_blackjack(self):
    #     player_has_blackjack = False
    #     dealer_has_blackjack = False
    #     if self.player_hand.get_value() == 21:
    #         player_has_blackjack = True
    #     if self.dealer_hand.get_value() == 21:
    #         dealer_has_blackjack = True
    #     return player_has_blackjack, dealer_has_blackjack
    
    # def show_blackjack_results(self, player_has_blackjack, dealer_has_blackjack):
    #     if player_has_blackjack == (True, True) and dealer_has_blackjack == (True, True):
    #         print("Both players have blackjack! It is a draw!")
        
    #     elif player_has_blackjack == (True, False):
    #         print("You have blackjack! You win!")
        
    #     elif dealer_has_blackjack == (False, True):
    #         print("Dealer has blackjack! Dealer wins!")
 

    def play(self):
        simulations = int(input("Number of simulations? "))
        results_arr = np.zeros(simulations, dtype=int)
        for index in range(0, simulations):
            self.deck = deck()
            self.deck.shuffle()
        
            self.player_hand = hand()
            self.dealer_hand = hand(dealer=True)
            
            self.dealer_hand.add_card(self.deck.deal())

            for _ in range(2):
                self.player_hand.add_card(self.deck.deal())

            self.hit_or_stay()

            self.dealer_hand.add_card(self.deck.deal())
            self.dealer_draw()

            dealer_hand_value = self.dealer_hand.get_value()
            player_hand_value = self.player_hand.get_value()

            # player_has_blackjack = self.check_for_blackjack()
            # dealer_has_blackjack = self.check_for_blackjack()
            
            # if player_has_blackjack == True or dealer_has_blackjack == True:
            #     self.show_blackjack_results(player_has_blackjack, dealer_has_blackjack)
            # else:
            #     break
        
            if dealer_hand_value > 21 or player_hand_value > dealer_hand_value:
                results_arr[index] = 1
            elif player_hand_value == dealer_hand_value:
                results_arr[index] = 2
            else:
                results_arr[index] = 3

        print(str(simulations) + " Simulations") 
        player_wins = np.count_nonzero(results_arr == 1)
        dealer_wins = np.count_nonzero(results_arr == 2)
        ties = np.count_nonzero(results_arr == 3)
        player_percent = (player_wins / simulations) * 100
        dealer_percent = (dealer_wins / simulations) * 100
        ties_percent = (ties / simulations) * 100
        print(str(player_percent) + "%")
        print(str(dealer_percent) + "%")
        print(str(ties_percent) + "%")
        print(str(time.time() - start_time) + " seconds")
        
    
if __name__ == "__main__":
    game = Gameloop()
    game.play()
