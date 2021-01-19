from enum import Enum
from abc import ABC, abstractmethod
import datetime
import random

"""
Title: An on-Terminal Blackjack game for 1-player. (A python OOP exercise)
Author: Nicholas Frederiksen (Github: @Nfrederiksen)
"""

# ----------------------------------
# STATIC FUNCTIONS & VARIABLES
# ----------------------------------
CARD = """\
┌───┐
│ {}│
| {}│
└───┘
""".format('{rank: <2}', '{suit: <2}', '{rank: >2}')

name_to_symbol = {
    'SPADES': '♠',
    'DIAMONDS': '♦',
    'HEARTS': '♥',
    'CLUBS': '♣',
}


def join_lines(strings):
    """
    Stack strings horizontally.
    This doesn't keep lines aligned unless the preceding lines have the same length.
    :param strings: Strings to stack
    :return: String consisting of the horizontally stacked input
    """
    split_lines_list = [string.splitlines() for string in strings]
    return '\n'.join(''.join(lines) for lines in zip(*split_lines_list))


def numbers_to_strings(argument):
    switcher = {
        11: "J",
        12: "Q",
        13: "K",
        1: "A"
    }
    return switcher.get(argument, argument)


# ----------------------------------
# FUNCTIONS FOR PRETTY CARD PRINTING
# ----------------------------------
def card_to_string(card):
    rank = card.get_face_value()
    suit = card.get_suit().name
    # add the individual card on a line by line basis
    return CARD.format(rank=numbers_to_strings(rank), suit=name_to_symbol[suit])


def pretty_print_cards_in_row(cards):
    print(join_lines(map(card_to_string, cards)))


# ----------------------------------
# CLASSES
# ----------------------------------
# Required enumerator.
class SUIT(Enum):
    HEARTS, DIAMONDS, CLUBS, SPADES = 1, 2, 3, 4


# The following class encapsulates a playing card
class Card:
    def __init__(self, suit, face_value):
        self.__suit = suit
        self.__face_value = face_value

    def get_suit(self):
        return self.__suit

    def get_face_value(self):
        return self.__face_value


# Extends Card class, to follow blackjack value rules.
class BlackJackCard(Card):
    def __init__(self, suit, face_value):
        super().__init__(suit, face_value)
        # param: __game_value, Face cards are 10 and any other card is its pip value.
        if face_value > 10:
            self.__game_value = 10
        else:
            self.__game_value = face_value

    def get_game_value(self):
        return self.__game_value


class Deck:
    def __init__(self):
        self.__cards = []
        self.__creation_date = datetime.date.today()
        for val in range(1, 14):
            for suit in SUIT:
                self.__cards.append(BlackJackCard(suit=suit, face_value=val))

    def get_cards(self):
        return self.__cards


class Shoe:
    def __init__(self, number_of_decks):
        self.__cards = []
        self.__number_of_decks = number_of_decks
        self.create_shoe()
        self.shuffle()

    def create_shoe(self):
        for decks in range(0, self.__number_of_decks):
            myDeck = Deck()
            new_cards = myDeck.get_cards()
            self.__cards.extend(myDeck.get_cards())

    def shuffle(self):
        card_count = len(self.__cards)
        for i in range(0, card_count):
            j = random.randrange(0, card_count - 1, 1)
            self.__cards[i], self.__cards[j] = self.__cards[j], self.__cards[i]

    # Get the next card from the shoe
    def deal_card(self):
        if len(self.__cards) == 0:
            self.create_shoe()
        else:
            dealt_card = self.__cards.pop(0)
            return dealt_card


# Hand: Hand class encapsulates a blackjack hand which can contain multiple cards:
class Hand:
    def __init__(self, blackjack_card1, blackjack_card2):
        self.__cards = [blackjack_card1, blackjack_card2]
        self.__stand_state = False

    def add_card(self, card):
        self.__cards.append(card)

    def get_cards(self):
        return self.__cards

    def get_first_card_value(self):
        return self.__cards[0].get_game_value()

    def get_stand_state(self):
        return self.__stand_state

    def set_stand_state(self, boolean):
        self.__stand_state = boolean

    def get_scores(self):
        """ Summarize the face value of each card, but
        if an Ace is involved then there are 2 versions of the score """
        totals = [0]
        for card in self.__cards:
            new_total = []
            for score in totals:
                new_total.append(card.get_game_value() + score)
                if card.get_game_value() == 1:
                    new_total.append(11 + score)
                else:
                    continue
            totals = new_total
        return totals

    # get highest score which is less than or equal to 21
    def resolve_score(self):
        scores = self.get_scores()
        best_score = 0
        for score in scores:
            if 21 >= score > best_score:
                best_score = score
            else:
                continue
        return best_score

    def get_final_score(self):
        if self.resolve_score() == 0:
            return self.get_scores()[0]
        else:
            return self.resolve_score()


