import sys

from games.tetris.colors import Colors
from objects import Shape, BlockStruct, Pos, Field, FallingShape

from tools import Tools
class Game:
    def __init__(self):

        self.tools = Tools()

        Shape.loadShapes()
        self.shapeCollection = Shape.SHAPES

        self.playField: dict[Pos, Field] = {}

        self.tickCount = 0

        self.fallingShape = FallingShape()

        self.score = 0

    def updateOnTick(self)->bool:

        nextFallingShapeBS = self.fallingShape.blockStructByOffsetAndRotation(offset=Pos(0, 1))

        if self.checkBSValidity(nextFallingShapeBS):
            self.fallingShape.midPos += Pos(0,1)

        else:
            self.addBStoPlayField(self.fallingShape.blockStruct)

            if self.isGameOver():
                return False

            self.fallingShape = FallingShape()

        rowsToClear = self.rowsToClear()
        self.clearRows(rowsToClear)
        self.score += len(rowsToClear)


        self.fallingShape.updateBS()

        self.tickCount += 1
        return True

    def checkBSValidity(self, bs:BlockStruct)->bool:
        """true: ok; false: wrong"""
        placedBlocks = self.playField.keys()

        for block in bs.blocks:
            if not self.tools.isPosValid(block):
                return False
            if block in placedBlocks:
                return False
        return True

    def addBStoPlayField(self, bs:BlockStruct)->None:
        for block in bs.blocks:
            self.playField[block] = Field(block, bs.color)

    def isGameOver(self)->bool:
        for block in self.fallingShape.blockStruct.blocks:
            if not self.tools.isPosOnScreen(block):
                return True
        return False

    def rowsToClear(self)->list[int]:
        rows = list(range(Colors.gameSize[1]))

        blocksPlaced = self.playField.keys()

        for y in range(Colors.gameSize[1]):
            for x in range(Colors.gameSize[0]):
                if Pos(x, y) not in blocksPlaced:
                    rows.remove(y)
                    break

        return sorted(list(rows), reverse=True)


    def clearRows(self, rows:list[int])->None:
        newPlayFiled: dict[Pos, Field] = {}

        for row in rows:
            # remove the blocks in the line and shift blocks with smaller y val one down
            blocks = self.playField.values()
            for field in blocks:

                if field.pos.y > row:
                    newPlayFiled[field.pos] = field

                elif field.pos.y < row:
                    field.pos += Pos(0, 1)
                    newPlayFiled[field.pos] = field

            self.playField = newPlayFiled