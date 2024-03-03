from PyQt5.QtCore import *
from cardlib import *


class CardModel(QObject):
    """ Base class that described what is expected from the CardView widget """

    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abc.abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abc.abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""


class HandModel(Hand, CardModel):
    def __init__(self):
        Hand.__init__(self)
        CardModel.__init__(self)
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!

    def clear(self):
        self.cards.clear()
        self.new_cards.emit()

    def drop_cards(self, indices):
        super().drop_cards(indices)
        self.new_cards.emit()


class PlayerModel(QObject):
    """The model representing a player. It will have: the player name, the total money possessed by the player,
    the money deposited in any bet and the active state"""

    # def __init__(self, name, total_money, deck_model):
    def __init__(self, name, total_money):
        super().__init__()
        self.name = name
        self.hand = HandModel()
        self.total_money = total_money
        self.bet_money = 0
        self.total_bet_money = 0
        self.active = None
        self.turns = 0


    def toggle_active(self):
        self.active = not self.active


class TableModel(CardModel):

    # def __init__(self, deck_model):
    def __init__(self):
        super().__init__()
        self.hand = HandModel()
        self.hand.flipped_cards = True

    def __iter__(self):
        return iter(self.cards)

    def flipped(self):
        return self.flipped_cards

    def flop(self, deck):
        self.hand.add_card(deck.draw())
        self.hand.add_card(deck.draw())
        self.hand.add_card(deck.draw())
        self.new_cards.emit()  # something changed, better emit the signal!

    def turn(self, deck):
        self.hand.add_card(deck.draw())
        self.new_cards.emit()  # something changed, better emit the signal!

    def river(self, deck):
        # self.index = 4
        self.hand.add_card(deck.draw())
        self.new_cards.emit()  # something changed, better emit the signal!


