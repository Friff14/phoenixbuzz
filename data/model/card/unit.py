from data.model.card import Card


class Unit(Card):
    attack = 0
    life = 0
    recover = 0

    def __init__(self):
        super().__init__()
