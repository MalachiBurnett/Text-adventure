import enemy
import random

class Goblin(enemy.Enemy):
    def __init__(self):
        super().__init__(
            "Goblin", 
            power=4, 
            toughness=4,
            intro_text=
                "The next room is circular, with cracked stone tiles and\n"
                "scorch marks along the walls. In the centre stands a goblin\n"
                "clutching an ornate wooden staff far too large for it.\n"
                "Arcane sparks crawl along its length."
        )

    def take_turn(self, player, game_interface):
        if random.random() < 0.5:
            self.wild_magic(player, game_interface)
        
        enemy_roll = random.randrange(1, self.power + 1)
        player.toughness -= enemy_roll
        game_interface.display(f"The goblin rolls {enemy_roll}! Your toughness is now {player.toughness}.")
        
        if player.toughness <= 0:
            game_interface.display("You fall to the goblin's chaotic magic...")
            return False
            
        return True

    def wild_magic(self, player, game_interface):
        roll = random.randint(1, 6)

        if roll == 1:
            game_interface.display("The staff backfires! The goblin is struck by arcane force.")
            dmg = random.randint(1, 4)
            self.take_damage(dmg)
            game_interface.display(f"The goblin takes {dmg} damage from the backlash!")

        elif roll == 2:
            game_interface.display("A distorted memory echoes in your mind… but it does nothing.")

        elif roll == 3:
            game_interface.display("Ice spreads across the floor! You slip and lose your next attack.")

        elif roll == 4:
            game_interface.display("A burst of fire shoots from the staff!")
            dmg = random.randint(1, 4)
            player.toughness -= dmg
            game_interface.display(f"You take {dmg} fire damage! Your toughness is now {player.toughness}.")

        elif roll == 5:
            game_interface.display("The goblin flickers and teleports behind you!")

        elif roll == 6:
            game_interface.display("Arcane power surges through the goblin!")
            self.power += 2
            game_interface.display("The goblin grows stronger!")
