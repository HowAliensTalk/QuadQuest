import time
import random

class Tools:

    @staticmethod
    def get_time_ms():
        return round(time.time() * 1000)

    @staticmethod
    def generate_id():
        return Tools.get_time_ms()

    @staticmethod
    def calc_damage(sender, target, action):
        if action.acc < 100:
            if random.randrange(0, 100) > action.acc:
                return 0

        dmg_out = round((action.dmg+sender.attack.val)*(100/(100+target.defense.val)))
        return dmg_out if action.type.id not in target.type.weakness else round(dmg_out * 1.75)
