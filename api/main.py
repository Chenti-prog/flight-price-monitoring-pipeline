from __future__ import annotations

from datetime import date
from typing import Optional
from fastapi import FastAPI, Query
import random

app = FastAPI(title="Flight Prices API (Local)", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/flight-prices")
def flight_prices(
    origin: str = Query(..., min_length=3, max_length=3, description="IATA code like ORD"),
    destination: str = Query(..., min_length=3, max_length=3, description="IATA code like JFK"),
    departure_date: date = Query(..., description="YYYY-MM-DD"),
    max_results: int = Query(5, ge=1, le=50),
    currency: str = Query("USD", min_length=3, max_length=3),
    airline: Optional[str] = Query(None, description="Optional airline code like AA"),
):
    """
    Returns mock flight offers in a consistent structure.
    This mimics what a real provider would return, so your ingestion pipeline is real.
    """
    airlines = ["AA", "DL", "UA", "WN", "B6"]
    if airline:
        airlines = [airline.upper()]

    offers = []
    for i in range(max_results):
        carrier = random.choice(airlines)
        price = round(random.uniform(120, 650), 2)

        offers.append(
            {
                "origin": origin.upper(),
                "destination": destination.upper(),
                "departure_date": str(departure_date),
                "airline": carrier,
                "price": price,
                "currency": currency.upper(),
                "provider": "local-api",
                "offer_id": f"{origin.upper()}-{destination.upper()}-{departure_date}-{carrier}-{i}",
            }
        )

    return {"data": offers}
