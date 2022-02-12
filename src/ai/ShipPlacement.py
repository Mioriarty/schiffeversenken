from typing import Union
import random
from Board import Board
from ShipShape import ShipShape


class ShipPlacement:

    def __init__(self, ships : list[ShipShape] = []):
        self.ships = ships.copy()

    
    def fitsIn(self, ship : ShipShape) -> bool:
        return all(not ship.interferesWith(other) for other in self.ships)
    
    def add(self, ship : ShipShape) -> None:
        if not self.fitsIn(ship):
            raise ValueError("Ship doesnt fit in the ship placement")
        
        self.ships.append(ship)
    
    def cellOccupied(self, cell : tuple[int]) -> bool:
        cell = (cell[0], cell[1]) # in case it is a np.ndarray
        return any((cell in ship.occupiedTiles()) for ship in self.ships)
    


    # generate random playcement
    @classmethod
    def generate(cls, boardWidth : int, boardHeight : int, numShips : dict[int, int]) -> 'ShipPlacement':
        board = Board(boardWidth, boardHeight)
        
        # construct ships to do
        shipsToDo : list[int] = []
        for length, count in sorted(numShips.items(), reverse=True):
            shipsToDo += [ length ] * count

        return cls.__generateInner(shipsToDo, cls(), board)
    
    @classmethod
    def __generateInner(self, shipsToDo : list[int], crntPlacement : 'ShipPlacement', board : Board) -> Union['ShipPlacement',  None]:
        if len(shipsToDo) == 0:
            return crntPlacement

        crntLength = shipsToDo.pop(0)
        
        for pos in board.shuffledIndex():
            orientations = random.sample([ ShipShape.VERTICAL, ShipShape.HORIZONTAL ], 2)
            for orientation in orientations:
                tempShip = ShipShape(crntLength, pos, orientation)
                if tempShip.isInBoardBounds(board.width, board.height) and crntPlacement.fitsIn(tempShip):
                    finalPlacement = self.__generateInner(shipsToDo, ShipPlacement(crntPlacement.ships + [ tempShip ]), board)
                    if finalPlacement != None:
                        return finalPlacement
        return None
    
    # print function
    def print(self, boardWidth : int, boardHeight : int) -> None:
        board = Board(boardWidth, boardHeight)
        for ship in self.ships:
            for p in ship.occupiedTiles():
                board[p] = Board.SHIP
        board.print()