class BasePlayer(ABC):
    def __init__(self, balance):
        self.__balance = balance
        self.__hands = []

    def reset_password(self):
        pass

    def get_hands(self):
        return self.__hands

    def add_hand(self, hand):
        self.__hands.append(hand)

    def remove_hand(self, hand):
        self.__hands.remove(hand)

    def clear_hands(self):
        self.__hands.clear()

    def all_hands_standing(self):
        # If a hand is not in stand-state, then false.
        for hand in self.__hands:
            if not hand.get_stand_state():
                return False
            else:
                continue
        return True

    def has_blackjack(self, hand):
        # Condition for blackjack is, that player has 1 hand and only 2 cards that make 21.
        if hand.resolve_score() is 21 and len(self.get_hands()) is 1 and len(self.get_hands()[0].get_cards()) is 2:
            return True
        else:
            return False

    @abstractmethod
    def print_hands(self, _format):
        pass


# Player: Player class extends from BasePlayer:
class Player(BasePlayer):
    def __init__(self, balance=1000):
        super().__init__(balance)
        self.__bet = 0
        self.__side_bet = 0

    def place_bet(self, bet):
        self.__bet = bet

    def place_side_bet(self, side_bet):
        self.__side_bet = side_bet

    def get_bet(self):
        return self.__bet

    def get_side_bet(self):
        return self.__side_bet

    def get_balance(self):
        return self.__balance

    def set_balance(self, balance):
        self.__balance = balance

    def add_to_balance(self, cash):
        self.__balance = self.__balance + cash

    def print_hands(self, _format='ascii'):
        hand_number = 0
        for hand in super().get_hands():
            hand_number = hand_number + 1
            print(f'Player Hand #{hand_number}:')
            if _format == "text":
                for card in hand.get_cards():
                    print("\tA Card Shows:", card.get_face_value(), "of", card.get_suit().name)
            else:
                pretty_print_cards_in_row(hand.get_cards())


# Dealer: Dealer class extends from BasePlayer:
class Dealer(BasePlayer):
    def __init__(self, balance=1000):
        super().__init__(balance)

    def print_first_card(self, _format="ascii"):
        dealers_hand = super().get_hands()
        dealers_hand_copy = Hand(dealers_hand[0].get_cards()[0], dealers_hand[0].get_cards()[0])
        dealers_hand_copy.get_cards().pop()
        dealers_first_card = dealers_hand_copy
        if _format == "text":
            print("\tA Card Shows:", dealers_first_card.get_face_value(),
                  "of", dealers_first_card.get_suit().name)
        else:
            pretty_print_cards_in_row(dealers_hand_copy.get_cards())

    def print_hands(self, _format="ascii"):
        for hand in super().get_hands():
            if _format == "text":
                for card in hand.get_cards():
                    print("\tA Card Shows:", card.get_face_value(), "of", card.get_suit().name)
            else:
                pretty_print_cards_in_row(hand.get_cards())


