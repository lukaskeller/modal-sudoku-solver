import os
import requests
import json
import time

from dotenv import load_dotenv

load_dotenv()

# TOKEN_SECRET
# TOKEN_ID
# https://lukaskeller--sudoku-solver-solve-dev.modal.run/
# post request with json body: {"puzzle": "1.4.28...3.815...7265.7.4.17438..15...2.4.73...97.162..3.......8.1..6....263.7.4.", "level": "easy"}


request_response =     {
      "puzzle": ".2...6.9....2..3...5...9..1..39......9.7..4...48....3.4.....6..2..47.983.....3..7",
      "solution": "721356894984217356356849271673984125192735468548162739437598612265471983819623547"
    }
# make post with headers and correclty formatted json body
# curl -H "Modal-Key: $TOKEN_ID" -H "Modal-Secret: $TOKEN_SECRET" -H "Content-Type: application/json"
# import TOKEN_ID from .env file
# import TOKEN_SECRET from .env file

url = 'https://lukaskeller--sudoku-solver-solve-dev.modal.run/'


data = {'puzzle': '..2.......9857....5....6.4....2.1..5...63.....3..4...9....5...76....435...1....2.', 'level': 'easy'}
headers = {'Content-type': 'application/json', 'Modal-Key': os.environ['TOKEN_ID'], 'Modal-Secret': os.environ['TOKEN_SECRET']}

tick = time.time()
r = requests.post(url, data=json.dumps(data), headers=headers)
print(f"Time taken: {time.time() - tick:.2f} seconds")

assert r.status_code == 200

sudoku_solution = r.json()
print("Puzzle:   " + request_response['puzzle'])
print("Expected: " + request_response['solution'])
print("Produced: " + sudoku_solution['solution'] )

assert sudoku_solution['solution'] == request_response['solution']