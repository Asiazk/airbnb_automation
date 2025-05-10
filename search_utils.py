from playwright.sync_api import Page, expect
import re
from listing_result import ListingResult
from page_model import ResultsPage, ReservationPage, ListingPage
from listing_result import ListingResult


def is_in_suggestion_carousel(result):
    in_suggested_carousel = result.evaluate(
        'el => !!el.closest("div[aria-labelledby=\'carousel-label\']")')
    return in_suggested_carousel


def get_listing_result_url(result):
    return result.query_selector('meta[itemprop="url"]').get_attribute('content')


def get_listing_rate(result):
    curr_rate = None
    rate_text_res = result.query_selector('span:has-text("out of 5")')
    # need to check if rating exists in current result
    if rate_text_res:
        rate_text_res = rate_text_res.inner_text()
        curr_rate = float(rate_text_res.split()[0])
    return curr_rate


def get_listing_price(result):
    curr_price = None
    price_text_res = result.query_selector('span:has-text("per night")')
    # need to check if rating exists in current result
    if price_text_res:
        price_text_res = price_text_res.inner_text()
        print(f'{price_text_res=}')
        matches = re.findall(r'\d[\d,]*', price_text_res)
        numbers = [int(m.replace(',', '')) for m in matches]
        curr_price = min(numbers)
    return curr_price


def get_listing_details(result: ListingResult, result_title):
    print(f"************** {result_title} *************")
    print(f"Title: {result.title}")
    print(f"Price Per Night: {result.price_per_night}")
    print(f"Rating: {result.rating}")
    print(f"URL: {result.url}")


def get_location_result(page):
    location = page.title()
    return location if location else "Unavailable"


