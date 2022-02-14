from ai.Board import Board
from ai.ShipPlacement import ShipPlacement
from threading import Thread


class ShipPlacingAi:

    def __init__(self, numTries : int, board : Board, numShips : dict[int, int]):
        self.generateThred = Thread(target=self.__generate, args=(numTries, board, numShips))
        self.placement = None

        self.generateThred.daemon = True
        self.generateThred.start()
    
    def __generate(self, numTries : int, board : Board, numShips : dict[int, int]):
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
        self.generateThred.join()
        return self.placement