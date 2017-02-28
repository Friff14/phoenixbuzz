class Ability:
    cost = None
    exhaustible = True
    constant = False

    def __init__(self, cost, context):
        self.cost = cost

    def get_context(self):
        return self.cost.context

    def is_valid(self, cost):
        return cost.context == self.get_context() and cost == self.cost
