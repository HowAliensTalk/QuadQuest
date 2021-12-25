class Stat:

    def __init__(self, name, _val):
        self.name = name
        self._val = _val
        self.base_val = _val

    def __lt__(self, other):
        return self._val < other._val

    def __gt__(self, other):
        return self._val  > other._val

    def __le__(self, other):
        return self._val <= other._val

    def __ge__(self, other):
        return self._val >= other._val

    def __eq__(self, other):
        return self._val == other._val

    def __ne__(self, other):
        return self._val != other._val


    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, new_val):
        if new_val < 0:
            self._val = 0
        else:
            self._val = new_val

    def diff_base_to_val(self):
        return self.base_val - self.val

    def inc_base_val(self, amt):
        self.base_val += amt
        self.restore_val()

    def dec_base_val(self, amt):
        self.base_val -= amt if (self.base_val - amt) <= 0 else 0
        self.restore_val()

    def restore_val(self):
        self.val = self.base_val

    def fraction_str(self):
        return self.name + ": " + str(self.val) + "/" + str(self.base_val) + "\n"

class Attack(Stat):

    def __init__(self, _val=0):
        super().__init__('ATK', _val)

class Defense(Stat):

    def __init__(self, _val=0):
        super().__init__('DEF', _val)

class Speed(Stat):

    def __init__(self, _val=0):
        super().__init__('SPD', _val)


class HP(Stat):

    def __init__(self, _val=0):
        super().__init__('HP', _val)
