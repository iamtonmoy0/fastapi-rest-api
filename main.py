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


fake_db = [
    {"item": "apple"},
    {"item": "banana"},
    {"item": "cherry"},
    {"item": "date"},
    {"item": "elderberry"},
]


# pagination and filtering
@app.get("/products")
async def get_product(skip: int = 0, limit: int = 0):
    return fake_db[skip : skip + limit]


# filtering with query added


@app.get("/product/{id}")
async def get_product_by_filter(id: str, query: str = None, short: bool = False):
    product = {"product": "hello world"}
    if query:
        product.update({"query": query})
    if not short:
        product.update(
            {
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
            }
        )
    return product
