from data.model.card.card import Card


class Alteration(Card):
    attack_bonus = 0
    life_bonus = 0
    recover_bonus = 0

    def __init__(self):
        super().__init__()
