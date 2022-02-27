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

    BRUTE_FORCE_SHIP_THRESHOLD = 3

    def __init__(self, boardWidth : int, boardHeight : int, chanceOfMistake : float, numShipPlacementTries : int, useProAi : bool, numShips : dict[int, int] = {2: 4, 3: 3, 4: 2, 5: 1}):
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
        if self.bruteForceMode:
            self.bruteForceAi.submitInfo(pos, state)
        else:
            self.board = self.classicAi.submitInfo(pos, state, self.board)

        self.board[pos] = state

    def generateShipPlacement(self) -> ShipPlacement:
        return self.shipPlacingAi.get()
    
    def __shouldUseBruteForce(self) -> bool:
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

        self.bruteForceAi.kickOffGeneration(self.board, self.classicAi.numShips)
        self.bruteForceMode = True
        
        return False
    
    def printState(self) -> None:
        if self.bruteForceMode:
            print("Brute Force State")
            print(self.bruteForceAi.cellPropabilities)
            print("Possible Placaments: " + str(len(self.bruteForceAi.possiblePlacements)))
        
        else:
            print("Classic State")
            self.board.print()
            print(self.classicAi.numShips)
        print()

if __name__ == "__main__":

    ai = AiMaster(11, 11, 0)
    placement = ai.generateShipPlacement()
    placement.print(ai.board.width, ai.board.height)

    bfAi = BruteForceGameAi()

    while True:
        z = input()
        if z == "now":
            bfAi.kickOffGeneration(ai.board, {2: 4, 3: 3, 4: 2, 5: 1})


        shot = ai.getNextShot()
        val = Board.SUBMIT_SHIP if placement.cellOccupied(shot) else Board.SUBMIT_NO_SHIP
        ai.submitInfo(shot, val)

        ai.board.print()
        

        
        