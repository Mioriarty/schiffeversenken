
from Board import Board


class RandomGameAi:

    def getNextShot(self, board : Board) -> tuple[int]:
        for cell in board.shuffledIndex():
            if not(board.check(cell, Board.SHIP | Board.CHECKED_NO_SHIP)):
                return cell