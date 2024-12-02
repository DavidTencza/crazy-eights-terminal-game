import random
import time
import sys
import os


SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
CRAZY_EIGHT = '8'
LEADER_TAG = "LEADER"
SUIT_MAP = {
    'h': 'Hearts', 'hearts': 'Hearts', 'H': 'Hearts', 'Hearts': 'Hearts',
    'd': 'Diamonds', 'diamonds': 'Diamonds', 'D': 'Diamonds', 'Diamonds': 'Diamonds',
    'c': 'Clubs', 'clubs': 'Clubs', 'C': 'Clubs', 'Clubs': 'Clubs',
    's': 'Spades', 'spades': 'Spades', 'S': 'Spades', 'Spades': 'Spades'
}
NAMES_LIST = ['Alan', 'Barry', 'Chris', 'David', 'Edgar', 'Frank', 'George', 'Harry', 'Ivan', 
              'John', 'Ken', 'Leo', 'Martin', 'Nate', 'Oswald', 'Peter', 'Quinn', 'Randall', 
              'Steve', 'Tom', 'Umberto', 'Vince', 'Wally', 'Xavier', 'Yair', 'Zachary',
              'Anna', 'Betty', 'Carla', 'Donna', 'Eleanor', 'Francine', 'Gina', 'Helen',
              'Ingrid', 'Janet', 'Kelly', 'Linda', 'Mary', 'Nina', 'Olivia', 'Patty', 
              'Quintina', 'Rachel', 'Samantha', 'Tammy', 'Ursula', 'Virginia', 'Wanda',
              'Xiana', 'Yolanda', 'Zelda']


def assign_names():
    selected_names = random.sample(NAMES_LIST, 3)
    selected_names.insert(0, 'Player')
    return selected_names


def create_deck():
    return [f'{rank} of {suit}' for suit in SUITS for rank in RANKS]


def draw_card(deck):
    return deck.pop() if deck else None


def get_suit(card):
    return card.split(' of ')[1]


def get_rank(card):
    return card.split(' of ')[0]


def is_valid_play(card, top_card, chosen_suit):
    card_suit = get_suit(card)
    card_rank = get_rank(card)
    top_card_rank = get_rank(top_card)
    
    # When a suit has been chosen due to an 8, only allow cards that match the chosen suit or the rank of the top card
    if chosen_suit:
        return card_suit == chosen_suit or card_rank == top_card_rank
    else:
        return card_suit == get_suit(top_card) or card_rank == top_card_rank or card_rank == CRAZY_EIGHT


def display_hand(hand):
    return ', '.join(f'[{i+1}] {card}' for i, card in enumerate(hand))


def show_instructions():
    print("\nObjectives of Crazy Eights:")
    print("The goal of each round is to be the first player to discard all of your cards.")
    print("The goal of the game is to be the first player to reach the target score.")
    print("\nHow to Play:")
    print("1. Match the card on the center pile by either suit or rank.")
    print("2. If you play an 8, you can change the suit to any of your choosing.")
    print("3. If you can’t play, you draw a card from the deck.")
    print("4. The round ends when a player runs out of cards.")
    print("5. The winning player scores points from the cards held by the other players:")
    print("   * An Eight scores 50 points" )
    print("   * Tens, Jacks, Queens, and Kings score 10 points" )
    print("   * An Ace scores 1 point" )
    print("   * All other cards score points equal to their face values")
    print("6. Rounds continue until a player reaches the target number of points:")
    print("   * The target is 50 points times the number of players")
    print("\n   Enjoy the game!")
    print("   David Tencza, November 2024")
    input("\nPress Enter to return to the menu...")
    os.system('cls||clear')


def calculate_score(hand, i, names):
    score = 0
    print(f"{'Player (YOU)' if i == 0 else names[i]} was holding:")
    for card in hand:
        rank = get_rank(card)
        if rank == '8':
            score += 50
        elif rank in ['10', 'J', 'Q', 'K']:
            score += 10
        elif rank == 'A':
            score += 1
        else:
            score += int(rank)
        print(f'  * {card}')
    print(f'Totaling: {score} points')
    return score


