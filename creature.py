import random

class Creature:
    def __init__(self, name, power, toughness):
        self.name = name
        self.power = power
        self.toughness = toughness
        self.max_toughness = toughness

    def is_alive(self):
        return self.toughness > 0

    def take_damage(self, amount):
        self.toughness -= amount

    def attack(self, target):
        roll = random.randrange(1, self.power + 1)
        target.take_damage(roll)
        return roll