from get_ua import get_ua
from bs4 import BeautifulSoup
import requests
from dotenv import dotenv_values


class HouseRenting:
    def __init__(self):
        self.all_price_list = []
        self.all_product_link = []
        self.all_address_list = []
        self.config = {**dotenv_values("./venv/.env")}

    def extracting_data(self):
        headers = {
            "user-agent": get_ua(),
            "accept-language": "en,en-US;q=0.9,bn;q=0.8",
        }

        data = requests.get(self.config["url"], headers=headers).text

        soup = BeautifulSoup(data, "html.parser")

        all_photo_card = soup.select(
            ".PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 "
        )
        self.all_price_list = [
            price.get_text().split("+")[0] for price in all_photo_card
        ]

        all_address = soup.find_all(name="address")
        self.all_address_list = [
            address.get_text().split("|")[1].strip()
            if "|" in address
            else address.strip()
            for address in all_address
        ]
        print(self.all_address_list)
