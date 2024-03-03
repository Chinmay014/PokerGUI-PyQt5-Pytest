import abc
import enum
from random import shuffle
from collections import Counter  


class Suit(enum.Enum):
    """ creates a suit of Enum type, in order of Hearts, Spades, Clubs and Diamonds """
    Hearts = 1
    Spades = 2
    Clubs = 3
    Diamonds = 4

    def __repr__(self):
        """this method is called when print() is executed. Used later in GUI"""
        if self == Suit.Hearts:
            return "H"
        if self == Suit.Spades:
            return "S"
        if self == Suit.Clubs:
            return "C"
        if self == Suit.Diamonds:
            return "D"

    def __str__(self):
        """this method is called when print() is executed"""
        if self == Suit.Hearts:
            return "\u2665"
        if self == Suit.Spades:
            return "\u2660"
        if self == Suit.Clubs:
            return "\u2663"
        if self == Suit.Diamonds:
            return "\u2666"


class PlayingCard(metaclass=abc.ABCMeta):
    """Superclass for all cards in the deck"""

    def __init__(self, suit: Suit):
        self.suit = suit

    def __str__(self):
        """this method is called when print() is executed"""

    @abc.abstractmethod
    def get_value(self):
        """ returns value from 2 to 10 for card value"""

    @abc.abstractmethod
    def suit(self):
        """returns suit of card"""

    def __eq__(self, other):
        """ checks whether card(s) in self are comparable to other card(s)"""
        return self.get_value() == other.get_value()

    def __lt__(self, other):  # We only check the magnitude:
        """ checks whether card(s) in self are less than other card(s)"""
        return self.get_value() < other.get_value()


class NumberedCard(PlayingCard):
    """Creates a Numbered card. Takes a number(2-10) and suit as input"""

    def __init__(self, value: int, suit: Suit):
        super().__init__(suit)
        self.value = value

    def get_value(self):
        """ returns from 2 to 10 for card value"""
        return self.value

    def suit(self):
        """returns suit of card"""
        return self.suit

    def __str__(self):
        return "{} of {}".format(self.value, self.suit)

    def __repr__(self):
        return "{} of {}".format(self.value, self.suit)


class JackCard(PlayingCard):
    """Creates a Jack card. Takes a suit as input"""

    def __init__(self, suit: Suit):
        super().__init__(suit)

    def get_value(self):
        """ returns from 2 to 10 for card value"""
        return 11

    def suit(self):
        """returns suit of card"""
        return self.suit

    def __str__(self):
        return "Jack of {}".format(self.suit)

    def __repr__(self):
        return "Jack of {}".format(self.suit)


class KingCard(PlayingCard):
    """Creates a King card. Takes a suit as input"""

    def __init__(self, suit: Suit):
        super().__init__(suit)

    def get_value(self):
        """ returns from 2 to 10 for card value"""
        # This is called them you do:   a = x[i]
        return 13

    def suit(self):
        """returns suit of card"""
        return self.suit

    def __str__(self):
        return "King of {}".format(self.suit)

    def __repr__(self):
        return "King of {}".format(self.suit)


class QueenCard(PlayingCard):
    """Creates a Queen card. Takes a suit as input"""

    def __init__(self, suit: Suit):
        super().__init__(suit)

    def get_value(self):
        """ returns from 2 to 10 for card value"""
        # This is called them you do:   a = x[i]
        return 12

    def suit(self):
        """returns suit of card"""
        return self.suit

    def __str__(self):
        return "Queen of {}".format(self.suit)

    def __repr__(self):
        return "Queen of {}".format(self.suit)


class AceCard(PlayingCard):
    """Creates an Ace card. Takes a suit as input"""

    def __init__(self, suit: Suit):
        super().__init__(suit)

    def get_value(self):
        """ returns from 2 to 10 for card value"""
        return 14

    def suit(self):
        """returns suit of card"""
        return self.suit

    def __str__(self):
        return "Ace of {}".format(self.suit)

    def __repr__(self):
        return "Ace of {}".format(self.suit)


