import re


class StoryEngine:
    def __init__(self, game):
        self.label_order = None
        self.game = game
        self.script = {}

    # ----------------------------
    # PUBLIC ENTRY POINT
    # ----------------------------

    def run(self, script_path):
        self.script = self.load_script(script_path)
        current_label = "start"

        while True:
            if current_label not in self.script:
                self.game.display(f"Script error: label '{current_label}' not found.")
                return

            block = self.script[current_label]
            jumped = False

            i = 0
            while i < len(block):
                line = block[i].strip()

                # Plain text
                if not line.startswith("#"):
                    processed = self.process_line(line)
                    if processed:
                        self.game.display(processed)
                    i += 1
                    continue

                # Choice
                if line.startswith("#choice"):
                    prompt = line.replace("#choice", "").strip()
                    options = {}
                    i += 1

                    while not block[i].startswith("#endchoice"):
                        choice_line = block[i].strip()
                        text, target = choice_line.split("->")
                        text = text.strip().strip('"')
                        target = target.strip()
                        options[text] = target
                        i += 1

                    selection = self.game.make_selection(
                        list(options.keys()),
                        prompt if prompt else "What do you do? "
                    )

                    current_label = options[selection]
                    jumped = True
                    break

                # Encounter
                if line.startswith("#encounter"):
                    enemy_name = line.split()[1]
                    outcomes = {}
                    i += 1

                    while not block[i].startswith("#endencounter"):
                        outcome_line = block[i].strip()
                        key, target = outcome_line.split("->")
                        outcomes[key.strip()] = target.strip()
                        i += 1

                    enemy = self.create_enemy(enemy_name)

                    if self.game.run_encounter(enemy):
                        current_label = outcomes.get("win")
                    else:
                        current_label = outcomes.get("lose")

                    jumped = True
                    break

                # Goto
                if line.startswith("#goto"):
                    current_label = line.split()[1]
                    jumped = True
                    break

                # End
                if line.startswith("#end"):
                    return

                i += 1

            if not jumped:
                current_index = self.label_order.index(current_label)

                if current_index + 1 >= len(self.label_order):
                    return  # no more labels, end story

                current_label = self.label_order[current_index + 1]

    # ----------------------------
    # SCRIPT LOADING
    # ----------------------------

    def load_script(self, path):
        script = {}
        label_order = []
        current_label = "start"

        script[current_label] = []
        label_order.append(current_label)

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")

                if line.startswith(";"):
                    current_label = line[1:].strip()
                    script[current_label] = []
                    label_order.append(current_label)
                else:
                    script[current_label].append(line)

        self.label_order = label_order
        return script

    # ----------------------------
    # VARIABLE PROCESSING
    # ----------------------------

    def process_line(self, line):
        def replacer(match):
            content = match.group(1).strip()

            # Stat modification
            if "+=" in content:
                obj, value = content.split("+=")
                obj = obj.strip()
                value = int(value.strip())

                if obj == "player.potions":
                    self.game.player.potions += value
                    return str(self.game.player.potions)

            # Simple variables
            if content == "player.name":
                return self.game.player.name
            if content == "player.race":
                return self.game.player.race
            if content in ("player.class", "player.pc"):
                return self.game.player.pc
            if content == "player.potions":
                return str(self.game.player.potions)

            return ""

        return re.sub(r"\{([^}]+)}", replacer, line)

    # ----------------------------
    # ENEMY FACTORY
    # ----------------------------

    def create_enemy(self, name):
        name = name.lower()

        if name == "goblin":
            import goblin
            return goblin.Goblin()

        if name == "frostelemental":
            import elemental
            return elemental.FrostElemental()

        self.game.display(f"Unknown enemy: {name}")
        return None
