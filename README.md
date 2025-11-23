# 🏰 Palace — Python Terminal Card Game

This project is a full implementation of the card game Palace written entirely in Python.
It includes full game rules, card logic, a computer opponent, hand management, and custom shuffle mechanisms.

The game runs in any terminal and requires no external libraries.

## 📦 Features

- ✔️ Complete Palace Rules

This implementation supports all standard Palace mechanics:
	•	3 → Shadows the card below (always playable)
	•	7 → Must play 7 or lower
	•	2 → Resets the pile (anything can follow)
	•	10 → Burns the entire pile
	•	Normal rule: Must play equal or higher than the effective top card
	•	Face-down cards are played randomly and blindly
	•	Always maintain at least 3 cards in hand (while draw pile exists)
	•	Effective top card ignores 3s stacked on top

- ✔️ Turn Phases

Each player must clear their cards in order:
	1.	Hand cards
	2.	Face-up cards
	3.	Face-down cards

Face-down cards are a gamble — if the flipped card is illegal, the player must pick up the entire pile.

⸻

- ✔️ Custom Shuffle

The deck can be shuffled using:
	•	Fisher–Yates (perfect randomness)
	•	Riffle shuffle (human-style imperfect shuffle)

⸻

- ✔️ Computer Opponent

The built-in CPU:
	•	Follows the same rules as the player
	•	Chooses randomly from its valid plays
	•	Plays blind from face-down cards

Simple, fair, and challenging enough for casual play.

⸻

# 🚀 Getting Started

- Requirements
	•	Python 3.8+

- Installation
git clone https://github.com/amirtak0685/Card_Games.git
cd Card_Games

- Running the Game
python3 palace.py

# 🧠 Game Structure

- Deck Representation

Cards are stored as tuples:
("Rank", "Suit")
# Example: ("Ace", "Spades")
The deck is built with a list comprehension and then manually shuffled.

- Core Logic

- Valid Moves
All card-play logic is handled by:
can_play(card, effective_top_card)

This accounts for:
	•	Shadowing 3s
	•	The 7-or-lower rule
	•	Special cards (2 and 10)
	•	Normal rank-comparison rules

Effective Top Card
If multiple 3s are stacked on the pile, the game finds the first non-3 card below them to determine legality.

⸻

- Turn Flow

Both player and computer follow the same progression:
Hand → Face-Up → Face-Down → Win
Each phase must be completely emptied before moving to the next.

# 🏆 Winning

A player wins upon having:
0 hand cards  
0 face-up cards  
0 face-down cards  

If the opponent reaches this first, the game ends with their victory.

⸻

# 🔧 Future Enhancements

Possible extensions:
	•	More advanced CPU logic
	•	Four-of-a-kind auto-burn rule
	•	Ability to play multiple cards of the same value simultaneously
	•	Multiplayer mode
	•	GUI using Tkinter, PyGame, or web front-end
	•	Game history and logging

⸻

# 📄 License

This project is released under the MIT License.
Use, modify, and distribute freely.