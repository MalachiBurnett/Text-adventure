import enemy
import random

class FrostElemental(enemy.Enemy):
    def __init__(self):
        super().__init__(
            "Frost Elemental", 
            power=6, 
            toughness=25,
            intro_text="At the top of the spiralling staircase, the air turns\n"
            "bitterly cold. A vast frozen chamber stretches before you.\n"
            "In the centre stands a humanoid figure made entirely of\n"
            "swirling ice and mist. The frost elemental awakens."
        )
        self.frozen_state = False

    def take_turn(self, player, game_interface):
        enemy_roll = random.randrange(1, self.power + 1)
        game_interface.display(f"The elemental strikes for {enemy_roll} cold damage!")
        player.toughness -= enemy_roll
        game_interface.display(f"Your toughness is now {player.toughness}/{player.max_toughness}")

        if player.toughness <= 0 and not self.frozen_state:
            self.frozen_state = True
            game_interface.display(
                "As your toghness drops to 0, Ice engulfs you.\n"
                "You are petrified in frozen crystal.\n"
                "but you realise your right arm is still free,\n"
                "and you can still move it slightly.\n"
                "You might be able to use it to interact with the\n"
                "environment around you,\n"
                "but you can't attack or defend yourself in this state."
            )

        if self.frozen_state:
            return self.handle_frozen_event(player, game_interface)
        
        return player.is_alive()

    def handle_frozen_event(self, player, game_interface):
        game_interface.display(
            "You notice a nearby brazier flickering.\n"
            "It seems to be just within reach.\n"
            "I wonder if you could use the fire to un-freeze yourself.\n"
        )
        game_interface.display("Use the fire to un-freeze yourself?")
        choice = game_interface.make_selection(["yes", "no"], "choose: ")

        if choice == "yes":
            revive_roll = random.randrange(1, player.power + 1)
            fire_damage = random.randrange(1, 5)

            game_interface.display(f"You revive with {revive_roll} HP from the warmth!")
            revive_roll -= fire_damage
            game_interface.display(f"However, the fire burns you for {fire_damage} damage!")

            if revive_roll <= 0:
                game_interface.display("You collapse from the burns...")
                return False
            else:
                player.toughness = revive_roll
                self.frozen_state = False
                return True
        else:
            game_interface.display("You remain frozen as the cold tightens...")
            return False


