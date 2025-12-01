import os
from datetime import datetime
from functools import wraps
from typing import TypedDict

from pymongo import MongoClient
from pymongo.server_api import ServerApi

MONGODB_URI = os.getenv("MONGODB_URI")


def init_client():
    return MongoClient(
        MONGODB_URI,
        server_api=ServerApi(version="1", strict=True, deprecation_errors=True),
    )


def test_connection():
    client = init_client()
    try:
        # Send a ping to confirm a successful connection
        client.admin.command({"ping": 1})
        print("Pinged your deployment. You successfully connected to MongoDB!")
    finally:
        client.close()


def create_record(year, day, part, result_time, timestamp, comment, person, code):
    client = init_client()
    try:
        collection = client.aoc.records
        record = Record(
            year=year,
            day=day,
            part=part,
            result_time=result_time,
            timestamp=timestamp,
            person=person,
            code=code,
            comment=comment,
        )

        with collection.find(
            {"year": year, "day": day, "part": part, "code": code}
        ) as cursor:
            for doc in cursor:
                return doc["_id"]

        inserted = collection.insert_one(record)
        return inserted.inserted_id
    finally:
        client.close()


class Record(TypedDict):
    year: int
    day: int
    part: int
    result_time: float
    timestamp: datetime
    person: str
    comment: str
    code: str