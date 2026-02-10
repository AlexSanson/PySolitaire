from random import shuffle
from time import sleep as wait
import io
import sys

from CardPrinter import card, card_dict

global cards_left
global card_list
global ab_length
global assigned_blanks
global trash

debug = 0 # Adds aditional print info if set to 1

card_list = list(card_dict.values())
cards_left = len(card_list)
for _ in range(5):
    shuffle(card_list)

blankc = ("n", "n", "n")
slotc = ("nil", "nil", "nil")

rank_order = {
    "A": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
}

def parse_card_input(card_str):
    cleaned = card_str.strip().upper()
    if cleaned == "":
        return None
    if cleaned.startswith("10"):
        rank = "10"
        suit = cleaned[2:].lower()
    else:
        rank = cleaned[0]
        suit = cleaned[1:].lower()
        if rank == "1":
            rank = "A"
    if rank not in rank_order or suit not in {"h", "d", "c", "s"}:
        return None
    return (rank, suit)

def parse_foundation_input(card_str):
    cleaned = card_str.strip().lower()
    if not cleaned.startswith("f") or len(cleaned) < 2:
        return None
    if not cleaned[1].isdigit():
        return None
    index = int(cleaned[1]) - 1
    if index not in {0, 1, 2, 3}:
        return None
    return index

def parse_column_input(card_str):
    cleaned = card_str.strip().lower()
    if not cleaned.startswith("c") or len(cleaned) < 2:
        return None
    if not cleaned[1].isdigit():
        return None
    index = int(cleaned[1]) - 1
    if index not in {0, 1, 2, 3, 4, 5, 6}:
        return None
    return index

def add_color_to_card(card_rank_suit):
    suit = card_rank_suit[1]
    return card_rank_suit + ("r" if suit in {"h", "d"} else "b",)

def is_draw_slot(card_rank_suit):
    draw_card = header[len(header) - 2]
    if draw_card in {slotc, blankc, "", None}:
        return False
    rank, suit = card_rank_suit
    color = suit_to_color(suit)
    return draw_card[:3] == (rank, suit, color)

def is_card_lower(card_to_move, target_card):
    if card_to_move == blankc or target_card == blankc:
        return False
    card_to_move_rank = rank_order[card_to_move[0]]
    target_card_rank = rank_order[target_card[0]]
    return card_to_move_rank < target_card_rank and target_card_rank - card_to_move_rank == 1

def suit_to_color(suit):
    return "r" if suit in {"h", "d"} else "b"

def get_foundation_top(foundation_index):
    foundation = foundations[foundation_index]
    return foundation[-1] if foundation else slotc

def update_foundation_header(foundation_index):
    header[foundation_index] = get_foundation_top(foundation_index)

def is_card_available_in_columns(card_rank_suit):
    false = 0
    rank, suit = card_rank_suit
    color = suit_to_color(suit)
    for column in columns:
        for card_tuple in column:
            if card_tuple == blankc:
                continue
            if card_tuple[:3] == (rank, suit, color):
                return True
    if debug == 1:
        print(header)
    for card_tuple in header:
        if card_tuple == blankc:
            continue
        if card_tuple[:3] == (rank, suit, color):
            return True
        for foundation in foundations:
            if not foundation:
                continue
            if foundation[-1][:3] == (rank, suit, color):
                return True
    return False

def add():
    global cards_left
    global card_list
    if cards_left > 0:
        card_to_add = card_list.pop()
        cards_left -= 1
        return card_to_add
    else:
        print("Error: Failed to add card.")
        wait(2)
        return None

trash = []
def draw():
    global assigned_blanks
    global ab_length
    global trash
    if debug == 1:
        print(assigned_blanks)
        print(trash)
        print(ab_length)
    if ab_length > 0:
        trash.append(assigned_blanks[ab_length-1])
        card_to_add = assigned_blanks.pop()
        ab_length -= 1
        return card_to_add
    else:
        print("Refreshing draw pile.")
        assigned_blanks = trash[:]
        assigned_blanks.reverse()
        trash = []
        ab_length = len(assigned_blanks)
        return slotc

def replace(selected_card=None):
    global card_list
    global cards_left
    if cards_left > 0:
        card_to_add = card_list.pop()
        cards_left -= 1
        return card_to_add
    if selected_card is not None:
        return selected_card
    print("No more cards left to replace.")
    wait(2)
    return None

def move_card(card_to_move, target_card):
    global trash
    if card_to_move == "d":
        return "d"
    if card_to_move in [foundation[-1] for foundation in foundations if foundation]:
        for foundation_index, foundation in enumerate(foundations):
            if foundation and foundation[-1] == card_to_move:
                moving_cards = [card_to_move]
                foundation.pop()
                update_foundation_header(foundation_index)
                break
        else:
            print("Error cannot move card.")
            return False
    elif card_to_move in header:
        header_index = header.index(card_to_move)
        moving_cards = [card_to_move]
        trash.pop() if trash else None
        header[header_index] = trash[len(trash)-1] if trash else slotc
    else:
        for column in columns:
            if card_to_move in column:
                card_index = column.index(card_to_move)
                moving_cards = column[card_index:]
                del column[card_index:]
                if card_index == 0:
                    column.append(slotc)
                elif column and column[-1] == blankc:
                    replacement_card = replace()
                    if replacement_card is not None:
                        column[-1] = replacement_card
                break
        else:
            print("Error cannot move card.")
            return False

    for column in columns:
        if target_card in column:
            target_index = column.index(target_card)
            column[target_index + 1:target_index + 1] = moving_cards
            return True

    print("Target card not found in columns.")
    wait(2)
    return False

