import random
import sys

from colors import Colors

class Pos:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y
        self.pos = (x, y)

    def __add__(self, other):
        if isinstance(other, Pos):
            new = Pos(self.x + other.x, self.y + other.y)
            return new
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Pos):
            if self.x == other.x and self.y == other.y:
                return True
        return False

    def __neg__(self):
        return Pos(-self.x, -self.y)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Pos(self.x / other, self.y / other)
        return NotImplemented

    def __round__(self, n=None):
        return Pos(round(self.x, n), round(self.y, n))

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def distanceTo(self, other):

        if isinstance(other, Pos):
            dx = abs(self.x - other.x)
            dy = abs(self.y - other.y)

            return dx + dy
        else:
            return NotImplemented

    def rotateLeft(self):
        x = -self.y
        y = self.x
        return Pos(x, y)

class BlockStruct:
    def __init__(self, blocks:list[Pos], color:tuple[int,int,int]):
        self.blocks = blocks
        self.color = color

    def rotateLeft(self):
        newBlocks = []
        for block in self.blocks:

            newBlocks.append(block.rotateLeft())

        return BlockStruct(newBlocks, self.color)

    def shiftBy(self, shift:Pos):
        newBlocks = []
        for block in self.blocks:
            newBlocks.append(block+shift)

        return BlockStruct(newBlocks, self.color)

class Shape:
    SHAPES = []

    def __init__(self, states:list[BlockStruct]):
        self.states: list[BlockStruct] = states

    def __getitem__(self, item:int):
        return self.states[item]

    def generateAdditionalRotationStates(self, states:int)->None:
        if len(self.states) == 0:
            raise KeyError("Shape states is empty...")

        for i in range(1, states + 1):
            originalStruct = self.states[i-1]
            self.states.append(originalStruct.rotateLeft())

    @staticmethod
    def loadShapes()->None:
        # 0: line Red, states: 2
        line = BlockStruct([Pos(-2, 0), Pos(-1, 0), Pos(0,0), Pos(1, 0)], color=(255,0,0))
        lineShape = Shape([line])
        lineShape.generateAdditionalRotationStates(1)
        Shape.SHAPES.append(lineShape)

        # 1: block Blue state 1
        block = BlockStruct([Pos(-1, 0), Pos(0, 0), Pos(-1,-1), Pos(0, -1)], color=(0,0,255))
        blockShape = Shape([block])
        Shape.SHAPES.append(blockShape)

        # 2: snake Green states 2
        snakeRight = BlockStruct([Pos(-1, -1), Pos(0, -1), Pos(0,0), Pos(1, 0)], color=(0,255,0))
        snakeRightSHape = Shape([snakeRight])
        snakeRightSHape.generateAdditionalRotationStates(1)
        Shape.SHAPES.append(snakeRightSHape)

        # 3: snake Blue s: 2
        snakeLeft = BlockStruct([Pos(-1, 0), Pos(0, 0), Pos(0, -1), Pos(1, -1)], color=(100, 100, 255))
        snakeLeftSHape = Shape([snakeLeft])
        snakeLeftSHape.generateAdditionalRotationStates(1)
        Shape.SHAPES.append(snakeLeftSHape)

        # 4: l white s:4
        lRight = BlockStruct([Pos(-1, 0), Pos(0, 0), Pos(1, 0), Pos(1, -1)], color=(83, 250, 252))
        lRightShape = Shape([lRight])
        lRightShape.generateAdditionalRotationStates(3)
        Shape.SHAPES.append(lRightShape)

        # 5: l pink s:5
        rRight = BlockStruct([Pos(-1, 0), Pos(0, 0), Pos(1, 0), Pos(1, -1)], color=(202, 3, 252))
        rRightShape = Shape([rRight])
        rRightShape.generateAdditionalRotationStates(3)
        Shape.SHAPES.append(rRightShape)

        # 6: turd brown s:6
        turd = BlockStruct([Pos(-1, 0), Pos(0, 0), Pos(1, 0), Pos(0, -1)], color=(156, 73, 5))
        turdShape = Shape([turd])
        turdShape.generateAdditionalRotationStates(3)
        Shape.SHAPES.append(turdShape)

    @staticmethod
    def randomShape():
        return random.choice(Shape.SHAPES)

class FallingShape:
    def __init__(self):
        self.shape: Shape = Shape.randomShape()

        self.midPos:Pos = Pos(Colors.gameSize[0] // 2, -2)
        self.rotationState:int = 0

        self.blockStruct = self.shape[self.rotationState]
        self.updateBS()

    def updateBS(self)->None:
        self.blockStruct = self.shape[self.rotationState]
        self.blockStruct = self.blockStruct.shiftBy(self.midPos)

    def clacNewAngle(self, angle:int)->int:
        """1: 90 to the right
        Shape.states are originated left ascending"""
        new = self.rotationState - angle

        # clamp
        if new < 0:
            new = len(self.shape.states) - 1
        elif new > len(self.shape.states) - 1:
            new = 0
        return new

    def rotate(self, angle:int)->None:
        self.rotationState = self.clacNewAngle(angle)

    def blockStructByOffsetAndRotation(self, offset:Pos=Pos(0,0), rotation:int=0)->BlockStruct:
        newAngle = self.clacNewAngle(rotation)
        rotated = self.shape[newAngle]
        offsetBS = rotated.shiftBy(offset + self.midPos)
        return offsetBS

class Field:
    def __init__(self, pos:Pos, color:tuple[int,int,int])->None:
        self.pos = pos
        self.color = color
