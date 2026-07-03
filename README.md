# Usage

Make sure you installed `uv` from the [official website](https://docs.astral.sh/uv/getting-started/installation/).
Make should also be available on any UNIX system.

Some commands are available such as make, make tests, make setup.
You also need [ollama](https://ollama.com/) for the AI features.

This project was tested on linux only.


# General remark
* 2048 is not a valid name for a python package, and the lack of inspiration made me use "demo" instead.
* Could have gone for numpy array but it adds a dependency for a small project.
* I could directly write powers of two, but that's a bit of a waste since we actually
dont use that information for anything else than display, and I might or might not allow players
to play with their faces/images instead of numbers. Additionally what if we want to be able to go much higher ?
Like 30 iterations ?
* We could store None|Null instead of PowerOfTwo(0) since 2**0 == 1
  But it's easy to work with non null values when not needed.
* Could have gone full OOP and representing cells as objects, but
I found the matrix approach a little bit more straightforward.
* Devops wise I wont put a precommit not docker img nor anything overkill for this project.

* I played 2048 and my understanding of the game is that if we have such a state
```
2 . .
2 . .
2 . .
2 . .
```
and we do a "move down" action, then we would get:
```
. . .
. . .
4 . .
4 . .
```
and not:
```
. . .
2 . .
2 . .
4 . .
```



## How I decide if the game is over
If the  user cannot make any legal move, it's considered as over.

A legal move is considered as a move that would change the state of the board.

## Why using a TUI instead of a web ui

It's not common so I wanted to do it.
Note that not much effort was put into the ui since it uses a framework (textual) and some of the decisions are related to its limitation.


## why that strategy for the LLM ai mode

Using a structured output is quite convenient to get the next instruction.

However I think that a normal "AI" that would not use an LLM would be more efficient, but this is just to try it out.


## Improvements

The UI is still not super ergonomic, in particular for the AI suggestion. I could add a timebar, a better popup etc ...
