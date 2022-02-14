from ai.Board import Board
from ai.ClassicGameAi import ClassicGameAi
from ai.RandomGameAi import RandomGameAi
from ai.ShipPlacement import ShipPlacement
from ai.ShipPlacingAi import ShipPlacingAi
from ai.ShipShape import ShipShape
import random

from ai.BruteForceGameAi import BruteForceGameAi

class AiMaster:

    BRUTE_FORCE_THRESHOLD = 85

    def __init__(self, boardWidth : int, boardHeight : int, chanceOfMistake : float, numShipPlacementTries : int, numShips : dict[int, int] = {2: 4, 3: 3, 4: 2, 5: 1}):
        self.board = Board(boardWidth, boardHeight)
        self.chanceOfMistake = chanceOfMistake
        self.numShips = numShips.copy()

        self.shipPlacingAi = ShipPlacingAi(numShipPlacementTries, self.board, numShips)
        self.randomAi      = RandomGameAi()
        self.classicAi     = ClassicGameAi(numShips)
        self.bruteForceAi  = BruteForceGameAi()

        self.bruteForceMode = False

    def getNextShot(self) -> tuple[int]:
        if random.random() < self.chanceOfMistake:
            return self.randomAi.getNextShot(self.board)
        
        if self.__shouldUseBruteForce():
            return self.bruteForceAi.getNextShot()
        else:
            return self.classicAi.getNextShot(self.board)
    
    def submitInfo(self, pos : tuple[int], state : int):
        if self.bruteForceMode:
            self.bruteForceAi.submitInfo(pos, state)
            if not self.bruteForceAi.generationDone():
                self.board = self.classicAi.submitInfo(pos, state, self.board)
        else:
            self.board = self.classicAi.submitInfo(pos, state, self.board)
        
        self.board[pos] = state

    def generateShipPlacement(self) -> ShipPlacement:
        return self.shipPlacingAi.get()
    
    def __shouldUseBruteForce(self) -> bool:
        # it will start using the brute force ai if t was already used or
        # - a certain number of cell infos are known AND
        # - no SHIP_LIKELY tile is on the board

        if self.bruteForceMode:
            return self.bruteForceAi.generationDone()
        
        knownTilesCount = 0
        for cell in self.board.orderedIndex():
            if self.board.check(cell, Board.SHIP_LIKELY):
                return False
            
            if not self.board.check(cell, Board.NO_INFO):
                knownTilesCount += 1

        if knownTilesCount >= AiMaster.BRUTE_FORCE_THRESHOLD:
            self.bruteForceAi.start(self.board, self.classicAi.numShips)
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
            bfAi.start(ai.board, {2: 4, 3: 3, 4: 2, 5: 1})


        shot = ai.getNextShot()
        val = Board.SUBMIT_SHIP if placement.cellOccupied(shot) else Board.SUBMIT_NO_SHIP
        ai.submitInfo(shot, val)

        ai.board.print()
        

        
        