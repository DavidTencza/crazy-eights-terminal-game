import pytest
from project import get_suit, get_rank, draw_card, display_hand, is_valid_play, calculate_score


def test_get_suit():
    assert get_suit("2 of Hearts") == "Hearts"
    assert get_suit("Q of Spades") == "Spades"
    assert get_suit("8 of Clubs") == "Clubs"
    assert get_suit("10 of Diamonds") == "Diamonds"


def test_get_rank():
    assert get_rank("2 of Hearts") == "2"
    assert get_rank("Q of Spades") == "Q"
    assert get_rank("8 of Clubs") == "8"
    assert get_rank("10 of Diamonds") == "10"


def test_draw_card():
    assert draw_card(["2 of Hearts", "3 of Hearts", "4 of Hearts", "5 of Hearts"]) == "5 of Hearts"
    assert draw_card(["7 of Clubs", "J of Diamonds", "6 of Hearts", "9 of Spades"]) == "9 of Spades"
    assert draw_card([]) == None


def test_display_hand():
    assert display_hand(["7 of Clubs", "J of Diamonds", "6 of Hearts", "9 of Spades", "K of Clubs"]) == "[1] 7 of Clubs, [2] J of Diamonds, [3] 6 of Hearts, [4] 9 of Spades, [5] K of Clubs"
    assert display_hand(["9 of Diamonds", "8 of Hearts"]) == "[1] 9 of Diamonds, [2] 8 of Hearts"
    assert display_hand(["A of Hearts"]) == "[1] A of Hearts"
    assert display_hand([]) == ""


def test_is_valid_play():
    assert is_valid_play("2 of Hearts", "7 of Hearts", None) == True
    assert is_valid_play("K of Clubs", "K of Diamonds", None) == True
    assert is_valid_play("6 of Spades", "9 of Clubs", None) == False
    assert is_valid_play("J of Hearts", "Q of Hearts", None) == True
    assert is_valid_play("8 of Diamonds", "K of Spades", None) == True
    assert is_valid_play("5 of Clubs", "8 of Hearts", "Spades") == False
    assert is_valid_play("5 of Clubs", "8 of Hearts", "Clubs") == True
    assert is_valid_play("8 of Spades", "8 of Clubs", "Diamonds") == True
    assert is_valid_play("8 of Clubs", "8 of Diamonds", "Clubs") == True


def test_calculate_score():
    assert calculate_score(["7 of Clubs", "J of Diamonds", "6 of Hearts", "9 of Spades", "K of Clubs"], 0, ["Player", "Alan"]) == 42
    assert calculate_score(["9 of Diamonds", "8 of Hearts"], 1, ["Player", "Barry"]) == 59
    assert calculate_score(["A of Hearts"], 2, ["Player", "Tom", "Tammy"]) == 1
    assert calculate_score(["2 of Hearts", "3 of Hearts", "4 of Hearts", "5 of Hearts"], 3, ["Player", "Rachel", "Nate", "David"]) == 14
    assert calculate_score(["7 of Clubs", "J of Diamonds", "6 of Hearts", "9 of Spades"], 0, ["Player", "Olivia"]) == 32
