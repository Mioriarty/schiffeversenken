from ai.Board import Board
from ai.ShipPlacement import ShipPlacement
from threading import Thread


class ShipPlacingAi:
    """
    Places a certain number of ships in a board.

    It does so in multiple tries (if numTries > 1) trying to minimize the total blocked area.
    The consequence of that is, that you dont get as much info by finding one ship tile.

    But numTries shouln't be extremely high, as this will result in predictive behavior.

    Attributes:
        numTries (int): Number of placement tries.
        board (Board): The board on which to place the ships.
        numShips (dict[int, int]): How many ships of which length. The key is the length of the ships and values is the number of that kind of ships.
        placement (ShipPlacement): The final generated placement.
    """

    def __init__(self, numTries : int, board : Board, numShips : dict[int, int]):
        """
        Constructor of the ShipPlacingAi class.

        Starts a new thread where the placement is calculated.

        Args:
            numTries (int): Number of placement tries.
            board (Board): The board on which to place the ships.
            numShips (dict[int, int]): How many ships of which length. The key is the length of the ships and values is the number of that kind of ships.
        """
        self.generateThred = Thread(target=self.__generate, args=(numTries, board, numShips))
        self.placement = None

        self.generateThred.daemon = True
        self.generateThred.start()
    
    def __generate(self, numTries : int, board : Board, numShips : dict[int, int]):
        """
        Generates the placement by minimizing the blocked area.

        Args:
            numTries (int): Number of placement tries.
            board (Board): The board on which to place the ships.
            numShips (dict[int, int]): How many ships of which length. The key is the length of the ships and values is the number of that kind of ships.
        """
        bestPlacement = None
        bestBlockedCellsCount = 1 << 16

        for _ in range(numTries):
            placement = ShipPlacement.generate(board.width, board.height, numShips)
            blockedCellsCount = len(set(cell for cell in placement.blockedCells() if board.isInBounds(cell))) # discard duplicates

            if blockedCellsCount < bestBlockedCellsCount:
                bestPlacement = placement
                bestBlockedCellsCount = blockedCellsCount

        print(f"Placement Generation Done ({bestBlockedCellsCount})")
        
        self.placement = bestPlacement

    def get(self) -> ShipPlacement:
        """
        Returns the final generated placement. 

        If the generation is not done yet, it waits for the thread to finish.

        Returns:
            ShipPlacement: The final generated placement. 
        """
        self.generateThred.join()
        return self.placement