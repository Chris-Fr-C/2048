from typing import ClassVar, NamedTuple, NewType, Self
import random


# I define strong types just so we have the linter that
# helps us catch any mistakes that would come from mixing those two
# integers. I also recommend that with strings etc...
Height = NewType("Height", int)
"""Height of the matrix."""
Width = NewType("Width", int)
"""Width of the matrix"""

PowerOfTwo = NewType("PowerOfTwo", int)
"""We can just represent the exponent of two instead of handling the computation all the time.
This can also simplify if i decide to use pictures, colors, or anything else instead of powers of two."""


# Those two are not strong types to avoid having to typehint
# the Sequence for lists while still being explicit.
type X = int
"""X coordinate."""

type Y = int
"""Y coordinate."""


class CellPosition(NamedTuple):
    x: X
    y: Y


class BoardDimensions(NamedTuple):
    height: Height
    width: Width


class BoardConfig(NamedTuple):
    size: BoardDimensions = BoardDimensions(Height(4), Width(4))
    amount_new_per_tick: int = 3
    """This represents how many 2 appear on screen at each tick."""
    amount_initial: int = 4
    """How many two we have in the initial state."""


MAX_ITER = 100_000
"""Just a safety param to avoid infinite loops."""


class Board:
    """
    Represents the 2048 board and the actions
    that can be performed on it.
    """

    _cfg: BoardConfig
    cells: list[list[PowerOfTwo]]
    PLACEHOLDER: ClassVar[str] = "."
    """What we print when there is no value."""

    def __init__(self, cfg: BoardConfig | None = None):
        # Optional: Here we can do some validation on hte board config.
        self._cfg = cfg or BoardConfig()
        assert self._cfg.size.height > 1
        assert self._cfg.size.width > 1
        assert self._cfg.amount_new_per_tick > 0

        self._init_board()

    def _random_cell(self) -> CellPosition:
        """Retursn a random position on the board.

        Returns:
           Tuple with the random position.
        """
        return CellPosition(
            x=random.randint(
                0,
                self._cfg.size.height - 1,
            ),
            y=random.randint(
                0,
                self._cfg.size.width - 1,
            ),
        )

    def _init_board(self) -> Self:
        """Initialize empty cells and initial 2.

        Initializes the board with PowerOfTwo(0) for empty cells
        and PowerOfTwo(1) for some cells randomly picked.

        Returns:
            Fluent setter.
        """
        # We initialize things empty.
        # We could use numpy btw but thats an additional dependency for just a small project.
        self.cells = [
            [PowerOfTwo(0) for _ in range(self._cfg.size.width)]
            for _ in range(self._cfg.size.height)
        ]
        random_locations: set[CellPosition] = set()
        i = 0
        while len(random_locations) < self._cfg.amount_initial:
            i += 1
            assert i < MAX_ITER
            random_locations.add(self._random_cell())

        for loc in random_locations:
            self.cells[loc.x][loc.y] = PowerOfTwo(1)

        return self

    def _display_power(self, x: PowerOfTwo) -> str:
        """Returns a string to display the power of two

        Args:
            x (PowerOfTwo): value

        Returns:
            string adapted, or placeholder for the PowerOfTwo(0)
        """
        if x == PowerOfTwo(0):
            return self.PLACEHOLDER
        return str(2**x)

    def __str__(self) -> str:
        """Stringify the object.

        Returns:
           String for pretty print
        """
        return "\n".join(
            "\t".join(self._display_power(x) for x in row) for row in self.cells
        )