class GameModel(QObject):
    """The class simulating the poker game. It contains methods for initiating, folding, calling and raising a bet,
     progressing the game and restarting it once the game is over """
    money_changed = pyqtSignal()  # signal to communicate whenever total money changes for a player
    pot_money_changed = pyqtSignal()  # signal to communicate whenever pot money changes
    text_changed = pyqtSignal(str)  # signal to communicate whenever the status need to be updated
    game_message = pyqtSignal(str)  # signal to pop up message for restarting/quiting game
    flop_signal = pyqtSignal()  # signal to deal flop
    turn_signal = pyqtSignal()  # signal to deal turn
    river_signal = pyqtSignal()  # signal to deal river
    reveal_all_cards = pyqtSignal()  # signal to reveal all cards
    find_best_poker_hand = pyqtSignal()  # signal to find best poker hand
    reset_deck = pyqtSignal()  # signal to create a fresh deck

    def __init__(self, playermodels, tablemodel):
        super().__init__()
        self.playermodels = playermodels  # a list of playermodel object

        self.deck = StandardDeck()
        self.deck.shuffle()
        self.tablemodel = tablemodel
        self.counter = 0  # this tracks the game progress
        self.playermodels[0].active = True
        self.playermodels[1].active = False
        for player in self.playermodels:
            player.hand.add_card(self.deck.draw())
            player.hand.add_card(self.deck.draw())
        # first_player: Dealer/Small Blind
        # second_player: Big Blind
        self.pot_money = 0
        self.big_blind = self.playermodels[1].total_money // 100
        self.small_blind = self.big_blind // 2

        self.playermodels[0].bet_money = self.small_blind
        self.playermodels[0].total_bet_money += self.playermodels[0].bet_money
        self.playermodels[0].total_money -= self.playermodels[0].bet_money

        self.playermodels[1].bet_money = self.big_blind
        self.playermodels[1].total_bet_money += self.playermodels[1].bet_money
        self.playermodels[1].total_money -= self.playermodels[1].bet_money
        self.money_changed.emit()

        self.pot_money += self.small_blind + self.big_blind
        self.pot_money_changed.emit()
        log = "Start\n{} is the small blind and bets ${}\n{} is the big blind and bets ${}".format(
            self.playermodels[0].name, self.playermodels[0].bet_money, self.playermodels[1].name,
            self.playermodels[1].bet_money)
        self.text_changed.emit(log)

    def call_bet(self):
        call_amount = abs(self.playermodels[0].total_bet_money - self.playermodels[1].total_bet_money)
        # if self.playermodels[0].total_money == self.playermodels[1].total_money:
        if self.playermodels[0].total_bet_money == self.playermodels[1].total_bet_money:
            call_amount = self.small_blind
        if self.playermodels[0].active:
            log = "{} called ${}".format(self.playermodels[0].name, call_amount)
            self.text_changed.emit(log)
            self.pot_money += call_amount
            self.pot_money_changed.emit()
            self.playermodels[0].total_money -= call_amount
            self.playermodels[0].total_bet_money += call_amount
            self.money_changed.emit()
        else:
            log = "{} called ${}".format(self.playermodels[1].name, call_amount)
            self.text_changed.emit(log)
            self.pot_money += call_amount
            self.pot_money_changed.emit()
            self.playermodels[1].total_money -= call_amount
            self.playermodels[1].total_bet_money += call_amount
            self.money_changed.emit()
        self.progress_game()

    def fold_bet(self):
        if self.playermodels[0].active:
            self.playermodels[1].total_money += self.pot_money
            self.money_changed.emit()

            log = "{} folded. The pot money of {} goes to {}".format(self.playermodels[0].name, self.pot_money,
                                                                     self.playermodels[1].name)
            self.text_changed.emit(log)

            self.pot_money = 0
            self.playermodels[0].total_bet_money = 0
            self.playermodels[1].total_bet_money = 0
            self.pot_money_changed.emit()

            message = "{} won the game!".format(self.playermodels[1].name)
            self.game_message.emit(message)

        else:

            self.playermodels[0].total_money += self.pot_money
            self.money_changed.emit()
            log = "{} folded. The pot money of {} goes to {}".format(self.playermodels[1].name, self.pot_money,
                                                                          self.playermodels[0].name)
            self.text_changed.emit(log)
            self.pot_money = 0
            self.playermodels[0].total_bet_money = 0
            self.playermodels[1].total_bet_money = 0
            self.pot_money_changed.emit()

            message = "{} won the game!".format(self.playermodels[0].name)
            self.game_message.emit(message)

    def restart_game(self):
        # fresh deck
        self.deck = StandardDeck()
        self.deck.shuffle()
        # reset game progress
        self.counter = 0  # this tracks the game progress
        # reinitialise player
        for player in self.playermodels:
            player.hand.clear()
            for _ in range(2):
                player.hand.add_card(self.deck.draw())
        self.playermodels[0].hand.flipped_cards = False
        self.playermodels[1].hand.flipped_cards = True

        self.tablemodel.hand.clear()

        self.playermodels[0].active = False
        self.playermodels[1].active = True
        self.pot_money = 0

        self.playermodels[0].bet_money = self.small_blind
        self.playermodels[0].total_bet_money += self.playermodels[0].bet_money
        self.playermodels[0].total_money -= self.playermodels[0].bet_money

        self.playermodels[1].bet_money = self.big_blind
        self.playermodels[1].total_bet_money += self.playermodels[1].bet_money
        self.pot_money += self.small_blind + self.big_blind
        self.pot_money_changed.emit()
        self.playermodels[1].total_money -= self.playermodels[1].bet_money

        self.money_changed.emit()
        log = "================\nGame Restarted!================\n{} is the small blind and bets ${}\n" \
                   "{} is the big blind and bets ${}".format(self.playermodels[0].name, self.playermodels[0].bet_money,
                                                             self.playermodels[1].name, self.playermodels[1].bet_money)
        self.text_changed.emit(log)

    def raise_bet(self, raise_amount):
        call_amount = abs(self.playermodels[0].total_money - self.playermodels[1].total_money)
        self.pot_money += (raise_amount + call_amount)
        self.pot_money_changed.emit()
        if self.playermodels[0].active:
            self.playermodels[0].total_money -= (raise_amount + call_amount)
            self.playermodels[0].bet_money = (raise_amount + call_amount)
            self.playermodels[0].total_bet_money += self.playermodels[0].bet_money
            self.playermodels[0].turns += 1
            self.money_changed.emit()
            log = "{} raised the bet by ${} over the called bet of ${}. A total of ${}!" \
                .format(self.playermodels[0].name, raise_amount, call_amount, (raise_amount + call_amount))
            self.text_changed.emit(log)
        else:
            self.playermodels[1].total_money -= (raise_amount + call_amount)
            self.playermodels[1].bet_money = (raise_amount + call_amount)
            self.playermodels[1].total_bet_money += self.playermodels[1].bet_money
            self.playermodels[0].turns += 1
            self.money_changed.emit()
            log = "{} raised the bet by ${} over the called bet of ${}. A total of ${}!" \
                .format(self.playermodels[1].name, raise_amount, call_amount, (raise_amount + call_amount))
            self.text_changed.emit(log)

        self.progress_game()

    def progress_game(self):
        if self.playermodels[0].total_bet_money != 0:
            if self.playermodels[0].total_bet_money == self.playermodels[1].total_bet_money:

                if self.counter == 0:
                    log = "\n================\nFirst round of betting completed\n================\n Dealing the flop\n"
                    self.text_changed.emit(log)
                    self.tablemodel.flop(self.deck)

                if self.counter == 1:
                    log = "\n================\nSecond round of betting completed \n================\n" \
                               " Dealing the Turn\n"
                    self.text_changed.emit(log)
                    self.tablemodel.turn(self.deck)

                if self.counter == 2:
                    log = "\n================\nThird round of betting completed \n================\n The final card," \
                               " the river, is now shown\n"
                    self.text_changed.emit(log)
                    self.tablemodel.river(self.deck)

                if self.counter == 3:
                    log = "\n================\nFinal round of betting completed! \n================\n The players" \
                               " can now reveal their cards\n"
                    self.text_changed.emit(log)
                    self.reveal_all_cards.emit()
                    self.poker_best_hand()
                    self.counter -= 1
                self.counter += 1

    def poker_best_hand(self):
        p1hand = self.playermodels[0].hand
        pokerhand1 = p1hand.best_poker_hand(self.tablemodel.hand.cards)
        p2hand = self.playermodels[1].hand
        pokerhand2 = p2hand.best_poker_hand(self.tablemodel.hand.cards)
        if pokerhand1 < pokerhand2:
            if pokerhand1.rank == pokerhand2.rank:
                log = "Both players had same hand {}, but {}'s cards:{} win over {}'s cards:{}"\
                    .format(pokerhand2.rank.name, self.playermodels[1].name, pokerhand2.hand_cards,
                            self.playermodels[0].name, pokerhand1.hand_cards)
            else:
                log = "{} wins!\n {} had '{}' against {}'s '{}'".format(self.playermodels[1].name,
                                                                        self.playermodels[1].name,
                                                                        pokerhand2.rank.name,
                                                                        self.playermodels[0].name,
                                                                        pokerhand1.rank.name)
            self.playermodels[1].total_money += self.pot_money
            self.money_changed.emit()
            self.pot_money = 0
            self.playermodels[0].total_bet_money = 0
            self.playermodels[1].total_bet_money = 0
            self.pot_money_changed.emit()
            self.game_message.emit(log)

        if pokerhand2 < pokerhand1:
            if pokerhand1.rank == pokerhand2.rank:
                log = "Both players had same hand {}, but {}'s cards:{} win over {}'s cards:{}".\
                    format(pokerhand1.rank.name,self.playermodels[0].name, pokerhand1.hand_cards,
                           self.playermodels[1].name, pokerhand2.hand_cards)
            else:
                log = "{} wins!\n {} had '{}' against {}'s '{}'".format(self.playermodels[0].name,
                                                                        self.playermodels[0].name,
                                                                        pokerhand1.rank.name,
                                                                        self.playermodels[1].name,
                                                                        pokerhand2.rank.name)

            self.playermodels[0].total_money += self.pot_money
            self.money_changed.emit()
            self.pot_money = 0
            self.playermodels[0].total_bet_money = 0
            self.playermodels[1].total_bet_money = 0
            self.pot_money_changed.emit()
            self.game_message.emit(log)

        if pokerhand1 == pokerhand2:
            self.playermodels[0].total_money += 0.5 * self.pot_money
            self.playermodels[1].total_money += 0.5 * self.pot_money
            self.money_changed.emit()
            self.pot_money = 0
            self.playermodels[0].total_bet_money = 0
            self.playermodels[1].total_bet_money = 0
            self.pot_money_changed.emit()
            log = "It's a tie! Both players have '{}'".format(pokerhand1.rank.name)
            self.game_message.emit(log)
