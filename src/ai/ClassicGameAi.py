import random
from typing import Generator
import numpy as np
from ai.ShipShape import ShipShape
from ai.Board import Board

class ClassicGameAi:

    def __init__(self, numShips : dict[int, int]):
        self.numShips = numShips.copy()
        self.parity = random.randint(0, 1)


    def getNextShot(self, board : Board) -> tuple[int]:
        # find ship likely tiles with the greatest free space
        maxFreeSpace = -1
        bestShipLikelyTile = (0, 0)

        # saves all results in case it is needed
        freeSpaceByTile = {}

        for pos in board.shuffledIndex():
            if board.check(pos, Board.SHIP_LIKELY):
                # count the free space
                shipTile = self.findAdjacentTilesByState(pos, Board.SHIP, board)
                if len(shipTile) == 0:
                    raise RuntimeError("No ship tile adjacent to a ship likely tile")
                shipTile = shipTile[0]

                freeSpace = 0
                posArray = np.array(pos)
                direction = posArray - np.array(shipTile)

                while self.shipIsPossible(posArray + freeSpace * direction, board):
                    freeSpace += 1

                # save result
                freeSpaceByTile[pos] = freeSpace

                # save only the max free space
                if maxFreeSpace < freeSpace:
                    maxFreeSpace = freeSpace
                    bestShipLikelyTile = pos
        
        if maxFreeSpace > -1:
            # now we found the one tile with most space but in the case that the orthogonal direction hasn't been checked yet this would be an even better choice
            orthogonalTiles = self.findAdjacentTilesByState(bestShipLikelyTile, Board.SHIP_LIKELY, board, True)

            if len(orthogonalTiles) != 2:
                return bestShipLikelyTile
            
            # now check if maybe all 4 corners are left so the orthogonal direction isnt better
            # get the middle tile
            middle = (np.array(orthogonalTiles[0]) + np.array(orthogonalTiles[1])) / 2
            middle = (int(middle[0]), int(middle[1]))
            if len(self.findAdjacentTilesByState(middle, Board.SHIP_LIKELY, board)) == 4:
                return bestShipLikelyTile
            
            # now the orthogonal direction is prefered
            # choose the one with more free space
            if freeSpaceByTile[orthogonalTiles[0]] >= freeSpaceByTile[orthogonalTiles[1]]:
                return orthogonalTiles[0]
            else:
                return orthogonalTiles[1]


        # do random guess in checkerboard pattern
        for x, y in board.shuffledIndex():
            if (x + y) % 2 == self.parity and board.check((x, y), Board.NO_INFO):
                return (x, y)
        
        raise RuntimeError("Unexpected state reached: No No-Info-Tiles are left but game hasn't ended yet!")

    
    def submitInfo(self, pos : tuple[int], state : int, board : Board) -> Board:
        boardState = board[pos]

        if state == Board.CHECKED_NO_SHIP:
            if boardState == Board.SHIP_LIKELY:
                shipTile = self.findAdjacentTilesByState(pos, Board.SHIP, board)
                if len(shipTile) == 0:
                    raise RuntimeError("No ship tile adjacent to a ship likely tile")
                shipTile = shipTile[0]

                length, lastShipTile = self.countShipLength(shipTile, board)
                if length == self.currentLongestShip() or len(self.findAdjacentTilesByState(lastShipTile, Board.SHIP_LIKELY, board)) == 0:
                    # ship complete
                    board = self.replaceAdjacentCells(lastShipTile, Board.SHIP_LIKELY, Board.DEDUSED_NO_SHIP, board)
                    self.numShips[length] -= 1
                
            elif boardState & (Board.DEDUSED_NO_SHIP | Board.NO_INFO):
                # nothing of interest happened
                pass
            else:
                raise ValueError("A tile has been checked twice")
            
        elif state == Board.SHIP:
            if boardState == Board.SHIP_LIKELY:
                shipTile = self.findAdjacentTilesByState(pos, Board.SHIP, board)
                if len(shipTile) == 1:
                    # by far the most likely case
                    shipTile = shipTile[0]

                    length, lastShipTile = self.countShipLength(shipTile, board)
                    if length == 1:
                        # found the second tile
                        # remove orthogonal ship likely tiles
                        board = self.replaceAdjacentCells(pos, Board.SHIP_LIKELY, Board.DEDUSED_NO_SHIP, board, True)
                        board[pos] = Board.SHIP
                    
                    if length + 1 == self.currentLongestShip():
                        # found longest ship and thus submit it
                        board = self.replaceAdjacentCells(lastShipTile, Board.SHIP_LIKELY, Board.DEDUSED_NO_SHIP, board)
                        board = self.replaceAdjacentCells(pos, Board.NO_INFO, Board.DEDUSED_NO_SHIP, board)
                        self.numShips[length + 1] -= 1
                    else:
                        # check if the ship is against the wall and other side has been checked so its also completed
                        nextTile = 2 * np.array(pos) - np.array(shipTile)
                        if not self.shipIsPossible(nextTile, board) and len(self.findAdjacentTilesByState(lastShipTile, Board.SHIP_LIKELY, board)) == 0:
                            self.numShips[length + 1] -= 1

                elif len(shipTile) == 2:
                    # can only happen by accident when we have dicovered to side of the ship independently
                    # but maybe the ship is done so it has to be registered correctly
                    length1, corner1 = self.countShipLength(shipTile[0], board)
                    length2, corner2 = self.countShipLength(shipTile[1], board)

                    # first replace the corners so that ship likely tiles orthogonal to the ships direction cannot occur
                    board = self.replaceAdjacentCells(pos, Board.SHIP_LIKELY, Board.DEDUSED_NO_SHIP, board, True)
                    board = self.replaceAdjacentCells(pos, Board.NO_INFO, Board.DEDUSED_NO_SHIP, board)

                    # check if ship is done
                    if length1 + length2 + 1 == self.currentLongestShip():
                        board = self.replaceAdjacentCells(corner1, Board.SHIP_LIKELY, Board.DEDUSED_NO_SHIP, board)
                        board = self.replaceAdjacentCells(corner2, Board.SHIP_LIKELY, Board.DEDUSED_NO_SHIP, board)
                        self.numShips[length1 + length2 + 1] -= 1

                    elif len(self.findAdjacentTilesByState(corner1, Board.SHIP_LIKELY, board)) == 0 and len(self.findAdjacentTilesByState(corner2, Board.SHIP_LIKELY, board)) == 0:
                        self.numShips[length1 + length2 + 1] -= 1

                else:
                    raise RuntimeError("No ship tile adjacent to a ship likely tile")                    

            elif boardState == Board.NO_INFO:
                pass
            elif boardState == Board.DEDUSED_NO_SHIP:
                raise RuntimeError("Logic error has occured")
            else:
                raise ValueError("A tile has been checked twice")
            
            board = self.replaceAdjacentCells(pos, Board.NO_INFO, Board.SHIP_LIKELY, board)
            board = self.replaceAdjacentCells(pos, Board.NO_INFO, Board.DEDUSED_NO_SHIP, board, True)
        else:
            raise ValueError("Illegal state submitted")
        
        board[pos] = state
        return board

    def countShipLength(self, firstShipTile : tuple[int], board : Board):
        nextTiles = self.findAdjacentTilesByState(firstShipTile, Board.SHIP, board)
        if len(nextTiles) == 0:
            return 1, firstShipTile
        
        direction = np.array(nextTiles[0]) - np.array(firstShipTile)
        length = 2
        while 1:
            testingTile = firstShipTile + length * direction
            if not board.isInBounds(testingTile) or not board.check(testingTile, Board.SHIP):
                return length, firstShipTile + (length - 1) * direction
            length += 1

    
    def findAdjacentTilesByState(self, pos : tuple[int], state : int, board : Board, includeCorners : bool = False) -> list[tuple[int]]:
        positionsToCheck = [ (pos[0], pos[1]-1), (pos[0], pos[1]+1), (pos[0]-1, pos[1]), (pos[0]+1, pos[1]) ]

        if includeCorners:
            positionsToCheck += [(pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]-1, pos[1]+1), (pos[0]-1, pos[1]-1)]

        result = [(x, y) for x, y in positionsToCheck if board.isInBounds((x, y)) and board.check((x, y), state)]

        random.shuffle(result)
        return result
    
    def replaceAdjacentCells(self, pos : tuple[int], searchState : int, replaceState : int, board : Board, includeCorners : bool = False) -> None:
        pos = self.findAdjacentTilesByState(pos, searchState, board, includeCorners)
        for p in pos:
            board[p] = replaceState
        return board
        
    def currentLongestShip(self) -> int:
        crntMax = max(self.numShips.keys())
        while crntMax not in self.numShips or self.numShips[crntMax] == 0 or crntMax == 1:
            crntMax -= 1
        return crntMax
    
    def shipIsPossible(self, pos : tuple[int], board : Board) -> bool:
        return board.isInBounds(pos) and board.check(pos, Board.NO_INFO | Board.SHIP_LIKELY | Board.SHIP)