def can_place_on_foundation(card_tuple, foundation_index):
    top_card = get_foundation_top(foundation_index)
    if card_tuple[0] == "A":
        for idx, foundation in enumerate(foundations):
            if idx != foundation_index and foundation and foundation[0][:2] == ("A", card_tuple[1]):
                return False
    if top_card == slotc or top_card == blankc:
        return card_tuple[0] == "A"
    if top_card[1] != card_tuple[1]:
        return False
    return rank_order[card_tuple[0]] == rank_order[top_card[0]] + 1

def move_card_to_foundation(card_to_move, foundation_index):
    global trash
    if not can_place_on_foundation(card_to_move, foundation_index):
        print("Invalid move. Foundation piles stack from Ace to King by suit.")
        wait(2)
        return False
    if card_to_move in header:
        header_index = header.index(card_to_move)
        trash.pop() if trash else None
        header[header_index] = trash[len(trash)-1] if trash else slotc
        foundations[foundation_index].append(card_to_move)
        update_foundation_header(foundation_index)
        return True
    for column in columns:
        if card_to_move in column:
            card_index = column.index(card_to_move)
            if card_index != len(column) - 1:
                print("Invalid move. Only the top card can move to foundation.")
                wait(2)
                return False
            column.pop()
            if len(column) == 0:
                column.append(slotc)
            elif column and column[-1] == blankc:
                replacement_card = replace()
                if replacement_card is not None:
                    column[-1] = replacement_card
            foundations[foundation_index].append(card_to_move)
            update_foundation_header(foundation_index)
            return True
    print("Error cannot move card.")
    wait(2)
    return False

def is_column_empty(column_index):
    column = columns[column_index]
    return len(column) == 0 or (len(column) == 1 and column[0] == slotc)

def move_card_to_empty_column(card_to_move, column_index):
    global trash
    if card_to_move[0] != "K":
        print("Invalid move. Only kings can move to empty columns.")
        wait(2)
        return False
    if not is_column_empty(column_index):
        print("Invalid move. Column is not empty.")
        wait(2)
        return False
    if card_to_move in header:
        header_index = header.index(card_to_move)
        moving_cards = [card_to_move]
        trash.pop() if trash else None
        header[header_index] = trash[len(trash)-1] if trash else slotc
    else:
        for column in columns:
            if card_to_move in column:
                card_index = column.index(card_to_move)
                moving_cards = column[card_index:]
                del column[card_index:]
                if len(column) == 0:
                    column.append(slotc)
                elif column and column[-1] == blankc:
                    replacement_card = replace()
                    if replacement_card is not None:
                        column[-1] = replacement_card
                break
        else:
            print("Error cannot move card.")
            wait(2)
            return False
    columns[column_index] = moving_cards
    return True

if debug == 1:
    print(card_list)
    print(cards_left)
foundations = [[], [], [], []]
header = [get_foundation_top(0), get_foundation_top(1), get_foundation_top(2), get_foundation_top(3), '', slotc, blankc]
columns = [
    [add()],
    [blankc, add()],
    [blankc, blankc, add()],
    [blankc, blankc, blankc, add()],
    [blankc, blankc, blankc, blankc, add()],
    [blankc, blankc, blankc, blankc, blankc, add()],
    [blankc, blankc, blankc, blankc, blankc, blankc, add()]
]
assigned_blanks = [add() for _ in range(24)]
ab_length = len(assigned_blanks)

if debug == 1:
    print(card_list)
    print(cards_left)
    print()
    print(columns)


