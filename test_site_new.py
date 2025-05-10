import pytest

from page_model import HomePage, ListingPage, ResultsPage, ReservationPage
import search_utils
from listing_result import ListingResult, BookingBox
from playwright.sync_api import Page, expect, sync_playwright


@pytest.mark.parametrize(
    "curr_base_url, place, checkin_date, checkout_date, adults, children",
    [
        ("https://www.airbnb.com", "tel aviv", "2025-06-02", "2025-06-04", 2, 0)
    ]
)
def test_search(browser, curr_base_url, place, checkin_date, checkout_date, adults, children):

    assertions = []

    result_context = browser.new_context()
    listing_context = browser.new_context()
    results_page = result_context.new_page()
    listing_page = listing_context.new_page()

    home = HomePage(results_page,  curr_base_url)
    home.load_page()
    results_page_url = home.search(place=place, checkin_date=checkin_date, checkout_date=checkout_date, adults=adults)

    results_page.goto(results_page_url, wait_until="load")
    new_results_page = ResultsPage(results_page, home.base_url)

    highest_rate_result = ListingResult()
    cheapest_price_result = ListingResult()

    page_num = 0
    while True:
        page_num += 1
        print("Page number: ", page_num)
        print("Results url: ", results_page.url)
        results = new_results_page.get_results()
        # print("len of results", len(results))

        for result in results:
            in_suggested_carousel = search_utils.is_in_suggestion_carousel(result)
            # skip the element which inside the suggestion carousel
            if in_suggested_carousel:
                print('entered carousel, skipping current result listing')
                continue

            curr_rate = search_utils.get_listing_rate(result)

            result_url = search_utils.get_listing_result_url(result)
            curr_price = search_utils.get_listing_price(result)

            result_url = f"https://{result_url}"

            listing_page.goto(result_url, wait_until="load")
            new_listing_page = ListingPage(listing_page, result_url)

            validate_location = new_listing_page.get_listing_location()
            curr_assert = place.lower() in validate_location.lower()
            if not curr_assert:
                assertions.append(f"Error: expected location: {place}, got {validate_location}, at url: {result_url}")

            vadults, vchildren = new_listing_page.get_guests(children != 0)
            curr_assert = vadults == adults
            if not curr_assert:
                assertions.append(f"Error: expected adults: {adults}, got {vadults}, at url: {result_url}")
            curr_assert = vchildren == children
            if not curr_assert:
                assertions.append(f"Error: expected children: {children}, got {vchildren}, at url: {result_url}")

            validate_checkin, validate_checkout = new_listing_page.get_listing_dates()
            curr_assert = checkin_date in validate_checkin
            if not curr_assert:
                assertions.append(f"Error: expected check-in: {checkin_date}, got {validate_checkin}, at url: {result_url}")
            curr_assert = checkout_date in validate_checkout
            if not curr_assert:
                assertions.append(f"Error: expected check-out: {checkout_date}, got {validate_checkout}, at url: {result_url}")

            if not curr_assert:
                continue

            curr_result = ListingResult(result_url, curr_price, curr_rate, validate_location)

            # first highest rate and first cheapest price are selected in case of same rate and same price
            if curr_rate:
                if curr_rate > highest_rate_result.rating:
                    highest_rate_result = curr_result

            if curr_price:
                if curr_price < cheapest_price_result.price_per_night:
                    cheapest_price_result = curr_result

            # print(f'{result_url=}')
            # print(curr_price)
            # print(curr_rate)

        next_results_url = new_results_page.get_next_results_page_url()
        if not next_results_url:
            break
        next_results_url = f"{home.base_url}{next_results_url}"
        prev_result_url = results_page.url
        results_page.goto(next_results_url, wait_until="load")
        # make sure we are on next page
        assert prev_result_url != results_page.url
        new_results_page = ResultsPage(results_page, home.base_url)

    search_utils.get_listing_details(highest_rate_result, "Highest Rate Result")
    search_utils.get_listing_details(cheapest_price_result, "Cheapest Price Result")

    assert not assertions, f"Listing validation errors: {assertions}"


