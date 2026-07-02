import demo.board as board

def test_question_1():
    cfg = board.BoardConfig()
    brd = board.Board(cfg)
    initial_state = str(brd)
    assert initial_state.count("2") == cfg.amount_initial
    size = cfg.size.height * cfg.size.width
    assert initial_state.count(board.Board.PLACEHOLDER) == size-cfg.amount_initial

