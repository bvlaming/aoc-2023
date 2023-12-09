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
        score_hand*100000000000 + card1*20*20*20*20 + card2*20*20*20 + card3*20*20 + card4*20 + card5
    )



def score_cards(cards_str: str) -> int:
    # determine hand, high card, second high card, third high card, 4 high, 5 high
    int_map = {'T': '10', 'J': '11', 'Q': '12', 'K': '13', 'A': '14'}
    cards = [int(int_map.get(c,c)) for c in cards_str]
    # cards.sort(reverse=True)
    # card1, card2, card3, card4, card5 = 0, 0, 0, 0, 0
    mc = Counter(cards).most_common()
    if len(set(cards)) == 1:
        hand = Hand.FIVE
        # card1 = cards[0]
    elif len(set(cards)) == 2:
        # four of a kind or full house
        # card1 = mc[0][0]
        # card2 = mc[1][0]
        if mc[0][1] == 4:
            hand = Hand.FOUR
        else:
            hand = Hand.FULL
    elif len(set(cards)) == 3:
        if mc[0][1] == 3:
            hand = Hand.THREE
            # card1 = mc[0][0]
            # card2 = max(mc[1][0], mc[2][0])
            # card3 = min(mc[1][0], mc[2][0])
        else:
            hand = Hand.TWOPAIR
            # card1 = max(mc[0][0], mc[1][0])
            # card2 = min(mc[0][0], mc[1][0])
            # card3 = mc[2][0]
    elif len(set(cards)) == 2:
        hand = Hand.PAIR
        # card1 = mc[0][0]
        # rest_cards = [c for c in cards if c != card1]
        # rest_cards.sort(reverse=True)
        # card2 = rest_cards[0]
        # card3 = rest_cards[1]
        # card4 = rest_cards[2]
    else:
        hand = Hand.HIGH
    card1, card2, card3, card4, card5 = cards[0], cards[1], cards[2], cards[3], cards[4]

    return score(hand, card1, card2, card3, card4, card5)


def parse_data(data: list[str]) -> [list[tuple[int, int]]]:
    """pair: 100000. two pair: 200000. 3oak: 3000."""
    return [
        (score_cards(line.split()[0]), int(line.split()[1])) for line in data
    ]





def main():
    with open("data/day7.csv", "r") as file:
        data = file.read().splitlines()

    x = parse_data(data)
    x.sort(key=lambda t: t[0])

    score = 0
    for n, y in enumerate(x, start=1):
        score += n * y[1]
    print(score)


if __name__ == "__main__":
    main()
