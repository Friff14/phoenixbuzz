import random

DIE_MAGIC_LIST = [
    'Natural',
    'Charm',
    'Ceremonial',
    'Illusion',
]
DIE_MAGIC_ABBR_LIST = [
    'NA',
    'CH',
    'CE',
    'IL'
]
NATURAL_MAGIC = 0
CHARM_MAGIC = 1
CEREMONIAL_MAGIC = 2
ILLUSION_MAGIC = 3


class Die:

    # The side showing on the die. 0 is the side that's on all dice. 2 is the big one.
    level = 0
    # Which color the die is. See the constants list for which ones are available
    magic = 0
    # Whether the die has been used
    active = False

    def __init__(self, magic, level=-1):
        self.magic = magic
        # Initial roll
        if level in range(0, 3):
            self.level = level
        else:
            self.roll()
        # Make it active immediately
        self.activate()

    def roll(self):
        # Randomly pick a level
        self.level = random.choice([0, 0, 0, 1, 1, 2])
        # Move the die to your active pool
        self.activate()

    def set_level(self, level):
        # Re-roll the die and decide the result
        self.level = level

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def get_magic(self):
        # Return the string associated with the magic value
        return DIE_MAGIC_LIST[self.magic]

    def get_magic_abbr(self):
        return DIE_MAGIC_ABBR_LIST[self.magic]

    def __str__(self):
        face = self.get_magic() + \
               ' - ' + str(self.level) + ' - ' + \
               'Active' if self.active else 'Inactive'
        return face

    @staticmethod
    def get_magic_from_name(name):
        magics = {
            'Natural': 0,
            'Charm': 1,
            'Ceremonial': 2,
            'Illusion': 3,
        }
        return magics[name]


if __name__ == '__main__':
    dice = []
    for i in range(0, 10):
        dice.append(Die(CHARM_MAGIC if i < 5 else ILLUSION_MAGIC))

    for die in dice:
        print(die)
