# Crazy Eights Terminal Game
#### Video Demo: 
_(https://www.youtube.com/watch?v=ZXs4DBgHtkU)_
#### Description: 
_A Python-based implementation of the classic card game Crazy Eights, playable directly in the terminal. Players compete to reach a target score by playing cards in a turn-based system that follows the rules of Crazy Eights. The game supports two to four players, with one human player and up to three computer-controlled opponents._

## Table of Contents
- [Game Objectives](#game-objectives)
- [Features](#features)
- [Design Choices](#design-choices)
- [Developer](#developer)
- [Special Thanks](#special-thanks)
- [Updates](#updates)

## Game Objectives
The main objective in Crazy Eights is to be the first player to discard all cards in your hand during each round. Players score points based on the remaining cards in opponents' hands. The first player to reach a score threshold, determined by the number of players, wins the game.

### How to Play:
1. **Matching Cards**: Players can play cards that match the center pile's top card by either rank or suit.
2. **Special Card (Crazy 8)**: Playing an "8" allows the player to change the suit, introducing a new suit requirement for the next player.
3. **Drawing a Card**: If a player cannot match the suit or rank, they must draw a card.
4. **Scoring**: When a player empties their hand, they score points from the values of other players' cards:
   - **8**: 50 points
   - **10, J, Q, K**: 10 points each
   - **Ace**: 1 point
   - **Other cards**: face value

### Win Condition:
The game continues for multiple rounds until a player reaches the target score (50 points times the number of players).

## Features
- **Interactive Terminal UI**: A simple text-based menu to start the game, display instructions, or exit.
- **Multiplayer Support**: Choose from 2 to 4 players (one human and up to 3 computer-controlled opponents).
- **Automated Opponents**: Computer players make moves based on available card options and game rules.
- **Score Tracking**: Each round concludes with scoring based on opponents' remaining cards, displayed for all players.
- **Instructions**: A built-in tutorial from the main menu to explain the rules and objectives of Crazy Eights.

## Design Choices
- **Chosen Suit**: It got tiring typing the whole suit name (Hearts, Diamonds, Clubs, or Spades) when playing an 8 card and choosing a suit, so a dictionary constant (SUIT_MAP) was introduced:

   ```
   SUIT_MAP = {
      'h': 'Hearts', 'hearts': 'Hearts', 'H': 'Hearts', 'Hearts': 'Hearts',
      'd': 'Diamonds', 'diamonds': 'Diamonds', 'D': 'Diamonds', 'Diamonds': 'Diamonds',
      'c': 'Clubs', 'clubs': 'Clubs', 'C': 'Clubs', 'Clubs': 'Clubs',
      's': 'Spades', 'spades': 'Spades', 'S': 'Spades', 'Spades': 'Spades'
   }
   ```

   The suit map allows the user to type just "h" or "H" to select the Hearts suit, for example, making suit entry more convenient. If the player is driven enough to still type the whole suit name, but not quite driven enough to capitalize the first letter, this covers that, too!

- **Scoring Breakdown**: While it worked to have the _calculate_score()_ function just return the total number of points contributed by all of the losing players in each round, it was more interesting to instead have this function called multiple times from a for loop for each of the non-winning players' hands and show the cards each of them were holding when the round ended, as well as the score contributed from each of these players towards the total points awarded to the round's winner.

- **Chosen Suit Display**: Sometimes, after an 8 card is played, it may take multiple players' turns before someone has a card of the chosen suit to play. To avoid the player having to remember the chosen suit or scroll and read further back in this case, a feature was added to show the chosen suit with the Center Card display message with the center card is an 8:

   ```
   f"\nCenter Card: {center_card} {('(Chosen Suit is ' + chosen_suit + ')') if get_rank(center_card) == CRAZY_EIGHT else ''}"
   ```

- **Hand Counter**: After some testing, I discovered the good idea for the Chosen Suit Display enhancement had introduced a bug. When the first center card of the round was an 8, no suit has been chosen for it because none of the players played this card. With the chosen suit having a value of None, this couldn't be concatenated into the string. This _could_ have been resolved by making the chosen_suit's initial value a default string such as "Not Chosen", but this would have also caused me to edit the _is_valid_play()_ function since that is depending on the chosen_suit being None. Instead, I opted to keep a counter of the turns taken during the round. The player doesn't see this turn counter value, but incorporating this turn counter value into the Center Card's Chosen Suit display logic takes care of the issue: 

   ```
   f"\nCenter Card: {center_card} {('(Chosen Suit is ' + chosen_suit + ')') if get_rank(center_card) == CRAZY_EIGHT and turn_cnt > 0 else ''}"
   ```

- **Mid-Round Shuffling**: Many rounds end without exhausting the entire deck, but when that does happen, it was a small nice touch to inform the player that the deck is being shuffled with the ***SHUFFLING DECK*** notification, rather than handling this silently.

## Developer
Developed by David Tencza, November 2024.

## Special Thanks
To David J. Malan and Harvard University for making this course available for everyone. The lectures and exercises were enjoyable and educational! 

## Updates
_12-01-2024_
- **Named Computer Opponents**: Rather than having "Computer 1", "Computer 2", "Computer 3" to refer to the opponents, instead have three names randomly selected from a list of 52 names.
- **Bug fix: Multiple 8 cards for player in round**: Testing revealed that when the player used more than one Crazy 8 card within a round, the chosen suit was still set to the suit chosen from the first played Crazy 8 card, resulting in the player not getting to make a suit choice. Fixed by immediately setting the chosen suit to None when the player uses a Crazy 8 card. 

_12-02-2024_
- **Refreshes of Named Computer Opponents**: When more than one game is played during a session, refresh the names instead of retaining the first set of names selected.

_12-08-2024_
- **Computer Opponents have smarter suit selection**: Computer opponents now randomly select a suit based on a list of the suits of the cards held in hand, instead of randomly selecting any suit.
