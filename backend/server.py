from fastapi import FastAPI
from main import main
import type_classes

app = FastAPI()


@app.post("/")
async def root(inputArgs: type_classes.InputArgs):
    return main(inputArgs)
