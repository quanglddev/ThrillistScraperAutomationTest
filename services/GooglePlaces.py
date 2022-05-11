import os
from dataclasses import dataclass
from typing import Union

import googlemaps


@dataclass
class GooglePlaces:
    client: googlemaps.Client

    def __init__(self) -> None:
        self.client = googlemaps.Client(os.environ["GOOGLE_API_KEY"])

    def queryPlaceId(self, name: str) -> Union[str, None]:
        place = self.client.find_place(
            f"{name} {os.environ['MY_CITY']}",
            "textquery",
            fields=["place_id"],
            location_bias="point:90,90",
            language="en-US",
        )

        return (
            place["candidates"][0]["place_id"] if len(place["candidates"]) > 0 else None
        )

    def queryOpenHours(self, placeId: str) -> str:
        hours = self.client.place(
            placeId,
            fields=["opening_hours"],
            language="en-US",
        )
        if "opening_hours" not in hours["result"]:
            return ""

        saturday = hours["result"]["opening_hours"]["weekday_text"][5]

        openText = " ".join(saturday.split(" ")[1:])
        return openText

    def queryETAAndMode(self, startId, endId) -> str:
        walking = self.client.directions(
            f"place_id:{startId}",
            f"place_id:{endId}",
            mode="walking",
            units="metric",
            region="us",
        )
        walkingInfo = walking[0]["legs"][0]["duration"]
        transit = self.client.directions(
            f"place_id:{startId}",
            f"place_id:{endId}",
            mode="transit",
            units="metric",
            region="us",
        )
        transitInfo = transit[0]["legs"][0]["duration"]
        shouldWalk = walkingInfo["value"] < transitInfo["value"]

        if shouldWalk:
            return f"🚶‍♂️ {walkingInfo['text']}"
        else:
            return f"🚌 {transitInfo['text']}"
