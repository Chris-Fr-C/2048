"""This module will provide a minimalistic user interface."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Grid
from textual.screen import ModalScreen
from textual.widgets import Digits, Footer, Label, Log
import demo.ai as ai
import demo.board as board
from typing import Callable, ClassVar, cast
from threading import Thread
import sys


class PopOver(ModalScreen):
    """General popover class to use for modal messages."""
    BINDINGS = [
        Binding(key="escape,space,q", action="close", description="Close Overlay")
    ]

    def __init__(
        self, message: str, callback: Callable[[], None] = lambda: None, **kwargs
    ):
        super().__init__(**kwargs)
        self.message = message
        self.callback = callback

    def compose(self) -> ComposeResult:
        # A container centered via CSS holding the message box
        with Container(id="PopOver-Content"):
            yield Label(self.message, id="PopOver-Text")
            yield Footer()

    def action_close(self) -> None:
        self.dismiss()
        self.callback()

class AiPopover(ModalScreen):
    """General popover class to use for modal messages."""
    BINDINGS = [
        Binding(key="escape,space,q", action="close", description="Close Overlay")
    ]

    AI: ClassVar[ai.AIHelper] = ai.LLMImplementation()
    state: board.Board

    def __init__(
        self,  state: board.Board, **kwargs
    ):
        super().__init__(**kwargs)
        self.state=state

    def compose(self) -> ComposeResult:
        # A container centered via CSS holding the message box
        log = Log(id="PopOver-Text")
        with Container(id="PopOver-Content"):
            yield log
            yield Footer()
        
    def on_mount(self)->None:
        log: Log = cast(Log, self.query_one("#PopOver-Text"))
        def target():
            res = self.AI.help(self.state)
            log.write_line(f"AI recommendation: {res}")

        log.write_line("Ai help requested. Starting daemon.")
        thread = Thread(target=target, daemon=True)
        thread.start()


    def action_close(self) -> None:
        self.dismiss()





class Cell(Container):
    """Represents a specific cell of the table"""

    value: board.PowerOfTwo
    display_str: str

    def __init__(self, value: board.PowerOfTwo, display_str: str, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.display_str = display_str

    def compose(self) -> ComposeResult:
        yield Digits(self.display_str)

    def on_mount(self) -> None:
        self.add_class("Cell")

        # Adding the dynamic color.
        if self.value >= board.PowerOfTwo(0):
            value = min(self.value, board.PowerOfTwo(11))
            self.add_class(f"val-{value}")


class BoardApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    PopOver {
        align: center middle;
        background: rgba(0, 0, 0, 0.6);
    }
    #PopOver-Content {
        width: 40;
        height: auto;
        background: #34495e;
        border: heavy #2c3e50;
        padding: 2 4;
        align: center middle;
    }

    #PopOver-Text {
        text-align: center;
        width: 100%;
        color: #ecf0f1;
        margin-bottom: 1;
    }

    Grid {
        layout: grid;
        grid-size: 4 4;

        grid-columns: 10 10 10 10;
        grid-rows: 5 5 5 5;

        width: auto;
        height: auto;
        border: heavy gray;
        background: #bbada0; /* Completely stole the color from the original website */
    }

    Digits {
        width: 100%;
        height: 100%;
    }

    .Cell {
        content-align: center middle;
        padding: 0;
        margin: 0;
    }

    Message {
        width: 100%;
        height: 100%;
        align: center middle;
    }

    /* Hardcoded values for the colors cause artistiiiiiic */
    .val-0  { background: #eceff1; color: #607d8b; }
    .val-1  { background: #e8f5e9; color: #2e7d32; }
    .val-2  { background: #c8e6c9; color: #1b5e20; }
    .val-3  { background: #a5d6a7; color: #1b5e20; }
    .val-4  { background: #e1bee7; color: #4a148c; }
    .val-5  { background: #ce93d8; color: #4a148c; }
    .val-6  { background: #ba68c8; color: #ffffff; }
    .val-7  { background: #f8bbd0; color: #880e4f; }
    .val-8  { background: #ff8a80; color: #b71c1c; }
    .val-9  { background: #ff5252; color: #ffffff; }
    .val-10 { background: #ff1744; color: #ffffff; }
    .val-11 { background: #d50000; color: #ffffff; }
    """
    GAME: ClassVar[board.Board] = board.Board(board.BoardConfig(placeholder=" "))
    BINDINGS = [
        Binding(key="q", action="quit", description="Quit the app"),
        Binding(key="r", action="restart", description="Restart"),
        Binding(
            key="question_mark",
            action="help",
            description="Show AI recommendation",
            key_display="?",
        ),
        # The ascii codes where annoying to find :'D
        Binding(key="up", action="up", key_display="↑", description="", show=True),
        Binding(key="down", action="down", key_display="↓", description="", show=True),
        Binding(key="left", action="left", key_display="←", description="", show=True),
        Binding(
            key="right", action="right", key_display="→", description="", show=True
        ),
        # Also allowing wasd.
        Binding(key="w", action="up", key_display="w", description="", show=True),
        Binding(key="s", action="down", key_display="s", description="", show=True),
        Binding(key="a", action="left", key_display="a", description="", show=True),
        Binding(key="d", action="right", key_display="d", description="", show=True),
    ]

    def show_grid(self) -> ComposeResult:
        for row_num, row in enumerate(self.GAME.cells):
            for col in row:
                yield Cell(col, self.GAME._display_power(col))

    def compose(self) -> ComposeResult:
        self.base_grid = Grid(classes="Board", id="Grid")

        with self.base_grid:
            yield from self.show_grid()

        yield Footer()

    def refresh_board(self) -> None:
        grid = self.base_grid
        state = self.GAME.state
        grid.query().remove()  # Who is here for performances anyway.

        if state == board.GameState.DEFEAT:
            self.base_grid.remove_class("Board").add_class("Message")
            self.push_screen(
                PopOver(message="You lost :'(", callback=lambda: self.action_restart())
            )
            return
        elif state == board.GameState.VICTORY:
            self.base_grid.remove_class("Board").add_class("Message")

            self.push_screen(
                PopOver("You won :D", callback=lambda: self.action_restart())
            )
            return

        self.base_grid.remove_class("Message").add_class("Board")
        grid.mount(*self.show_grid())


    def _move(self, direction: board.Direction)->None:
        try:
            self.GAME.move(direction).fill_new()
            self.refresh_board()
        except board.IllegalMoveException:
            pass

    def action_left(self) -> None:
        self._move(board.Direction.LEFT)

    def action_right(self) -> None:
        self._move(board.Direction.RIGHT)

    def action_up(self) -> None:
        self._move(board.Direction.UP)

    def action_down(self) -> None:
        self._move(board.Direction.DOWN)

    def action_restart(self) -> None:
        self.GAME.reset()
        self.refresh_board()

    def action_help(self) -> None:
        # This part takes quite a while so we will make it run on a separate thread.
        self.push_screen(AiPopover(self.GAME))


if __name__ == "__main__":
    app = BoardApp()
    app.run()
