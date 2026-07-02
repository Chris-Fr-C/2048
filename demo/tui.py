"""This module will provide a minimalistic user interface."""

import demo.board as board
from textual.app import App, ComposeResult
from textual.widgets import Digits, Placeholder, Footer, Label, Button
from textual.containers import Grid, Container
from textual.binding import Binding


class BoardAppFooter(Placeholder):
    pass


class Cell(Container):
    """Represents a specific cell of the table"""

    value: board.PowerOfTwo
    display_str: str

    def __init__(self, value: board.PowerOfTwo, display_str: str, **kwargs):
        super().__init__(**kwargs)
        self.value = value
        self.display_str = display_str

    def compose(self) -> ComposeResult:
        with Container(classes="Cell"):
            yield Digits(self.display_str)

    def on_mount(self) -> None:
        # Adding the dynamic color.
        if self.value >= board.PowerOfTwo(0):
            value = min(self.value, board.PowerOfTwo(11))
            self.add_class(f"val-{value}")


class BoardApp(App):
    CSS = """
    Screen { align: center middle;}
    Grid { align: center middle; layout: grid; grid-size: 4 4; height: 95%; padding: 2; }
    Digits { width: auto; color: black; }
    .Cell { border: solid black;  }

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
    GAME = board.Board(board.BoardConfig(placeholder=" "))
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
    ]

    def show_grid(self) -> ComposeResult:
        for row_num, row in enumerate(self.GAME.cells):
            for col in row:
                yield Cell(col, self.GAME._display_power(col))

    def compose(self) -> ComposeResult:
        with Grid(classes="Board"):
            yield from self.show_grid()

        with Container():
            yield Footer()

    def on_mount(self) -> None:
        pass


if __name__ == "__main__":
    app = BoardApp()
    app.run()
