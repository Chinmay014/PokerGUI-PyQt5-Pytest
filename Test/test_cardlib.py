from enum import Enum
import pytest

from cardlib import *


# This test check suit class "Suit" and the suits "Hearts, "Spades", "Clubs" and "Diamonds"
def test_cards():
    # test for each type of card and how they output
    print("\n")
    h5 = NumberedCard(4, Suit.Hearts)
    assert isinstance(h5.suit, Enum)
    print(h5)

    anAce = AceCard(Suit.Hearts)
    assert anAce.get_value() == 14
    assert isinstance(anAce, PlayingCard)
    print(anAce)

    sk = KingCard(Suit.Spades)
    assert sk.get_value() == 13
    assert isinstance(anAce, PlayingCard)
    print(sk)

    Aqueen = QueenCard(Suit.Clubs)
    assert Aqueen.get_value() == 12
    assert isinstance(anAce, PlayingCard)
    print(Aqueen)

    Ajack = JackCard(Suit.Diamonds)
    assert Ajack.get_value() == 11
    assert isinstance(anAce, PlayingCard)
    print(Ajack)

    # test for comparing two cards, the __lt__ and __eq__ methods
    assert h5 < sk
    assert sk < anAce
    assert Ajack < Aqueen
    assert Aqueen < sk
    assert h5 == h5

    # What is this test for?
    with pytest.raises(TypeError):
        pc = PlayingCard(Suit.Clubs)


# This test checks the shuffle method:"shuffle" and the method to draw a card:"draw"
def test_deck():
    d = StandardDeck()
    assert len(d.cards) == 52
    c1 = d.draw()
    c2 = d.draw()
    assert not c1 == c2

    d2 = StandardDeck()
    d2.shuffle()
    assert len(d2.cards) == 52
    c3 = d2.draw()
    c4 = d2.draw()
    assert not ((c3, c4) == (c1, c2))


# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
def test_hand():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    assert len(h.cards) == 5

    h.sort()
    for i in range(4):
        assert h.cards[i] < h.cards[i + 1] or h.cards[i] == h.cards[i + 1]

    cards = h.cards.copy()
    h.drop_cards([3, 0, 1])
    assert len(h.cards) == 2
    assert h.cards[0] == cards[2]
    assert h.cards[1] == cards[4]


