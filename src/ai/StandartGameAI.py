import random
from typing import Generator
import numpy as np

class ShipShape:

    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, length : int, cell : tuple[int], orientation : int):
        self.length = length
        self.cell = cell
        self.orientation = orientation

    def occupiedTiles(self) -> list[tuple[int]]:
        tiles = []
        if self.orientation == ShipShape.HORIZONTAL:
            for i in range(self.length):
                tiles.append((self.cell[0] + i, self.cell[1]))
        elif self.orientation == ShipShape.VERTICAL:
            for i in range(self.length):
                tiles.append((self.cell[0], self.cell[1] + i))
        return tiles
    
    def blockedTiles(self) -> list[tuple[int]]:
        tiles = []
        if self.orientation == ShipShape.HORIZONTAL:
            for i in range(-1, self.length + 1):
                tiles.append((self.cell[0] + i, self.cell[1]))
                tiles.append((self.cell[0] + i, self.cell[1] - 1))
                tiles.append((self.cell[0] + i, self.cell[1] + 1))
        elif self.orientation == ShipShape.VERTICAL:
            for i in range(-1, self.length + 1):
                tiles.append((self.cell[0], self.cell[1] + i))
                tiles.append((self.cell[0] - 1, self.cell[1] + i))
                tiles.append((self.cell[0] + 1, self.cell[1] + i))
        return tiles
    
    def interferesWith(self, other : 'ShipShape') -> bool:
        blockedTiles = self.blockedTiles()
        for otherTile in other.occupiedTiles():
            if otherTile in blockedTiles:
                return True
        return False
    
    def isInBoardBounds(self, boardWidth : int, boardHeight : int) -> bool:
        if self.cell[0] < 0 or self.cell[1] < 0:
            return False

        if self.orientation == ShipShape.HORIZONTAL:
            boardWidth -= self.length
        elif self.orientation == ShipShape.VERTICAL:
            boardHeight -= self.length
        
        return self.cell[0] <= boardWidth and self.cell[1] <= boardHeight
    
    def fitsInShipPlacement(self, shipPlacement : list['ShipShape']) -> bool:
        return all(not self.interferesWith(ship) for ship in shipPlacement)
    
    @staticmethod
    def cellInPlacement(cell : tuple[int], placement : list['ShipShape']) -> None:
        return any((cell in ship.occupiedTiles()) for ship in placement)

