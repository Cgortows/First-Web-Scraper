import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

card_collection = pd.read_csv("practice87.csv")
card_name = card_collection["Card name"]
card_number = card_collection["Card number"]
expansion = card_collection["Expansion"]
card_type = card_collection["Card variant"]
card_type = [card for card in card_type]  # Make card type more readable

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
    number_of_cards_searched = 0

    for card in card_being_searched:
        driver.get(website)

        driver.find_element(By.NAME, search_bar).send_keys(str(card))  # Enter full name in searchbar
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, 'button.card-price-details-modal-show-button').click()  # Click area where price is hidden
        time.sleep(2)

        variant_finder = driver.find_elements(By.CLASS_NAME, variant_html)
        price_finder = driver.find_elements(By.XPATH, price_html)

        market_price = ""
        low_price = ""
        mid_price = ""
        try:  # searching for correct variant to then pull correct prices

            if card_type[number_of_cards_searched] == variant_finder[0].text:
                market_price = price_finder[0]
                low_price = price_finder[1]
                mid_price = price_finder[2]
                print(market_price.text, low_price.text, mid_price.text)
            elif (card_type[number_of_cards_searched]) in not_found_variants:  # Use base price
                market_price = price_finder[0]
                low_price = price_finder[1]
                mid_price = price_finder[2]
                print(market_price.text, low_price.text, mid_price.text)
            elif card_type[number_of_cards_searched] == variant_finder[1].text:
                market_price = price_finder[4]
                low_price = price_finder[5]
                mid_price = price_finder[6]
                print(market_price.text, low_price.text, mid_price.text)
            elif card_type[number_of_cards_searched] == variant_finder[2].text:
                market_price = price_finder[8]
                low_price = price_finder[9]
                mid_price = price_finder[10]
                print(market_price.text, low_price.text, mid_price.text)
            elif card_type[number_of_cards_searched] == variant_finder[3].text:
                market_price = price_finder[12]
                low_price = price_finder[13]
                mid_price = price_finder[14]
                print(market_price.text, low_price.text, mid_price.text)
            elif card_type[number_of_cards_searched] == variant_finder[4].text:
                market_price = price_finder[16]
                low_price = price_finder[17]
                mid_price = price_finder[18]
                print(market_price.text, low_price.text, mid_price.text)
            elif card_type[number_of_cards_searched] == variant_finder[5].text:
                market_price = price_finder[20]
                low_price = price_finder[21]
                mid_price = price_finder[22]
                print(market_price.text, low_price.text, mid_price.text)
            Market_list.append(market_price.text)
            Low_list.append(low_price.text)
            Mid_list.append(mid_price.text)

        except IndexError:
            Market_list.append("$0.01")
            Low_list.append("$0.01")
            Mid_list.append("$0.01")

        number_of_cards_searched += 1

    # card_collection["Market_price"] = Market_list
    # card_collection["Low_price"] = Low_list
    # card_collection["Mid_price"] = Mid_list
    # card_collection.to_csv("practice87.csv", mode='w', index=False)


remove_nan_if_present()
search_site()
