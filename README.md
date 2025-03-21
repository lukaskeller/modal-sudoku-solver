Invoke `uv run python -m pytest` to run tests

todo:
- how to run fastapi server locally?
- how to docs for local invocation? url deterministic? secret?
- example sudoku in docs. conversion instructions

Run on modal: `make serve`
(returns https://lukaskeller--sudoku-solver-solve-dev.modal.run/ as url)

then invoke example script to post puzzle and check solution with:
`uv run example_request.py`
cold start should be around 3s, then 1s per invocation
