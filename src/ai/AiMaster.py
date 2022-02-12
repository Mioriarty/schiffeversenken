from ai.Board import Board
from ai.ClassicGameAi import ClassicGameAi
from ai.RandomGameAi import RandomGameAi
from ai.ShipPlacement import ShipPlacement
from ai.ShipShape import ShipShape
import random

from ai.BruteForceGameAi import BruteForceGameAi

class AiMaster:

    def __init__(self, boardWidth : int, boardHeight : int, chanceOfMistake : float, numShips : dict[int, int] = {2: 4, 3: 3, 4: 2, 5: 1}):
        self.board = Board(boardWidth, boardHeight)
        self.chanceOfMistake = chanceOfMistake
        self.numShips = numShips.copy()

        self.randomAi  = RandomGameAi()
        self.classicAi = ClassicGameAi(numShips)
    

    def getNextShot(self) -> tuple[int]:
        if random.random() < self.chanceOfMistake:
            return self.randomAi.getNextShot(self.board)
        
        return self.classicAi.getNextShot(self.board)
    
    def submitInfo(self, pos : tuple[int], state : int):
        self.board = self.classicAi.submitInfo(pos, state, self.board)

    def generateShipPlacement(self) -> ShipPlacement:
        return ShipPlacement.generate(self.board.width, self.board.height, self.numShips)

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
        

        
        