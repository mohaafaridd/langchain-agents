from sqlalchemy import (
    MetaData,
    Column,
    Integer,
    String,
    Table,
    Date,
    Float,
    create_engine,
    insert,
)
from datetime import datetime

metadata_obj = MetaData()

stocks = Table(
    "stocks",
    metadata_obj,
    Column("obs_id", Integer, primary_key=True),
    Column("stock_ticker", String(4), nullable=False),
    Column("price", Float, nullable=False),
    Column("date", Date, nullable=False),
)

engine = create_engine("sqlite:///:memory:")
metadata_obj.create_all(engine)

observations = [
    [1, "ABC", 200, datetime(2023, 1, 1)],
    [2, "ABC", 208, datetime(2023, 1, 2)],
    [3, "ABC", 232, datetime(2023, 1, 3)],
    [4, "ABC", 225, datetime(2023, 1, 4)],
    [5, "ABC", 226, datetime(2023, 1, 5)],
    [6, "XYZ", 810, datetime(2023, 1, 1)],
    [7, "XYZ", 803, datetime(2023, 1, 2)],
    [8, "XYZ", 798, datetime(2023, 1, 3)],
    [9, "XYZ", 795, datetime(2023, 1, 4)],
    [10, "XYZ", 791, datetime(2023, 1, 5)],
]


def insert_obs(obs):
    stmt = insert(stocks).values(
        obs_id=obs[0], stock_ticker=obs[1], price=obs[2], date=obs[3]
    )

    with engine.begin() as conn:
        conn.execute(stmt)


for obs in observations:
    insert_obs(obs)
