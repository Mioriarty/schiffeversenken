from ai.Board import Board
from ai.ShipPlacement import ShipPlacement
from ai.ShipShape import ShipShape
import random
from threading import Thread


class BruteForceGameAi:
    """
    To calculate the next shot it tries all valid ship placements and selects the most likely tile.
    """

    MAX_POSSIBLE_SHIP_LOCATIONS = 16

    def __init__(self):
        """
        The constructor of the BruteForceGameAi class.
        """
        self.possiblePlacements : set[ShipPlacement] = None
        self.cellPropabilities = {}
        self.generateThread = None

        self.submitInfoQueue = set()

    
    def kickOffGeneration(self, board : Board, numShipsLeft : dict[int, int]) -> bool:
        """
        Kicks off the generation of all possible ship placements. Abords if there are propabably to many to handle.

        Args:
            board (Board): The current board state
            numShipsLeft (dict[int, int]):  How many ships of which length are left to place. The key is the length of the ships and values is the number of that kind of ships.

        Returns:
            bool: Whether the creation will be successfull.
        """
        self.possiblePlacements = set()

        possibleShipLocations = self.__getAllPossibleShipLocations(board)
        print(f"Possible Ship Locations: {len(possibleShipLocations)}")

        if len(possibleShipLocations) > BruteForceGameAi.MAX_POSSIBLE_SHIP_LOCATIONS:
            return False

        shipsToDo : list[int] = []
        for length, count in sorted(numShipsLeft.items(), reverse=True):
            shipsToDo += [ length ] * count
        
        def threadFun():
            print("Start generating values for the brute force ai")
            self.__generatePossiblePlacements(shipsToDo, ShipPlacement(), possibleShipLocations, board)
            print("Done generating values for the brute force ai")

        self.generateThread = Thread(target=threadFun)
        self.generateThread.daemon = True
        self.generateThread.start()

        return True

    def __generatePossiblePlacements(self, shipsToDo : list[int], crntPlacement : ShipPlacement, possibleShipLocations : list[tuple[int]], board : Board):
        """
        Recursively generates all possible ship placaments.

        Args:
            shipsToDo (list[int]): Ship length's that are left to place on the board
            crntPlacement (ShipPlacement): Placement of all the ships that allready have been placed.
            possibleShipLocations (list[tuple[int]]): All possible tiles where a ship can be.
            board (Board): The current state of the board.
        """
        if len(shipsToDo) == 0:
            self.__submitPossibleShipPlacement(crntPlacement)
            return
        
        crntLength = shipsToDo.pop(0)

        for (x, y) in possibleShipLocations:
            orientations = random.sample([ ShipShape.VERTICAL, ShipShape.HORIZONTAL ], 2)
            for orientation in orientations:
                tempShip = ShipShape(crntLength, (x, y), orientation)

                # is the ship on the board
                if not tempShip.isInBoardBounds(board.width, board.height):
                    continue

                # check if it matches the boards requirements
                if not all(board.check(tile, Board.NO_INFO) for tile in tempShip.occupiedTiles()):
                    continue
            
                # check if it fits in the ship placement
                if not crntPlacement.fitsIn(tempShip):
                    continue
                
                tempPlacement = crntPlacement.copy()
                tempPlacement.add(tempShip)
                self.__generatePossiblePlacements(shipsToDo.copy(), tempPlacement, possibleShipLocations, board)

    def __getAllPossibleShipLocations(self, board : Board) -> list[tuple[int]]:
        """
        Returns all possible tiles where a ship can be.

        Args:
            board (Board): The current state of the board.

        Returns:
            list[tuple[int]]: All possible tiles where a ship can be.
        """
        return [ (x, y) for x, y in board.orderedIndex() if board.check((x, y), Board.NO_INFO) and (board.check((x+1, y), Board.NO_INFO) or board.check((x, y+1), Board.NO_INFO)) ]

    def __submitPossibleShipPlacement(self, placement : ShipPlacement) -> None:
        """
        Adds placement to the list and updates all cells total.

        Args:
            placement (ShipPlacement): Placement to be added.
        """
        self.possiblePlacements.add(placement)
        
        for cell in placement.occupiedCells():
            if cell in self.cellPropabilities:
                self.cellPropabilities[cell] += 1
            else:
                self.cellPropabilities[cell] = 1
    
    def getNextShot(self):
        """
        Calculates the next shot. 

        Raises:
            RuntimeError: If the generation hasnt been kicked off yet.

        Returns:
            tuple[int]: Next shot position / tile.
        """
        if self.generateThread is None:
            raise RuntimeError("The Brute Force Ai hasnt been started yet so it cannot advice a shot position")

        print("get next shot from brute force")
        bestCell = (-1, -1)
        bestProp = -1

        for cell, prop in self.cellPropabilities.items():
            if prop > bestProp:
                bestCell = cell
                bestProp = prop
        
        return bestCell

    
    def submitInfo(self, pos : tuple[int], state : int) -> None:
        """
        Submits and forwards a new cell information to the ais.

        Args:
            pos (tuple[int]): The x and y coordinate of the cell in question.
            state (int): The found state. Either Board.SUBMIT_SHIP or Board.SUBMIT_NO_SHIP
        """
        if self.generateThread is not None:
            self.generateThread.join()

        isHit = state == Board.SHIP
        toRemove = { placement for placement in self.possiblePlacements if placement.cellOccupied(pos) != isHit }

        for placement in toRemove:
            self.__removePossibleShipPlacement(placement)
        
        # shouldnt be able to shoot it again
        if pos in self.cellPropabilities:
            del self.cellPropabilities[pos]

    def __removePossibleShipPlacement(self, placement : ShipPlacement) -> None:
        """
        Removes placement from the list and updates all cells total.

        Args:
            placement (ShipPlacement): Placement to be removed.
        """
        for cell in placement.occupiedCells():
            if cell in self.cellPropabilities:
                self.cellPropabilities[cell] -= 1
        
        self.possiblePlacements.remove(placement)


