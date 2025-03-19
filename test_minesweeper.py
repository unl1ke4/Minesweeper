import pytest
from minesweeper import GameBoard

def test_board_initialization():
    board = GameBoard(10, 10, 10)
    assert board.rows == 10
    assert board.cols == 10
    assert board.mines == 10
    assert len(board.mine_positions) == 10

def test_mine_placement():
    board = GameBoard(10, 10, 10)
    mine_count = sum(row.count(-1) for row in board.board)
    assert mine_count == 10

def test_number_calculation():
    board = GameBoard(5, 5, 5)
    for r in range(5):
        for c in range(5):
            if board.board[r][c] == -1:
                continue
            adjacent_mines = sum(
                (r + dr, c + dc) in board.mine_positions
                for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                if (dr, dc) != (0, 0)
            )
            assert board.board[r][c] == adjacent_mines

if __name__ == "__main__":
    pytest.main()