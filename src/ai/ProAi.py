from ai.Board import Board
from ai.ShipShape import ShipShape

class ProAi:
    """
    Sets shots using a mechenism that i saw here: https://www.youtube.com/watch?v=Sef2-aHGZDU.
    
    It's basically the BruteForceGameAi but it doesn't care if 2 ships of a guessed Placament overlap.
    """

    def __init__(self):
        """
        Constructor if the ProAi class.
        """
        self.propabilities = None
    
    def update(self, board : Board, numShips : dict[int, int]) -> None:
        """
        Updates stored propabilities.

        Args:
            board (Board): Board state.
            numShips (dict[int, int]): How many ships of which length. The key is the length of the ships and values is the number of that kind of ships.
        """
        possibleShipLocations = self.__getAllPossibleShipLocations(board)
        

        self.propabilities = [ [0 for _ in range(board.width) ] for _ in range(board.height) ]

        for (length, count) in numShips.items():
            if count == 0:
                continue
                
            props = self.__cellPropsForShip(board, possibleShipLocations, length)

            for (x, y) in board.orderedIndex():
                self.propabilities[x][y] += props[x][y] * count
        

    def __cellPropsForShip(self, board : Board, possibleShipLocations : list[tuple[int]], length : int) -> list[list[float]]:
        """
        Calculates for each cell the likelyhood that a ship of a given length is there.

        Args:
            board (Board): Board state.
            possibleShipLocations (list[tuple[int]]): All cells a ships can be.
            length (int): Length of the ship to be looking for.

        Raises:
            ValueError: If no possible ship position was found. That should not happen.

        Returns:
            list[list[float]]: For all cells the propability that a ship of a given length is there.
        """
        orientations = [ ShipShape.VERTICAL, ShipShape.HORIZONTAL ]
        props = [ [0 for _ in range(board.width) ] for _ in range(board.height) ]
        placementCount = 0

        for (x, y) in possibleShipLocations:
            for orientation in orientations:
                tempShip = ShipShape(length, (x, y), orientation)

                # is the ship on the board
                if not tempShip.isInBoardBounds(board.width, board.height):
                    continue

                # check if it matches the boards requirements
                if not all(board.check(tile, Board.NO_INFO) for tile in tempShip.occupiedTiles()):
                    continue
                    
                # register ship
                placementCount += 1
                for (shipX, shipY) in tempShip.occupiedTiles():
                    props[shipX][shipY] += 1
        
        if placementCount == 0:
            raise ValueError(f"Ship of length {length} coudnt be placed on the board")

        
        # normalize everything to 1
        for (x, y) in board.orderedIndex():
            props[x][y] = (props[x][y] / placementCount)**2
        
        return props

    def __getAllPossibleShipLocations(self, board : Board) -> list[tuple[int]]:
        """
        Calculates all cells a ships can be.

        Args:
            board (Board): Board state.

        Returns:
            list[tuple[int]]: All cells a ships can be.
        """
        return [ (x, y) for x, y in board.orderedIndex() if board.check((x, y), Board.NO_INFO) and (board.check((x+1, y), Board.NO_INFO) or board.check((x, y+1), Board.NO_INFO)) ]
    
    def getNextShot(self, board : Board, numShips : dict[int, int]) -> tuple[int]:
        """
        Calculates the next shot. 

        Args:
            board (Board): The current board state on which it shoots.
            numShips (dict[int, int]): How many ships of which length. The key is the length of the ships and values is the number of that kind of ships.

        Returns:
            tuple[int]: Next shot position / tile.
        """
        self.update(board, numShips)

        bestProp = -1
        bestCell = (-1, -1)

        for (x, y) in board.shuffledIndex():
            if self.propabilities[x][y] > bestProp:
                bestProp = self.propabilities[x][y]
                bestCell = (x, y)
        
        return bestCell