# # This test builds on the assumptions above. Add your type and data for the commented out tests
# # and uncomment them!
def test_pokerhands():
    # Case1: two players in game. they get no poker hands and the winner is decided by highest card held

    print("\nCase 1 start")
    h1 = Hand()
    h1.add_card(QueenCard(Suit.Diamonds))
    h1.add_card(KingCard(Suit.Hearts))

    h2 = Hand()
    h2.add_card(QueenCard(Suit.Hearts))
    h2.add_card(AceCard(Suit.Hearts))

    cl = [NumberedCard(10, Suit.Diamonds), NumberedCard(9, Suit.Diamonds),
          NumberedCard(8, Suit.Clubs), NumberedCard(6, Suit.Spades)]

    print("Player1:")
    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    assert isinstance(ph1.rank, Enum)
    print("Player2:")
    ph2 = h2.best_poker_hand(cl)
    # assert ph1.rank == HandRank.get_highest_card
    # assert ph1.rank == HandRank.get_highest_card

    assert ph1 < ph2
    print("Player 2 wins!")
    print("Case 1 end")

    # Case2: two players in game. Both players get a pair, and similar rest of the cards. The game ties.
    print("Case 2 start")
    h1 = Hand()
    h1.add_card(KingCard(Suit.Diamonds))
    h1.add_card(NumberedCard(4, Suit.Clubs))

    h2 = Hand()
    h2.add_card(KingCard(Suit.Hearts))
    h2.add_card(NumberedCard(4, Suit.Hearts))

    cl = [NumberedCard(10, Suit.Diamonds), NumberedCard(9, Suit.Diamonds),
          KingCard(Suit.Clubs), QueenCard(Suit.Spades)]

    print("Player1:")
    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    assert isinstance(ph1.rank, Enum)
    print("Player2:")
    ph2 = h2.best_poker_hand(cl)
    assert ph1.rank == HandRank.get_one_pairs
    assert ph1.rank == HandRank.get_one_pairs

    assert ph1 == ph2
    print("Its a tie!")
    print("Case 2 end")

    # Case3: two players in game. One player gets a flush and Player2 gets two pairs. Player 1 wins.
    print("Case 3 start")
    h1 = Hand()
    h1.add_card(JackCard(Suit.Diamonds))
    h1.add_card(NumberedCard(4, Suit.Diamonds))

    h2 = Hand()
    h2.add_card(QueenCard(Suit.Hearts))
    h2.add_card(NumberedCard(5, Suit.Diamonds))

    cl = [NumberedCard(10, Suit.Diamonds), NumberedCard(9, Suit.Diamonds),
          NumberedCard(5, Suit.Clubs), QueenCard(Suit.Diamonds)]

    print("Player1:")
    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    assert isinstance(ph1.rank, Enum)
    print("Player2:")
    ph2 = h2.best_poker_hand(cl)
    assert ph1.rank == HandRank.get_flush
    assert ph2.rank == HandRank.get_two_pairs

    assert ph2 < ph1
    print("Player 1 wins!")
    print("Case 3 end")

    # Case4: two players in game. One player gets a full house and Player2 gets four of a kind. Player 2 wins.
    print("Case 4 start")
    h1 = Hand()
    h1.add_card(JackCard(Suit.Diamonds))
    h1.add_card(NumberedCard(4, Suit.Diamonds))

    h2 = Hand()
    h2.add_card(NumberedCard(5, Suit.Hearts))
    h2.add_card(QueenCard(Suit.Clubs))

    cl = [NumberedCard(5, Suit.Spades), NumberedCard(5, Suit.Diamonds),
          NumberedCard(5, Suit.Clubs), JackCard(Suit.Diamonds), NumberedCard(6, Suit.Spades)]

    print("Player1:")
    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    assert isinstance(ph1.rank, Enum)
    print("Player2:")
    ph2 = h2.best_poker_hand(cl)
    assert ph1.rank == HandRank.get_full_house
    assert ph2.rank == HandRank.get_four_of_a_kind

    assert ph1 < ph2
    print("Player 2 wins!")
    print("Case 4 end")

    # Case5: two players in game. One player gets a full house and Player2 gets straight. Player 1 wins.
    print("Case 5 start")
    h1 = Hand()
    h1.add_card(JackCard(Suit.Diamonds))
    h1.add_card(NumberedCard(5, Suit.Diamonds))

    h2 = Hand()
    h2.add_card(NumberedCard(8, Suit.Hearts))
    h2.add_card(QueenCard(Suit.Clubs))

    cl = [NumberedCard(9, Suit.Spades), NumberedCard(9, Suit.Diamonds),
          NumberedCard(9, Suit.Clubs), JackCard(Suit.Diamonds), NumberedCard(10, Suit.Spades)]

    print("Player1:")
    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    assert isinstance(ph1.rank, Enum)
    print("Player2:")
    ph2 = h2.best_poker_hand(cl)
    assert ph1.rank == HandRank.get_full_house
    assert ph2.rank == HandRank.get_straight

    assert ph2 < ph1
    print("Player 1 wins!")
    print("Case 5 end")

    # Case5: two players in game. Both players get straight. The game is tied.
    print("Case 6 start")
    h1 = Hand()
    h1.add_card(NumberedCard(8, Suit.Clubs))
    h1.add_card(KingCard(Suit.Diamonds))

    h2 = Hand()
    h2.add_card(JackCard(Suit.Hearts))
    h2.add_card(KingCard(Suit.Clubs))

    cl = [NumberedCard(9, Suit.Spades), NumberedCard(9, Suit.Diamonds),
          NumberedCard(10, Suit.Clubs), JackCard(Suit.Diamonds), QueenCard(Suit.Spades)]

    print("Player1:")
    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    assert isinstance(ph1.rank, Enum)
    print("Player2:")
    ph2 = h2.best_poker_hand(cl)
    assert ph1.rank == HandRank.get_straight
    assert ph2.rank == HandRank.get_straight

    assert ph1 == ph2
    print("it's a draw!")
    print("Case 6 end")


def test_poker():
    """simulates a poker game.
    both players get random 2 cards and the cards on the table are also drawn from randomly shuffled deck"""
    print("\n")
    newdeck = StandardDeck()
    newdeck.shuffle()
    # player 1
    p1 = Hand()
    assert len(p1.cards) == 0
    p1.add_card(newdeck.draw())
    p1.add_card(newdeck.draw())
    print("For player 1, The first {} and second {}(known only to the player)".format(p1.cards[0], p1.cards[1]))

    # player 2
    p2 = Hand()
    p2.add_card(newdeck.draw())
    p2.add_card(newdeck.draw())
    print("For player 2, The first {} and second {}(known only to the player)".format(p2.cards[0], p2.cards[1]))

    # the table. Let us just draw 5 cards in one go for now
    table = Hand()
    table.add_card(newdeck.draw())
    table.add_card(newdeck.draw())
    table.add_card(newdeck.draw())
    table.add_card(newdeck.draw())
    table.add_card(newdeck.draw())
    print("\nCards on the table")
    for card in table.cards:
        print(card)

    # now both players show their best poker hand
    print("Player1:")
    ph1 = p1.best_poker_hand(table.cards)
    assert isinstance(ph1, PokerHand)
    assert isinstance(ph1.rank, Enum)
    print("Player2:")
    ph2 = p2.best_poker_hand(table.cards)
    # assert ph1.rank == HandRank.get_straight
    # assert ph2.rank == HandRank.get_straight
    if ph1 < ph2:
        print("Player 2 wins!")
    if ph2 < ph1:
        print("Player 1 wins!")

