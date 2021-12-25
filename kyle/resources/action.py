from resources.type import *
from resources.tools import *
from resources.stat import *

class Targets:
    _SELF = 0
    _OTHER = 1

class Action:


    def __init__(self, name, variable_name, type, dmg=1, pp=10, acc=100, info="Physical Attack", target=Targets._OTHER):
        self.name = name
        self.type = type
        self.dmg = dmg
        self.acc = acc
        self.target = target
        self.info = info
        self.variable_name = variable_name

    def perform(self, sender, target):
        dmg = Tools.calc_damage(sender, target, self)
        supereffective = self.type.id in target.type.weakness
        target.take_damage(dmg)

        msg = ""
        msg += sender.name + " used " + self.name + "!\n"
        if dmg == 0:
            msg += "Attack missed!\n"
        elif supereffective:
            msg += "It was super-effective!\n"

        msg += target.name + " took " + str(dmg) + " HP!"
        return msg

    def get_info(self):
        return self.info

    def restore_pp(self):
        pass

    def get_info_long(self):
        s = self.name + " [" + self.type.name + "]"
        s += "\n  ├ DMG: " + (str(self.dmg) if self.dmg > 0 else " - ")
        s += "\n  ├ ACC: " + str(self.acc)
        s += "\n  └ " + self.get_info()
        return s


# class AttackAction(Action):
#     def __init__(self, name, type, dmg=1, pp=5, acc=100):
#         super().__init__(name, type, dmg=dmg, pp=pp, acc=acc)

class SupportAction(Action):
    def __init__(self, name, variable_name, type, amt=0, pp=5, acc=100, target=Targets._OTHER, stats_affected=[], info="Status Effect Attack"):
        super().__init__(name, variable_name, type, dmg=0, pp=pp, acc=acc, info=info, target=target)
        self.stats_affected = stats_affected
        self.amt = amt

    def perform(self, sender, target):
        if self.target == Targets._SELF:
            target = sender

        s = sender.name + " used " + self.name + "\n"
        s += target.name + "'s:\n"

        def render(target_stat):
            s = ""
            if target_stat.val == 0:
                s += " └ " + target_stat.name + " won't go any lower!\n"
            else:
                inc_or_dec = "increased" if self.amt > 0 else  "decreased"
                target_stat.val += self.amt
                s += " └ " + target_stat.name + " "+ inc_or_dec + " by " + str(self.amt.__abs__()) + "\n"
            return s

        for stat in self.stats_affected:

            if stat == Attack:
                s += render(target.attack)
            elif stat == Defense:
                s += render(target.defense)
            elif stat == Speed:
                s += render(target.speed)
            elif stat == HP:
                s += render(target.health)

        return s.rstrip("\n")


class Actions:

    DEFAULT_ACTION = Action('Struggle', "DEFAULT_ACTION", NormalType(), 5)

    def __init__(self, actions={}):
        # self.actions = actions if len(actions) > 0 else [self.DEFAULT_ACTION
        # actions == {}
        if actions == {}:
            actions = {1: self.DEFAULT_ACTION}
        self.actions = actions

    def add(self, action):
        assert len(self.actions) <= 4
        self.actions[len(self.actions) + 1] = action

    def remove(self, action):
        pass

    def replace(self, old_action_pos, new_action):
        old_action = self.actions[old_action_pos]
        self.actions[old_action_pos] = new_action
        return old_action

    def get(self, action):
        return self.actions[action]

    def perform(self, sender, action, target):
        return self.actions[action].perform(sender, target)

    def get_actions_str(self):
        s = ""
        for ix in range(len(self.actions)):
            action = self.actions[ix+1]
            s += action.name + " [" + action.type.name + "]"
            s += "\n  ├ DMG: " + (str(action.dmg) if action.dmg > 0 else " - ")
            s += "\n  ├ ACC: " + str(action.acc)
            s += "\n  └ " + action.get_info() + "\n\n"

        return s

    def get_actions_choices(self):
        s = ""
        for ix in range(len(self.actions)):
            action = self.actions[ix+1]
            s += str(ix+1) + ") " + action.name
            s += "\n  └ DMG: " + (str(action.dmg) if action.dmg > 0 else " - ")
            s += "\n"
        return s

class DanceMoves:
    # Low end
    tendu = Action("Tendu", "DanceMoves.tendu", DanceType(), dmg=5, pp=30)
    frappe = Action("Frappe", "DanceMoves.frappe" , DanceType(), dmg=10, pp=25)
    degage = Action("Degage", "DanceMoves.degage", DanceType(), dmg=15, pp=30, acc=95)
    # Mid
    pirouette = Action("Pirouette", "DanceMoves.pirouette", DanceType(), dmg=30, pp=15)
    grande_battement = Action("Grande Battement", "DanceMoves.grande_battement", DanceType(), dmg=35, pp=15, acc=85)
    brisee = Action("Brisee", "DanceMoves.brisee", DanceType(), dmg=50, pp=10)
    # High end
    grand_jete_en_closhe_en_tournant = Action("Grande Jete en Closhe en Tournant", "DanceMoves.grand_jete_en_closhe_en_tournant", DanceType(), dmg=60, pp=10, acc=85)
    double_tour = Action("Double Tour", "DanceMoves.double_tour", DanceType(), dmg=100, pp=5, acc=80)
    saut_de_basque = Action("Saut de Basque", "DanceMoves.saut_de_basque", DanceType(), dmg=120, pp=5, acc=70)


