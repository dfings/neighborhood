from typing import List

from fastapi import FastAPI

from neighborhood import Result, find

app = FastAPI()

@app.get("/")
def find_action(address: str = "") -> List[Result]:
    return find(address)
