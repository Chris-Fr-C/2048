from typing import ClassVar, Literal, NamedTuple, NewType, Self
import random
from enum import Enum, auto


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

Matrix = list[list[PowerOfTwo]]

# Those two are not strong types to avoid having to typehint
# the Sequence for lists while still being explicit.
type X = int
"""X coordinate."""

type Y = int
"""Y coordinate."""


class GameState(Enum):
    PLAYING = auto()
    VICTORY = auto()
    DEFEAT = auto()


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()


class CellPosition(NamedTuple):
    x: X
    y: Y


class BoardDimensions(NamedTuple):
    height: Height
    """Equivalent to the max x."""
    width: Width
    """Equivalent to max y."""


class BoardConfig(NamedTuple):
    size: BoardDimensions = BoardDimensions(Height(4), Width(4))
    amount_new_per_tick: int = 3
    """This represents how many 2 appear on screen at each tick."""
    amount_initial: int = 4
    """How many two we have in the initial state."""
    win_condition: PowerOfTwo = PowerOfTwo(11)
    """When do we win. Default to reaching 2**11=2048"""
    placeholder: str = "."
    """What we print when there is no value (ie: PowerOfTwo(0))"""


class MoveStatus(Enum):
    """This enum indicates the result when we ask one cell to perform a move operation."""

    NO_OP = auto()
    """If cannot move to the adjacent cell."""
    MERGE = auto()
    """If adjacent cell has the same power of two, we merge."""
    MOVE_TO_EMPTY_ADJACENT = auto()
    """If current cell can move to the adjacent cell because that cell is empty."""


MAX_ITER = 100_000
"""Just a safety param to avoid infinite loops."""


