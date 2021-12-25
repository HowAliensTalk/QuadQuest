from resources.item import *
from resources.colors import *
from resources.action import NormalMoves

class ShopItemPair:

    def __init__(self, item, hairties):
        self.item = item
        self.hairties = hairties


class Shop:

    def __init__(self, name):
        self.name = name
        # Endless Item Bag
        self.items = {
                1: ShopItemPair(HealItem("Black Coffee", 20), Hairties(20)),
                2: ShopItemPair(HealItem("Espresso", 60), Hairties(40)),
                3: ShopItemPair(HealItem("Americano", 100), Hairties(80)),
                4: ShopItemPair(HealItem("Capuccino", 300), Hairties(140)),
                5: ShopItemPair(IncreaseHPItem("Pirouette Frappé", 50), Hairties(100)),
                6: ShopItemPair(IncreaseATKItem("Malfunction Frappé", 5), Hairties(300)),
                7: ShopItemPair(IncreaseDEFItem("Molten Frappé", 5), Hairties(300)),
                8: ShopItemPair(IncreaseSPDItem("Pas Frappé", 5), Hairties(300)),
                9: ShopItemPair(ActionItem(NormalMoves.avalanche_chaos), Hairties(800)),
                10: ShopItemPair(DoubleDamageItem("Fouetté Latté"), Hairties(1000)),

                # Item(),
                # Item(),
                # Item(),
                # Item(),
                # Item()
            }


    def display_items(self):
        s = "\n"
        for count, sip in self.items.items():
            s += '{}{}) {:20} ɦ {:} \n'.format(Colors.Green, count, sip.item.name, str(sip.hairties))
            s += '{}    └ {} \n\n{}'.format(Colors.Cyan, sip.item.get_info(), Colors.Green)
        return s

    def display_shop(self):
        pass


    def give_item(self, item, target):
        self.target.take_item(item)

    def preview_item(self, item):
        pass

    def get_items(self):
        return self.items.items()
