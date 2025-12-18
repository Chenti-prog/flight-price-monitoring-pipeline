from __future__ import annotations

import os
import requests
import psycopg2
from psycopg2.extras import execute_values

from utils.config import get_pg_config


BASE_URL = os.getenv("API_BASE_URL", "http://api:8000")


def fetch_offers(origin: str, destination: str, departure_date: str, max_results: int = 5) -> dict:
    url = f"{BASE_URL}/flight-prices"
    params = {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "max_results": max_results,
    }
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def parse_offers(payload: dict) -> list[dict]:
    rows = []
    for offer in payload.get("data", []):
        rows.append(
            {
                "origin": offer["origin"],
                "destination": offer["destination"],
                "departure_date": offer["departure_date"],
                "airline": offer["airline"],
                "price_usd": float(offer["price"]),
                "currency": offer["currency"],
            }
        )
    return rows


def insert_prices(rows: list[dict]) -> int:
    if not rows:
        return 0

    cfg = get_pg_config()
    conn = psycopg2.connect(**cfg)
    conn.autocommit = False

    try:
        with conn.cursor() as cur:
            values = [
                (r["origin"], r["destination"], r["departure_date"], r["airline"], r["price_usd"], r["currency"])
                for r in rows
            ]
            sql = """
                INSERT INTO flight_prices
                (origin, destination, departure_date, airline, price_usd, currency)
                VALUES %s
            """
            execute_values(cur, sql, values)

        conn.commit()
        return len(rows)
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def main():
    origin = "ORD"
    destination = "JFK"
    departure_date = "2026-01-20"

    payload = fetch_offers(origin, destination, departure_date, max_results=5)
    rows = parse_offers(payload)
    inserted = insert_prices(rows)

    print(f"[OK] Inserted {inserted} offers from local API for {origin}->{destination} on {departure_date}")


if __name__ == "__main__":
    main()
