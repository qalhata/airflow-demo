CREATE TABLE IF NOT EXISTS exchange_rates (
    id SERIAL PRIMARY KEY,
    currency TEXT,
    rate FLOAT,
    timestamp TIMESTAMP
);
