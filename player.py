import creature

class Player(creature.Creature):
    def __init__(self):
        super().__init__("Hero", 0, 0)
        self.pc = "none"
        self.race = "none"
        self.potions = 0

    def full_heal(self):
        self.toughness = self.max_toughness
    
    def drink_potion(self):
        if self.potions > 0:
            heal_amount = 8
            self.toughness = min(self.toughness + heal_amount, self.max_toughness)
            self.potions -= 1
            return True
        return False