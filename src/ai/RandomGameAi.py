
from ai.Board import Board


class RandomGameAi:
    """
    Shoots randomly on th board. Only pays attention where you already shot at.
    """

    def getNextShot(self, board : Board) -> tuple[int]:
        """
        Calculates the next shot. 

        Args:
            board (Board): The current board state on which it shoots.

        Returns:
            tuple[int]: Next shot position / tile.
        """
        for cell in board.shuffledIndex():
            if not(board.check(cell, Board.SHIP | Board.CHECKED_NO_SHIP)):
                return cell