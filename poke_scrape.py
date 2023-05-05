import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

chromedriver_autoinstaller.install()

card_collection = pd.read_csv("practice87.csv")
card_name = card_collection["Card name"]
card_number = card_collection["Card number"]
expansion = card_collection["Expansion"]
card_type = card_collection["Card variant"]
card_type = [card for card in card_type]  # Make card type more readable.

website = "https://www.tcgcollector.com/cards/intl"
search_bar = "cardSearch"
hidden_price_html = "card-image-controls-price"
variant_html = 'card-price-details-modal-entry-card-variant-type-name-container'
price_html = '//span[@class="card-price-details-modal-entry-price-value"]'

card_being_searched = []
pokemon_name = []

Market_list = []
Low_list = []
Mid_list = []

not_found_variants = ['Cracked Ice Holo', 'Cosmos Holo',  # Don't show up in hidden price window
                      'WC Deck 2016: Magical Symphony (Shintaro Ito)',
                      'WC Deck 2009: Stallgon (David Cohen)',
                      'WC Deck 2007: Legendary Ascent (Tom Roos)',
                      'WC Deck 2004: Team Rushdown (Kevin Nguyen)',
                      'Non-holo (Incorrect Illustrator "Toshinao Aoki")',
                      'Normal (Missing Expansion Symbol)', ]


card_being_searched = [f"{name} {number} {exp}" if not pd.isna(number)
                       else f"{name} {exp}" for name, number, exp in zip(card_name, card_number, expansion)]
assert len(card_being_searched) == len(card_name) == len(card_number) == len(expansion)


def search_site():
    options = webdriver.ChromeOptions()
    try:
        with webdriver.Chrome(options=options) as driver:
            variant_to_index = {'Regular': 0, 'Reverse Holo': 4, 'Holo Rare': 8, 'Full Art': 12, 'Rainbow Rare': 16, 'Alternate Art': 20}
            wait = WebDriverWait(driver, 5)

            for i, card in enumerate(card_being_searched):
                driver.get(website)
                driver.find_element(By.NAME, search_bar).send_keys(str(card))  # Enter full name in searchbar
                time.sleep(2)
                wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'button.card-price-details-modal-show-button'))).click()

                variant_finder = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, variant_html)))
                price_finder = wait.until(EC.presence_of_all_elements_located((By.XPATH, price_html)))

                market_price = ""
                low_price = ""
                mid_price = ""
                try:  # searching for correct variant to then pull correct prices
                    variant_index = variant_to_index.get(card_type[i], 0)
                    market_price = price_finder[variant_index]
                    low_price = price_finder[variant_index + 1]
                    mid_price = price_finder[variant_index + 2]
                    print(market_price.text, low_price.text, mid_price.text)
                    Market_list.append(market_price.text)
                    Low_list.append(low_price.text)
                    Mid_list.append(mid_price.text)
                    print(1)
                except IndexError:
                        Market_list.append("$0.01")
                        Low_list.append("$0.01")
                        Mid_list.append("$0.01")
                except NoSuchElementException as e:
                    print(f"Error: {e}")
                except ElementClickInterceptedException as e:
                    print(f"Error: {e}")
            # card_collection["Market_price"] = Market_list
            # card_collection["Low_price"] = Low_list
            # card_collection["Mid_price"] = Mid_list
            # card_collection.to_csv("practice87.csv", mode='w', index=False)
    finally:
        pass

search_site()