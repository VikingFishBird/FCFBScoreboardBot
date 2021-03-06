class Team(object):
    def __init__(self, n, t):
        self.name = n
        self.tag = t
        self.rank = 0
        self.inGame = False

    def printSetup(self):
        text = "[" + self.name + "](#f/" + self.tag + ") | "
        if self.rank != 0:
            text = text + self.rank + " " + self.name + " | "
        else:
            text = text + self.name + " | "
        return text
