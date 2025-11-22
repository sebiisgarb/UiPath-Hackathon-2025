import httpx
import time
from typing import Optional

AMADEUS_AUTH_URL = "https://test.api.amadeus.com/v1/security/oauth2/token"
AMADEUS_FLIGHTS_URL = "https://test.api.amadeus.com/v2/shopping/flight-offers"
AMADEUS_ACTIVITIES_URL = "https://test.api.amadeus.com/v1/shopping/activities"

# Token expiry buffer in seconds (use slightly less than actual expiry for safety)
TOKEN_EXPIRY_BUFFER = 1700


class AmadeusClient:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.token_expiry = 0

    async def get_access_token(self):
        if self.token and self.token_expiry > time.time():
            return self.token

        async with httpx.AsyncClient() as client:
            response = await client.post(
                AMADEUS_AUTH_URL,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data={
                    "grant_type": "client_credentials",
                    "client_id": self.client_id,
                    "client_secret": self.client_secret
                }
            )
            response.raise_for_status()
            data = response.json()

        self.token = data["access_token"]
        self.token_expiry = time.time() + TOKEN_EXPIRY_BUFFER
        return self.token

    async def get_activities(
        self,
        latitude: float,
        longitude: float,
        radius: int = 3,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        limit: Optional[int] = None,
        sort_by_rating: bool = False
    ):
        """
        Get activities with:
        - price filtering
        - sort by rating (descending)
        - limit number of returned activities
        - keep max 3 pictures
        """
        token = await self.get_access_token()

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius,
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(
                AMADEUS_ACTIVITIES_URL,
                params=params,
                headers={"Authorization": f"Bearer {token}"}
            )
            response.raise_for_status()
            data = response.json()

        activities = data.get("data", [])

        # -------------------------------
        # PRICE FILTERING
        # -------------------------------
        if min_price is not None:
            activities = [
                a for a in activities
                if a.get("price") and 
                   a["price"].get("amount") and
                   float(a["price"]["amount"]) >= min_price
            ]

        if max_price is not None:
            activities = [
                a for a in activities
                if a.get("price") and 
                   a["price"].get("amount") and
                   float(a["price"]["amount"]) <= max_price
            ]

        # -------------------------------
        # SORT BY RATING DESC
        # -------------------------------
        if sort_by_rating:
            activities = sorted(
                activities,
                key=lambda a: a.get("rating", 0),
                reverse=True
            )

        # -------------------------------
        # LIMIT NUMBER OF RESULTS
        # -------------------------------
        if limit is not None:
            activities = activities[:limit]

        # -------------------------------
        # KEEP ONLY 3 PICTURES
        # -------------------------------
        for a in activities:
            pics = a.get("pictures", [])
            a["pictures"] = pics[:3]

        return {"data": activities}
