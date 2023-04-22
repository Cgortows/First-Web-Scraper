import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

card_collection = pd.read_csv("Charizard_cards.csv")
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


def remove_nan_if_present():
    for (name, number, exp) in zip(card_name, card_number, expansion):
        pokemon_name.append(name)
        if str(number) == "nan":
            card_being_searched.append(str(name) + " " + str(exp))
        else:
            card_being_searched.append(str(name) + " " + str(number) + " " + str(exp))


def search_site():
    global driver
    driver = webdriver.Chrome()

    variant_to_index = {'Regular': 0, 'Reverse Holo': 4, 'Holo Rare': 8, 'Full Art': 12, 'Rainbow Rare': 16, 'Alternate Art': 20}

    for i, card in enumerate(card_being_searched):
        driver.get(website)
        driver.find_element(By.NAME, search_bar).send_keys(str(card))  # Enter full name in searchbar
        time.sleep(3)
        driver.find_element(By.PARTIAL_LINK_TEXT, pokemon_name[i]).click()  # Click link for name
        time.sleep(2)
        driver.find_element(By.CLASS_NAME, hidden_price_html).click()  # Click area where price is hidden
        time.sleep(2)

        variant_finder = driver.find_elements(By.CLASS_NAME, variant_html)
        price_finder = driver.find_elements(By.XPATH, price_html)

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

        except IndexError:
            Market_list.append("$0.01")
            Low_list.append("$0.01")
            Mid_list.append("$0.01")

    driver.quit()

    card_collection["Market_price"] = Market_list
    card_collection["Low_price"] = Low_list
    card_collection["Mid_price"] = Mid_list
    card_collection.to_csv("Charizard_cards.csv", mode='w', index=False)

remove_nan_if_present()
search_site()