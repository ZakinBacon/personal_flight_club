#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
from pprint import pprint
from data_manager import DataManager
from flight_search import FlightSearch

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
flight_search = FlightSearch()
ORIGIN_CITY_IATA = "SAN"
load_dotenv()

TEQUILA_API = os.getenv("TEQUILA_API")
BEAR = os.getenv("BEAR")
SHEETLY_ENDPOINT = os.getenv("SHEETLY_ENDPOINT")

tequila_endpoint = "https://api.tequila.kiwi.com/"

today = datetime.now()
today = today.strftime("%d/%m/%Y")


sheetly_header = {
    "Authorization": BEAR
}

response = requests.get(url=SHEETLY_ENDPOINT, headers=sheetly_header)
response.raise_for_status()
sheet_data = response.json()

iataCode_test = {
  "price": {
    "iataCode": "TESTING",
  }
}


if sheet_data["prices"][0]["iataCode"] == "":
    from flight_search import FlightSearch
    flight_search = FlightSearch()
    for row in sheet_data["prices"]:
        row["iataCode"] = flight_search.get_destination_code(row["city"])
    #print(f"sheet_data:\n {sheet_data}")

    data_manager.destination_data = sheet_data
    data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
six_month_from_today = datetime.now() + timedelta(days=(6 * 30))
#print(sheet_data)
for index, destination in enumerate(sheet_data["prices"]):
    #print(f"sheet data destination: {destination}")
    flight = flight_search.check_flights(
        ORIGIN_CITY_IATA,
        destination["iataCode"],
        from_time=tomorrow,
        to_time=six_month_from_today
    )

if flight.price < destination["lowestPrice"]:
        print(f"Low price alert! Only ${flight.price} to fly from {flight.origin_city}-{flight.origin_airport} to {flight.destination_city}-{flight.destination_airport}, from {flight.out_date} to {flight.return_date}")
