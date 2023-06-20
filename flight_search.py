import requests
import os
from dotenv import load_dotenv
from datetime import datetime
from flight_data import FlightData

load_dotenv()
tequila_endpoint = "https://api.tequila.kiwi.com/"
TEQUILA_API = os.getenv("TEQUILA_API")

today = datetime.now()
today = today.strftime("%d/%m/%Y")


tequila_search_params = {
    "apikey": f"{TEQUILA_API}",
    "fly_from": "LAX",
    "fly_to": "FRA",
    "date_from": f"{today}",
    "date_to": "30/06/2023"
}

class FlightSearch:

    def get_destination_code(self, city_name):
        print(f"This is the city name: {city_name}")
        location_endpoint = f"{tequila_endpoint}locations/query"
        headers = {"apikey": TEQUILA_API}
        query = {
            "term": city_name,
            "location_types": "city",
            "locale": "en-US"

        }
        response = requests.get(url=location_endpoint, params=query, headers=headers)

        results = response.json()
        code = results["locations"][0]["code"]
        return code

    def check_flights(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": TEQUILA_API}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 7,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(
            url=f"{tequila_endpoint}v2/search",
            headers=headers,
            params=query,
        )
        #print(f"This is the response of the search request: {response}")
        try:
            data = response.json()["data"][0]
            #print(f"This is the data from the search: {data}")
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: ${flight_data.price}")
        return flight_data