class Board:
    """
    Represents the 2048 board and the actions
    that can be performed on it.


    Board is represented such as

    -------y axis--------->
    |
    |
    |
    x axis
    |
    v
    """

    _cfg: BoardConfig
    cells: Matrix
    """Cells stored such as cell[x][y]"""

    def __init__(
        self,
        cfg: BoardConfig | None = None,
        override_cells: Matrix | None = None,
    ):
        # Optional: Here we can do some validation on hte board config.
        self._cfg = cfg or BoardConfig()

        assert self._cfg.size.height > 1
        assert self._cfg.size.width > 1
        assert self._cfg.amount_new_per_tick > 0
        if override_cells:
            self.cells = override_cells
        else:
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
            return self._cfg.placeholder
        return str(2**x)

    def __str__(self) -> str:
        """Stringify the object.

        Returns:
           String for pretty print
        """
        return "\n".join(
            "\t".join(self._display_power(x) for x in row) for row in self.cells
        )

    def align_horizontally(
        self, how: Literal[Direction.LEFT] | Literal[Direction.RIGHT]
    ) -> None:
        for row_i in range(self._cfg.size.height):
            # if we align on the left, then spaces are on the right.
            non_zero = [x for x in self.cells[row_i] if x > PowerOfTwo(0)]
            delta_entries = self._cfg.size.width - len(non_zero)
            left_pad = [PowerOfTwo(0)] * delta_entries * (how == Direction.RIGHT)
            right_pad = [PowerOfTwo(0)] * delta_entries * (how == Direction.LEFT)
            new_col = left_pad + non_zero + right_pad
            self.cells[row_i] = new_col

    def align_vertically(
        self, how: Literal[Direction.UP] | Literal[Direction.DOWN]
    ) -> None:
        for col_i in range(self._cfg.size.width):
            non_zero: list[PowerOfTwo] = []
            # We fetch non zero values in column, then we pad.
            for row_i in range(self._cfg.size.height):
                # count
                if self[CellPosition(row_i, col_i)] > PowerOfTwo(0):
                    non_zero.append(self[CellPosition(row_i, col_i)])
            # we reset to 0 first
            delta_entries = self._cfg.size.height - len(non_zero)
            # If we align on top, then spaced are on the bottom.
            up_pad = [PowerOfTwo(0)] * delta_entries * (how == Direction.DOWN)
            down_pad = [PowerOfTwo(0)] * delta_entries * (how == Direction.UP)
            new_col = up_pad + non_zero + down_pad
            # Then we reaffect the column values.
            for row_i in range(self._cfg.size.height):
                self[CellPosition(row_i, col_i)] = new_col[row_i]

    def align(self, direction: Direction) -> Self:
        if direction in {Direction.UP, Direction.DOWN}:
            self.align_vertically(direction)
        else:
            self.align_horizontally(direction)
        return self

    def move(self, direction: Direction) -> Self:
        """Moves the whole board towards a specific direction.

        Args:
            direction: Direction of the board. Direction relative to screen, 
            not to the internal axis.
        Returns:
            Fluent setter. In place mutation.
        """

        # We iterate on columns as much as we can.
        # The order in which we iterate is important for
        # the game rules. But we can simplify that by just aligning twice.

        self.align(direction)

        for x in range(self._cfg.size.height):
            for y in range(self._cfg.size.width):
                pos = CellPosition(x, y)
                self.move_single_cell(pos, direction=direction)

        # we have to align twice to be sure that we do not end up with
        # remaining spaces after merge operations
        self.align(direction)
        return self

    def move_down(self) -> Self:
        return self.move(Direction.DOWN)

    def move_up(self) -> Self:
        return self.move(Direction.UP)

    def move_left(self) -> Self:
        return self.move(Direction.LEFT)

    def move_right(self) -> Self:
        return self.move(Direction.RIGHT)

    def move_single_cell(
        self, location: CellPosition, direction: Direction
    ) -> MoveStatus:
        """Moves a single cell to a specific direction.

        Args:
            location: Cell to move.
            direction: Direction to move.

        Returns:
           True if it created an empty space in the location, false otherwise.
        """
        mapper = {
            Direction.LEFT: CellPosition(0, -1),
            Direction.RIGHT: CellPosition(0, 1),
            Direction.UP: CellPosition(-1, 0),
            Direction.DOWN: CellPosition(1, 0),
        }
        delta = mapper[direction]

        adjacent_location = CellPosition(x=location.x + delta.x, y=location.y + delta.y)
        current_exist = self._cell_exists(location)
        target_exists = self._cell_exists(adjacent_location)
        if not (current_exist and target_exists):
            # If we cant move the cell or the cell to which we want to move doenst exist
            # then we can just pass.
            return MoveStatus.NO_OP

        elif self[location] <= PowerOfTwo(0):
            return MoveStatus.NO_OP

        elif self[location] == self[adjacent_location]:
            # Case where we can do a merge.
            self[adjacent_location] = PowerOfTwo(self[adjacent_location] + 1)
            self[location] = PowerOfTwo(0)
            return MoveStatus.MERGE

        elif self[adjacent_location] == PowerOfTwo(0):
            # Case of empty space
            self[adjacent_location] = self[location]
            self[location] = PowerOfTwo(0)
            return MoveStatus.MOVE_TO_EMPTY_ADJACENT

        return MoveStatus.NO_OP

    def __getitem__(self, location: CellPosition) -> PowerOfTwo:
        """Convenience method to get the value in the board.

        Args:
            location: x,y tuple.

        Returns:
            PowerOfTwo at the location.
        """
        return self.cells[location.x][location.y]

    def __setitem__(self, location: CellPosition, value: PowerOfTwo) -> None:
        """Convenience method to set a specific cell value.

        Args:
            location: x,y tuple.
            value: PowerOfTwo
        """

        self.cells[location.x][location.y] = value

    def _cell_exists(self, position: CellPosition) -> bool:
        """Checks if the cell exists or if its out of bound.

        Args:
            position: cell to check.

        Returns:
            True if it exists.
        """

        valid_x = position.x >= 0 and position.x < self._cfg.size.height
        valid_y = position.y >= 0 and position.y < self._cfg.size.width
        return valid_x and valid_y

    @property
    def state(self) -> GameState:
        """
        Indicates if the game is won, still playing, or lost.

        Returns:
            Current state of the game.
        """
        for row in self.cells:
            for col in row:
                if col >= self._cfg.win_condition:
                    return GameState.VICTORY
        # Then we check if there is any legal move left.
        any_legal_move_left = False
        for direction in Direction:
            board_copy = Board(
                cfg=self._cfg,
                override_cells=[[col for col in row] for row in self.cells],
            )
            board_copy.move(direction)
            if board_copy.cells != self.cells:
                any_legal_move_left = True
                break

        if not any_legal_move_left:
            return GameState.DEFEAT

        return GameState.PLAYING
