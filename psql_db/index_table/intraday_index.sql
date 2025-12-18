CREATE INDEX idx_intraday_symbol_time
ON intraday_prices (symbol, open_time);