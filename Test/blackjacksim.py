import random

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

    def dealer_face_card(self):
        face_card = self.cards[1]
        self.get_value()

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
            self.deck = deck()
            self.deck.shuffle()
        
            self.player_hand = hand()
            self.dealer_hand = hand(dealer=True)
            
            for _ in range(2):
                self.player_hand.add_card(self.deck.deal())
                self.dealer_hand.add_card(self.deck.deal())
            
            game_over = False
            
            while not game_over:
                player_has_blackjack = self.check_for_blackjack()
                dealer_has_blackjack = self.check_for_blackjack()

                dealer_hand_value = self.dealer_hand.get_value()
                player_hand_value = self.player_hand.get_value()
                
                if player_has_blackjack == True or dealer_has_blackjack == True:
                    game_over = True
                    self.show_blackjack_results(player_has_blackjack, dealer_has_blackjack)
                else:
                    break
            
            if player_hand_value <= 13:
            # and (self.dealer_hand.dealer_face_value() == 2 or self.dealer_hand.dealer_face_value() == 3):
                print(self.dealer_hand.dealer_face_card())
                self.player_hand.add_card(self.deck.deal())
                game_over = True
            else:
                playing = False
                    
    def check_for_blackjack(self):
        player_has_blackjack = False
        dealer_has_blackjack = False
        if self.player_hand.get_value() == 21:
            player_has_blackjack = True
        if self.dealer_hand.get_value() == 21:
            dealer_has_blackjack = True

        return player_has_blackjack, dealer_has_blackjack

    def player_is_over(self):
        return self.player_hand.get_value() > 21   
    
if __name__ == "__main__":
    game = Gameloop()
    game.play()
