from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# get items
@app.get("/items")
async def get_items():
    return {"item": "this is items"}

# get item by id
@app.get("/items/{id}")
async def get_item(id):
    return {"item": id}
