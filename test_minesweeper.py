import pytest
from minesweeper import GameBoard
from unittest.mock import patch

@pytest.fixture
def sample_board():
    return GameBoard(10, 10, 10)

def test_board_initialization():
    board = GameBoard(10, 10, 10)
    assert board.rows == 10
    assert board.cols == 10
    assert board.mines == 10
    assert len(board.mine_positions) == 10

@pytest.parametrize("rows, cols, mines", [
    (5, 5, 5),
    (10, 10, 10),
    (15, 15, 20)
])

def test_mine_placement():
    board = GameBoard(10, 10, 10)
    mine_count = sum(row.count(-1) for row in board.board)
    assert mine_count == 10

@patch("minesweeper.random.sample")
def test_mine_positions(mock_sample):
    mock_sample.return_value = [(0, 0), (1, 1), (2, 2)]  # Фіксовані міни
    board = GameBoard(5, 5, 3)
    assert board.mine_positions == {(0, 0), (1, 1), (2, 2)}

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