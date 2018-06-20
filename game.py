class Game(object):
    def __init__(self):
        self.home = 0
        self.away = 0
        self.hScore = ""
        self.aScore = ""
        self.quarter = "1"
        self.gameThread = ""
        self.postThread = ""

        self.sortValue = 0
        self.watchValue = 0

    def setScores(self, h, a):
        self.hScore = h
        self.aScore = a

    # def addThread(self, threadLink):
    #    self.gThreads.append(threadLink)

