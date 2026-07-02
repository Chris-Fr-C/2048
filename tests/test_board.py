import demo.board as board
import pytest


def test_board_init():
    cfg = board.BoardConfig()
    brd = board.Board(cfg)
    initial_state = str(brd)
    assert initial_state.count("2") == cfg.amount_initial
    size = cfg.size.height * cfg.size.width
    assert initial_state.count(cfg.placeholder) == size - cfg.amount_initial


_4 = board.PowerOfTwo(2)
_2 = board.PowerOfTwo(1)
_0 = board.PowerOfTwo(0)
_W = board.PowerOfTwo(11)


def test_board_align():
    cfg = board.BoardConfig(
        size=board.BoardDimensions(board.Height(4), board.Width(4)),
    )
    brd = board.Board(
        cfg,
        [
            [_2, _0, _0, _0],
            [_0, _0, _0, _0],
            [_2, _0, _0, _0],
            [_0, _0, _0, _0],
        ],
    )
    brd.align(board.Direction.DOWN)
    assert brd.cells == [
        [_0, _0, _0, _0],
        [_0, _0, _0, _0],
        [_2, _0, _0, _0],
        [_2, _0, _0, _0],
    ]

    assert brd.align(board.Direction.UP).cells == [
        [_2, _0, _0, _0],
        [_2, _0, _0, _0],
        [_0, _0, _0, _0],
        [_0, _0, _0, _0],
    ]
    assert brd.align(board.Direction.RIGHT).cells == [
        [_0, _0, _0, _2],
        [_0, _0, _0, _2],
        [_0, _0, _0, _0],
        [_0, _0, _0, _0],
    ]

    assert brd.align(board.Direction.LEFT).cells == [
        [_2, _0, _0, _0],
        [_2, _0, _0, _0],
        [_0, _0, _0, _0],
        [_0, _0, _0, _0],
    ]


def test_board_move_down():
    cfg = board.BoardConfig(
        size=board.BoardDimensions(board.Height(4), board.Width(4)),
    )
    brd = board.Board(
        cfg,
        [
            [_2, _0, _0, _0],
            [_0, _0, _0, _0],
            [_2, _0, _0, _0],
            [_0, _0, _0, _0],
        ],
    )
    brd.move_down()

    assert brd.cells == [
        [_0, _0, _0, _0],
        [_0, _0, _0, _0],
        [_0, _0, _0, _0],
        [_4, _0, _0, _0],
    ]


@pytest.mark.parametrize(
    "cells,expected_state",
    [
        pytest.param(
            [
                [_2, _0, _0, _0],
                [_0, _0, _0, _0],
                [_2, _0, _0, _0],
                [_0, _0, _0, _0],
            ],
            board.GameState.PLAYING,
        ),
        pytest.param(
            [
                [_2, _0, _0, _0],
                [_0, _0, _0, _0],
                [_2, _0, _W, _0],
                [_0, _0, _0, _0],
            ],
            board.GameState.VICTORY,
        ),
        pytest.param(
            [
                [_2, _4, _2, _4],
                [_4, _2, _4, _2],
                [_2, _4, _2, _4],
                [_4, _2, _4, _2],
            ],
            board.GameState.DEFEAT,
        ),
    ],
)
def test_board_state(cells: board.Matrix, expected_state: board.GameState):
    cfg = board.BoardConfig(
        size=board.BoardDimensions(board.Height(4), board.Width(4)),
    )
    brd = board.Board(
        cfg,
        override_cells=cells,
    )

    assert brd.state == expected_state
