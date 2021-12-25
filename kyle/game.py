from file import *
from input import *
from resources.character import *
from resources.tools import *
from resources.colors import Colors
from resources.shop import *
from resources.action import *
from resources.type import *
import sys

# ===================================================================
# OTHER
# ===================================================================

class Game:

    TITLE = "Quad Quest"
    GAME_CREDITS = """

               Quad Quest

                Credits

             ┌ Created By ┐

             ┌ Developers ┐
              Dylan Greko

            ┌ Design Team ┐
            Nick Bartolotti
            Jillian Van Cura
             Claire Cordano
            Christian Knopp
              Adam Butler

 I hope you had a wonderful Christmas.
     This game was an exercise for
    me in that I used stuff in here
     I hardly ever use for my job.
    It was pretty satisfying and it
    showed me the joy of programming
     in full color. I've never done
     something like this for anyone
    so I guess this is my little way
    of showing you how much you mean
    to me. Thank you for being you.
     Continue being sexy..as always.
            Love you, buddy.

         - Other Sexy Man, Dyl


"""

    class Options:
        SHOP = 1
        BATTLE = 2
        CHARACTER = 3
        HELP = 4
        SAVE = 5
        EXIT = 6



    def __init__(self):
        self.input = InputManager()
        self.loaded_from_save = False
        self.print_title()
        if not self.preview_save_data():
            self.game_file = GameFile('game.txt', self.input)
            self.init_intro()
        else:
            while True:
                usr_choice = self.input.prompt("Load last save?", command="[Y/N]", is_numeric=False)
                if usr_choice.lower() == "y":
                    self.loaded_from_save = True
                    self.load_save_data()
                    break
                elif usr_choice.lower() == "n":
                    self.game_file = GameFile('game.txt', self.input)
                    self.init_intro()
                    break

        self.is_playing = False
        self.is_performing_action = False
        self.in_battle = False
        self.in_shop = False
        self.in_inspecting_character = False
        self.levels = {
            1: {
                1: [Minion('Bug Overflow', BugType(), 25, 5, 5, 10,
                        actions=Actions({1: BugMoves.bitfire, 2: BugMoves.bitrage, 3: BugMoves.method_overload})),
                    Minion('Bug Error', BugType(), 25, 5, 5, 10,
                        actions=Actions({1: BugMoves.bitfire, 2: BugMoves.bitrage, 3: BugMoves.method_overload}))],
                2: [Minion('Joedy Grunt', DarkType(), 55, 6, 10, 6,
                        actions=Actions({1: DarkMoves.snarl, 2: DarkMoves.foul_play, 3: NormalMoves.bonk}))]
                }, # Done
            2: {
                1: [Minion("Maddie Goblin", FiendType(), 55, 10, 20, 2,
                        actions=Actions({1: FiendMoves.imp_slash, 2: FiendMoves.brute_slash, 3: BugMoves.method_overload})),
                    MiniBoss("Crystallized Phalanx", CelestialType(), 75, 10, 25, 5,
                        actions=Actions({1: CelestialMoves.moonblast, 2: NormalMoves.yeet, 3: DanceMoves.grande_battement, 4: FiendMoves.brute_slash}))],
                2: [MiniBoss("Maddie Gargoyle of Baddance", DanceType(), 105, 15, 12, 15,
                        actions=Actions({1: DanceMoves.pirouette, 2: DanceMoves.degage, 3: CelestialMoves.lightwish}))],
                3: [Minion("Bug Overflow", BugType(), 75, 20, 70, 40,
                        actions=Actions({1: BugMoves.bitfire, 2: BugMoves.bitrage, 3: BugMoves.method_overload})),
                    Minion("Bug Overflow", BugType(), 75, 22, 70, 40,
                            actions=Actions({1: BugMoves.bitfire, 2: BugMoves.bitrage, 3: BugMoves.method_overload})),
                    Minion("Bug Overflow", BugType(), 75, 25, 70, 40,
                            actions=Actions({1: BugMoves.bitfire, 2: BugMoves.bitrage, 3: BugMoves.method_overload}))
                        ],
                }, # Done
            3: {
                1: [Minion("Parasitic Joedy Craigspider", BugType(), 100, 45, 20, 15,
                        actions=Actions({1: BugMoves.woven_venom_blast, 2: BugMoves.method_overload, 3: NormalMoves.slam, 4: CelestialMoves.lightwish})),
                    Minion("Rudderless Client of Want", NormalType(), 70, 40, 40, 20,
                        actions=Actions({1: NormalMoves.bonk, 2: NormalMoves.want_want, 3: DarkMoves.foul_play})),
                    Minion("Rudderless Client of Want", NormalType(), 100, 40, 40, 20,
                        actions=Actions({1: NormalMoves.bonk, 2: NormalMoves.want_want, 3: DarkMoves.foul_play})),
                    Minion("Rudderless Client of Want", NormalType(), 120, 40, 40, 20,
                        actions=Actions({1: NormalMoves.bonk, 2: NormalMoves.want_want, 3: DarkMoves.foul_play})),
                    ],
                2: [
                    MiniBoss("Crystal Client of Confusion", FiendType(), 200, 30, 40, 10,
                        actions=Actions({1: CelestialMoves.golf_le_fleur, 2: CelestialMoves.lightwish, 2: FiendMoves.brute_slash})),
                    MiniBoss("Fiendish Batwing Demon", FiendType(), 170, 40, 40, 30,
                        actions=Actions({1: FiendMoves.imp_slash, 2: FiendMoves.hellhaze, 3: FiendMoves.darkmist}))
                ],
                3: [
                    MiniBoss("Maddie Gargoyle of Soredance", DanceType(), 165, 30, 20, 15,
                            actions=Actions({1: DanceMoves.pirouette, 2: DanceMoves.grande_battement, 3: CelestialMoves.lightwish})),
                    MiniBoss("Maddie Gargoyle of Trashdance", DanceType(), 165, 30, 20, 15,
                            actions=Actions({1: DanceMoves.pirouette, 2: DanceMoves.grande_battement, 3: CelestialMoves.lightwish})),
                    MiniBoss("Maddie Gargoyle of Uglydance", DanceType(), 185, 30, 20, 15,
                            actions=Actions({1: DanceMoves.pirouette, 2: DanceMoves.grande_battement, 3: CelestialMoves.lightwish})),
                    Boss("Courtney", NormalType(), 300, 45, 50, 20,
                        actions=Actions({1: NormalMoves.want_want, 2: NormalMoves.bonk, 3: DarkMoves.devious_moonstrike, 4: FiendMoves.darkmist}))
                ],
                4: [Boss("Resurrected Courtney", DarkType(), 360, 40, 55, 20,
                    actions=Actions({1: NormalMoves.want_want, 2: DarkMoves.j_slash, 3: DarkMoves.devious_moonstrike, 4: FiendMoves.darkmist}))]
                },
            4: {
                1: [
                    Minion("Mad Die Spider", BugType(), 250, 30, 70, 45,
                            actions=Actions({1: BugMoves.woven_venom_blast, 2: BugMoves.conversion, 3: NormalMoves.bonk})),
                    Minion("Crystallized Mad Die Spider", CelestialType(), 270, 40, 40, 40,
                            actions=Actions({1: CelestialMoves.geomancy, 2: BugMoves.conversion, 3: CelestialMoves.starshift})),
                    Minion("Undead Mad Die Spider", FiendType(), 220, 45, 20, 40,
                            actions=Actions({1: FiendMoves.darkmist, 2: BugMoves.conversion, 3: FiendMoves.wicked_fire})),
                ],
                2: [
                    Minion("Bloathead Joedy Slavespider", BugType(), 400, 50, 40, 35,
                            actions=Actions({1: BugMoves.c_matrix, 2: FiendMoves.affinity, 3: FiendMoves.darkmist, 4: DarkMoves.nasty_plot}))
                ],
                3: [
                    Minion("Undead Mad Die Spider", FiendType(), 150, 20, 20, 40,
                            actions=Actions({1: FiendMoves.darkmist, 2: BugMoves.conversion, 3: FiendMoves.wicked_fire})),
                    Boss("Joedy", FiendType(), 500, 40, 60, 60,
                        actions=Actions({1: DarkMoves.bitch_rage, 2: FiendMoves.affinity, 3: FiendMoves.demonwish, 4: DarkMoves.j_slash}))
                ],
                4: [
                    Boss("Resurrected Joedy", DarkType(), 600, 50, 50, 65,
                        actions=Actions({1: DarkMoves.bitch_rage, 2: FiendMoves.affinity, 3: FiendMoves.demonwish, 4: DarkMoves.j_slash}))
                ]
            }
        }

        self.rewards = {
            1: {
                1: [Hairties(100)],
                2: [Hairties(75), BugMoves.stack_overflow],
                },
            2: {
                1: [Hairties(700)],
                2: [Hairties(500)],
                3: [Hairties(500), DanceMoves.brisee]
                },
            3: {
                1: [Hairties(750), BugMoves.conversion],
                2: [Hairties(900), CelestialMoves.golf_le_fleur],
                3: [Hairties(1000), NormalMoves.want_want],
                4: [Hairties(1500), FiendMoves.wicked_fire]
                },
            4: {
                1: [Hairties(1200), BugMoves.lambda_x],
                2: [Hairties(1100), DanceMoves.saut_de_basque],
                # 3: [Hairties(2000), CelestialMoves.sunbeam],
                3: [Hairties(10), "2 Comp Tickets"]
                }

        }

        self.menu_options = {
            Game.Options.SHOP: 'Shop',
            Game.Options.BATTLE: 'Battle',
            Game.Options.CHARACTER: 'Inspect Character',
            Game.Options.HELP: 'Help',
            Game.Options.SAVE: 'Save',
            Game.Options.EXIT: 'Exit'
        }

        if not self.loaded_from_save:
            self.level = 1
            self.sub_level = 1
            self.kyle = Kyle("Kyle", DanceType(), 100, 15, 10, 20, Actions({1: DanceMoves.tendu, 2: NormalMoves.yeet}))
            # actions={1: DanceMoves.tendu, 2: NormalMoves.yeet, 3: BugMoves.stack_overflow, 4: NormalMoves.avalanche_chaos}
            # actions={1: DanceMoves.tendu, 2: NormalMoves.yeet, 3: BugMoves.lambda_x}
        self.last_level = len(self.levels)
        self.last_sub_level = len(self.levels[self.last_level])
        # self.kyle.attack = Attack(1000)
        self.shop = Shop(name="Claire's Curio Shop")
        self.play()

    def play(self):
        self.is_playing = True
        while self.is_playing:

            while self.level <= len(self.levels):
                # Show Kyle options for Shop, Battle, and Character
                choice = self.input.prompt(self.get_options(), title='Menu', choices=[val + 1 for val in range(len(self.menu_options))], is_numeric=True, color=Colors.White)

                if choice == Game.Options.SHOP:
                    self.go_to_shop()


                elif choice == Game.Options.BATTLE:
                    self.input.typeout_speed = 50
                    kyle_before_battle = self.kyle.copy()
                    double_damage_items_before_battle = len(self.kyle.item_bag.items)
                    battle_won = self.battle()
                    if battle_won:
                        self._reward()
                        if self.sub_level < len(self.levels[self.level]):
                            self.sub_level += 1
                        else:
                            self.sub_level = 1
                            self.level += 1

                        if self.level > self.last_level and self.last_sub_level > self.sub_level:
                            self.input.prompt("YOU WON THE GAME!")
                            self.save_game()
                            self.show_credits()

                    else:
                        # Prompt fuck, you died nerd
                        self.input.border_msg("YOU DIED!", char="~", color=Colors.Red)
                        for enemy in self.levels[self.level][self.sub_level]:
                            enemy.restore_pp()
                            enemy.restore_stats(health=True)

                        self.kyle = kyle_before_battle
                        self.kyle.item_bag.items = {DoubleDamageItem("Fouetté Latté"): double_damage_items_before_battle}

                elif choice == Game.Options.CHARACTER:
                    self.inspect_character()

                elif choice == Game.Options.HELP:
                    self.input.stdoutln("\n")
                    self.input.reverse_color_msg("Weakness Chart")
                    self.input.stdoutln(WEAKNESS_CHART)
                    self.input.stdoutln("\n\n   ■ Battle items are good for one sub-level")
                    self.input.stdoutln("\n   ■ All stats are restored to their base value at the end of each battle except for HP")
                    self.input.stdoutln("\n   ■ HP is restored at the shop")
                    self.input.stdoutln("\n   ■ Hairties are your currency symbolized by 'ɦ'")
                    self.input.stdoutln("\n   ■ SPD plays a factor in who attacks before the other. This can change mid-battle.")
                    self.input.prompt("Enter any key to return")

                elif choice == Game.Options.EXIT:
                    usr_choice = self.input.prompt("Quitting game...", title="Save and Exit?", command="Enter 1 to Save and Exit\nEnter 2 to Exit without saving", choices=[1,2], is_numeric=True)
                    if usr_choice == 1:
                        self.save_game()
                        self.input.stdoutln("GOODBYE..." + Colors.Reset)
                        sys.exit(1)
                    elif usr_choice == 2:
                        self.input.stdoutln("GOODBYE..." + Colors.Reset)
                        sys.exit(1)

                elif choice == Game.Options.SAVE:
                    self.save_game()

            self.is_playing = False

    def battle(self):
        # Returns 0 if user died, 1 if all lore died
        self.in_battle = True
        lore_in_sub_level = self.levels[self.level][self.sub_level]
        lore_killed = 0 # counter
        used_item_for_battle = False
        assert self.kyle.is_alive()
        self._prompt_items_for_battle()

        # Battle loop
        while lore_killed < len(lore_in_sub_level) and self.kyle.is_alive():
            clore = lore_in_sub_level[lore_killed]


            self.input.set_color(Colors.Yellow)
            self.input.typeout("A wild " + clore.name + " [" + str(clore.type.name) + "]"+ " appeared!!")
            self.input.stdoutln()

            def hp():
                hp_printout = '\n{:15} {:15}\n{:15} {:15}\n\n'.format(self.kyle.name, clore.name, self.kyle.health.fraction_str().rstrip("\n"), clore.health.fraction_str().rstrip("\n"))
                self.input.color_msg(hp_printout, Colors.Cyan)

            hp()

            # Enter battle
            first_flag = 1
            while clore.is_alive() and self.kyle.is_alive():
                first = self.kyle if self.kyle.speed > clore.speed else clore

                def bot_move():
                    bot_choice = self.input.border_msg(clore.perform_action(random.randrange(1, len(clore.moveset.actions) + 1), self.kyle), char='#', color=Colors.Green)

                def usr_move():
                    hp()
                    usr_choice = self.input.prompt(self.kyle.get_actions_choices(), title="Your move", command="Choose a move!", choices=[val + 1 for val in range(len(self.kyle.moveset.actions))], is_numeric=True, color=Colors.Yellow)
                    self.input.border_msg(self.kyle.perform_action(usr_choice, clore), char="#", color=Colors.White)

                # Determine First

                if first_flag and first == self.kyle:
                    # User choice
                    usr_move()
                elif first_flag and first == clore:
                    # Bot move
                    bot_move()
                elif not first_flag and first == self.kyle:
                    # Bot choice
                    bot_move()
                elif not first_flag and first == clore:
                    # User choice
                    usr_move()

                first_flag = not first_flag

            if self.kyle.is_alive():
                lore_killed += 1
                hp()
                self.kyle.restore_stats(health=False)
                self.input.border_msg("You killed " + clore.name + "!")
                if lore_killed < len(lore_in_sub_level):
                    usr_choice = self.input.prompt("", command="Enter any key to continue to the next battle...", color=Colors.Green)
                self.input.stdoutln("\n\n\n\n")
            else:
                hp()

        self.kyle.restore_pp()
        if self.kyle.has_double_damage:
            self.kyle.has_double_damage = False
        self.in_battle = False
        return lore_killed == len(lore_in_sub_level) and self.kyle.is_alive() # True or false

    def _reward(self):
        rewards = self.rewards[self.level][self.sub_level]
        msg = "Level " + str(self.level) + " Part " + str(self.sub_level) + " CLEARED!\n"
        for reward in rewards:
            if type(reward) == Hairties:
                self.kyle.hairties += reward
                msg += "You earned ɦ " + reward.__str__() + "!\n"
            elif type(reward) in [Action, SupportAction]:
                if len(self.kyle.moveset.actions) < 4:
                    # Add move
                    self.kyle.moveset.add(reward)
                    msg += "You learned " + reward.name + "!\n"

                else: # len(self.kyle.moveset.actions) == 4:
                    self.input.stdoutln(Colors.White + "You earned:\n"  + reward.get_info_long())

                    usr_choice = self.input.prompt("Must make room for move...\n"+ self.kyle.moveset.get_actions_choices(), command="Which move should be removed? Enter 0 to not learn move", choices=[val + 1 for val in range(len(self.kyle.moveset.actions))] + [0] , is_numeric=True, color=Colors.White)
                    if usr_choice == 0:
                        self.input.border_msg("You did not learn " + reward.name)
                    else:
                        old_action = self.kyle.moveset.replace(usr_choice, reward)
                        self.input.border_msg(old_action.name + " was replaced with " + reward.name, char="═» ")
            elif type(reward) == str:
                msg += "You earned " + reward + "! Finally!!"

        self.input.border_msg(msg.rstrip("\n"), char="@")

    def _prompt_items_for_battle(self):
        if len(self.kyle.item_bag.items) == 0:
            self.input.border_msg("No items to use...battle is starting!", char="*", color=Colors.White)
            self.input.stdoutln("\n")
        else:

            START = 0
            while True:
                message = "\n" + self.kyle.item_bag.get_items_choices_pretty_str()
                usr_choice = self.input.prompt(message, title="Use Battle Items", choices=[val + 1 for val in range(len(self.kyle.item_bag.items))] + [0], command="Choose item(s) to use in battle - Enter 0 to start",
                is_numeric=True, color=Colors.White)

                if usr_choice == START:
                    break

                msg = self.kyle.item_bag.use(list(self.kyle.item_bag.items.keys())[usr_choice -1], self.kyle)
                self.input.border_msg(msg, char="%", color=Colors.White)

                if len(self.kyle.item_bag.items) == 0:
                    break

            self.input.stdoutln("» "*25 + "\n")

    def inspect_character(self):
        self.in_inspecting_character = True
        message = "Level " + self.level.__str__() + " Part " + self.sub_level.__str__() + "\n"
        message += "\n" + self.kyle.str_stats() + "\n"
        hairties = "ɦ " + self.kyle.hairties.__str__() + "\n"
        message += self.input.border(char="-", len=len(hairties), end="\n")
        message += hairties + self.input.border(char="-", len=len(hairties), end="")
        message += "\n\nItem Sack: " + self.kyle.item_bag.get_items_pretty_str()
        self.input.prompt(message, title='Character Inspect', command='Enter any key to return', color=Colors.Yellow)
        self.in_inspecting_character = False

    def go_to_shop(self):
        self.in_shop = True
        self.input.set_color(Colors.Green)
        self._shop_intro()
        LEAVE_SHOP = 0

        usr_choice = None
        while True:

            # Print current hairties and bag items
            character_info = "Hairties: " + self.kyle.hairties.__str__() + "\n"
            character_info += self.kyle.health.fraction_str()
            # Get his choice
            usr_choice = self.input.prompt(character_info,
                    choices=[val for val in range(len(self.shop.get_items()) + 1)],
                    color=Colors.Green,
                    is_numeric=True
                )
            if usr_choice == LEAVE_SHOP:
                break

            shopitem = self.shop.items[usr_choice]
            self._handle_shop_choice(shopitem)

        self.input.stdoutln("\n")
        self.input.color_msg('"Good riddance!" - Claire', Colors.Cyan)
        self.in_shop = False

    def _shop_intro(self):
        self.input.stdoutln("\n")
        self.input.reverse_color_msg(self.shop.name)
        self.input.stdoutln(self.shop.display_items())
        self.input.stdoutln('"Fuckin Kyle. What do YOU want?" - Claire\nEnter 0 to leave shop')

    def _handle_shop_choice(self, shop_item):
        if self.kyle.hairties - shop_item.hairties < 0:
            self.input.border_msg("Insufficient Funds!", char="*", color=Colors.Red)
            return

        message = ""
        item_message = ""
        item_bought = False
        if shop_item.item.type == Item.Types.Heal:

            if not self.kyle.is_healed():
                item_message = shop_item.item.use(self.kyle)
                item_bought = True
            else:
                message = "You are already healed, nerd! No mo' heal"

        elif shop_item.item.type == Item.Types.DoubleDamage:
            self.kyle.item_bag.add(shop_item.item)
            item_bought = True


        elif shop_item.item.type in [Item.Types.IncreaseHP, Item.Types.IncreaseATK, Item.Types.IncreaseDEF, Item.Types.IncreaseSPD]:

            item_message = shop_item.item.use(self.kyle)
            item_bought = True


        elif shop_item.item.type == Item.Types.Action:
            if shop_item.item in self.kyle.moveset.actions:
                message = "You already have this move!"
            elif len(self.kyle.moveset.actions) < 4:
                self.kyle.moveset.add(shop_item.item.action)
            elif len(self.kyle.moveset.actions) == 4:
                usr_choice = self.input.prompt("Must make room for move...\n" + self.kyle.moveset.get_actions_choices(), command="Which move should be removed?", choices=[val + 1 for val in range(len(self.kyle.moveset.actions))], is_numeric=True, color=Colors.White)
                old_action = self.kyle.moveset.replace(usr_choice, shop_item.item.action)
                self.input.border_msg(old_action.name + " was replaced with " + shop_item.item.action.name, char="═» ")
            # Add action if enough space if not replace one
            item_bought = True

        if item_bought:
            self.kyle.hairties -= shop_item.hairties
            message = "You bought " + shop_item.item.name + "!"

        self.input.border_msg(message + ("\n" + item_message if item_message else ""), char="*", color=Colors.White)

    def out(self, msg):
        self.input.out(msg)

    def get_options(self):
        s = ''
        for option, name in self.menu_options.items():
            s += str(option) + ') ' + name + '\n'
        return s

    def init_intro(self):
        self.game_file.next_line()

    def print_title(self):
        s = """
           ____                 _     ____                 _
          /___ \_   _  __ _  __| |   /___ \_   _  ___  ___| |_
         //  / / | | |/ _` |/ _` |  //  / / | | |/ _ \/ __| __|
        / \_/ /| |_| | (_| | (_| | / \_/ /| |_| |  __/\__ \ |_
        \___,_\ \__,_|\__,_|\__,_| \___,_\ \__,_|\___||___/\__|

        """
        self.input.stdoutln(s)

    def show_credits(self):
        self.input.out(self.GAME_CREDITS)

    def save_game(self):
        self.input.stdoutln("Saving game...")
        with open("save.txt", "w") as save_file:
            # Level and sub level
            save_data = {"LEVEL": self.level, "SUB_LEVEL": self.sub_level}
            for key, value in save_data.items():
                save_file.write(key + " " + value.__str__() + "\n")

            for key, value in self.kyle.save_data().items():
                s = ""
                for item in value:
                    s += item.__str__() + " "

                save_file.write(key + " " + s + "\n")
        self.input.stdoutln("Game saved!")

    def preview_save_data(self):
        try:
            with open("save.txt", "r") as save_file:
                return len(save_file.read().split("\n")) > 1
        except:
            return False

    def load_save_data(self):
        data = {}
        with open("save.txt", "r") as save_file:
            for line in save_file.read().split("\n"):
                try:
                    items = line.split(" ")
                    if '' in items:
                        items.remove('')

                    if len(items) < 2:
                        pass

                    elif items[0] in ["ITEMS", "MOVES", "HP"]:
                        for idx in range(1, len(items)):
                            if items[0] in data:
                                data[items[0]].append(items[idx])
                            else:
                                data[items[0]] = [items[idx]]
                    else:
                        data[items[0]] = int(items[1])
                except Exception as e:
                    # Except silently
                    pass

        moves = {}
        for count, move in enumerate(data["MOVES"]):
            moves[count + 1] = get_move_by_str(move)

        items = ItemBag()
        if "ITEMS" in data:
            for item in data["ITEMS"]:
                items.add(eval(item+"('Fouetté Latté')"))

        self.kyle = Kyle("Kyle", DanceType(),
            int(data["HP"][0]),
            data["ATK"],
            data["DEF"],
            data["SPD"],
            Actions(moves))
        self.kyle.health.base_val = int(data["HP"][1])
        self.kyle.item_bag = items
        self.kyle.hairties = data["HAIRTIES"]
        self.level = data["LEVEL"]
        self.sub_level = data["SUB_LEVEL"]


if __name__ == "__main__":
    g = Game()
