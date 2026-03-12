import string
import time
import random
import goblin
import player
import elemental
from story import StoryEngine

class Game:
    TEXT_SPEED = 0.002

    def __init__(self):
        self.player = player.Player()
        self.text_mode = "immersive"
        self.classes = ["Rogue", "Wizard", "Artificer", "Potato", "Bard", "Programmer"]
        self.races = ["Ethan", "Triangle", "Dwarf", "Akim", "Human", "Elf", 
                      "NVIDEA x86_64 NVME RAM for New Nintendo switch 2 XL Pro U", 
                      "Orc", "Nyan cat"]

    def select_text_mode(self):
        print("Select text mode:")
        print("1 - Immersive (default)")
        print("2 - Fast (instant)")
        print("3 - Slow (dramatic)")
        choice = input("Enter 1, 2, or 3: ")

        if choice == "2":
            self.text_mode = "fast"
        elif choice == "3":
            self.text_mode = "slow"
            self.TEXT_SPEED = 0.01
        else:
            self.text_mode = "immersive"
            self.TEXT_SPEED = 0.002

    def display(self, text):
        import shutil
        terminal_width = shutil.get_terminal_size().columns
        
        for line in text.strip('\n').split('\n'):
            words = line.split(' ')
            current_line = ""
            
            for word in words:
                if len(current_line) + len(word) + 1 <= terminal_width:
                    current_line += word + " "
                else:
                    if current_line:
                        self._output_line(current_line.rstrip())
                    current_line = word + " "
            
            if current_line:
                self._output_line(current_line.rstrip())
            
            print()

    def _output_line(self, line):
        if self.text_mode == "fast":
            print(line, end='')
            return

        charset = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890.,!?';:()%*+-/=_" + string.printable

        for target_char in line:
            if target_char.isspace():
                print(target_char, end='', flush=True)
                continue

            for trial_char in charset:
                print(trial_char, end='', flush=True)
                time.sleep(self.TEXT_SPEED)
                if trial_char == target_char:
                    break
                print('\b', end='', flush=True)


    def make_selection(self, array, prompt):
        letters_taken = []
        for i in array:
            index = 0
            array_input = i[index].lower()
            while array_input in letters_taken and index < len(i):
                index += 1
                array_input = i[:index].lower()
            letters_taken.append(array_input)
            self.display("\n")
            self.display(f"{i} (type {array_input.lower()} to select)\n")

        self.display("\n")
        self.display(prompt)
        choice = input().lower()

        if choice in letters_taken:
            return array[letters_taken.index(choice)]
        else:
            self.display("you imbicile!")
            return self.make_selection(array, prompt)

    def roll_stats(self, options=None):
        if options is None:
            options = ["re-roll (1 left)", "power", "toughness"]

        result = random.randrange(1, 10)

        if len(options) == 1:
            match(options[0]):
                case "re-roll (1 left)":
                    self.display(f"Your final stats are: power:{self.player.power}, toughness:{self.player.toughness}")
                case "power":
                    player.power = result
                    self.display(f"The result of a 10-sided dice is {result}. Since you have no other options left, your power will be automatically set to {result}. Your final stats are: power:{self.player.power}, toughness:{self.player.toughness}")
                case "toughness":
                    player.toughness = result
                    self.display(f"The result of a 10-sided dice is {result}. Since you have no other options left, your toughness will be automatically set to {result}. Your final stats are: power:{self.player.power}, toughness:{self.player.toughness}")
            return

        if len(options) == 0:
            return

        self.display(f"the result of a 10-sided dice is {result}.\nChoose which stat you would like to set to {result}:")

        selection = self.make_selection(options, f"choose which stat to assign {result} to: ")
        
        if selection == "re-roll (1 left)":
            options.remove("re-roll (1 left)")
            self.roll_stats(options)
        elif selection == "power":
            self.player.power = result
            options.remove("power")
            self.roll_stats(options)
        elif selection == "toughness":
            self.player.toughness = result
            self.player.max_toughness = result
            options.remove("toughness")
            self.roll_stats(options)

    def a_or_an(self, string):
        if string[0] in "AEIOU":
            return "an"
        return "a"

    def character_creation(self):
        self.display("Welcome adventurer!")
        self.display("its time to build your character!")
        self.display("first, please select a class.")
        self.display("your options are: ")
        self.player.pc = self.make_selection(self.classes, "Choose your class: ")

        self.display(f"Ah! you have chosen to be {self.a_or_an(self.player.pc)} {self.player.pc}!")
        self.display("excellent choice!")
        self.display("now its time to choose a Race.")
        self.display("your options are: ")
        self.player.race = self.make_selection(self.races, "Choose your Race: ")

        self.display(f"Ah! you have chosen to be {self.a_or_an(self.player.race)} {self.player.race}!")
        self.display("excellent choice!")
        self.display("now its time to choose your stats.")

        self.display("the way combat works in this game is as follows:")
        self.display("each creature you encounter will have a power and a toughness.")
        self.display("when you fight, you each roll a dice with a number")
        self.display("of sides equal to your power.")
        self.display("your opponents toughness is then reduced by the result.")
        self.display("if your toughness is less than 0, you die.")
        self.display("this gets repeated until someone dies.")
        self.display("when you finish combat, your toughness returns to its")
        self.display("original value.")
        self.display("its time to choose your power and toughness.")

        self.roll_stats()

        self.display("Lastly, what shall i call you?")
        self.display("Enter your name: ")
        self.player.name = input()

    def run_encounter(self, enemy):
        self.display(enemy.intro_text)
        
        while self.player.is_alive() and enemy.is_alive():
            action_options = ["attack"]
            if self.player.potions > 0:
                action_options.append("drink potion")
            action_options.append("hide")
            
            action = self.make_selection(action_options, "What do you do? ")
            
            if action == "attack":
                player_roll = random.randrange(1, self.player.power + 1)
                enemy.take_damage(player_roll)
                self.display(f"You roll a {player_roll}! the enemy's toughness is")
                self.display(f"now {enemy.toughness}.")

                if not enemy.is_alive():
                    self.display("you win the fight!")
                        
                    self.player.full_heal()
                    return True
            
            elif action == "drink potion":
                if self.player.drink_potion():
                    self.display(f"You drink a healing potion and restore 8 HP!")
                    self.display(f"You now have {self.player.toughness}/{self.player.max_toughness} HP.")
                    self.display(f"You have {self.player.potions} potion(s) left.")
                else:
                    self.display("You have no potions left!")
                    continue
            
            elif action == "hide":
                hide_chance = random.random()
                if hide_chance < 0.6:
                    self.display("You manage to hide! The enemy's attack misses you.")
                    continue
                else:
                    self.display("You fail to hide! The enemy spots you.")
            
            if not enemy.take_turn(self.player, self):
                return False
                
        return False

    def story(self):
        engine = StoryEngine(self)
        engine.run("script.tas")

    def main(self):
        self.select_text_mode()
        self.character_creation()
        self.story()

