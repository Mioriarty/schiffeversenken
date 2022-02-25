import random
from typing import Generator


class Board:
    """
    Holds possible states of any cell of a board as well as stretegic states.

    Attributes:
        width (int): Amount of columns.
        height (int): Amount of rows.
        data (list[int]): All stored states

    """

    # internal values
    NO_INFO         = 0b00001
    CHECKED_NO_SHIP = 0b00010
    DEDUSED_NO_SHIP = 0b00100
    SHIP            = 0b01000
    SHIP_LIKELY     = 0b10000

    # values to submit
    SUBMIT_SHIP    = SHIP
    SUBMIT_NO_SHIP = CHECKED_NO_SHIP

    def __init__(self, width : int, height : int):
        """
        Constructor of the Board class.

        Args:
            width (int): Amount of columns.
            height (int): Amount of rows.
        """
        self.width = width
        self.height = height

        self.data = [[Board.NO_INFO for _ in range(width)] for _ in range(height)]
    
    def __getitem__(self, cell : tuple[int]) -> int:
        """
        Gets the state of a specified cell.

        Args:
            cell (tuple[int]): x and y coordinate of the cell

        Returns:
            int: Current state of the specified cell.
        """
        return self.data[cell[0]][cell[1]]
    
    def __setitem__(self, cell : tuple[int], newVal : int) -> None:
        """
        Gets the state of a specified cell.

        Args:
            cell (tuple[int]): x and y coordinate of the cell
            newVal (int): New state of the specified cell
        """
        self.data[cell[0]][cell[1]] = newVal
    
    def check(self, cell : tuple[int], value : int) -> bool:
        """
        Checks if the cell is in one or more states.

        To submit multiple states, seperate them with |. Example: check((x, y), Board.NO_INFO | Board.DEDUSED_NO_SHIP)

        Args:
            cell (tuple[int]): x and y coordinate of the cell
            value (int): On ore more states (seperated by |) that the states should e checked against.

        Returns:
            bool: If the states cell is included in the specified states .
        """
        return self.isInBounds(cell) and bool(self[cell] & value)
    
    def isInBounds(self, cell : tuple[int]) -> bool:
        """
        Checks if a certain coordinate is in bounds of the board.

        Args:
            cell (tuple[int]): x and y coordinate to be checked against.

        Returns:
            bool: Ifthecoordinate is in bounds of the board.
        """
        return cell[0] >= 0 and cell[1] >= 0 and cell[0] < self.width and cell[1] < self.height

    def shuffledIndex(self) -> Generator[tuple[int], None, None]:
        """
        Enables to loop through all cells in the board randomly.

        Yields:
            Generator[tuple[int], None, None]: All cells on the board in a random order.
        """
        for y in random.sample(list(range(self.height)), self.height):
            for x in random.sample(list(range(self.width)), self.width):
                yield (x, y)
    
    def orderedIndex(self) -> Generator[tuple[int], None, None]:
        """
        Enables to loop through all cells in the board in order.

        Yields:
            Generator[tuple[int], None, None]: All cells on the board in order.
        """
        for y in range(self.height):
            for x in range(self.width):
                yield (x, y)

    def print(self) -> None:
        """
        Prints the board's state to the console.
        """
        for y in range(self.height):
            for x in range(self.width):
                val = self.data[x][y]

                if val == Board.NO_INFO:
                    print(".", end="")
                elif val == Board.CHECKED_NO_SHIP:
                    print("x", end="")
                elif val == Board.DEDUSED_NO_SHIP:
                    print("o", end="")
                elif val == Board.SHIP:
                    print("S", end="")
                elif val == Board.SHIP_LIKELY:
                    print("?", end="")
                else:
                    print("!", end="")
            print()
    


    