# Game: This class encapsulates a blackjack game:
class Game:
    def __init__(self, player, dealer):
        self.__player = player
        self.__dealer = dealer
        self.__gameUI = GameUI(player, dealer)
        self.__MAX_NUM_OF_DECKS = 3
        self.__shoe = Shoe(self.__MAX_NUM_OF_DECKS)

    def play_action(self, action, hand):
        print(f'(Your action was: {action})')
        if action.lower() == "hit":
            self.hit(hand)
            print(f'->[] You were dealt a: {hand.get_cards()[-1].get_face_value()}'
                  f' of {hand.get_cards()[-1].get_suit().name}')
            self.bust_check(hand)

        elif action.lower() == "split":
            self.split(hand)
        elif action.lower() == "stand":
            hand.set_stand_state(True)
            self.stand(hand)
        elif action.lower() == "double down":
            self.double_down(hand)
        else:
            print("\nError Invalid Action!")

    def dealer_plays(self):
        dealers_hand = self.__dealer.get_hands()[0]
        while True:
            best_score = dealers_hand.resolve_score()
            if best_score == 0:
                print("Yep, dealer went BUST!\n")
                break
            elif best_score < 17:
                self.hit(dealers_hand)
                # Print latest added card to hand.
                print(f'->[] Dealer was dealt a:'
                      f' {dealers_hand.get_cards()[-1].get_face_value()}'
                      f' of {dealers_hand.get_cards()[-1].get_suit().name}')
            else:
                break
        return best_score

    def hit(self, hand):
        new_card = self.__shoe.deal_card()
        hand.add_card(new_card)

    def bust_check(self, hand):
        if hand.resolve_score() == 0:
            # Hand is Bust, then auto-stand
            self.__gameUI.bust_msg()
            hand.set_stand_state(True)
            self.stand(hand)
        else:
            hand.set_stand_state(False)

    def stand(self, hand):
        # Only if all hands are in Stand-state.
        if self.__player.all_hands_standing():
            dealers_hand = self.__dealer.get_hands()[0]
            hands = self.__player.get_hands()
            print("\n\n_____________________________"
                  "\n     S E T T L E M E N T!    ")
            print("No. Hands:", len(hands))
            print(f'Total bet is at: {self.__player.get_bet()}')
            self.__gameUI.show_all_hands()
            for hand in hands:
                # If player's hand is busted or dealer has under 16, no need for the dealer to play any further.
                if hand.resolve_score() is not 0 and dealers_hand.resolve_score() < 17:
                    dealer_score = self.dealer_plays()
                    self.__gameUI.show_all_hands()
                else:
                    dealer_score = dealers_hand.resolve_score()
                print(f'Dealer has:{dealers_hand.get_final_score()}')
                print(f'And Player has:{hand.get_final_score()}')
                best_score = hand.resolve_score()
                # If player has Blackjack and dealer doesn't.
                if self.__player.has_blackjack(hand) and not self.__dealer.has_blackjack(dealers_hand):
                    self.__gameUI.win_by_blackjack_msg()
                    self.__player.add_to_balance(round(self.__player.get_bet() * 1.5))
                # If dealer instead has blackjack and player doesn't
                elif self.__dealer.has_blackjack(dealers_hand) and not self.__player.has_blackjack(hand):
                    self.__gameUI.lose_by_blackjack_msg()
                    self.__player.add_to_balance(-1 * self.__player.get_bet())
                # If player scores better than dealer.
                elif best_score > dealer_score:
                    self.__gameUI.win_msg()
                    self.__player.add_to_balance(self.__player.get_bet())
                # If dealer scores better than player.
                elif best_score < dealer_score:
                    self.__gameUI.lose_msg()
                    self.__player.add_to_balance(-1 * self.__player.get_bet())
                # If both have equal score.
                else:
                    self.__gameUI.tie_msg()
        else:
            pass

    def double_down(self, hand):
        self.__player.place_bet(self.__player.get_bet() * 2)
        self.hit(hand)
        print(f'->[] You were dealt a: {hand.get_cards()[-1].get_face_value()}'
              f' of {hand.get_cards()[-1].get_suit().name}')
        self.bust_check(hand)
        if not hand.get_stand_state():
            hand.set_stand_state(True)
            self.stand(hand)
        else:
            pass

    def split(self, hand):
        # Player gets 2 hands
        cards = hand.get_cards()
        self.__player.add_hand(Hand(cards[0], self.__shoe.deal_card()))
        self.__player.add_hand(Hand(cards[1], self.__shoe.deal_card()))
        self.__player.remove_hand(hand)

    def start(self):
        while True:
            self.__player.set_balance(1000)
            on_round = 1
            while True:
                self.__gameUI.start_screen(on_round)
                my_bet = self.__gameUI.get_bet_from_user()
                self.__player.place_bet(my_bet)
                # Deal to Player
                player_hand = Hand(self.__shoe.deal_card(),
                                   self.__shoe.deal_card())
                self.__player.add_hand(player_hand)
                # Deal to Dealer
                dealer_hand = Hand(self.__shoe.deal_card(),
                                   self.__shoe.deal_card())
                self.__dealer.add_hand(dealer_hand)
                # Show cards to User
                self.__gameUI.show_starting_hands()
                # ---- GAME: Insurance Scenario ----
                if dealer_hand.get_first_card_value() is 10 or dealer_hand.get_first_card_value() is 1:
                    self.__gameUI.offer_insurance_msg()
                    if self.__gameUI.get_insurance_bet_from_user() == "y":
                        self.__player.place_side_bet(round(0.5 * my_bet))
                        # Resolve to Side bet/Insurance bet.
                        if self.__dealer.has_blackjack(dealer_hand):
                            player_hand.set_stand_state(True)
                            self.stand(player_hand)
                            self.__gameUI.insurance_win_msg()
                            self.__player.add_to_balance(2 * self.__player.get_side_bet())
                            # Clear Hands and Move on to next round!
                            self.__player.clear_hands()
                            self.__dealer.clear_hands()
                            continue
                        else:
                            self.__gameUI.insurance_lose_msg()
                            self.__player.add_to_balance(-1 * self.__player.get_side_bet())
                            # Then we continue to play the round.
                    else:
                        print("No...? Well fine then, it's your credits after all!")

                # ---- GAME: Main Event ----
                # Break out of this loop for a new round!
                while True:
                    action = ""
                    hands = self.__player.get_hands()
                    for hand_num, hand in enumerate(hands):
                        if not hand.get_stand_state():
                            if hand.resolve_score() == 21:
                                # Hand is 21, then auto-stand.
                                print("Good hand! You have 21.")
                                hand.set_stand_state(True)
                                self.stand(hand)
                            else:
                                # User gets to choose an action.
                                self.__gameUI.show_scores(hand_num)
                                action = self.__gameUI.get_user_action(hand)
                                self.play_action(action, hand)
                                if action == 'split':
                                    break
                                else:
                                    continue
                        else:
                            continue
                    if self.__player.all_hands_standing():
                        print("Moving on to the next round... ")
                        break
                    else:
                        self.__gameUI.show_starting_hands()
                # Ending the round.
                self.__player.clear_hands()
                self.__dealer.clear_hands()
                if self.__player.get_balance() <= 0:
                    self.__gameUI.game_over_screen()
                    break
                elif self.__player.get_balance() >= 20000:
                    self.__gameUI.EPIC_WIN_SCREEN()
                    break
                else:
                    on_round = on_round + 1
            # Offer the User a Restart
            if input("Do you want to restart [Y/N]?").lower() == "n":
                break
            else:
                continue
        print("Thank you for playing...Good bye ;)")


