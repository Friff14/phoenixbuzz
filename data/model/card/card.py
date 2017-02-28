class Card:
    title = None
    play_cost = None
    placement = 0
    effects = []
    counters = {}
    conjuration = False

    def __init__(self,
                 title,
                 play_cost,
                 placement,
                 effects):
        self.title = title
        self.play_cost = play_cost
        self.placement = placement
        self.effects = effects
