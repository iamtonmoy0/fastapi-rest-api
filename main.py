from fastapi import FastAPI, Query
from pydantic import BaseModel

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


# create product with type  validation


class Product(BaseModel):
    name: str
    description: str
    price: float
    tax: float


@app.post("/product")
async def create_product(product: Product):
    product_dict = product.dict()
    if product.tax:
        price_with_tax = product.price + product.tax
        product_dict.update({"price with tax": price_with_tax})
    return product_dict


# query parameter with string validation
# regex validation
@app.get("/read-product")
async def read_product(
    q: list[str] | None = Query(None, min_length=3, max_length=10, regex="^okayok$"),
):
    results = {"product": [{"hello": "world"}]}
    if q:
        results.update({"q": q})
    return results
