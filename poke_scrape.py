import pandas as pd
from selenium import webdriver
import time
import chromedriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Automatically install and set up the chromedriver
chromedriver_autoinstaller.install()

# Load the card data from a CSV file using pandas
card_collection = pd.read_csv("practice87.csv")
card_name = card_collection["Card name"]
card_number = card_collection["Card number"]
expansion = card_collection["Expansion"]
card_type = card_collection["Card variant"]
card_type = [card for card in card_type]

# Define the website URL and HTML element identifiers
website = "https://www.tcgcollector.com/cards/intl"
search_bar = "cardSearch"
hidden_price_html = "card-image-controls-price"
variant_html = 'card-price-details-modal-entry-card-variant-type-name-container'
price_html = '//span[@class="card-price-details-modal-entry-price-value"]'

# Create empty lists for the card data being searched and the market/low/mid prices
card_being_searched = []
pokemon_name = []
Market_list = []
Low_list = []
Mid_list = []

# These are varients that cant be searched up in the hidden price window
not_found_variants = ['Cracked Ice Holo', 'Cosmos Holo',
                      'WC Deck 2016: Magical Symphony (Shintaro Ito)',
                      'WC Deck 2009: Stallgon (David Cohen)',
                      'WC Deck 2007: Legendary Ascent (Tom Roos)',
                      'WC Deck 2004: Team Rushdown (Kevin Nguyen)',
                      'Non-holo (Incorrect Illustrator "Toshinao Aoki")',
                      'Normal (Missing Expansion Symbol)', ]

# List comprehension for searching by name and expansion if card number doesnt exist
card_being_searched = [f"{name} {number} {exp}" if not pd.isna(number)
                       else f"{name} {exp}" for name, number, exp in zip(card_name, card_number, expansion)]

# Verify that the length of the card data and the length of the searched card data is the same
assert len(card_being_searched) == len(card_name) == len(card_number) == len(expansion)


def search_site():
    options = webdriver.ChromeOptions()
    try:
        # We use a with statement, along with the try and finally blocks, to ensure the webdriver closes after using it
        with webdriver.Chrome(options=options) as driver:

            # Here we use a dictionary instead of aa long column of elif statements
            variant_to_index = {'Regular': 0, 'Reverse Holo': 4, 'Holo Rare': 8,
                                'Full Art': 12, 'Rainbow Rare': 16, 'Alternate Art': 20}
            wait = WebDriverWait(driver, 5)

            # Much more pythonic way using enumerate to access elements instead of using a seperate counter variable
            for i, card in enumerate(card_being_searched):
                driver.get(website)

                driver.find_element(By.NAME, search_bar).send_keys(str(card))
                time.sleep(2)
                wait.until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, 'button.card-price-details-modal-show-button'))).click()

                # Find the HTML elements for the variant type and price
                variant_finder = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, variant_html)))
                price_finder = wait.until(EC.presence_of_all_elements_located((By.XPATH, price_html)))

                market_price = ""
                low_price = ""
                mid_price = ""

                try:
                    # Here we use the get method on the dictionary to get the index of the variant we are searching
                    # for and use it to extract the corresponding prices from the 'price_finder' list
                    variant_index = variant_to_index.get(card_type[i], 0)

                    market_price = price_finder[variant_index]
                    low_price = price_finder[variant_index + 1]
                    mid_price = price_finder[variant_index + 2]

                    Market_list.append(market_price.text)
                    Low_list.append(low_price.text)
                    Mid_list.append(mid_price.text)

                # We added a couple more exceptions to make debugging a bit easier
                except IndexError:
                    # If an IndexError is raised, it means that we could not find the variant of the card we were
                    # searching for, so we assume that the card is not being sold and set the prices to $0.01
                    Market_list.append("$0.01")
                    Low_list.append("$0.01")
                    Mid_list.append("$0.01")
                except NoSuchElementException as e:
                    # If a NoSuchElementException is raised, it means that the element we are trying
                    # to access cannot be found on the page
                    print(f"Error: {e}")
                except ElementClickInterceptedException as e:
                    # If an ElementClickInterceptedException is raised, it means that the element
                    # we are trying to click on is being blocked by another element
                    print(f"Error: {e}")

            # Add the price lists to the card_collection dictionary as new columns and save to csv
            card_collection["Market_price"] = Market_list
            card_collection["Low_price"] = Low_list
            card_collection["Mid_price"] = Mid_list
            card_collection.to_csv("practice87.csv", mode='w', index=False)

    # This 'finally' block will be executed regardless of whether or not an exception is raised,
    # and is used for any necessary cleanup code
    finally:
        pass

search_site()