class StandardDeck:
    """Creates a deck of 52 cards, in order of Hearts,Spades, Clubs and Diamonds"""

    def __init__(self):
        self.cards = []
        self.make_deck()

    def make_deck(self):
        """generates a list of 52 cards"""
        for x in Suit:
            for t in range(2, 11, 1):
                self.cards.append(NumberedCard(t, x))
            self.cards.append(JackCard(x))
            self.cards.append(QueenCard(x))
            self.cards.append(KingCard(x))
            self.cards.append(AceCard(x))

    def shuffle(self):
        """ Shuffles the deck in random order"""
        # assigning an index for each card
        # random.seed(123)
        range_of_numbers = [m for m in range(len(self.cards))]
        shuffle(range_of_numbers)
        self.cards = [self.cards[x] for x in range_of_numbers]

    def draw(self):
        """ picks a card from the deck"""
        # pop out top card
        return self.cards.pop(0)


class Hand:
    """Creates a hand with card list"""

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """add cards to hand"""
        self.cards.append(card)

    def sort(self):
        """sorts cards in hand"""
        self.cards.sort()

    def __str__(self):
        return "cards in hand:{}".format(self.cards)

    def drop_cards(self, indices):
        """
        drops cards as specified in the index

        :param indices: the indices of the dropped cards
        :return: the updated hand after the cards are dropped
        """
        # find the cards for the given index
        dropped_cards = [self.cards[j] for j in indices]
        for card_index in dropped_cards:
            self.cards.remove(card_index)
        # return self.cards

    def best_poker_hand(self, other: list[PlayingCard] = []):
        """
        returns the best poker hand possible from the cards in hand and the poker table

        :param other: cards on the poker table
        :return: a poker hand object
        """
        myp = PokerHand(self.cards + other)
        return myp


class HandRank(enum.IntEnum):
    """Class representing Poker HandType in an Enum format"""
    get_highest_card = 1
    get_one_pairs = 2
    get_two_pairs = 3
    get_three_of_a_kind = 4
    get_straight = 5
    get_flush = 6
    get_full_house = 7
    get_four_of_a_kind = 8
    get_straight_flush = 9


