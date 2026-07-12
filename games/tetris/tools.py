from objects import Pos
from colors import Colors

class Tools:
    def __init__(self)->None:
        self.windowSize = Colors.windowSize
        self.gameSize = Colors.gameSize

        self.sField = self.calcSField()
        self.sFieldHalf = self.sField / 2
        self.playFiledX = self.clacXofPlayField()

        self.zeroPos = Pos(self.playFiledX, Colors.topMarginPx)
        self.scorePos = Pos(self.windowSize[0] - self.zeroPos.x / 2, self.zeroPos.x / 2)
        print(self.zeroPos)
        print(self.sField)

        print(self.translateCoords(Pos(0,0)))

    def calcSField(self)->float|int:
        height = self.windowSize[1] - Colors.topMarginPx - Colors.botMarginPx
        return height / self.gameSize[1]

    def clacXofPlayField(self)->float|int:
        bot = self.sField * self.gameSize[0]
        return (self.windowSize[0] - bot) / 2

    def translateCoords(self, p: Pos)->Pos:
        return Pos(p.x * self.sField + self.sFieldHalf, p.y*self.sField + self.sFieldHalf) + self.zeroPos

    @staticmethod
    def brightenColor(c:tuple[int,int,int]):
        return tuple(min(ch + 30, 255) for ch in c)

    def isPosValid(self, p:Pos)->bool:
        if 0 <= p.x < self.gameSize[0] and p.y < self.gameSize[1]:
            return True
        return False
    def isPosOnScreen(self, p:Pos)->bool:
        if 0 <= p.x < self.gameSize[0] and 0 <= p.y < self.gameSize[1]:
            return True
        return False