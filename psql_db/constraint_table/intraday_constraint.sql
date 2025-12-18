ALTER TABLE intraday_prices
ADD CONSTRAINT uniq_intraday_symbol_time
UNIQUE (symbol,open_time);