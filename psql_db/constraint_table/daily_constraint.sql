ALTER TABLE daily_prices
ADD CONSTRAINT  uniq_daily_symbol_date
UNIQUE (symbol, date) ;