class StandartGameAI:

    NO_INFO = 0
    CHECKED_NO_SHIP = 1
    DEDUSED_NO_SHIP = 2
    SHIP = 3
    SHIP_LIKELY = 4


    def __init__(self, boardWidth : int, boardHeight : int, chanceOfMistake : float, numShips : dict[int, int] = {2: 4, 3: 3, 4: 2, 5: 1}):
        self.board : list[list[int]] = [[StandartGameAI.NO_INFO for _ in range(boardHeight)] for _ in range(boardWidth)]
        self.width = boardWidth
        self.height = boardHeight
        self.chanceOfMistake = chanceOfMistake
        self.numShips = numShips
        self.parity = random.randint(0, 1)
    
    def getShipPlacement(self) -> list[ShipShape]:
        # construct ships to do
        shipsToDo : list[int] = []
        for length, count in sorted(self.numShips.items(), reverse=True):
            shipsToDo += [ length ] * count

        return self.getShipPlacementInner(shipsToDo, [])

    def getShipPlacementInner(self, shipsToDo : list[int], crntPlacement : list[ShipShape]) -> list[ShipShape] | None:
        if len(shipsToDo) == 0:
            return crntPlacement

        crntLength = shipsToDo.pop(0)
        
        for pos in self.shuffledIndex():
            orientations = random.sample([ ShipShape.VERTICAL, ShipShape.HORIZONTAL ], 2)
            for orientation in orientations:
                tempShip = ShipShape(crntLength, pos, orientation)
                if tempShip.isInBoardBounds(self.width, self.height) and tempShip.fitsInShipPlacement(crntPlacement):
                    finalPlacement = self.getShipPlacementInner(shipsToDo, crntPlacement + [ tempShip ])
                    if finalPlacement != None:
                        return finalPlacement
        return None

            

    def getNextShotAsRandom(self) -> tuple[int]:
        for x, y in self.shuffledIndex():
            if self.board[x][y] != StandartGameAI.SHIP and self.board[x][y] != StandartGameAI.CHECKED_NO_SHIP:
                return (x, y)

    def getNextShot(self) -> tuple[int]:
        if random.random() < self.chanceOfMistake:
            print("Mistake!")
            return self.getNextShotAsRandom() # do a mistake
        
        # get proper guess

        # find ship likely tiles with the greatest free space
        maxFreeSpace = -1
        bestShipLikelyTile = (0, 0)
        for pos in self.shuffledIndex():
            if self.board[pos[0]][pos[1]] == StandartGameAI.SHIP_LIKELY:
                # count the free space
                shipTile = self.findAdjacentTilesByState(pos, StandartGameAI.SHIP)
                if len(shipTile) == 0:
                    raise RuntimeError("No ship tile adjacent to a ship likely tile")
                shipTile = shipTile[0]

                freeSpace = 0
                pos = np.array(pos)
                direction = pos - np.array(shipTile)

                while self.shipIsPossible(pos + freeSpace * direction):
                    freeSpace += 1

                # save only the max free space
                if maxFreeSpace < freeSpace:
                    maxFreeSpace = freeSpace
                    bestShipLikelyTile = pos
        
        if maxFreeSpace > -1:
            return bestShipLikelyTile

        # do random guess in checkerboard pattern
        for x, y in self.shuffledIndex():
            if (x + y) % 2 == self.parity and self.board[x][y] == StandartGameAI.NO_INFO:
                return (x, y)
        
        raise RuntimeError("Unexpected state reached: No No-Info-Tiles are left but game hasn't ended yet!")

    
    def shuffledIndex(self) -> Generator[tuple[int], None, None]:
        for y in random.sample(list(range(self.height)), self.height):
            for x in random.sample(list(range(self.width)), self.width):
                yield (x, y)
    
    def submitInfo(self, pos : tuple[int], state : int) -> None:
        boardState = self.board[pos[0]][pos[1]]

        if state == StandartGameAI.CHECKED_NO_SHIP:
            if boardState == StandartGameAI.SHIP_LIKELY:
                shipTile = self.findAdjacentTilesByState(pos, StandartGameAI.SHIP)
                if len(shipTile) == 0:
                    raise RuntimeError("No ship tile adjacent to a ship likely tile")
                shipTile = shipTile[0]

                length, lastShipTile = self.countShipLength(shipTile)
                if length == self.currentLongestShip() or len(self.findAdjacentTilesByState(lastShipTile, StandartGameAI.SHIP_LIKELY)) == 0:
                    # ship complete
                    self.replaceAdjacentCells(lastShipTile, StandartGameAI.SHIP_LIKELY, StandartGameAI.DEDUSED_NO_SHIP)
                    self.numShips[length] -= 1
                
            elif boardState == StandartGameAI.DEDUSED_NO_SHIP or boardState == StandartGameAI.NO_INFO:
                # nothing of interest happened
                pass
            else:
                raise ValueError("A tile has been checked twice")
            
        elif state == StandartGameAI.SHIP:
            if boardState == StandartGameAI.SHIP_LIKELY:
                shipTile = self.findAdjacentTilesByState(pos, StandartGameAI.SHIP)
                if len(shipTile) == 1:
                    # by far the most likely case
                    shipTile = shipTile[0]

                    length, lastShipTile = self.countShipLength(shipTile)
                    if length == 1:
                        # found the second tile
                        # remove orthogonal ship likely tiles
                        self.replaceAdjacentCells(shipTile, StandartGameAI.SHIP_LIKELY, StandartGameAI.DEDUSED_NO_SHIP)
                        # get tile on the other side of the ship tile
                        otherSideTile = 2 * np.array(shipTile) - np.array(pos)
                        if self.isInBounds(otherSideTile) and self.board[otherSideTile[0]][otherSideTile[1]] == StandartGameAI.DEDUSED_NO_SHIP:
                            self.board[otherSideTile[0]][otherSideTile[1]] = StandartGameAI.SHIP_LIKELY
                    
                    if length + 1 == self.currentLongestShip():
                        # found longest ship and thus submit it
                        self.replaceAdjacentCells(lastShipTile, StandartGameAI.SHIP_LIKELY, StandartGameAI.DEDUSED_NO_SHIP)
                        self.replaceAdjacentCells(pos, StandartGameAI.NO_INFO, StandartGameAI.DEDUSED_NO_SHIP)
                        self.numShips[length + 1] -= 1
                    else:
                        # check if the ship is against the wall and other side has been checked so its also completed
                        nextTile = 2 * np.array(pos) - np.array(shipTile)
                        if not self.shipIsPossible(nextTile) and len(self.findAdjacentTilesByState(lastShipTile, StandartGameAI.SHIP_LIKELY)) == 0:
                            self.numShips[length + 1] -= 1

                elif len(shipTile) == 2:
                    # can only happen by accident when we have dicovered to side of the ship independently
                    # but maybe the ship is done so it has to be registered correctly
                    corner1, length1 = self.countShipLength(shipTile[0])
                    corner2, length2 = self.countShipLength(shipTile[1])

                    # first replace the corners so that ship likely tiles orthogonal to the ships direction cannot occur
                    self.replaceAdjacentCells(pos, StandartGameAI.SHIP_LIKELY, StandartGameAI.DEDUSED_NO_SHIP, True)
                    self.replaceAdjacentCells(pos, StandartGameAI.NO_INFO, StandartGameAI.DEDUSED_NO_SHIP)

                    # check if ship is done
                    if length1 + length2 + 1 == self.currentLongestShip():
                        self.replaceAdjacentCells(corner1, StandartGameAI.SHIP_LIKELY, StandartGameAI.DEDUSED_NO_SHIP)
                        self.replaceAdjacentCells(corner2, StandartGameAI.SHIP_LIKELY, StandartGameAI.DEDUSED_NO_SHIP)
                        self.numShips[length1 + length2 + 1] -= 1

                    elif len(self.findAdjacentTilesByState(corner1, StandartGameAI.SHIP_LIKELY)) == 0 and len(self.findAdjacentTilesByState(corner2, StandartGameAI.SHIP_LIKELY)) == 0:
                        self.numShips[length1 + length2 + 1] -= 1

                else:
                    raise RuntimeError("No ship tile adjacent to a ship likely tile")                    

            elif boardState == StandartGameAI.NO_INFO:
                pass
            elif boardState == StandartGameAI.DEDUSED_NO_SHIP:
                raise RuntimeError("Logic error has occured")
            else:
                raise ValueError("A tile has been checked twice")
            
            self.replaceAdjacentCells(pos, StandartGameAI.NO_INFO, StandartGameAI.SHIP_LIKELY)
            self.replaceAdjacentCells(pos, StandartGameAI.NO_INFO, StandartGameAI.DEDUSED_NO_SHIP, True)
        else:
            raise ValueError("Illegal state submitted")
        
        self.board[pos[0]][pos[1]] = state

    def countShipLength(self, firstShipTile : tuple[int]):
        nextTiles = self.findAdjacentTilesByState(firstShipTile, StandartGameAI.SHIP)
        if len(nextTiles) == 0:
            return 1, firstShipTile
        
        direction = np.array(nextTiles[0]) - np.array(firstShipTile)
        length = 2
        while 1:
            testingTile = firstShipTile + length * direction
            if not self.isInBounds(testingTile) or self.board[testingTile[0]][testingTile[1]] != StandartGameAI.SHIP:
                return length, firstShipTile + (length - 1) * direction
            length += 1

    
    def findAdjacentTilesByState(self, pos : tuple[int], state : int, includeCorners : bool = False) -> list[tuple[int]]:
        positionsToCheck = [ (pos[0], pos[1]-1), (pos[0], pos[1]+1), (pos[0]-1, pos[1]), (pos[0]+1, pos[1]) ]

        if includeCorners:
            positionsToCheck += [(pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]-1, pos[1]+1), (pos[0]-1, pos[1]-1)]

        result = [(x, y) for x, y in positionsToCheck if self.isInBounds((x, y)) and self.board[x][y] == state]

        random.shuffle(result)
        return result
    
    def replaceAdjacentCells(self, pos : tuple[int], searchState : int, replaceState : int, includeCorners : bool = False) -> None:
        pos = self.findAdjacentTilesByState(pos, searchState, includeCorners)
        for p in pos:
            self.board[p[0]][p[1]] = replaceState
        
    def currentLongestShip(self) -> int:
        crntMax = max(self.numShips.keys())
        while crntMax not in self.numShips or self.numShips[crntMax] == 0 or crntMax == 1:
            crntMax -= 1
        return crntMax
    
    def isInBounds(self, pos : tuple[int]) -> bool:
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < self.width and pos[1] < self.height
    
    def shipIsPossible(self, pos : tuple[int]) -> bool:
        return self.isInBounds(pos) and (self.board[pos[0]][pos[1]] == StandartGameAI.NO_INFO or self.board[pos[0]][pos[1]] == StandartGameAI.SHIP_LIKELY or self.board[pos[0]][pos[1]] == StandartGameAI.SHIP)


