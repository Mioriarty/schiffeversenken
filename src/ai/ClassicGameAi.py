import random
from typing import Generator
import numpy as np
from ai.ShipShape import ShipShape
from ai.Board import Board

class ClassicGameAi:
    """
    Sets shots as a human would do.

    It shoots randomly in a checkerboard pattern im no ship is found.
    If one is found, it will try to inish it as qickly as possible.

    Attributes:
        numShips (dict[int, int]): How many ships of which length are left. The key is the length of the ships and values is the number of that kind of ships.
        parity (int): Is 0 or 1 randomly and specifies which of the 2 checkerboard patterns to use.
    """

    def __init__(self, numShips : dict[int, int]):
        """
        The constructor of the ClassicGameai class.

        Args:
            numShips (dict[int, int]):  How many ships of which length shell be found. The key is the length of the ships and values is the number of that kind of ships.
        """
        self.numShips = numShips.copy()
        self.parity = random.randint(0, 1)


    def getNextShot(self, board : Board) -> tuple[int]:
        """
        Calculates the next shot. 

        Args:
            board (Board): The current board state on which it shoots.

        Returns:
            tuple[int]: Next shot position / tile.
        """

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
        """
        Submits and interpretes a new cell information.

        Args:
            pos (tuple[int]): The x and y coordinate of the cell in question.
            state (int): The found state. Either Board.SUBMIT_SHIP or Board.SUBMIT_NO_SHIP
            board (Board): The current board state.

        Returns:
            Board: The new board state.
        """
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
        
        return board

    def countShipLength(self, firstShipTile : tuple[int], board : Board) -> tuple[int, tuple[int]]:
        """
        Counts all ship tiles connected to the firstShipTile.

        Args:
            firstShipTile (tuple[int]): The first know ship tile position.
            board (Board): The current board state.

        Returns:
            int: The length of the current ship.
            tuple[int]: The last ship tile.
        """
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
        """
        Find all adjacent tiles if a certain state.

        Args:
            pos (tuple[int]): Coordinates of the center tile.
            state (int): State to look for.
            board (Board): Current board state. 
            includeCorners (bool, optional): Should the corners be included in the search. Defaults to False.

        Returns:
            list[tuple[int]]: All tiles that meet the creteria.
        """
        positionsToCheck = [ (pos[0], pos[1]-1), (pos[0], pos[1]+1), (pos[0]-1, pos[1]), (pos[0]+1, pos[1]) ]

        if includeCorners:
            positionsToCheck += [(pos[0]+1, pos[1]+1), (pos[0]+1, pos[1]-1), (pos[0]-1, pos[1]+1), (pos[0]-1, pos[1]-1)]

        result = [(x, y) for x, y in positionsToCheck if board.isInBounds((x, y)) and board.check((x, y), state)]

        random.shuffle(result)
        return result
    
    def replaceAdjacentCells(self, pos : tuple[int], searchState : int, replaceState : int, board : Board, includeCorners : bool = False) -> Board:
        """
        Replaces all adjacent tiles if a certain state.

        Args:
            pos (tuple[int]): Coordinates of the center tile.
            searchState (int): State to look for.
            replaceState (int): new state of found tiles.
            board (Board): Current board state. 
            includeCorners (bool, optional): Should the corners be included in the search. Defaults to False.

        Returns:
            Board: New board state.
        """
        pos = self.findAdjacentTilesByState(pos, searchState, board, includeCorners)
        for p in pos:
            board[p] = replaceState
        return board
        
    def currentLongestShip(self) -> int:
        """
        Returns the length of the longest ship that has not been found yet.

        Returns:
            int: The length of the longest ship that has not been found yet.
        """
        crntMax = max(self.numShips.keys())
        while crntMax not in self.numShips or self.numShips[crntMax] == 0 or crntMax == 1:
            crntMax -= 1
        return crntMax
    
    def shipIsPossible(self, pos : tuple[int], board : Board) -> bool:
        """
        Checks whether on the position can be a ship tile or not.

        It can be forbidden, because the tile might not be on the vboard or the state is in a conflicting state.

        Args:
            pos (tuple[int]): Position to check.
            board (Board): Current board state. 

        Returns:
            bool: If on the position can be a ship tile or not.
        """
        return board.isInBounds(pos) and board.check(pos, Board.NO_INFO | Board.SHIP_LIKELY | Board.SHIP)

