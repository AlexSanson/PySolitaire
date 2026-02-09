"""Code from: https://github.com/naivoder/ascii_cards"""
from random import shuffle
import io
import sys

# Lots of modifications made from the original code
def card(rank, suit, color, stacked="f", reduced_stack="f"):
    """
    Prints an ASCII representation of a single playing card.

    Args:
        rank (str): The rank of the card ('n', '2'-'10', 'J', 'Q', 'K', 'A').
        suit (str): The suit of the card ('s', 'h', 'd', 'c', 'n').
        color (str): The color of the card ('r' for red, 'b' for black, 'n' for none).
        stacked (str): Whether the card is stacked ('t' for true, 'f' for false).
        reduced_stack (str): Whether the card stack is reduced ('t' for true, 'f' for false).
    """

    # Convert suit letters to symbols
    suit_map = {'s': '♠',
                'h': '♥',
                'd': '♦',
                'c': '♣',
                'n': ' '}
    suit = suit_map.get(suit.lower(), suit)

    w = "\033[47m\033[30m"
    r = "\033[47m\033[31m"
    clr = "\033[0m"

    top = f"{w}┌─────────┐{clr}"
    bottom = f"{w}└─────────┘{clr}"
    side = f"{w}│         │{clr}" # 9 spaces
    if rank == "10":  # Ten is the only rank with two digits
        rank_right = rank
        rank_left = rank
    else:
        rank_right = rank + " "
        rank_left = " " + rank
    

    if stacked == "f":
        stacked = False
    elif stacked == "t":
        stacked = True
    else:
        raise ValueError("Invalid value for stacked. Use 't' for true or 'f' for false.")

    if reduced_stack == "f":
        reduced_stack = False
    elif reduced_stack == "t":
        reduced_stack = True
    else:
        raise ValueError("Invalid value for reduced_stack. Use 't' for true or 'f' for false.")

    if color == "r":
        suit_left_red = f"{w}│{r} {suit}       {w}│{clr}"
        suit_right_red = f"{w}│{r}       {suit} {w}│{clr}"
        rank_left_red = f"{w}│{r}{rank_left}       {w}│{clr}"
        rank_right_red = f"{w}│{r}       {rank_right}{w}│{clr}"

        print(top)
        print(rank_left_red)
        print(suit_left_red)
        if not stacked:
            print(side)
            print(suit_right_red)
            print(rank_right_red)
            print(bottom)
    elif color == "b":
        suit_left_black = f"{w}│ {suit}       │{clr}"
        suit_right_black = f"{w}│       {suit} │{clr}"
        rank_left_black = f"{w}│{rank_left}       │{clr}"
        rank_right_black = f"{w}│       {rank_right}│{clr}"

        print(top)
        print(rank_left_black)
        print(suit_left_black)
        if not stacked:
            print(side)
            print(suit_right_black)
            print(rank_right_black)
            print(bottom)
    elif color == "n":
        blank = f"{w}│ {r}♥{w} ♠ {r}♦{w} ♣ │{clr}"
        blank_alt = f"{w}│ ♣ {r}♦{w} ♠ {r}♥{w} │{clr}"
        print(top)
        print(blank)
        if not reduced_stack:
            print(blank_alt)
        if not stacked:
            print(blank)
            print(blank_alt)
            print(blank)
            print(bottom)
    elif color == "nil":
        top_nil = f"┌ ─ ─ ─ ─ ┐"
        bottom_nil = f"└ ─ ─ ─ ─ ┘"
        side_nil = f"│         │"
        blank_nil = f"           "
        print(top_nil)
        print(blank_nil)
        print(side_nil)
        print(blank_nil)
        print(side_nil)
        print(blank_nil)
        print(bottom_nil)

    else:
        raise ValueError("Invalid color. Use 'r' for red, 'b' for black, or 'n' for none.")


def main():
    cards = [("A", "s", "b"), ("10", "h", "r"), ("K", "d", "r"),
             ("7", "c", "b"), ("n", "n", "n"), ("nil", "nil", "nil")]
    for rank, suit, color in cards:
        card(rank, suit, color)
        print()  # Add a space between cards


def print_all_cards():
    """Print all cards from the dictionary in random order, 5 per line, stacked."""
    card_list = list(card_dict.values())
    for i in range(0, len(card_list), 4):
        cards_batch = card_list[i:i+4]
        lines = [[] for _ in range(7)]  # 7 lines per stacked card
        
        for rank, suit, color in cards_batch:
            # Capture card output
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            card(rank, suit, color,)
            sys.stdout = old_stdout
            card_lines = buffer.getvalue().strip().split('\n')
            
            # Add each line to corresponding row
            for j, line in enumerate(card_lines):
                lines[j].append(line)
        
        # Print all lines side by side
        for line_group in lines:
            print(" ".join(line_group))
        print()
        


card_dict = {
    1: ("A", "s", "b"),
    2: ("A", "c", "b"),
    3: ("A", "d", "r"),
    4: ("A", "h", "r"),
    5: ("2", "s", "b"),
    6: ("2", "c", "b"),
    7: ("2", "d", "r"),
    8: ("2", "h", "r"),
    9: ("3", "s", "b"),
    10: ("3", "c", "b"),
    11: ("3", "d", "r"),
    12: ("3", "h", "r"),
    13: ("4", "s", "b"),
    14: ("4", "c", "b"),
    15: ("4", "d", "r"),
    16: ("4", "h", "r"),
    17: ("5", "s", "b"),
    18: ("5", "c", "b"),
    19: ("5", "d", "r"),
    20: ("5", "h", "r"),
    21: ("6", "s", "b"),
    22: ("6", "c", "b"),
    23: ("6", "d", "r"),
    24: ("6", "h", "r"),
    25: ("7", "s", "b"),
    26: ("7", "c", "b"),
    27: ("7", "d", "r"),
    28: ("7", "h", "r"),
    29: ("8", "s", "b"),
    30: ("8", "c", "b"),
    31: ("8", "d", "r"),
    32: ("8", "h", "r"),
    33: ("9", "s", "b"),
    34: ("9", "c", "b"),
    35: ("9", "d", "r"),
    36: ("9", "h", "r"),
    37: ("10", "s", "b"),
    38: ("10", "c", "b"),
    39: ("10", "d", "r"),
    40: ("10", "h", "r"),
    41: ("J", "s", "b"),
    42: ("J", "c", "b"),
    43: ("J", "d", "r"),
    44: ("J", "h", "r"),
    45: ("Q", "s", "b"),
    46: ("Q", "c", "b"),
    47: ("Q", "d", "r"),
    48: ("Q", "h", "r"),
    49: ("K", "s", "b"),
    50: ("K", "c", "b"),
    51: ("K", "d", "r"),
    52: ("K", "h", "r")
}


if __name__ == "__main__":
    if input("Print all cards? (y/n): ").lower() == "y":
        print_all_cards()
    else:
        print("Sample:")
        main()