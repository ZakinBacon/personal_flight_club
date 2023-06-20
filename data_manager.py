import requests
import os
from dotenv import load_dotenv

load_dotenv()
SHEETLY_ENDPOINT = os.getenv("SHEETLY_ENDPOINT")
BEAR = os.getenv("BEAR")

sheetly_header = {
    "Authorization": BEAR
}

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_destination_data(self):
        # 2. Use the Sheety API to GET all the data in that sheet and print it out.
        response = requests.get(url=SHEETLY_ENDPOINT, headers=sheetly_header)
        data = response.json()
        #print(data)
        self.destination_data = data["prices"]
        #print(f"This is destination data: {self.destination_data}")
        # 3. Try importing pretty print and printing the data out again using pprint() to see it formatted.
        # pprint(data)
        return self.destination_data

    # 6. In the DataManager Class make a PUT request and use the row id from sheet_data
    # to update the Google Sheet with the IATA codes. (Do this using code).
    def update_destination_codes(self):
        for city in self.destination_data["prices"]:
            print(f"This is City{city}")
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETLY_ENDPOINT}/{city['id']}",
                json=new_data,
                headers=sheetly_header,
            )
            #print(response.text)
