# Cost class, handling the costs of cards and abilities
import operator

from data.model.dice_pool import *
from data.model.die import *

REGULAR_DICE = "regular"

CONTEXT_LIST = [
    "Main Action",
    "Side Action",
    "Unit Died",
    "Start of Turn"
]

class Cost:
    context = 0
    values = {REGULAR_DICE: [0]}

    def __init__(self, dice, context=0):
        self.context = context
        self.values = {REGULAR_DICE: [0]}
        if type(dice) != DiceGroup:

            if type(dice) == dict:
                dice = DiceGroup(dice)
            elif type(dice) == list:
                new_dice_list = []
                for die in dice:
                    magic = DIE_MAGIC_ABBR_LIST.index(die[0:2])
                    new_die = Die(magic, int(die[2]))
                    new_dice_list.append(new_die)
                dice = DiceGroup(new_dice_list)

        for die in dice.pool:
            magic = die.get_magic()
            if magic not in self.values:
                self.values[magic] = [0, 0]
            self.values[REGULAR_DICE][0] += 1
            if die.level >= 1:
                self.values[magic][0] += 1
            if die.level == 2:
                self.values[magic][1] += 1

    def __eq__(self, other):
        for magic in other.values:
            if magic not in self.values:
                return False
            print(list(map(operator.eq, self.values[magic], other.values[magic])))
            if False in list(map(operator.eq, self.values[magic], other.values[magic])):
                return False
        return True

    def __gt__(self, other):
        for magic in other.values:
            # If the other has a magic that's not in self, return false
            if magic not in self.values:
                return False
            print(list(map(operator.gt, self.values[magic], other.values[magic])))
            print(list(map(operator.le, self.values[magic], other.values[magic])))
            # Otherwise, compare all the magics
            if False in list(map(operator.gt, self.values[magic], other.values[magic]))\
                    and True not in list(map(operator.le, self.values[magic], other.values[magic])):
                return False

        return True

    def __ge__(self, other):
        for magic in other.values:
            # If the other has a magic that's not in self, return false
            if magic not in self.values:
               return False
            # Otherwise, compare all the magics
            if False in list(map(operator.ge, self.values[magic], other.values[magic])):
                return False
        return True
        # return self == other or self > other

    def __lt__(self, other):
        return not self >= other

    def __le__(self, other):
        return not self > other

if __name__ == '__main__':
    ############### TESTING HOW DICE COSTS WORK ################

    print(''' ### Set dice - 3 charm, 7 illusion, all mid-level ### ''')
    dp = DiceGroup(
        {"Charm": 3,
         "Illusion": 7}
    )
    dp.pool[0].set_level(1)
    dp.pool[1].set_level(1)
    dp.pool[2].set_level(1)
    dp.pool[3].set_level(1)
    dp.pool[4].set_level(1)
    dp.pool[5].set_level(1)
    dp.pool[6].set_level(1)
    dp.pool[7].set_level(1)
    dp.pool[8].set_level(1)
    dp.pool[9].set_level(1)
    print(dp.get_dice_dict())
    print()

    print(''' ### Create pool - 1 mid-charm, 1 high-charm, 1 regular ### ''')
    mixed_charm_cost = DiceGroup(
        {"Charm": 3}
    )
    mixed_charm_cost.pool[0].set_level(1)
    mixed_charm_cost.pool[1].set_level(2)
    mixed_charm_cost.pool[2].set_level(0)

    print(''' ### Create pool - 3 mid-charm dice ###''')
    mid_charm_3_cost = DiceGroup(
        {"Charm": 3}
    )
    mid_charm_3_cost.pool[0].set_level(1)
    mid_charm_3_cost.pool[1].set_level(1)
    mid_charm_3_cost.pool[2].set_level(1)
    print(mid_charm_3_cost.get_dice_dict())
    print()

    print(''' ### Create pool - 3 mixed-symbol dice ### ''')
    mixed_symbol_dice = DiceGroup(
        {"Charm": 1, "Illusion": 1, "Natural": 1, "Ceremonial": 1}
    )
    mixed_symbol_dice.pool[0].set_level(1)
    mixed_symbol_dice.pool[1].set_level(1)
    mixed_symbol_dice.pool[2].set_level(1)
    mixed_symbol_dice.pool[3].set_level(1)

    print(''' ### a = dice pool cost ### ''')
    a = Cost(dp)
    print(a.values)

    print(''' ### b = mid charm cost ### ''')
    b = Cost(mid_charm_3_cost)
    print(b.values)

    print(''' ### b1 = mixed charm cost ### ''')
    b1 = Cost(mixed_charm_cost)
    print(b1.values)

    print(''' ### b2 = mixed symbol cost ### ''')
    b2 = Cost({"Charm": 1, "Illusion": 1, "Natural": 1, "Ceremonial": 1})
    print(b2.values)

    print(''' ### c = cost created from {"Charm": 3} ### ''')
    c = Cost({"Charm": 3})
    print(c.values)

    print(''' ### c1 = trying out the letter-number method ### ''')
    c1 = Cost([
        "CE1",
        "CH1",
        "CH2",
        "IL1"
    ])
    print(c1.values)

    print(''' ### a == b: should return false (a should be > b) ###''')
    print(a == b)
    print()

    print(''' ### a > b: should return true ###''')
    print(a > b)
    print()

    print(''' ### a >= b: should return true''')
    print(a >= b)
    print()

    print(''' ### a >= b1: should return false''')
    print(a >= b1)
    print()

    print(''' ### a < b: should return false ''')
    print(a < b)
    print()

    print(''' ### a <= b: should return false ''')
    print(a <= b)

    print(b <= c)

