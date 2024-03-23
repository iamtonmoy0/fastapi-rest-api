from fastapi import Body, FastAPI, Query, Path
from pydantic import BaseModel, Field
from typing import List

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


@app.get("/item-hidden")
async def item_hidden_func(
    hidden_query: str | None = Query(None, include_in_schema=False),
):
    if hidden_query:
        return {"hidden query": hidden_query}
    return {"not found": "not found"}


# request body
"""
Request body param
"""


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float


@app.put("/item/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="item id of the item", ge=0, le=150),
    q: str | None = None,
    item: Item | None = None,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results


class User(BaseModel):
    name: str
    description: str | None = Field(
        None, title="the discription of the item", max_length=300
    )


@app.post("/user")
async def create_user(user: User = Body(..., embed=True)):
    return user


# body


class Image(BaseModel):
    url: str


class Items(BaseModel):
    name: str
    description: str
    tags: list[str] = []
    image: Image | None = None


@app.post("/item-create")
def create_items(items: Items):
    return items
