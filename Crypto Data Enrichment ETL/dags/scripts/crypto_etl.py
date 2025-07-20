
import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from decimal import *

def main():

  #https://data-api.binance.vision/api/v3/ticker/price?symbol=DOGEUSDT

  # Define the base URL for Binance API
  base_url = "https://api.binance.com/api/v3/ticker/price"

  # Define the trading pairs
  symbols = ["ETHUSDT", "DOGEUSDT", "BTCUSDT"]
  interval = '1d'

  # Calculate the start and end timestamps for the last 30 days
  end_time = datetime.now() - timedelta(days=1)
  start_time = end_time - timedelta(days=31)

  # Convert to milliseconds
  start_timestamp = int(start_time.timestamp() * 1000)
  end_timestamp = int(end_time.timestamp() * 1000)
  
  #creating main dataframe
  df=pd.DataFrame()
  result= write_to_db( symbols, interval, start_timestamp, end_timestamp, df)
  return result

def fetch_klines(symbol, interval, start_timestamp, end_timestamp):
  url = 'https://api.binance.com/api/v3/klines'
  params = {
      'symbol': symbol,
      'interval': interval,
      'startTime': start_timestamp,
      'endTime': end_timestamp,
      'limit': 1000  # Max limit per request
  }
  response = requests.get(url, params=params)
  response.raise_for_status()
  return response.json()

# Fetch and process data for each symbol
def data_processing( symbols, interval, start_timestamp, end_timestamp, df):
  
  for symbol in symbols:
      data = fetch_klines(symbol, interval, start_timestamp, end_timestamp)
      #print(type(data))
      new_df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
      new_df['symbol'] = symbol

      # castig columns to numeric datatype
      new_df[['open', 'high', 'low', 'close', 'volume','quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']] = new_df[['open', 'high', 'low', 'close', 'volume','quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume']].apply(pd.to_numeric)
      #print(new_df.dtypes)

      # Fill missing values with the mean of each column
      new_df['close'] = new_df['close'].fillna(new_df['close'].mean())
      new_df['open'] = new_df['open'].fillna(new_df['open'].mean())
      new_df['high'] = new_df['high'].fillna(new_df['high'].mean())

      # removing duplicates from dataframes evaluated on the basis of all column values
      new_df = new_df.drop_duplicates()
      
      #handling timestamps
      new_df['trade_datetime'] = pd.to_datetime(new_df['timestamp'], unit='ms')
      new_df['trade_datetime_index'] = pd.to_datetime(new_df['timestamp'], unit='ms')
      new_df['close_datetime'] = pd.to_datetime(new_df['close_time'], unit='ms')
      
      #setting index
      new_df.set_index('trade_datetime_index', inplace=True)
      
      # Check if the 'timestamp' column is timezone-aware
      if new_df['trade_datetime'].dt.tz is not None:
          print(" The 'Timestamp' column is timezone-aware.")
      else:
          # print("The 'timestamp' column is naive.")
          new_df['trade_datetime'] = new_df['trade_datetime'].dt.tz_localize('UTC')
      
      # Check if the 'closing_time' column is timezone-aware
      if new_df['close_datetime'].dt.tz is not None:
          print("The 'close_time' column is timezone-aware.")
      else:
          new_df['close_datetime'] = new_df['close_datetime'].dt.tz_localize('UTC')
      
      #adding metrics
      new_df['pct_change'] = new_df.groupby('symbol')['close'].pct_change() * 100 
      
      new_df['volatility'] = new_df.groupby('symbol')['pct_change'].rolling(window=30, min_periods=1).std().reset_index(level=0, drop=True)
      #expanding(min_periods=2).std()
      new_df['moving_average']= new_df.groupby('symbol')['close'].rolling(window=30, min_periods=1).mean().reset_index(level=0, drop=True)

      #trimming unnecessary fields
      new_df= new_df[['trade_datetime', 'open', 'close', 'volume', 'close_datetime', 'number_of_trades', 'symbol', 'pct_change', 'volatility', 'moving_average']]

      # Define the desired precision and scale
      precision = 12
      scale = 6
      quantize_value = Decimal(10) ** -scale

      # Convert columns to Decimal with specified precision and scale
      for col in new_df[['open','close','volume','pct_change','volatility','moving_average']].columns:
          new_df[col] = new_df[col].apply(lambda x: Decimal(str(x)).quantize(quantize_value, rounding=ROUND_HALF_UP))
      
      # concatenating dataframe of each currency into main dataframe
      df= pd.concat([new_df,df], axis=0, ignore_index=True)
  #print(df.dtypes)
  return df

#print(df)
#writing dataframe into csv file
# filename='cryptodata30d.csv'
# df.to_csv(filename,index=False)

def write_to_db(symbols, interval, start_timestamp, end_timestamp, df):
    
  #writing data into postgresdb
  table_name = "crypto_data"
  DB_URI= "postgresql+psycopg2://crypto_user:crypto_123@testing-crypto_server-1:5432/crypto_data"

  try:
      df= data_processing( symbols, interval, start_timestamp, end_timestamp, df)
      #print(df.dtypes)
      #conn_string = 'postgresql://postgres:postgres@localhost:5432/postgres'
      engine1 = create_engine(DB_URI)
      with Session(engine1) as session:
          # session.execute(text(f'TRUNCATE TABLE {table_name} IF EXISTS RESTART IDENTITY CASCADE'))
          session.execute(text(f'TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE'))
          session.commit()

      df.to_sql('crypto_data', engine1, if_exists='append', index=False, method='multi', chunksize=1000)
      return "Task completed successfuly"
    
  except Exception as e:
      er={"error": str(e)}
      print(er["error"])
      return er["error"]
    
rs=main()
print(rs)
