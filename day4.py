from dataclasses import dataclass


@dataclass
class Card:
    id: int
    winning_numbers: list[int]
    owned_numbers: list[int]

    def owned_winning_cnt(self):
        return len(set(self.winning_numbers).intersection(set(self.owned_numbers)))

    def score(self):
        owc = self.owned_winning_cnt()
        return 0 if owc == 0 else pow(2, owc - 1)

    def __hash__(self):
        return hash(str(self.id))


def parse_card(line: str) -> Card:
    card_str, numbers_str = line.split(":")
    card_id = int("".join([c for c in card_str if c.isdigit()]))
    winning_nrs, owned_nrs = numbers_str.split("|")
    winning = [int(w) for w in winning_nrs.split()]
    owned = [int(x) for x in owned_nrs.split()]
    return Card(card_id, winning, owned)


def find_end_cards(cards: list[Card]) -> int:
    """Go through cards."""
    card_dict = {card.id: card for card in cards}
    card_count = {card.id: 1 for card in cards}
    # card_count = [(1, card) for card in cards]
    for idx, card in enumerate(cards, start=1):
        score = card.owned_winning_cnt()
        multiplier = card_count[idx]
        for n in range(1, score + 1):
            card_count[idx + n] += multiplier

    return sum(card_count.values())


def main():
    with open("data/day4.csv", "r") as file:
        data = file.read().splitlines()
    cards = [parse_card(line) for line in data]
    answer4a = sum([card.score() for card in cards])
    print(answer4a)

    print(find_end_cards(cards))


if __name__ == "__main__":
    main()