@pytest.mark.parametrize(
    "curr_base_url, place, checkin_date, checkout_date, adults, children, phone",
    [
        ("https://www.airbnb.com", "tel aviv", "2025-06-02", "2025-06-04", 2, 1, "0500000000")
    ]
)
def test_second_search(browser, curr_base_url, place, checkin_date, checkout_date, adults, children, phone):

    assertions = []

    result_context = browser.new_context()
    listing_context = browser.new_context()
    results_page = result_context.new_page()
    listing_page = listing_context.new_page()

    home = HomePage(results_page,  curr_base_url)
    home.load_page()
    results_page_url = home.search(place=place, checkin_date=checkin_date,
                                   checkout_date=checkout_date, adults=adults, children=children)

    results_page.goto(results_page_url, wait_until="load")
    new_results_page = ResultsPage(results_page, home.base_url)

    highest_rate_result = ListingResult()

    page_num = 0
    while True:
        page_num += 1
        print("Page number: ", page_num)
        print("Results url: ", results_page.url)
        results = new_results_page.get_results()
        # print("len of results", len(results))

        for result in results:
            in_suggested_carousel = search_utils.is_in_suggestion_carousel(result)
            # skip the element which inside the suggestion carousel
            if in_suggested_carousel:
                print('entered carousel, skipping current result listing')
                continue

            curr_rate = search_utils.get_listing_rate(result)

            result_url = search_utils.get_listing_result_url(result)
            curr_price = search_utils.get_listing_price(result)

            result_url = f"https://{result_url}"

            listing_page.goto(result_url, wait_until="load")
            new_listing_page = ListingPage(listing_page, result_url)

            validate_location = new_listing_page.get_listing_location()
            curr_assert = place.lower() in validate_location.lower()
            if not curr_assert:
                assertions.append(f"Error: expected location: {place}, got {validate_location}, at url: {result_url}")

            vadults, vchildren = new_listing_page.get_guests(children != 0)
            curr_assert = vadults == adults
            if not curr_assert:
                assertions.append(f"Error: expected adults: {adults}, got {vadults}, at url: {result_url}")
            curr_assert = vchildren == children
            if not curr_assert:
                assertions.append(f"Error: expected children: {children}, got {vchildren}, at url: {result_url}")


            validate_checkin, validate_checkout = new_listing_page.get_listing_dates()
            curr_assert = checkin_date in validate_checkin
            if not curr_assert:
                assertions.append(f"Error: expected check-in: {checkin_date}, got {validate_checkin}, at url: {result_url}")
            curr_assert = checkout_date in validate_checkout
            if not curr_assert:
                assertions.append(f"Error: expected check-out: {checkout_date}, got {validate_checkout}, at url: {result_url}")

            if not curr_assert:
                continue

            curr_result = ListingResult(result_url, curr_price, curr_rate, validate_location)

            # first highest rate is selected in case of same rate
            if curr_rate:
                if curr_rate > highest_rate_result.rating:
                    highest_rate_result = curr_result

            # print(f'{result_url=}')
            # print(curr_price)
            # print(curr_rate)

        next_results_url = new_results_page.get_next_results_page_url()
        if not next_results_url:
            break
        next_results_url = f"{home.base_url}{next_results_url}"
        prev_result_url = results_page.url
        results_page.goto(next_results_url, wait_until="load")
        # make sure we are on next page
        assert prev_result_url != results_page.url
        new_results_page = ResultsPage(results_page, home.base_url)

    listing_page.goto(highest_rate_result.url, wait_until="load")
    search_utils.get_listing_details(highest_rate_result, "Highest Rate Result")
    highest_rate_listing_page = ListingPage(listing_page, home.base_url)
    highest_rate_listing_page.find_and_close_popup()
    bdates, badults, bchildren = highest_rate_listing_page.get_details_booking_box()
    booking_box_details = BookingBox(bdates, badults, bchildren)
    print("\nBooking box details from listing page: \n", booking_box_details)
    highest_rate_listing_page.make_reservation()
    reservation_listing = ReservationPage(listing_page)
    vadults, vcheckin, vcheckout, vchildren = reservation_listing.get_reservation_details(children != 0)
    assert vcheckin == checkin_date
    assert vcheckout == checkout_date
    assert vchildren == children
    assert vadults == adults
    reservation_listing.set_phone_input(phone) # not always appears on page, may fail
    assert reservation_listing.get_phone_input() == phone[1:]

    assert not assertions, f"Listing validation errors: {assertions}"

