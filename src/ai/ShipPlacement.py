from typing import Generator, Union
import random
from ai.Board import Board
from ai.ShipShape import ShipShape


class ShipPlacement:
    """
    Represents a collection of ships that together make up a ShipPlacmeent on the board.

    A placement is valid if no pair of ships in the placement interfere. Meaning that they don't cross and are not in the surrounding tiles. See ShipShape.interfere

    Attributes:
        ships (set[ShipShape]): collection of ships in the placement
    """

    def __init__(self, ships : list[ShipShape] = []):
        """
        Constructor og the ShipPlacement class.

        Args:
            ships (list[ShipShape], optional): Predefined collection of ships that should be included. Defaults to [].
        """
        self.ships = set(ships)

    
    def fitsIn(self, ship : ShipShape) -> bool:
        """
        Checks if the ship meets the creteria to be added to the placement. Meaning that if it would be added, whether the new ShipPlacement would be valid.

        Args:
            ship (ShipShape): ShipShape to check against.

        Returns:
            bool: If the ship meets the creteria to be added to the placement. Meaning that if it would be added, whether the new ShipPlacement would be valid.
        """
        return all(not ship.interferesWith(other) for other in self.ships)
    
    def add(self, ship : ShipShape) -> None:
        """
        Adds a ShipShape to the placement not regarding if it fits in. (See ShipPlacemnt.fitsIn).

        The resulting ship placement might not be valid.

        Args:
            ship (ShipShape): The new ShipShape to be added
        """
        self.ships.add(ship)
    
    def cellOccupied(self, cell : tuple[int]) -> bool:
        """
        Checks if the specified cell is occupied by any ship in the placement. (See ShipShape.occupiedTiles)

        Args:
            cell (tuple[int]): The cell / tile to check against.

        Returns:
            bool: If the specified cell is occupied by any ship in the placement. (See ShipShape.occupiedTiles)
        """
        cell = (cell[0], cell[1]) # in case it is a np.ndarray
        return any(ship.getOccupiedRect().includesPoint(cell) for ship in self.ships)

    def occupiedCells(self) -> Generator[tuple[int], None, None]:
        """
        Yields all occupied cells by all ships. (See ShipShape.occupiedTiles)

        Yields:
            Generator[tuple[int], None, None]: All occupied cells by all ships. (See ShipShape.occupiedTiles)
        """
        for ship in self.ships:
            yield from ship.occupiedTiles()
    
    def blockedCells(self) -> Generator[tuple[int], None, None]:
        """
        Yields all blocked cells by all ships. (See ShipShape.blockedTiles)

        Yields:
            Generator[tuple[int], None, None]: All blocked cells by all ships. (See ShipShape.blockedTiles)
        """
        for ship in self.ships:
            yield from ship.blockedTiles()
    
    def copy(self) -> 'ShipPlacement':
        """
        Creates a copy of itself.

        Returns:
            ShipPlacement: Newly created copy.
        """
        cpy = ShipPlacement()
        cpy.ships = self.ships.copy()
        return cpy

    # generate random playcement
    @classmethod
    def generate(cls, boardWidth : int, boardHeight : int, numShips : dict[int, int]) -> 'ShipPlacement':
        """
        Recursively generates a valid ShipPlacement for a board with certain number of ship lengths.

        Args:
            boardWidth (int): Amount of columns of the board.
            boardHeight (int): Amount of rows of the board.
            numShips (dict[int, int]): How many ships of which length. The key is the length of the ships and values is the number of that kind of ships.

        Returns:
            ShipPlacement: The newly generated ship placement
        """
        board = Board(boardWidth, boardHeight)
        
        # construct ships to do
        shipsToDo : list[int] = []
        for length, count in sorted(numShips.items(), reverse=True):
            shipsToDo += [ length ] * count

        return cls.__generateInner(shipsToDo, cls(), board)
    
    @classmethod
    def __generateInner(self, shipsToDo : list[int], crntPlacement : 'ShipPlacement', board : Board) -> Union['ShipPlacement',  None]:
        """
        Inner recursive step for generating a new ship placement.

        Args:
            shipsToDo(list[int]): Ship lengths more to place
            crntPlacement(ShipPlacement): Already placed ships.
            board (Board): Board on which you want to place the ships.

        Returns:
            ShipPlacement: Successfully generated ShipPlacement. Or:
            None: If no placement could be found.
        """
        if len(shipsToDo) == 0:
            return crntPlacement

        crntLength = shipsToDo.pop(0)
        
        for pos in board.shuffledIndex():
            orientations = random.sample([ ShipShape.VERTICAL, ShipShape.HORIZONTAL ], 2)
            for orientation in orientations:
                tempShip = ShipShape(crntLength, pos, orientation)
                if tempShip.isInBoardBounds(board.width, board.height) and crntPlacement.fitsIn(tempShip):
                    tempPlacement = crntPlacement.copy()
                    tempPlacement.add(tempShip)
                    finalPlacement = self.__generateInner(shipsToDo, tempPlacement, board)
                    if finalPlacement != None:
                        return finalPlacement
        return None
    
    def print(self, boardWidth : int, boardHeight : int) -> None:
        """
        Prints the ShipPlacement to the board.

        Args:
            boardWidth (int): Amount of columns of the board.
            boardHeight (int): Amount of rows of the board.
        """
        board = Board(boardWidth, boardHeight)
        for ship in self.ships:
            for p in ship.occupiedTiles():
                board[p] = Board.SHIP
        board.print()