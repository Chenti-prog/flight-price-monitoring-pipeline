CREATE TABLE IF NOT EXISTS flight_prices (
    id SERIAL PRIMARY KEY,
    origin VARCHAR(10),
    destination VARCHAR(10),
    departure_date DATE,
    airline VARCHAR(50),
    price_usd NUMERIC(10,2),
    currency VARCHAR(5),
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
