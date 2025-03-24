# Sudoku Solver
Simple Sudoku solver on Modal, using mixed-integer programming, exposed as a RESTful service. Accepts a Sudoku puzzle and returns the solved puzzle.

Solves sudoku puzzles in this format (rows first, empty cells as `.`):
```
# in 
.2...6.9....2..3...5...9..1..39......9.7..4...48....3.4.....6..2..47.983.....3..7
# out
721356894984217356356849271673984125192735468548162739437598612265471983819623547
```


## Requirements
You need the `glpk` MILP solver and `uv` for all python requirements
```bash
# linux:
# sudo apt-get install glpk-utils
# mac:
brew install glpk
curl -LsSf https://astral.sh/uv/install.sh | sh
git clone git@github.com:lukaskeller/modal-sudoku-solver.git
cd modal-sudoku-solver && uv sync
``` 

## Modal credentials
You need 2 credentials:
- `uv run modal setup` will bootstrap your account and config
- To secure your web endpoint, you need to [generate proxy credentials](https://modal.com/settings/proxy-auth-tokens) in the Modal UI and place them in a `.env` file
 ```env
 TOKEN_ID=your_token_id
 TOKEN_SECRET=your_token_secret
 ```

## Deploy
`make serve` for live deployment (hot reload, blocks shell) or `make deploy` for background deployment

Make a request:
```sh
uv run example_request.py
```
or build your own with curl (don't forget the `TOKEN_ID` and `TOKEN_SECRET` in the header)
```sh
curl -X POST 
   -H "Content-Type: application/json" \
   -H "Modal-Key: $TOKEN_ID" \
   -H "Modal-Secret: $TOKEN_SECRET" \
   -d '{"puzzle": ".2...6.9....2..3...5...9..1..39......9.7..4...48....3.4.....6..2..47.983.....3..7"}' \
   <your_url>
```

## Tests
`make test` to run the tests


## To do

- how to run fastapi server locally?
- how to docs for local invocation? url deterministic? secret?
- example sudoku in docs. conversion instructions
- test case for bad formatting for request puzzle
- bad sudoku puzzle test case (unsolvable)
- ambiguous sudoku puzzle test case (multiple solutions)
- test case for empty puzzle
- 

cold start should be around 3s, then 1s per invocation
