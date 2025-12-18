CREATE TABLE IF NOT EXIST intraday_prices (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    open_time TIMESTAMP NOT NULL,
    open_price NUMERIC(18,8) NOT NULL,
    high_price NUMERIC(18,8) NOT NULL,
    low_price NUMERIC(18,8) NOT NULL,
    close_price NUMERIC(18,8) NOT NULL,
    volume NUMERIC(18,8),
    created_at TIMESTAMP DEFAULT now()

);