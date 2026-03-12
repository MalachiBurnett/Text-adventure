import creature

class Enemy(creature.Creature):
    def __init__(self, name, power, toughness, intro_text):
        super().__init__(name, power, toughness)
        self.intro_text = intro_text

    def take_turn(self, player, game_interface):
        enemy_roll = self.attack(player)
        game_interface.display(f"The {self.name} rolls a {enemy_roll}! your toughness is now {player.toughness}.")
        return player.is_alive()