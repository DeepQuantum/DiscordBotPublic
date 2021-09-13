from utils.botexceptions import InvalidParameterRangeError


class BattleshipPlayer():
    def __init__(self, user):
        self.user = user
        self.name = user.name
        self.ownfield = [[0 for x in range(10)] for x in range(10)]
        self.enemyfield = [[0 for x in range(10)] for x in range(10)]
        self.ownfieldstr = self.constructfield()
        self.enemyfieldstr = self.constructfield()
        self.remainingships = BattleshipPlayer.getships()[1:]
        self.firemessagecount = 0
        self.discmessages = {}
        self.ready = False

    @staticmethod
    def getships() -> list:
        return [None, "Destroyer", "Frigate", "Carrier"]

    def constructfield(self) -> str:
        cases = ["\u2b1b", "\U0001F6A2", "\u274c", "\U0001F4A5"]
        result = "```\n 1 2  3 4  5 6  7 8  9 10\n"
        for y in range(10):
            for x in range(10):
                result += cases[self.ownfield[x][y]]
            result += f"   {y + 1}\n"
        return result + "```"


    def place(self, stype, x, y, r) -> str:
        if stype in self.remainingships:
            typelength = BattleshipPlayer.getships().index(stype) + 1
            validpos = []
            try:
                if (r == "v"):
                    for i in range(typelength):
                        if self.ownfield[x][y + i] != 1:
                            validpos.append([x, y + i])
                        else:
                            return "Invalid position. Spot already occupied!"
                elif (r == "h"):
                    for i in range(typelength):
                        if self.ownfield[x + i][y] != 1:
                            validpos.append([x + i, y])
                        else:
                            return "Invalid position. Spot already occupied!"
            except IndexError:
                return "Invalid position. The ship can't go over the bounds of the field."
            for i in validpos:
                self.ownfield[i[0]][i[1]] = 1
            self.remainingships.remove(stype)
        else:
            return "Ship already used!"

        return 1

    def checkhit(self, x, y):
        if self.ownfield[x][y] == 1:
            self.ownfield[x][y] = 3
            return 3
        elif self.ownfield[x][y] == 0:
            self.ownfield[x][y] = 2
            return 2
        elif self.ownfield[x][y] == 2 or self.ownfield[x][y] == 3:
            return -1