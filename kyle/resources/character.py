from resources.stat import *
from resources.action import *
from resources.type import *
from resources.colors import Colors
from resources.item import *

# ===================================================================
# CHARACTER
# ===================================================================

class Entity:

    def __init__(self, interactable=True, *a, **k):
        self.interactable = interactable

class CharacterIDs:
    Kyle = 0
    Minion = 1
    Boss = 2
    MiniBoss = 3

class CharacterInterface(Entity):

    def take_damage(self, dmg):
        pass

    def give_damage(self, other, dmg):
        pass

    def take_item(self, item):
        pass

    def use_item(self, item):
        pass


class Character(CharacterInterface):
    def __init__(self, name, type, hp, atk, df, spd, char_id, actions=Actions()):
        super().__init__()
        self.name = name
        self.type = type
        self.char_id = char_id
        self.health = HP(hp)
        self.attack = Attack(atk)
        self.defense = Defense(df)
        self.speed = Speed(spd)
        self.moveset = actions
        self.item_bag = ItemBag()
        self._has_double_damage = False

    @property
    def has_double_damage(self):
        return self._has_double_damage

    @has_double_damage.setter
    def has_double_damage(self, bool):
        if bool:
            self.attack.val *= 2
        else:
            self.attack.restore_val()

    def take_damage(self, dmg):
        self.health.val -= dmg

    def perform_action(self, action, target):
        return self.moveset.perform(self, action, target)

    def restore_stats(self, health=False):
        self.attack.restore_val()
        self.defense.restore_val()
        self.speed.restore_val()
        if health:
            self.health.restore_val()

    def add_item(self, item):
        self.item_bag.add(item)

    def str_stats(self):
        s =  self.name + "\n\n"
        s += "TYPE: " + self.type.name + "\n"
        # FUTURE:
        # Print out reverse color progress bar for health
        s += "HP  : " + str(self.health.val) + "/" + str(self.health.base_val) + "\n"
        s += "ATK : " + str(self.attack.val) + "\n"
        s += "DEF : " + str(self.defense.val) + "\n"
        s += "SPD : " + str(self.speed.val) + "\n\n"
        s += "MOVES: \n" + self.get_actions_str()
        return s

    def reduce_str_stats(self):
        s = "TYPE: " + self.type.name + "\n"
        s += "HP  : " + str(self.health.val) + "/" + str(self.health.base_val)
        return s

    def is_alive(self):
        return self.health.val > 0

    def is_dead(self):
        return not self.is_alive()

    def current_health(self):
        return self.health.val

    def is_healed(self):
        return self.current_health() == self.health.base_val

    def get_actions_str(self):
        return self.moveset.get_actions_str()

    def get_actions_choices(self):
        return self.moveset.get_actions_choices()

    def restore_pp(self):
        for ix in range(len(self.moveset.actions)):
            self.moveset.actions[ix+1].restore_pp()

class Minion(Character):

    def __init__(self, name, type, hp, atk, df, spd, actions=Actions()):
        super().__init__(name, type, hp, atk, df, spd, CharacterIDs.Minion, actions=actions)

class MiniBoss(Character):

    def __init__(self, name, type, hp, atk, df, spd, actions=Actions()):
        super().__init__(name, type, hp, atk, df, spd, CharacterIDs.MiniBoss, actions=actions)

class Boss(Character):

    def __init__(self, name, type, hp, atk, df, spd, actions=Actions()):
        super().__init__(name, type, hp, atk, df, spd, CharacterIDs.Boss, actions=actions)

class Kyle(Character):

    def __init__(self, name, type, hp, atk, df, spd, actions):
        super().__init__(name, type, hp, atk, df, spd, CharacterIDs.Kyle, actions=actions)
        self.hairties = Hairties(120)

    def rand_inc_stats(self):
        self.health.inc_base_val(random.randrange(5, 15))
        self.attack.inc_base_val(random.randrange(2, 7))
        self.defense.inc_base_val(random.randrange(2, 10))
        self.speed.inc_base_val(random.randrange(1, 7))

    def copy(self):
        _copy = Kyle("Kyle", DanceType(), self.health.base_val, self.attack.val, self.defense.val, self.speed.val, actions=self.moveset)
        _copy.health.val = self.health.val
        _copy.hairties = self.hairties
        _copy.item_bag.items = self.item_bag.items
        return _copy

    def save_data(self):
        return {
            "HP": [self.health.val, self.health.base_val],
            "ATK": [self.attack.val],
            "DEF": [self.defense.val],
            "SPD": [self.speed.val],
            "HAIRTIES": [self.hairties],
            "MOVES": [move.variable_name for move in list(self.moveset.actions.values())],
            "ITEMS": [item.__class__.__name__ for item in self.item_bag.items]
        }
