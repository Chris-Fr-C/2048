"""This module will provide a minimalistic user interface."""

import demo.board as board
from textual.app import App, ComposeResult
from textual.widgets import Digits, Placeholder, Footer
from textual.containers import Grid, Container
from textual.binding import Binding


class BoardAppFooter(Placeholder):
    pass


class BoardApp(App):
    CSS = """
    Screen { align: center middle;}
    Grid { align: center middle; layout: grid; grid-size: 4 4; height: 95%; padding: 2; }
    Digits { width: auto; }
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
        Binding(key="left", action="left", key_display="↑", description="", show=True),
        Binding(key="right", action="right", key_display="↓", description="", show=True),
        Binding(key="up", action="up", key_display="←",description="", show=True),
        Binding(key="down", action="down",key_display="→", description="", show=True),
    ]

    def compose(self) -> ComposeResult:
        with Grid(classes="Board"):
            for row_num, row in enumerate(self.GAME.cells):
                for col in row:
                    yield Placeholder(label=f"{row_num} {col} - ")
        with Container():
            yield Footer()

    def on_ready(self) -> None:
        # self.set_interval(1, self.update_clock)
        pass


if __name__ == "__main__":
    app = BoardApp()
    app.run()