def printShipPlacement(shipPlacement : list[ShipShape], width, height):
    board : list[list[int]] = [[StandartGameAI.NO_INFO for _ in range(height)] for _ in range(width)]
    for ship in shipPlacement:
        for p in ship.occupiedTiles():
            board[p[0]][p[1]] = StandartGameAI.SHIP
    printBoard(board, width, height)
    return board

def printBoard(board : list[list[int]], width : int, height : int):
    for y in range(height):
        for x in range(width):
            val = board[x][y]
            if val == StandartGameAI.NO_INFO:
                print(".", end="")
            elif val == StandartGameAI.CHECKED_NO_SHIP:
                print("x", end="")
            elif val == StandartGameAI.DEDUSED_NO_SHIP:
                print("o", end="")
            elif val == StandartGameAI.SHIP:
                print("S", end="")
            elif val == StandartGameAI.SHIP_LIKELY:
                print("?", end="")
            else:
                print("!", end="")
        print()
    
# Testing area
if __name__ == "__main__":
    ai = StandartGameAI(11, 11, 0.5)
    placement = ai.getShipPlacement()
    board = printShipPlacement(placement, 11, 11)
    print()
    print("***********************")
    print()
    while True:
        input()
        shot = ai.getNextShot()
        answer = StandartGameAI.CHECKED_NO_SHIP if board[shot[0]][shot[1]] == StandartGameAI.NO_INFO else StandartGameAI.SHIP
        print("Next Shot: " + str(shot) + ": " + str(answer))
        ai.submitInfo(shot, answer)
        printBoard(ai.board, ai.width, ai.height)
        print("Ships left: " + str(ai.numShips))
        print()
        