from playwright.sync_api import Page, expect
import re
from listing_result import ListingResult
from page_model import ResultsPage, ReservationPage, ListingPage
from listing_result import ListingResult

# def search_infra(lowest_price, highest_rated,
#                  results_page, listing_page,
#                  new_results_page, place):
#     page_num = 0
#     while True:
#         page_num += 1
#         print("Page number: ", page_num)
#         print("Results url: ", results_page.url)
#         results = new_results_page.get_results()
#         # print("len of results", len(results))
#
#         for result in results:
#             in_suggested_carousel = is_in_suggestion_carousel(result)
#             # skip the element which inside the suggestion carousel
#             if in_suggested_carousel:
#                 print('entered carousel, skipping current result listing')
#                 continue
#
#             curr_rate = .get_listing_rate(result)
#
#             result_url = get_listing_result_url(result)
#             curr_price = get_listing_price(result)
#
#             result_url = f"https://{result_url}"
#
#             listing_page.goto(result_url, wait_until="load")
#             new_listing_page = ListingPage(listing_page, result_url)
#
#             validate_location = new_listing_page.get_listing_location()
#             curr_assert = place.lower() in validate_location.lower()
#             if not curr_assert:
#                 assertions.append(f"Error: expected location: {place}, got {validate_location}, at url: {result_url}")
#
#             vadults, vchildren = new_listing_page.get_guests(children != 0)
#             assert vadults == adults
#             if not curr_assert:
#                 assertions.append(f"Error: expected adults: {adults}, got {vadults}")
#             assert  vchildren == children
#             if not curr_assert:
#                 assertions.append(f"Error: expected children: {children}, got {vchildren}")
#
#
#             validate_checkin, validate_checkout = new_listing_page.get_listing_dates()
#             curr_assert = checkin_date in validate_checkin
#             if not curr_assert:
#                 assertions.append(f"Error: expected check-in: {checkin_date}, got {validate_checkin}, at url: {result_url}")
#             curr_assert = checkout_date in validate_checkout
#             if not curr_assert:
#                 assertions.append(f"Error: expected check-out: {checkout_date}, got {validate_checkout}, at url: {result_url}")
#
#             if not curr_assert:
#                 continue
#
#             curr_result = ListingResult(result_url, curr_price, curr_rate, validate_location)
#
#             # first highest rate is selected in case of same rate
#             if curr_rate:
#                 if curr_rate > highest_rate_result.rating:
#                     highest_rate_result = curr_result
#
#             print(f'{result_url=}')
#             print(curr_price)
#             print(curr_rate)
#
#         next_results_url = new_results_page.get_next_results_page_url()
#         if not next_results_url:
#             break
#         next_results_url = f"{home.base_url}{next_results_url}"
#         prev_result_url = results_page.url
#         results_page.goto(next_results_url, wait_until="load")
#         # make sure we are on next page
#         assert prev_result_url != results_page.url
#         new_results_page = ResultsPage(results_page, home.base_url)
#

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


# def get_rate(page, url):
#     page.goto(url)
#     curr_rate = page.query_selector('span:has-text("Rated")').inner_text()
#     print(f'{curr_rate=}')
#     curr_rate.split()
#     return int(curr_rate[1])


def get_listing_details(result: ListingResult, result_title):
    print(f"************** {result_title} *************")
    print(f"Title: {result.title}")
    print(f"Price Per Night: {result.price_per_night}")
    print(f"Rating: {result.rating}")
    print(f"URL: {result.url}")


def get_location_result(page):
    location = page.title()
    return location if location else "Unavailable"


# def get_dates_result(page):
#     dates = page.locator('//button[contains(@aria-label, "Check-in")]').get_attribute('aria-label')
#     match = re.search(r'Check-in:\s*([\d-]+);\s*Checkout:\s*([\d-]+)', dates)
#     if match:
#         checkin = match.group(1)
#         checkout = match.group(2)
#         return checkin, checkout
#     return "Unavailable checkin", "Unavailable checkout"


def lowest_rate():
    pass


