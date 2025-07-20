from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from pydantic import BaseModel, ConfigDict
from typing import List
import pandas as pd
from datetime import *

table_name = "crypto_data"
#observe and update as per environment
DB_URL= "postgresql+psycopg2://crypto_user:crypto_123@crypto_server:5432/crypto_data"
engine = create_engine(DB_URL)
#SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

crypto_app = FastAPI()

class price_request(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    coin: str
    start_date: date
    end_date: date

@crypto_app.get("/")
def read_root():
    return "Message: Welcome to your Crypto Serving"

#@crypto_app.get("/prices?coin={coin}&start_date={start_date}&end_date={end_date}")
@crypto_app.get("/prices")
def read_prices(coin:str, start_date:str, end_date:str):
    with Session(engine) as session:
        result=session.execute(
        text(
                "SELECT trade_datetime, close, symbol FROM crypto_data "
                "WHERE symbol = :coin AND trade_datetime BETWEEN :start_date AND :end_date"
            ),
        {"coin": coin, "start_date": start_date, "end_date": end_date}
        )
        rows = result.fetchall()
        return [
            {
                "trade_datetime": r[0],
                "close": r[1],
                "symbol": r[2]
            } for r in rows
        ]
        
@crypto_app.get("/metrics/volatility")
def read_prices(coin:str, period:str):
    period1=int(period[:-1])
    with Session(engine) as session:
        result=session.execute(
        text(
                "SELECT trade_datetime, symbol, volatility FROM crypto_data "
                "WHERE symbol = :coin AND trade_datetime BETWEEN (current_date - :period1) AND (current_date-1)"
            ),
        {"coin": coin, "period1": period1}
        )
        rows = result.fetchall()
        return [
            {
                "trade_datetime": r[0],
                "symbol": r[1],
                "volatility": r[2]
            } for r in rows
        ]
        