first = 0
def card_input():
    global first
    if get_foundation_top(0) == ("K", "s", "b") and get_foundation_top(1) == ("K", "h", "r") and get_foundation_top(2) == ("K", "d", "r") and get_foundation_top(3) == ("K", "c", "b"):
        print("Congratulations! You won!")
        exit()
    print("# -------------------------------------------------------------------------------------------------------------------------------- #")
    if first < 3:
        print("Full instructions will show for 3 turns.")
        print("To move a card onto another card, type the card number (1-10, A, J, Q, K) and its suit (h, d, c, s) of the card you wish to move,")
        print("then type the same for the card you wish to move it onto, for example '5h' and '6s' would move the 5 of hearts onto the 6 of spades.")
        print("To move a card to foundation type the card you want to move and then the foundation pile to move to f(1-4) Example: 'ah' and 'f1' would move the Ace of Hearts to foundation pile 1.")
        print("To move a king to an empty column, type the card and then c(1-7) Example: 'kd' and 'c1' would move the King of Diamonds to column 1.")
        first += 1
    else:
        print("Input format: (1-10, A, J, Q, K)(h, d, c, s), f(1-4), c(1-7), or 'd' to draw a card")
    while True:
        card1 = input("Card to move: ")
        if card1.lower() == "d":
            header[len(header)-2] = draw()
            return "d", None
        if card1.lower() == "wheredidmycardgo":
            print("Debug info:")
            print("Header:", header)
            print("Foundations:", foundations)
            print("Columns:")
            for i, column in enumerate(columns):
                print(f"Column {i+1}:", column)
            print("Assigned blanks:", assigned_blanks)
            print("Leftover cards:", card_list)
            continue
        elif len(card1.lower()) < 2 and not card1.startswith("10"):
            print("Invalid input. Please try again.")
            wait(2)
            continue
        card2 = input("Card to move onto: ")
        if len(card2.lower()) < 2 and not card2.startswith("10"):
            print("Invalid input. Please try again.")
            wait(2)
            continue
        parsed_card1 = parse_card_input(card1)
        if parsed_card1 is None:
            print("Invalid input. Please try again.")
            wait(2)
            continue
        foundation_index = parse_foundation_input(card2)
        if foundation_index is not None:
            if not is_card_available_in_columns(parsed_card1):
                print("Invalid move. The card you want to move is not in the columns.")
                wait(2)
                continue
            parsed_card1 = add_color_to_card(parsed_card1)
            return "foundation", parsed_card1, foundation_index
        column_index = parse_column_input(card2)
        if column_index is not None:
            if not is_card_available_in_columns(parsed_card1):
                print("Invalid move. The card you want to move is not in the columns.")
                wait(2)
                continue
            parsed_card1 = add_color_to_card(parsed_card1)
            return "empty_column", parsed_card1, column_index
        parsed_card2 = parse_card_input(card2)
        if parsed_card2 is None:
            print("Invalid input. Please try again.")
            wait(2)
            continue
        if is_draw_slot(parsed_card2):
            print("Invalid move. You cannot move cards onto the draw pile.")
            wait(2)
            continue
        suit1 = parsed_card1[1]
        suit2 = parsed_card2[1]
        if not is_card_lower(parsed_card1, parsed_card2):
            print("Invalid move. The card you move must be lower than the target card.")
            wait(2)
            continue
        if (suit1 in {"h", "d"} and suit2 in {"h", "d"}) or (suit1 in {"c", "s"} and suit2 in {"c", "s"}):
            print("Invalid move. Cards must be of opposite suit colors.")
            wait(2)
            continue
        if not is_card_available_in_columns(parsed_card1):
            print("Invalid move. The card you want to move is not in the columns.")
            wait(2)
            continue
        if not is_card_available_in_columns(parsed_card2):
            print("Invalid move. The target card is not in the columns.")
            wait(2)
            continue
        parsed_card1 = add_color_to_card(parsed_card1)
        parsed_card2 = add_color_to_card(parsed_card2)
        if debug == 1:
            print(parsed_card1, parsed_card2)
        return parsed_card1, parsed_card2
            

def get_card_lines(card_tuple, stacked=False, reduced_stack=False):
    if card_tuple is None or card_tuple == "":
        return [" " * 11 for _ in range(3 if stacked else 7)]

    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()
    card(*card_tuple, "t" if stacked else "f", "t" if reduced_stack else "f")
    sys.stdout = old_stdout
    lines = buffer.getvalue().splitlines()
    if stacked:
        return lines[:3]
    if len(lines) < 7:
        lines.extend([" " * 11 for _ in range(7 - len(lines))])
    return lines

def display_game():
    column_line_groups = []
    for column in columns:
        column_lines = []
        reduced_stack = len(column) >= 8
        for idx, card_tuple in enumerate(column):
            stacked = idx < len(column) - 1
            column_lines.extend(
                get_card_lines(card_tuple, stacked=stacked, reduced_stack=reduced_stack)
            )
        column_line_groups.append(column_lines[:])

    max_lines = max(len(column_lines) for column_lines in column_line_groups)
    for i in range(len(column_line_groups)):
        if len(column_line_groups[i]) < max_lines:
            column_line_groups[i].extend([" " * 11 for _ in range(max_lines - len(column_line_groups[i]))])

    header_line_groups = [get_card_lines(card_tuple, stacked=False) for card_tuple in header]
    max_header_lines = max(len(lines) for lines in header_line_groups)
    for header_lines in header_line_groups:
        if len(header_lines) < max_header_lines:
            header_lines.extend([" " * 11 for _ in range(max_header_lines - len(header_lines))])

    for line_index in range(max_header_lines):
        print(" ".join(header_lines[line_index] for header_lines in header_line_groups))
    print()

    for line_index in range(max_lines):
        print(" ".join(column_lines[line_index] for column_lines in column_line_groups))
    print()


while True:
    display_game()
    move_result = card_input()
    if move_result[0] == "foundation":
        move_card_to_foundation(move_result[1], move_result[2])
    elif move_result[0] == "empty_column":
        move_card_to_empty_column(move_result[1], move_result[2])
    else:
        move_card(*move_result)
    
    


