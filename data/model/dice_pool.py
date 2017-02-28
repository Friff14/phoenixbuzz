import operator

from data.model.die import Die
from data.model import die as dice_magics


class DiceGroup:
    pool = []

    def __init__(self, dice):
        """
        :param dice: Dictionary of dice, grouped by magic types
        """

        if type(dice) == list:
            self.pool = dice
            return
        self.pool = []
        # Go through the dictionary of dice. Each is in the format "{magic}": {count}.
        for magic in dice:
            if magic == 'regular':
                continue
            # If you want to pass in pre-rolled dice, make dice[magic] a list of dice instead of a number.
            if type(dice[magic]) == list:
                # Add the dice, pre-rolled
                for j in range(0, 2):
                    for i in range(0, dice[magic]):
                        added_die = Die(Die.get_magic(magic))
                        added_die.set_level(j)
                        self.pool.append(added_die)
                pass
            else:
                # Add a number of dice equal to the number requested
                for i in range(0, dice[magic]):
                    self.pool.append(
                        # get_magic_from_name returns the number (constant) corresponding with that name
                        Die(Die.get_magic_from_name(magic))
                        # so we pass it in the key from the passed-in dice dictionary
                    )

    def get_dice_dict(self):
        """
        :return: JSON-formatted dictionary of dice, grouped by magic type
        """

        # Returned list of dice
        dice = {'inactive': {}}

        for die in self.pool:
            # Add to the list of active dice if the die in question is active
            #  Otherwise, add to the inactive list
            dict_to_add_to = dice if die.active else dice['inactive']
            magic = die.get_magic()
            # If the dict in question does not have any of that type of die, add to it
            if magic not in dict_to_add_to:
                dict_to_add_to[magic] = [0, 0, 0]
            # Increment the count of that kind of die at that level
            dict_to_add_to[magic][die.level] += 1
        return dice

    def reroll(self):
        for die in self.pool:
            die.roll()
        return self.get_dice_dict()

    def spend_dice(self, dice_dict=None, dice_list=None):
        """
        :param dice_list: int[] of the dice in this group to be spent
        OR
        :param dice_dict: result of a DiceGroup.get_dice_dict() function
        :return: int. 0 if passed. -1 or -2 if failed.
        """
        if dice_dict is not None:
            try:
                pool = self.get_dice_dict()
                for magic_type in dice_dict:
                    for i in range(0, 2):
                        if pool[magic_type][i] < dice_dict[magic_type][i]:
                            return -1
            except KeyError:
                return -2

            for magic_type in dice_dict:
                for i in range(0, 2):
                    while dice_dict[magic_type][i] > 0:
                        magic_numbah = Die.get_magic_from_name(magic_type)
                        for die in self.pool:
                            if die.active and die.magic == magic_numbah and die.level == i:
                                die.deactivate()
                                break
                        dice_dict[magic_type][i] -= 1

            return 0

        elif dice_list is not None:
            # If the passed-in parameter is, instead, the list of dice
            for die in dice_list:
                if not self.pool[die].active:
                    return -3
            for die in dice_list:
                self.pool[die].deactivate()

            return 0

    def select(self, dice):
        """
        :param dice: int[]
        :return: DiceGroup
        Returns a sub-group of dice from the list passed in.
        Example: dice_group.select([a, b, c])
            returns a new dice group made up of dice at dice_group.pool's a, b, and c.
        Use this to calculate costs.
        """
        return DiceGroup([self.pool[i] for i in dice])


if __name__ == '__main__':
    dp = DiceGroup(
        {"Charm": 3,
         "Illusion": 7}
    )

    print(dp.get_dice_dict())
    print(dp.spend_dice(dice_dict={
        "Charm": [2, 1, 0],
        "Illusion": [1, 1, 0]
    }))
    print(dp.get_dice_dict())
    print(dp.reroll())

    for die in dp.pool: print(die)
    print(dp.select([0, 1, 2]).get_dice_dict())
    dp.spend_dice(dice_list=[0, 1, 2])
    print(dp.get_dice_dict())
