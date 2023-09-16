import requests
from time import sleep
from get_ua import get_ua
from bs4 import BeautifulSoup
from dotenv import dotenv_values
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


class HouseRenting:
    def __init__(self):
        self.all_price_list = []
        self.all_properties_link = []
        self.all_address_list = []
        self.config = {**dotenv_values("./venv/.env")}
        self.all_data = {}
        self.driver = Chrome()

    def extracting_data(self):
        headers = {
            "user-agent": get_ua(),
            "accept-language": "en,en-US;q=0.9,bn;q=0.8",
        }

        data = requests.get(self.config["url"], headers=headers).text

        soup = BeautifulSoup(data, "html.parser")

        all_photo_card = soup.find_all(
            "span", class_="PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1"
        )
        # extracting the property price
        self.all_price_list = [
            price.get_text().split("+")[0] for price in all_photo_card
        ]

        print(self.all_price_list)
        all_address = soup.find_all(name="address")
        # extracting the property address
        self.all_address_list = [
            address.get_text().replace("|", "").strip() for address in all_address
        ]

        all_links = soup.find_all(
            "a",
            class_="property-card-link",
            attrs={"tabindex": "-1", "aria-hidden": "false"},
        )
        # extracting the property address link
        self.all_properties_link = [
            link.get("href")
            if "https://www.zillow.com" in link.get("href")
            else f"https://www.zillow.com{link.get('href')}"
            for link in all_links
        ]
        # combining all data together
        for x, (address, price, link) in enumerate(
            zip(self.all_address_list, self.all_price_list, self.all_properties_link)
        ):
            self.all_data[str(x)] = {
                "address": address,
                "price": price,
                "link": link,
            }

    def form_data_input(self):
        for x in self.all_data.keys():
            self.driver.get(self.config["form"])
            sleep(5)
            address_input = self.driver.find_element(
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div['
                "1]/div/div[1]/input",
            )
            address_input.send_keys(self.all_data[x]["address"])

            price_input = self.driver.find_element(
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
            price_input.send_keys(self.all_data[x]["price"])

            property_link_input = self.driver.find_element(
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input',
            )
            property_link_input.send_keys(self.all_data[x]["link"])

            submit_btn = self.driver.find_element(
                By.XPATH,
                '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span',
            )

            submit_btn.click()

    def create_sheet(self):
        self.driver.get(
            "https://accounts.google.com/v3/signin/identifier?continue=https%3A%2F%2Fdocs.google.com%2Fforms%2Fu%2F0%2F%3Ftgif%3Dd&followup=https%3A%2F%2Fdocs.google.com%2Fforms%2Fu%2F0%2F%3Ftgif%3Dd&ifkv=AYZoVhcGslrCJO8_h4PQlOJDyxdsma17yh1x-iNBkdaa5wV4S9hi4qclbtqx80bw9yHlswLGfOsD&ltmpl=forms&osid=1&passive=1209600&service=wise&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-804957902%3A1694855013214208&theme=glif"
        )
        sleep(10)
        email_input = self.driver.find_element(By.XPATH, '//*[@id="identifierId"]')
        email_input.send_keys(self.config["email"])

        next_btn = self.driver.find_element(
            By.XPATH, '//*[@id="identifierNext"]/div/button/span'
        )
        next_btn.click()

        sheet_btn = self.driver.find_element(
            By.XPATH,
            '//*[@id="ResponsesView"]/div/div[1]/div[1]/div[2]/div[1]/div[1]/div/span/span[2]',
        )
        sheet_btn.click()
