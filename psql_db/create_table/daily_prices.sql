CREATE TABLE IF NOT EXISTS daily_prices (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL,
    date DATE NOT NULL,
    open_price NUMERIC(18,8),
    high_price NUMERIC(18,8),
    low_price NUMERIC(18,8),
    close_price NUMERIC(18,8),
    volume NUMERIC(18,8),
    created_at TIMESTAMP DEFAULT now()
);