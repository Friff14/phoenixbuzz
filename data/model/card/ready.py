from data.model.card.card import Card


class Ready(Card):
    # This might not actually be a thing. Focus might be implemented some other way. No idea yet.
    focus = None

    def __init__(self):
        super().__init__()
