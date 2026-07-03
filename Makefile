default:
	uv run -m demo 

tests:
	uv run -m pytest

play:
	uv run -m demo

setup:
	ollama pull devstral-small-2
	ollama serve
