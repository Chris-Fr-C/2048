"""
This game definitely doesnt need an LLM.
If we want to put help we could just create a score for the current
board situation, and then estimate the gradient based on the 4 moves we can do.
That's a bit similar to what we could do in chess.
But for the exercice, we will do an AI with an LLM.
"""

from typing import Literal, Protocol
import demo.board as board
import instructor
from pydantic import BaseModel


class AIHelper(Protocol):
    # Always separate interface from implementation.
    def help(self, state: board.Board) -> board.Direction: ...


type Direction= Literal["up"] | Literal["down"] | Literal["left"] | Literal["right"]
class Suggestion(BaseModel):
    next_move: Direction 

    


class LLMImplementation(AIHelper):

    def __init__(self, model: str = "devstral-small-2"):
        self.client = instructor.from_provider(f"ollama/{model}")

    def help(self, state: board.Board) -> board.Direction:
        suggestion = self.client.chat.completions.create(
            response_model=Suggestion,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI assistant that only outputs raw JSON. "
                        "Do not include any introduction, explanations, or markdown code fences. "
                        "Your response must match this schema strictly."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "I want you to tell me the next best move to win this 2048 game. "
                            "You can only answer with as single word: left, right, up, or down. The current board is the following: \n"
                        +
                        str(state)
                    ),
                }
            ],
        )


        return board.Direction(suggestion.next_move.strip().lower())


if __name__=="__main__":
    brd = board.Board()
    ai = LLMImplementation()
    res = ai.help(brd)
    print("=>",res)