def crazy_eights(num_players):
    deck = create_deck()
    random.shuffle(deck)
    names = assign_names()
    
    scores = [0] * num_players
    target_score = num_players * 50
    round_num = 0
    
    print(f"\nGet ready for Crazy Eights! There are {num_players} players.")
    print(f"The first player to reach {target_score} points wins the game. Good luck!\n")

    # Begin rounds which will keep going until someone reaches the target score
    while max(scores) < target_score:

        if round_num > 0:
            print(f"\n--- RESULTS AFTER ROUND {round_num} ---")
            leader_index = scores.index(max(scores))
            for i, score in enumerate(scores):
                status = LEADER_TAG if i == leader_index else ""
                print(f"{'Player (YOU)' if i == 0 else names[i]}: {score} points {status}")
            print(f"\nLeader needs {target_score - scores[leader_index]} more points to win. Target to win: {target_score} points.\n")
            time.sleep(.5)
            input("Press Enter to start the next round...")
            os.system('cls||clear')
        elif round_num == 0:
            input("Press Enter to start the first round...")
            os.system('cls||clear')

        deck = create_deck()
        random.shuffle(deck)
        
        hands = [[draw_card(deck) for _ in range(5)] for _ in range(num_players)]
        center_card = draw_card(deck)
        discard_pile = [center_card]
        player_turn = 0
        chosen_suit = None
        turn_cnt = 0
        
        round_winner = None
        while not round_winner:
            print(f"\nCenter Card: {center_card} {('(Chosen Suit is ' + chosen_suit + ')') if get_rank(center_card) == CRAZY_EIGHT and turn_cnt > 0 else ''}")

            # Show all players' card counts for the human player's turn
            if player_turn == 0:
                print(f"Player's hand ({len(hands[0])} cards): {display_hand(hands[0])}")
                print("\n".join([f"{names[i]} holds {len(hand)} card{'s' if len(hand) > 1 else ''}." for i, hand in enumerate(hands[1:], start=1)]))
            
            current_hand = hands[player_turn]
            valid_moves = [i for i, card in enumerate(current_hand)
                           if is_valid_play(card, center_card, chosen_suit)]
            
            if player_turn == 0:  # Human player's turn
                turn_cnt += 1
                if valid_moves:
                    move = None
                    while move not in valid_moves:
                        move = input(f"Choose a card to play {[(i+1) for i in valid_moves]} or type 'D' to draw: ") #LIVE, REMOVE FOR TESTING
                        #move = random.choice(valid_moves)  #TEST LINE FOR AUTOPLAY
                        if move.upper() == 'D': #REMOVE if block FOR TESTING TO AVOID ATTRIBUTE ERROR
                            move = 'D'
                            break
                        try:
                            move = int(move) - 1
                        except ValueError:
                            print("Invalid input. Enter a valid number or 'D' to draw.")
                            move = None
                    
                    if move == 'D':
                        input("Press Enter to draw a card.")
                        new_card = draw_card(deck)
                        current_hand.append(new_card)
                        print("You drew:", new_card)

                    else:
                        chosen_card = current_hand.pop(move)
                        print("You played:", chosen_card)
                        center_card = chosen_card
                        discard_pile.append(center_card)
                        time.sleep(1)
                        
                        if get_rank(center_card) == CRAZY_EIGHT:
                            chosen_suit = None
                            while chosen_suit not in SUITS:
                                user_input = input("Choose a new suit ([H]earts, [D]iamonds, [C]lubs, [S]pades): ").strip() #LIVE
                                #chosen_suit = random.choice(SUITS) #TEST
                                chosen_suit = SUIT_MAP.get(user_input.capitalize(), None) #LIVE
                else:
                    input("No valid moves. Press Enter to draw a card.") #REMOVE FOR TESTING SO IT JUST DRAWS
                    new_card = draw_card(deck)
                    current_hand.append(new_card)
                    print("You drew:", new_card)
            
            else:  # Computer turns
                turn_cnt += 1
                print(f"\n{names[player_turn]}'s turn...")
                time.sleep(1)
                if valid_moves:
                    move = random.choice(valid_moves)
                    chosen_card = current_hand.pop(move)
                    print(f"{names[player_turn]} played:", chosen_card)
                    center_card = chosen_card
                    discard_pile.append(center_card)
                    time.sleep(1)
                    
                    if get_rank(center_card) == CRAZY_EIGHT:
                        chosen_suit = random.choice(SUITS)
                        print(f"{names[player_turn]} changed suit to:", chosen_suit)
                    else:
                        chosen_suit = None
                else:
                    print(f"{names[player_turn]} has no valid moves and draws a card.")
                    time.sleep(1)
                    new_card = draw_card(deck)
                    current_hand.append(new_card)
            
            if not current_hand:
                round_winner = player_turn
                break

            # If deck runs out, reshuffle the discard pile minus the top center card
            if not deck:
                print("**SHUFFLING DECK**")
                deck = discard_pile[:-1]
                discard_pile = [center_card]
                random.shuffle(deck)
                
            player_turn = (player_turn + 1) % num_players

        # Show scoring and declare the round winner 
        print("\nSCORING")
        round_score = sum(calculate_score(hand, i, names) for i, hand in enumerate(hands) if i != round_winner)
        scores[round_winner] += round_score
        print(f"**{'Player (YOU)' if round_winner == 0 else names[round_winner]} wins the round and earns {round_score} points!**")
        round_num += 1
        turn_cnt = 0
    
    # Declare the winner of the game!
    winner = scores.index(max(scores))
    print(f"\n***{'Player (YOU)' if winner == 0 else names[winner]} wins the game with {scores[winner]} points!***\n")
    input("Hit Enter to return to the Main Menu!")
    main()


def main():
    ascii_banner = r'   ____ ____      _     _______   __  _____ ___ ____ _   _ _____ ____  ' + '\n' + \
                   r'  / ___|  _ \    / \   |__  /\ \ / / | ____|_ _/ ___| | | |_   _/ ___| ' + '\n' + \
                   r' | |   | |_) |  / _ \    / /  \ V /  |  _|  | | |  _| |_| | | | \___ \ ' + '\n' + \
                   r' | |___|  _ <  / ___ \  / /_   | |   | |___ | | |_| |  _  | | |  ___) |' + '\n' + \
                   r'  \____|_| \_\/_/   \_\/____|  |_|   |_____|___\____|_| |_| |_| |____/ ' + '\n\n'
    print(ascii_banner)
    while True:
        print("Menu:")
        print("1) Play Crazy Eights")
        print("2) Show Instructions")
        print("3) Quit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            num_players = 0
            while num_players < 2 or num_players > 4:
                try:
                    num_players = int(input("Enter the number of players (2-4): "))
                    if num_players < 2 or num_players > 4:
                        print("Please enter a number between 2 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            crazy_eights(num_players)
        elif choice == '2':
            os.system('cls||clear')
            show_instructions()
        elif choice == '3':
            sys.exit("Thanks for playing Crazy Eights! Goodbye!")
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
