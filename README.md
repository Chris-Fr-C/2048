

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