class BugMoves:

    bitfire = Action("Bitfire", "BugMoves.bitfire",BugType(), dmg=5, pp=30)
    bitrage = Action("Bitrage", "BugMoves.bitrage",BugType(), dmg=5, pp=20)
    bityell = Action("Bityell", "BugMoves.bityell",BugType(), dmg=10, pp=20)

    method_overload = SupportAction("Method Overload", "BugMoves.method_overload", BugType(), amt=-4, pp=20, stats_affected=[Defense], info="Decrease target DEF by 4")
    stack_overflow = Action("Stack Overflow", "BugMoves.stack_overflow", BugType(), dmg=35, pp=15, acc=95)
    spirit_sap = Action("Spirit Sap", "BugMoves.spirit_sap", BugType(), dmg=30, pp=20, acc=95)
    woven_venom_blast = Action("Woven Venom Blast", "BugMoves.woven_venom_blast", BugType(), dmg=40, pp=10, acc=85)

    conversion = SupportAction("Conversion", "BugMoves.conversion", BugType(), amt=15, pp=5, stats_affected=[Attack, Defense], info="Increase own ATK, DEF by 20", target=Targets._SELF)
    c_matrix = Action("C-Matrix", "BugMoves.c_matrix", BugType(), dmg=70, pp=10, acc=80)
    lambda_x = Action("Lambda X:", "BugMoves.lambda_x", BugType(), dmg=140, pp=5, acc=95)


class NormalMoves:

    strike = Action("Strike", "NormalMoves.strike", NormalType(), dmg=10, pp=15)
    yeet = SupportAction("Yeet", "NormalMoves.yeet", NormalType(), amt=-2, pp=20, stats_affected=[Attack, Defense, Speed], info="Decreases target ATK, DEF, SPD by 2")
    pound = Action("Pound", "NormalMoves.pound", NormalType(), dmg=15, pp=20)
    slam = Action("Slam", "NormalMoves.slam", NormalType(), dmg=40, pp=20)
    bonk = Action("Bonk", "NormalMoves.bonk", NormalType(), dmg=40, pp=25, acc=90)
    want_want = SupportAction("Want Want", "NormalMoves.want_want", NormalType(), amt=10, pp=10, stats_affected=[Defense, Speed], info="Increase own DEF, SPD by 10", target=Targets._SELF)
    avalanche_chaos = Action("Avalanche Chaos", "NormalMoves.avalanche_chaos", NormalType(), dmg=80, pp=10, acc=85)

class DarkMoves:

    snarl = Action("Snarl", "DarkMoves.snarl", DarkType(), dmg=15, pp=20)
    foul_play = Action("Foul Play", "DarkMoves.foul_play", DarkType(), dmg=20, pp=30)
    devious_moonstrike = Action("Devious Moonstrike", "DarkMoves.devious_moonstrike", DarkType(), dmg=40, pp=10)
    j_slash = Action("J Slash", "DarkMoves.j_slash", DarkType(), dmg=50, pp=10, acc=80)
    nasty_plot = Action("Nasty Plot", "DarkMoves.nasty_plot", DarkType(), dmg=80, pp=10, acc=90)
    bitch_rage = Action("Bitch Rage", "DarkMoves.bitch_rage", DarkType(), dmg=100, pp=5, acc=100)

class FiendMoves:

    brute_slash = Action("Brute Slash", "FiendMoves.brute_slash", FiendType(), dmg=15, pp=20)
    imp_slash = Action("Imp Slash", "FiendMoves.imp_slash", FiendType(), dmg=20, pp=30)
    hellhaze = Action("Hellhaze", "FiendMoves.hellhaze", FiendType(), dmg=40, pp=20)
    darkmist = SupportAction("Dark Mist", "FiendMoves.darkmist", FiendType(), amt=-10, stats_affected=[Defense], info="Decreases target DEF by 10", target=Targets._OTHER)
    demonwish = SupportAction("Demonwish", "FiendMoves.demonwish", FiendType(), amt=-10, stats_affected=[Attack, Defense], info="Decreases target ATK, DEF by 10", target=Targets._OTHER)
    wicked_fire = Action("Wicked Fire", "FiendMoves.wicked_fire", FiendType(), dmg=75, pp=15, acc=95)
    affinity = Action("Affinity", "FiendMoves.affinity", FiendType(), dmg=90, pp=5, acc=70)


class CelestialMoves:

    moonblast = Action("Moonblast", "CelestialMoves.moonblast", CelestialType(), dmg=20, pp=10, acc=95)
    lightwish = SupportAction("Lightwish", "CelestialMoves.lightwish", CelestialType(), amt=5, pp=10, stats_affected=[Attack], info="Increases own ATK by 5", target=Targets._SELF)
    sunwish = SupportAction("Lightwish", "CelestialMoves.sunwish", CelestialType(), amt=15, pp=10, stats_affected=[Attack], info="Increases own ATK by 15", target=Targets._SELF)
    golf_le_fleur = Action("Golf Le Fleur", "CelestialMoves.golf_le_fleur", CelestialType(), dmg=80, pp=15)
    geomancy = Action("Geomancy", "CelestialMoves.geomancy", CelestialType(), dmg=65, pp=15)
    mist_ball = Action("Mist Ball", "CelestialMoves.mist_ball", CelestialType(), dmg=40, pp=20)
    sunbeam = Action("Sun Beam", "CelestialMoves.sunbeam", CelestialType(), dmg=140, pp=5, acc=85)
    starshift = Action("Starshift", "CelestialMoves.starshift", CelestialType(), dmg=100, pp=10, acc=50)


def get_move_by_str(str):
    return eval(str)
# https://bulbapedia.bulbagarden.net/wiki/List_of_moves
