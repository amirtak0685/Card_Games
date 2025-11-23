import random

def riffle_shuffle(deck):
    import random

    # Cut roughly in half
    cut = random.randint(len(deck)//3, 2*len(deck)//3)
    left = deck[:cut]
    right = deck[cut:]

    shuffled = []
    while left or right:
        # Randomly drop 1–3 cards from either side
        if left and (not right or random.random() < 0.5):
            take = random.randint(1, 3)
            shuffled.extend(left[:take])
            left = left[take:]
        else:
            take = random.randint(1, 3)
            shuffled.extend(right[:take])
            right = right[take:]
    return shuffled

# ======== SETUP ========

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
rank_values = {r: i for i, r in enumerate(ranks, start=2)}

# Make and shuffle the deck
deck = [(rank, suit) for suit in suits for rank in ranks]
deck = riffle_shuffle(deck)

# Deal cards
player_hand = deck[:3]
computer_hand = deck[3:6]

player_face_down = deck[6:9]
computer_face_down = deck[9:12]

player_face_up = deck[12:15]
computer_face_up = deck[15:18]

draw_pile = deck[18:]
discard_pile = []

# ======== HELPER FUNCTIONS ========

def refill_hand(hand):
    while len(hand) < 3 and draw_pile:
        hand.append(draw_pile.pop(0))

def effective_top_card():
    """Return the top non-3 card, or None if pile empty/only 3s."""
    for card in reversed(discard_pile):
        if card[0] != '3':
            return card
    return None

def can_play(card, top_card):
    """
    Return True if `card` is legal to play given the effective top_card.
    Rules implemented:
      - '2' and '10' always playable (reset / burn)
      - '3' always playable (mirrors / shadows the below card)
      - If no effective top_card -> anything goes
      - If effective top is '7' -> must play <= 7 (unless card is 2/10/3)
      - Otherwise must play >= effective top rank
    """
    rank = card[0]

    # 2, 10, and 3 can always be played
    if rank in ('2', '10', '3'):
        return True

    # No effective top card → anything goes
    if not top_card:
        return True

    top_rank = top_card[0]

    # 7 rule → must play ≤ 7 (except special 2/10/3 already handled)
    if top_rank == '7':
        return rank_values[rank] <= rank_values['7']

    # Normal rule → must be >= effective top rank
    return rank_values[rank] >= rank_values[top_rank]

def play_card(from_zone, card):
    """Place card onto discard pile and remove from its zone if provided."""
    discard_pile.append(card)
    if from_zone is not None:
        if card in from_zone:
            from_zone.remove(card)
    print(f"Played {card[0]} of {card[1]}")

def burn_pile():
    global discard_pile
    print("🔥 BURN! Pile cleared!")
    discard_pile = []

def top_card():
    return effective_top_card()

def player_phase():
    if player_hand:
        return "hand"
    if player_face_up:
        return "face_up"
    return "face_down"

def computer_phase():
    if computer_hand:
        return "hand"
    if computer_face_up:
        return "face_up"
    return "face_down"

def get_valid_index_input(prompt, max_index):
    """
    Keep asking until the user provides a valid integer index between 0 and max_index inclusive.
    Returns the integer index.
    """
    while True:
        raw = input(prompt).strip()
        if raw.lower() in ('q', 'quit', 'exit'):
            print("Quitting game.")
            exit()
        if not raw.isdigit():
            print("Please enter a number corresponding to the choice.")
            continue
        idx = int(raw)
        if 0 <= idx <= max_index:
            return idx
        print(f"Please enter a number between 0 and {max_index}.")

# ======== PLAYER TURN ========

def player_turn():
    phase = player_phase()
    print("\n===== YOUR TURN =====")
    print(f"Phase: {phase}")
    print(f"Top of pile: {top_card()}")
    print(f"Your hand: {player_hand}")
    print(f"Face-up: {player_face_up}")
    print(f"Face-down: {['??'] * len(player_face_down)}")

    # ----- FACE-DOWN PHASE -----
    if phase == "face_down":
        print("You must play a face-down card blindly...")
        chosen = random.choice(player_face_down)
        player_face_down.remove(chosen)

        print(f"You flip: {chosen[0]} of {chosen[1]}")

        if can_play(chosen, top_card()):
            play_card(None, chosen)
            if chosen[0] == '10':
                burn_pile()
        else:
            print("Not playable → You pick up the entire pile.")
            player_hand.extend(discard_pile)
            discard_pile.clear()
            player_hand.append(chosen)
            refill_hand(player_hand)
        return

    # ----- FACE-UP PHASE -----
    if phase == "face_up":
        print("Playing from face-up cards")
        playable = [c for c in player_face_up if can_play(c, top_card())]

        if not playable:
            print("No playable face-up cards → pick up pile.")
            player_hand.extend(discard_pile)
            discard_pile.clear()
            player_hand.extend(player_face_up)
            player_face_up.clear()
            refill_hand(player_hand)
            return

        # Show playable with stable indices (0..n-1)
        for i, c in enumerate(playable):
            print(f"{i}: {c}")

        idx = get_valid_index_input(f"Choose card number (0-{len(playable)-1}): ", len(playable)-1)
        chosen = playable[idx]

        play_card(player_face_up, chosen)
        if chosen[0] == '10':
            burn_pile()
        elif chosen[0] == '2':
            print("Pile reset!")

        refill_hand(player_hand)
        return

    # ----- NORMAL HAND PHASE -----
    playable = [c for c in player_hand if can_play(c, top_card())]

    if not playable:
        print("No playable cards → pick up pile.")
        player_hand.extend(discard_pile)
        discard_pile.clear()
        refill_hand(player_hand)
        return

    # Show playable options
    for i, c in enumerate(playable):
        print(f"{i}: {c}")

    idx = get_valid_index_input(f"Choose card (0-{len(playable)-1}): ", len(playable)-1)
    chosen = playable[idx]
    play_card(player_hand, chosen)

    if chosen[0] == '10':
        burn_pile()
    elif chosen[0] == '2':
        print("Pile reset!")

    refill_hand(player_hand)

# ======== COMPUTER TURN ========

def computer_turn():
    phase = computer_phase()
    print("\n===== COMPUTER TURN =====")
    print(f"Computer phase: {phase}")
    print(f"Top of pile: {top_card()}")

    # ----- FACE-DOWN -----
    if phase == "face_down":
        chosen = random.choice(computer_face_down)
        computer_face_down.remove(chosen)
        print(f"Computer flips: {chosen[0]} of {chosen[1]}")

        if can_play(chosen, top_card()):
            play_card(None, chosen)
            if chosen[0] == '10':
                burn_pile()
        else:
            print("Computer fails → picks up pile.")
            computer_hand.extend(discard_pile)
            discard_pile.clear()
            computer_hand.append(chosen)
            refill_hand(computer_hand)
        return

    # ----- FACE-UP -----
    if phase == "face_up":
        playable = [c for c in computer_face_up if can_play(c, top_card())]

        if not playable:
            print("Computer picks up pile.")
            computer_hand.extend(discard_pile)
            discard_pile.clear()
            computer_hand.extend(computer_face_up)
            computer_face_up.clear()
            refill_hand(computer_hand)
            return

        chosen = random.choice(playable)
        print(f"Computer plays {chosen}")

        play_card(computer_face_up, chosen)
        if chosen[0] == '10':
            burn_pile()
        elif chosen[0] == '2':
            print("Pile reset!")

        refill_hand(computer_hand)
        return

    # ----- NORMAL HAND -----
    playable = [c for c in computer_hand if can_play(c, top_card())]

    if not playable:
        print("Computer picks up pile.")
        computer_hand.extend(discard_pile)
        discard_pile.clear()
        refill_hand(computer_hand)
        return

    chosen = random.choice(playable)
    print(f"Computer plays {chosen}")

    play_card(computer_hand, chosen)

    if chosen[0] == '10':
        burn_pile()
    elif chosen[0] == '2':
        print("Pile reset!")

    refill_hand(computer_hand)

# ======== MAIN GAME LOOP ========

while True:
    # Win conditions
    if not player_hand and not player_face_up and not player_face_down:
        print("\n🎉 YOU WIN!")
        break

    if not computer_hand and not computer_face_up and not computer_face_down:
        print("\n💀 COMPUTER WINS!")
        break

    player_turn()
    if not player_hand and not player_face_up and not player_face_down:
        print("\n🎉 YOU WIN!")
        break

    computer_turn()