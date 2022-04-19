from typing import List, Optional

from fastapi import FastAPI, Query
from pydantic import BaseModel

from pymongo import MongoClient
from .settings import MONGO_URI, MONGO_COLLECTION


def get_collection():
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    return db[MONGO_COLLECTION]


class TargetKG(BaseModel):
    min: Optional[float] = None
    max: Optional[float] = None

class Diaper(BaseModel):
    description: str
    price: float
    url: Optional[str] = None
    image: Optional[str] = None
    website: Optional[str] = None
    brand: Optional[str] = None # enum
    size: Optional[str] = None # enum
    target_kg: Optional[TargetKG] = None
    units: Optional[int] = None
    unit_price: Optional[float] = None


def range_query(query, key, lte=None, gte=None):
    range = {}
    if lte:
        range.update({"$lte": lte})
    if gte:
        range.update({"$gte": gte})
    if range:
        query.update({key: range})
    return query

def in_query(query, key, _in=None):
    if _in:
        query.update({key: { "$in": _in.split(",") }})
    return query

def or_range_query(query, key_min, key_max, value=None):
    if value:
        query.update({ "$or": [{key_min: {"$gte": value}}, {key_max: {"$lte": value}}]})
    return query

def query_diapers(
        collection,
        price_lte,
        price_gte,
        brands,
        sizes,
        target_kg,
        unit_price_lte,
        unit_price_gte,
        page,
        page_limit,
    ):
    query = {}
    query = range_query(query, "price", price_lte, price_gte)
    query = range_query(query, "unit_price", unit_price_lte, unit_price_gte)
    query = in_query(query, "brand", brands)
    query = in_query(query, "size", sizes)
    query = or_range_query(query, "target_kg.min", "target_kg.max", target_kg)
    result = collection.find(query).sort('_id', -1).skip(page_limit * (page - 1)).limit(page_limit)
    if not result:
        return None
    for res in result:
        yield Diaper(**res)


# FastAPI specific code
app = FastAPI()

@app.get("/query-diapers", response_model=List[Diaper])
def get_diapers(
        price_lte: Optional[float] = Query(None),
        price_gte: Optional[float] = Query(None),
        brands: Optional[str] = Query(None),
        sizes: Optional[str] = Query(None),
        target_kg: Optional[float] = Query(None),
        unit_price_lte: Optional[float] = Query(None),
        unit_price_gte: Optional[float] = Query(None),
        page: Optional[float] = Query(1),
        page_limit: Optional[float] = Query(20)
    ):
    collection = get_collection()
    diapers = query_diapers(collection, price_lte, price_gte, brands, sizes, target_kg, unit_price_lte, unit_price_gte, page, page_limit)
    return diapers
