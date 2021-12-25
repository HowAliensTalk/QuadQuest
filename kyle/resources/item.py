from resources.tools import *

class Item:

    class Types:
        Heal = 0
        DoubleDamage = 1
        IncreaseHP = 2
        IncreaseATK = 3
        IncreaseDEF = 4
        IncreaseSPD = 5
        Action = 6
        Misc = -1

    def __init__(self, name=None, is_disposable=False, type=None, *a, **k):
        assert name != None
        self.name = name
        self.is_disposable = is_disposable
        self.type = type

    def get_info(self):
        raise NotImplementedError()

    def use(self):
        raise NotImplementedError()



class HealItem(Item):


    def __init__(self, name, amt):
        super().__init__(name=name, is_disposable=True, type=Item.Types.Heal)
        self.amt = amt

    def __mul__(self, other):
        return self

    def use(self, target):
        old_health = target.health.val
        if target.health.diff_base_to_val() <= self.amt:
            target.health.restore_val()
        else:
            target.health.val += self.amt
        return target.name + " healed " + str(target.health.val - old_health) + " HP"


    def get_info(self):
        return "Restores " + str(self.amt) + " HP"


class DoubleDamageItem(Item):

    def __init__(self, name):
        super().__init__(name=name, is_disposable=True, type=Item.Types.DoubleDamage)

    def __mul__(self, other):
        return self

    def use(self, target):
        target.has_double_damage = True
        return target.name + " now has double damage!"

    def get_info(self):
        return "Good for One Sub-Level: Doubles Attack Damage Given"

class IncreaseHPItem(Item):

    def __init__(self, name, amt):
        super().__init__(name=name, is_disposable=True, type=Item.Types.IncreaseHP)
        self.amt = amt

    def use(self, target):
        target.health.base_val += self.amt
        target.health.val += self.amt
        return target.name + " increased base HP!"

    def get_info(self):
        return "Increases base HP by " + str(self.amt)


class IncreaseATKItem(Item):

    def __init__(self, name, amt):
        super().__init__(name=name, is_disposable=True, type=Item.Types.IncreaseATK)
        self.amt = amt

    def use(self, target):
        target.attack.base_val += self.amt
        target.attack.val += self.amt
        return target.name + " increased base ATK!"

    def get_info(self):
        return "Increases base ATK by " + str(self.amt)


class IncreaseDEFItem(Item):

    def __init__(self, name, amt):
        super().__init__(name=name, is_disposable=True, type=Item.Types.IncreaseDEF)
        self.amt = amt

    def use(self, target):
        target.defense.base_val += self.amt
        target.defense.val += self.amt
        return target.name + " increased base DEF!"

    def get_info(self):
        return "Increases base DEF by " + str(self.amt)

class IncreaseSPDItem(Item):

    def __init__(self, name, amt):
        super().__init__(name=name, is_disposable=True, type=Item.Types.IncreaseSPD)
        self.amt = amt

    def use(self, target):
        target.speed.base_val += self.amt
        target.speed.val += self.amt
        return target.name + " increased base SPD!"

    def get_info(self):
        return "Increases base SPD by " + str(self.amt)

class ActionItem(Item):

        def __init__(self, action):
            super().__init__(name=action.name, is_disposable=False, type=Item.Types.Action)
            self.action = action

        def get_info(self):
            return self.action.get_info() + " ["+ self.action.type.name +"] ─ DMG: " + (str(self.action.dmg) if self.action.dmg > 0 else " - ")


class ItemBag:

    def __init__(self, items={}, *a, **k):
        # Item : Qty
        self.items = items

    def remove(self, item):
        if self.items[item] == 1:
            self.items.pop(item)
        else:
            self.items[item] -= 1

    def add(self, new_item):
        item_names_in_bag = [item.name for item in list(self.items.keys())]

        if new_item.name not in item_names_in_bag:
            self.items[new_item] = 1
        else:

            self.items[self.get_item_by_name(new_item.name)] += 1

    def get_item_by_name(self, str):
        return [item for item in list(self.items.keys()) if item.name == str][0]

    def get_items(self):
        return self.items

    def use(self, item, target):
        msg = item.use(target)
        if item.is_disposable and item in self.items:
            self.remove(item)
        return msg

    def get_items_pretty_str(self):
        s = "\n"
        for item, qty in self.get_items().items():
            s += '- {:10}  ~ QTY: {}\n'.format(item.name, qty)
            s += '  └ {} \n'.format(item.get_info())
        return s

    def get_items_choices_pretty_str(self):
        count = 1
        s = ""
        for item, qty in self.get_items().items():
            s += '{}) {:10}  ~ QTY: {}\n'.format(count, item.name, qty)
            s += '    └ {} \n'.format(item.get_info())
            count += 1
        return s


class Hairties(int):

    def __init__(self, val=0):
        self.val = val
    # Ƕ
    def __str__(self):
        return str(self.val)

    def __sub__(self, other):
        return self.val - other.val

    def __add__(self, other):
        return self.val + other.val

    def __eq__(self, other):
        return self.val == other.val

    def __lt__(self, other):
        return self.val < other.val

    def __gt__(self, other):
        return self.val > other.val

    def __le__(self, other):
        return self.val <= other.val

    def __ge__(self, other):
        return self.val >= other.val

    def __ne__(self, other):
        return self.val != other.val
