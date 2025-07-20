CREATE TABLE crypto_data (
  trade_datetime     TIMESTAMPTZ       ,    -- precise trade timestamp with timezone
  open               numeric(12,6)     ,    -- opening price, high precision float
  close              numeric(12,6) 	   ,    -- closing price
  volume             BIGINT            ,    -- total volume (integer)
  close_datetime     TIMESTAMPTZ       ,    -- timestamp when closed
  number_of_trades   INTEGER           ,    -- count of trades
  symbol             VARCHAR(50)       ,    -- trading symbol, e.g. 'BTCUSD'
  pct_change         numeric(12,6)     ,	-- percentage change (float)
  volatility         numeric(12,6)     ,    -- price volatility (float)
  moving_average     numeric(12,6)     ,        -- moving average price (higher precision)
  PRIMARY KEY (trade_datetime, symbol)
  );

-- select * from crypto_data order by trade_datetime  desc;

-- drop table crypto_data;

-- truncate crypto_data;
