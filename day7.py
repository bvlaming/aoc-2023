from enum import Enum
from collections import Counter
class Hand(Enum):
    HIGH = "1high"
    PAIR = "2pair"
    TWOPAIR = "3twopair"
    THREE = "4three"
    FULL = "5full"
    FOUR = "6four"
    FIVE = "7five"


def score(hand: Hand, card1: int, card2: int=0, card3: int=0, card4: int=0, card5:int=0) -> int:
    score_hand = int(hand.value[0])
    return (
        score_hand*10000000 + card1*20*20*20*20 + card2*20*20*20 + card3*20*20 + card4*20 + card5
    )

def find_hand(cards: list[int]) -> Hand:
    mc = Counter(cards).most_common()
    if len(set(cards)) == 1:
        hand = Hand.FIVE
    elif len(set(cards)) == 2:
        # four of a kind or full house
        if mc[0][1] == 4:
            hand = Hand.FOUR
        else:
            hand = Hand.FULL
    elif len(set(cards)) == 3:
        if mc[0][1] == 3:
            hand = Hand.THREE
        else:
            hand = Hand.TWOPAIR
    elif len(set(cards)) == 4:
        hand = Hand.PAIR
    else:
        hand = Hand.HIGH
    return hand

def score_cards(cards_str: str, uses_joker: bool = False) -> int:
    # determine hand, high card, second high card, third high card, 4 high, 5 high
    if uses_joker:
        int_map = {'T': '10', 'J': '1', 'Q': '12', 'K': '13', 'A': '14'}
    else:
        int_map = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}

    cards = [int(int_map.get(c,c)) for c in cards_str]
    if any(c == 1 for c in cards) and uses_joker:
        if all(c == 1 for c in cards):
            # if all J: transfer to A
            cards_with_joker = [14]*5
        else:
            # add J to the most frequent card
            mc_type = Counter([c for c in cards if c!=1]).most_common()[0][0]
            cards_with_joker = [c if c != 1 else mc_type for c in cards]
            # print(mc_type)
            # print(cards_with_joker)
        hand = find_hand(cards_with_joker)
        # print(hand)
    else:
        hand = find_hand(cards)
    # print(hand)
    card1, card2, card3, card4, card5 = cards[0], cards[1], cards[2], cards[3], cards[4]
    return score(hand, card1, card2, card3, card4, card5)


def parse_data(data: list[str], uses_joker: bool) -> [list[tuple[int, int]]]:
    """pair: 100000. two pair: 200000. 3oak: 3000."""
    return [
        (score_cards(line.split()[0], uses_joker), int(line.split()[1]), line.split()[0]) for line in data
    ]


def total_score(data: list[str], uses_joker: bool):
    x = parse_data(data, uses_joker=uses_joker)
    x.sort(key=lambda t: t[0])
    print(x[:20])
    score = 0
    for n, y in enumerate(x, start=1):
        score += n * y[1]
    return score

def main():
    with open("data/day7.csv", "r") as file:
        data = file.read().splitlines()
    # data = ['J28TQ  666']
    print(total_score(data, uses_joker=False))
    print(total_score(data, uses_joker=True))

# 249748283
if __name__ == "__main__":
    main()
