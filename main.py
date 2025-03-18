import modal


from fastapi_models import Sudoku

#image = modal.Image.debian_slim().pip_install("fastapi[standard]")
image = modal.Image.debian_slim().pip_install_from_pyproject("pyproject.toml")

app = modal.App(image=image)

@app.function()
@modal.fastapi_endpoint(requires_proxy_auth=True, method="POST")
def f(s: Sudoku) -> str:
                      
   return f"Hello, {s.level}: {s.grid}!"
# 
# gen curl request for the endpoint
# with out null
# curl -H "Modal-Key: $TOKEN_ID" -H "Modal-Secret: $TOKEN_SECRET" -H "Content-Type: application/json" -X POST https://lukaskeller--main-py-f-dev.modal.run/ -d '{"grid": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "level": "easy"}' 
# with null (nulls symbolize empty cells)
# curl -H "Modal-Key: $TOKEN_ID" -H "Modal-Secret: $TOKEN_SECRET" -H "Content-Type: application/json" -X POST https://lukaskeller--main-py-f-dev.modal.run/ -d '{"grid": [[1, 2, 3], [4, 5, 6], [7, 8, null]], "level": "easy"}' 
