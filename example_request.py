import os
import requests
import json
import time

from dotenv import load_dotenv

load_dotenv()  # load modal secrets from .env to env


request_response = {
    "puzzle": ".2...6.9....2..3...5...9..1..39......9.7..4...48....3.4.....6..2..47.983.....3..7",
    "solution": "721356894984217356356849271673984125192735468548162739437598612265471983819623547",
}

url = "https://lukaskeller--sudoku-solver-solve-dev.modal.run/"

payload = {
    "puzzle": request_response["puzzle"],
    "level": "easy",
}
headers = {
    "Content-type": "application/json",
    "Modal-Key": os.environ["TOKEN_ID"],
    "Modal-Secret": os.environ["TOKEN_SECRET"],
}

# timed submit
tick = time.time()
r = requests.post(url, data=json.dumps(payload), headers=headers)
print(f"Time taken: {time.time() - tick:.2f} seconds")  # around 1s

# check solution
assert r.status_code == 200, f"Failed to submit puzzle: {r.status_code, r.text}"
sudoku_solution = r.json()
assert sudoku_solution["solution"] == request_response["solution"]
print("Submitted Puzzle:" + request_response["puzzle"])
print("Expected Result: " + request_response["solution"])
print("Returned Result: " + sudoku_solution["solution"])
