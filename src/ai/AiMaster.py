from ai.Board import Board
from ai.ClassicGameAi import ClassicGameAi
from ai.ProAi import ProAi
from ai.RandomGameAi import RandomGameAi
from ai.ShipPlacement import ShipPlacement
from ai.ShipPlacingAi import ShipPlacingAi
from ai.ShipShape import ShipShape
import random

from ai.BruteForceGameAi import BruteForceGameAi

class AiMaster:
    """
    Decides which ai to use when.

    Possible Ai's:
        Random Ai: When a mistake should be made.
        Classic Ai: Shoots as a human would do. (checkerboard pattern, completes ships, etc)
        BruteForce Ai: Tries all combinations of ships and shoots where a ship is in most of these combionations. As the calculations are quite heavy, it only starts when 3 Ships are left.
        Pro Ai: Just like BruteForce, but it doesn't pay attention to whether the ships overlap and thus drastically reduce computation time. It can be used from the beginning. It won't finish ships so if this ai is used, a Classic Ai will be kept up to date so it can handle found ships. 
        ShipPlacing Ai: Places the ships on the board. It will try to minimize the blocked area.
    """

    BRUTE_FORCE_SHIP_THRESHOLD = 3

    def __init__(self, boardWidth : int, boardHeight : int, chanceOfMistake : float, numShipPlacementTries : int, useProAi : bool, numShips : dict[int, int] = {2: 4, 3: 3, 4: 2, 5: 1}):
        """
        Constructor of the AiMaster class.

        Args:
            boardWidth (int): Amount of columns of the board.
            boardHeight (int): Amount of rows of the board.
            chanceOfMistake (float): Likelyhood that a random shot happens when getNextShot is called.
            numShipPlacementTries (int): How many tries should the ship Placing Ai have to minimize the blocked area.
            useProAi (bool): Determines if the Pro Ai will be used.
            numShips (_type_, optional): How many ships of which length are in the game. The key is the length of the ships and values is the number of that kind of ships. Defaults to {2: 4, 3: 3, 4: 2, 5: 1}.
        """
        self.board = Board(boardWidth, boardHeight)
        self.chanceOfMistake = chanceOfMistake
        self.numShips = numShips.copy()

        self.shipPlacingAi = ShipPlacingAi(numShipPlacementTries, self.board, numShips)
        self.randomAi      = RandomGameAi()
        self.classicAi     = ClassicGameAi(numShips)
        self.proAi         = ProAi() if useProAi else None
        self.bruteForceAi  = BruteForceGameAi()

        self.bruteForceMode = False

    def getNextShot(self) -> tuple[int]:
        """
        Calculates the next shot. 

        Returns:
            tuple[int]: Next shot position / tile.
        """
        if random.random() < self.chanceOfMistake:
            return self.randomAi.getNextShot(self.board)
        
        if self.__shouldUseBruteForce():
            return self.bruteForceAi.getNextShot()
        else:
            # only do pro ai if no SHIP_LIKELY tiles are on screen
            if self.proAi is not None and not any(self.board.check(cell, Board.SHIP_LIKELY) for cell in self.board.orderedIndex()):
                return self.proAi.getNextShot(self.board, self.classicAi.numShips)
            else:
                return self.classicAi.getNextShot(self.board)
    
    def submitInfo(self, pos : tuple[int], state : int) -> None:
        """
        Submits and forwards a new cell information to the ais.

        Args:
            pos (tuple[int]): The x and y coordinate of the cell in question.
            state (int): The found state. Either Board.SUBMIT_SHIP or Board.SUBMIT_NO_SHIP
        """
        if self.bruteForceMode:
            self.bruteForceAi.submitInfo(pos, state)
        else:
            self.board = self.classicAi.submitInfo(pos, state, self.board)

        self.board[pos] = state

    def generateShipPlacement(self) -> ShipPlacement:
        """
        Return the pre-calculated ShipPlacement.

        Returns:
            ShipPlacement: ShipPlacement used in the game.
        """
        return self.shipPlacingAi.get()
    
    def __shouldUseBruteForce(self) -> bool:
        """
        Returns whether the BruteForce Ai should be used for a shot.

        It can also kick of  its generation.

        Returns:
            bool: If the BruteForce Ai should be used for a shot.
        """

        # it will start using the brute force ai if t was already used or
        # - only a certain numbers of unknown ships left AND
        # - no SHIP_LIKELY tile is on the board

        if self.bruteForceMode:
            return True

        # ship count too big
        if sum(count for (_, count) in self.classicAi.numShips.items()) > AiMaster.BRUTE_FORCE_SHIP_THRESHOLD:
            return False
        
        # ship likely tile is on the board
        if any(self.board.check(cell, Board.SHIP_LIKELY) for cell in self.board.orderedIndex()):
            return False

        self.bruteForceMode = self.bruteForceAi.kickOffGeneration(self.board, self.classicAi.numShips)
        
        return False
    
    def printState(self) -> None:
        """
        Prints the current ai state for debugging purpose.
        """
        if self.bruteForceMode:
            print("Brute Force State")
            print(self.bruteForceAi.cellPropabilities)
            print("Possible Placaments: " + str(len(self.bruteForceAi.possiblePlacements)))
        
        else:
            print("Classic State")
            self.board.print()
            print(self.classicAi.numShips)
        print()
        