# GameUI: This class contains functions for user prompts and messages:
class GameUI:
    def __init__(self, player, dealer):
        self.__player = player
        self.__dealer = dealer

    @staticmethod
    def get_user_action(hand):
        list_of_actions = ["hit", "stand", "double down"]

        while True:
            print("_____________________________"
                  "\n  T I M E   T O   P L A Y! ")
            # Check for Split scenario
            cards = hand.get_cards()
            if len(cards) == 2 and cards[0].get_face_value() == cards[1].get_face_value():
                if "split" not in list_of_actions:
                    list_of_actions.append("split")
                print('Your options are:', *list_of_actions, sep='\n\t')
                player_action = input("Do you want to do?:\n")
            else:
                print('Your options are:', *list_of_actions, sep='\n\t')
                player_action = input("Do you want to do?:\n")
            # Validate Player Action
            if player_action.lower() in list_of_actions:
                return player_action
            else:
                print("x x x x x x x x x x x x")
                print("Error! Invalid action!")
                print("x x x x x x x x x x x x")
                continue  # Try again, for a valid action.

    def get_bet_from_user(self):
        while True:
            try:
                bet = int(input("Place your bet!:\n"))
            except ValueError:
                print("Sorry, I didn't understand that. Try Again.")
                continue
            else:
                if bet <= self.__player.get_balance():
                    print(f'Ok, You are betting {bet} credits.')
                    break
                else:
                    print(f'Sorry, but that is more then your current balance: {self.__player.get_balance()}')
                    print("\nTry entering a lower amount.")
        return bet

    @staticmethod
    def get_insurance_bet_from_user():
        while True:
            player_response = input("Accept Insurance Bet? [Y/N]").lower()
            if player_response == "y" or player_response == "n":
                break
            else:
                print("x x x x x x x x x x x x")
                print("Error! Invalid action!")
                print("x x x x x x x x x x x x")
                continue  # Try again, for a valid action.
        return player_response

    def show_starting_hands(self):
        print("=============  [?]  [ ]  ==============|")
        print("Dealer's Hand:")
        self.__dealer.print_first_card()
        self.__player.print_hands()
        print("=============  [ ]  [ ]  ==============|")

    def show_all_hands(self):
        print("===========================|")
        print("Dealer's Hand:")
        self.__dealer.print_hands()
        self.__player.print_hands()
        print("===========================|")

    def show_scores(self, hand_num):
        hands = self.__player.get_hands()
        if hands[hand_num].resolve_score() == 0:
            end_str = '\t[bust]\n'
        elif hands[hand_num].get_stand_state():
            end_str = '\t[stand]\n'
        else:
            end_str = '\n'

        if len(hands) > 1:
            print("_____________________________")
            print(f'\nYour scores for Hand #{hand_num + 1} are:')
            print(sep='/', *hands[hand_num].get_scores(), end=end_str)
        else:
            print("_____________________________")
            print(f'\nYour scores are:')
            print(sep='/', *hands[0].get_scores())

    def start_screen(self, round_number):
        print("\n=======@┌──────────────────────┐@======  ___  ____ ===")
        print("=======@| Let's Play Blackjack |@====== | A |/ K / ===")
        print("=======@└──────────────────────┘@====== | ♥_| ♦_/  ===")
        print(f'Round {round_number} \t\t\t Balance: {self.__player.get_balance()} CREDITS')

    @staticmethod
    def game_over_screen():
        print("==================================\n")
        print("======== G A M E    O V E R ======\n")
        print("==================================\n")

    @staticmethod
    def EPIC_WIN_SCREEN(self):
        print("\nMan, You. Are. An. Absolute. Legend!")
        print("You reached over 20.000 credits! Congrats! You are the Blackjack EPIC...\n")
        print("$$\      $$\ $$$$$$\ $$\   $$\ $$\   $$\ $$$$$$$$\ $$$$$$$\  ")
        print("$$ | $\  $$ |\_$$  _|$$$\  $$ |$$$\  $$ |$$  _____|$$  __$$\ ")
        print("$$ |$$$\ $$ |  $$ |  $$$$\ $$ |$$$$\ $$ |$$ |      $$ |  $$ |")
        print("$$ $$ $$\$$ |  $$ |  $$ $$\$$ |$$ $$\$$ |$$$$$\    $$$$$$$  |")
        print("$$$$  _$$$$ |  $$ |  $$ \$$$$ |$$ \$$$$ |$$  __|   $$  __$$< ")
        print("$$$  / \$$$ |  $$ |  $$ |\$$$ |$$ |\$$$ |$$ |      $$ |  $$ |")
        print("$$  /   \$$ |$$$$$$\ $$ | \$$ |$$ | \$$ |$$$$$$$$\ $$ |  $$ |")
        print("\__/     \__|\______|\__|  \__|\__|  \__|\________|\__|  \__|")

    @staticmethod
    def win_by_blackjack_msg():
        print("##########################################################")
        print("#  We Got BlackJack baby! Pay 3:2 of the bet! [X_____x]  #")
        print("##########################################################")

    @staticmethod
    def win_msg():
        print("################################################")
        print("#  Player Wins! Pay 1:1 of the bet! [>_____<]  #")
        print("################################################")

    @staticmethod
    def lose_by_blackjack_msg():
        print("############################################################################")
        print("#  Player Loses, Dealer has Blackjack! Collect bet from player! [^_____^]  #")
        print("############################################################################")

    @staticmethod
    def lose_msg():
        print("###################################################################")
        print("#  Player Loses, Dealer wins! Collect bet from player! [^_____^]  #")
        print("###################################################################")

    @staticmethod
    def tie_msg():
        print("##############################################################")
        print("#  We tied! Pay Nothing. Bet goes back to player. [-_____-]  #")
        print("##############################################################")

    @staticmethod
    def bust_msg():
        print("/|/|/|/|/|/|/|/|/|/|/|/|/")
        print("|  Oh no! It's a BUST!  |")
        print("|/|/|/|/|/|/|/|/|/|/|/|/|")

    @staticmethod
    def offer_insurance_msg():
        print("-------------------------------------------------------")
        print("| Yikes! Dealer might have a blackjack on their hand. |")
        print("| Would you like some Insurance?      ['  ..  ']      |")
        print("-------------------------------------------------------")

    @staticmethod
    def insurance_win_msg():
        print("##############################################################")
        print("#  ...Hey, but look at that!     [O  .  O]                   #")
        print("#  Player Wins Insurance Bet! Pay 2:1 of the bet! [>_____<]  #")
        print("##############################################################")

    def insurance_lose_msg(self):
        print("#########################################################################")
        print("#  Player Loses Insurance Bet! Collect side-bet from player! [^_____^]  #")
        print(f'#  [Player lost {self.__player.get_side_bet()} credits]')
        print("#########################################################################")


# ----------------------------------
# DRIVER FUNCTION
# ----------------------------------
def main():
    player = Player()
    dealer = Dealer()
    game = Game(player, dealer)
    game.start()


if __name__ == "__main__":
    # execute only if run as a script
    main()
