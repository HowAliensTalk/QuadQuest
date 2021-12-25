class Type:

    def __init__(self, name="", id=-1, weakness=[], resistance=[]):
        self.name = name
        self.id = id
        self.weakness = weakness
        self.resistance = resistance

class Types:
    Celestial = 0
    Fiend = 1
    Bug = 2
    Dark = 3
    Normal = 4
    Dance = 5

class CelestialType(Type):

    def __init__(self):
        super().__init__(name="Celestial", id=Types.Celestial, weakness=[Types.Dark])

class FiendType(Type):

    def __init__(self):
        super().__init__(name="Fiend", id=Types.Fiend, weakness=[Types.Normal])

class BugType(Type):

    def __init__(self):
        super().__init__(name="Bug", id=Types.Bug, weakness=[Types.Celestial])

class DarkType(Type):

    def __init__(self):
        super().__init__(name="Dark", id=Types.Dark, weakness=[Types.Dance])

class NormalType(Type):

    def __init__(self):
        super().__init__(name="Normal", id=Types.Normal, weakness=[Types.Bug])

class DanceType(Type):

    def __init__(self):
        super().__init__(name="Dance", id=Types.Dance, weakness=[Types.Fiend])

WEAKNESS_CHART = "Normal →  Fiend  → Dance\n↑                   ↓\nBug ← Celestial ← Dark"