class PokerHand:
    """This class checks different poker hand possibilities given a set of cards"""

    def __init__(self, cards=None):
        if cards is None:
            self.cards = []
        else:
            self.cards = cards
        self.rank = HandRank.get_highest_card
        self.hand_cards = []
        poker_hand_list = [self.get_straight_flush, self.get_four_of_a_kind, self.get_full_house, self.get_flush,
                           self.get_straight, self.get_three_of_a_kind, self.get_pairs, self.get_highest_card]
        for best_hand in poker_hand_list:
            if best_hand() is not None:
                best_hand()
                break

    def __str__(self):
        return "The best poker hand is {} with card values {}".format(self.rank.name, self.hand_cards)

    def get_highest_card(self):
        """ Finds the highest value card in a set of cards """
        self.cards.sort(reverse=True)
        self.rank = HandRank.get_highest_card
        self.hand_cards = self.cards
        return self.cards[0]

    def get_pairs(self):
        """checks for pairs(1 or 2) in a set of cards.

         Returns the value of paired card if found, otherwise returns None"""
        self.cards.sort(reverse=True)
        value_count = Counter()
        for c in self.cards:
            value_count[c.get_value()] += 1
        pairs = [v[0] for v in value_count.items() if v[1] >= 2]
        remaining_cards = [v[0] for v in value_count.items() if v[1] == 1]
        pairs.sort()
        self.rank = HandRank.get_highest_card
        if pairs:
            if len(pairs) == 1:
                self.rank = HandRank.get_one_pairs
                self.hand_cards = pairs + remaining_cards[0:3]
            if len(pairs) == 2:
                self.rank = HandRank.get_two_pairs
                self.hand_cards = pairs + remaining_cards[0:1]
            return pairs

    def get_three_of_a_kind(self):
        """checks for triplets in a set of cards.

        Returns the value of triplet card if found, otherwise returns None"""
        self.cards.sort(reverse=True)
        value_count = Counter()
        for c in self.cards:
            value_count[c.get_value()] += 1
        three_kind = [v[0] for v in value_count.items() if v[1] >= 3]
        remaining_cards = [v[0] for v in value_count.items() if v[1] == 1]
        self.rank = HandRank.get_one_pairs
        if three_kind:
            self.rank = HandRank.get_three_of_a_kind
            self.hand_cards = three_kind + remaining_cards[0:2]
            return three_kind

    def get_straight(self):
        """checks for straight in a set of cards.

        Returns the value of the highest card in the straight set if found, otherwise returns None"""
        self.cards.sort(reverse=True)
        self.rank = HandRank.get_three_of_a_kind
        vals = [c.get_value() for c in self.cards] + [1 for c in self.cards if c.get_value() == 14]
        for c in reversed(self.cards):
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k) not in vals:
                    found_straight = False
                    self.hand_cards = c.get_value()
                    break

            if found_straight:
                self.rank = HandRank.get_straight
                return c.get_value()

    def get_flush(self):
        """Checks whether the set of cards contain a flush(5 cards of same suit).

        Returns the value of flush suit if found, otherwise returns None"""
        self.cards.sort(reverse=True)
        suit_count = Counter()
        for c in self.cards:
            suit_count[c.suit] += 1
        flush_suit = [v[0] for v in suit_count.items() if v[1] >= 5]
        self.rank = HandRank.get_straight
        if flush_suit:
            self.rank = HandRank.get_flush
            return flush_suit

    def get_full_house(self):
        """Checks for full house in a set of cards.

        Returns the set of triplets and pairs if found, otherwise returns None"""
        self.cards.sort(reverse=True)
        value_count = Counter()
        self.rank = HandRank.get_flush
        for c in self.cards:
            value_count[c.get_value()] += 1
        threes = [v[0] for v in value_count.items() if v[1] >= 3]
        threes.sort()
        twos = [v[0] for v in value_count.items() if v[1] >= 2]
        twos.sort()
        self.hand_cards = threes + twos
        for three in reversed(threes):
            for two in reversed(twos):
                if two != three:
                    self.rank = HandRank.get_full_house
                    return three, two

    def get_four_of_a_kind(self):
        """checks for quadruplet of cards having same value from a set of cards

        Returns the value of the quadruplet if found, otherwise returns None"""
        self.cards.sort(reverse=True)
        value_count = Counter()
        self.rank = HandRank.get_full_house
        for c in self.cards:
            value_count[c.get_value()] += 1
        four_kind = [v[0] for v in value_count.items() if v[1] >= 4]
        remaining_cards = [v[0] for v in value_count.items() if v[1] == 1]
        # self.hand_cards =
        if four_kind:
            self.rank = HandRank.get_four_of_a_kind
            self.hand_cards = four_kind + remaining_cards[0:1]
            return four_kind

    def get_straight_flush(self):
        """
        Checks for the best straight flush in a list of cards (maybe more than just 5)

         :return: None if no straight flush is found, else the value of the top card.
        """
        self.cards.sort(reverse=True)
        self.rank = HandRank.get_four_of_a_kind
        vals = [(c.get_value(), c.suit) for c in self.cards] \
               + [(1, c.suit) for c in self.cards if c.get_value() == 14]  # Add the aces!
        for c in reversed(self.cards):  # Starting point (high card)
            found_straight = True
            for k in range(1, 5):
                if (c.get_value() - k, c.suit) not in vals:
                    found_straight = False
                    break
            if found_straight:
                self.rank = HandRank.get_straight_flush
                self.hand_cards = c.get_value()
                return c.get_value()

    def __eq__(self, other):
        """checks whether two poker hands are comparable"""
        self.cards.sort(reverse=True)
        other.cards.sort(reverse=True)
        return other.rank == self.rank

    def __lt__(self, other):
        """checks whether first poker hand(self) is less than the second(other)"""
        return (self.rank, self.hand_cards) < (other.rank, other.hand_cards)