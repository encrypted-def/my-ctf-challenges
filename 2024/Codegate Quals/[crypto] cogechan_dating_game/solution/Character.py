class Character:
    def __init__(self, nickname='', day=0, stamina=0, intelligence=0, friendship=0):
        self.nickname = nickname
        self.day = day
        self.stamina = stamina
        self.intelligence = intelligence
        self.friendship = friendship

    def __eq__(self, other):
        return self.nickname == other.nickname and \
               self.day == other.day and \
               self.stamina == other.stamina and \
               self.intelligence == other.intelligence and \
               self.friendship == other.friendship