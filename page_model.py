from playwright.sync_api import Page
import re


class HomePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.search_box = page.locator('#bigsearch-query-location-input')
        self.search_button = page.locator('[data-testid="structured-search-input-search-button"]')
        self.base_url = base_url
        self.checkin_button = page.locator('[data-testid="structured-search-input-field-split-dates-0"]')
        self.checkout_button = page.locator('[data-testid="structured-search-input-field-split-dates-1"]')
        self.guest_box = page.locator('[data-testid="structured-search-input-field-guests-button"]')
        self.increase_adult = page.locator('[data-testid="stepper-adults-increase-button"]')
        self.increase_children = page.locator('[data-testid="stepper-children-increase-button"]')
        # self.increase_pets = None
        # self.increase_infants = None

    def load_page(self):
        self.page.goto(self.base_url)

    def set_page(self, new_page: Page):
        self.page = new_page

    def search(self, place, checkin_date, checkout_date, adults, children=0):
        self.search_box.fill(place)

        self.checkin_button.click()
        self.page.locator(f'[data-state--date-string="{checkin_date}"]').click()

        self.checkout_button.click()
        self.checkout_button.click()
        self.page.locator(f'[data-state--date-string="{checkout_date}"]').click()
        self.guest_box.click()

        if adults:
            for _ in range(adults):
                self.increase_adult.click()

        if children:
            for _ in range(children):
                self.increase_children.click()

        self.search_button.click()
        return self.page.url


class ResultsPage:
    def __init__(self, page: Page, base_url):
        self.page = page
        self.base_url = base_url
        self.results_selector = "div[itemscope][itemtype='http://schema.org/ListItem']"
        self.next_button_selector = 'a[aria-label="Next"]'

    def load_page(self, url):
        self.page.goto(url)

    def get_results(self):
        self.page.wait_for_selector(self.results_selector)
        return self.page.query_selector_all(self.results_selector)

    def get_next_results_page_url(self):
        next_buttons = self.page.query_selector_all(self.next_button_selector)
        if next_buttons:
            last_next_button = next_buttons[-1]
            if last_next_button:
                next_page_url = last_next_button.get_attribute('href')
                # print(f'{next_page_url=}')
                return next_page_url
        else:
            next_buttons = self.page.query_selector_all('button[aria-label="Next"]')
            if next_buttons:
                next_button_disabled = next_buttons[-1].get_attribute('aria-disabled')
                if next_button_disabled == 'true':
                    return ""
        return ""


class ListingPage:
    def __init__(self, page: Page, url):
        self.page = page
        self.url = url
        self.price_selector = 'div[aria-hidden="true"] span:has-text("₪")'
        self.booking_box = page.locator('[data-testid="book-it-default"]')
        self.booking_box_dates = page.locator('xpath=//button[contains(@aria-label, "Change dates")]')
        self.translation_popup = page.locator('div[role="dialog"][aria-label="Translation on"]')
        self.title = page.title()

    def load_page(self, url):
        self.page.goto(url)

    def set_page(self, new_page: Page):
        self.page = new_page

    def get_listing_location(self):
        title = self.page.title()
        return title if title else "Unavailable"

    def get_listing_price(self):
        curr_price = None
        self.page.wait_for_selector(self.price_selector)
        curr_price_res = self.page.query_selector(self.price_selector)
        if curr_price_res:
            curr_price_text = curr_price_res.text_content()
            match = re.search(r'\d+', curr_price_text)
            if match:
                curr_price = int(match.group())
        return curr_price

    def get_listing_dates(self):
        dates = self.page.locator('//button[contains(@aria-label, "Check-in")]').get_attribute('aria-label')
        match = re.search(r'Check-in:\s*([\d-]+);\s*Checkout:\s*([\d-]+)', dates)
        if match:
            checkin = match.group(1)
            checkout = match.group(2)
            return checkin, checkout
        return "Unavailable checkin", "Unavailable checkout"

    def find_and_close_popup(self):
        popup = self.translation_popup
        if popup:
            close_button = popup.locator('button[aria-label="Close"]')
            close_button.click()
        else:
            return

    def get_details_booking_box(self):
        dates = self.booking_box_dates.inner_text()
        guests_button = self.booking_box.locator('#GuestPicker-book_it-trigger')
        guests_button.click()
        guests = self.booking_box.locator('[aria-labelledby="GuestPicker-book_it-form"]')
        guests.click()
        adults = guests.locator('[data-testid="GuestPicker-book_it-form-adults-stepper-value"]').inner_text()
        children = guests.locator('[data-testid="GuestPicker-book_it-form-children-stepper-value"]').inner_text()
        guests_button.click()
        return dates, adults, children

    def make_reservation(self):
        reserve_button = self.booking_box.locator('[data-testid="homes-pdp-cta-btn"]').nth(1)
        # reserve_button.wait_for(state="visible")
        reserve_button.click()

    def get_guests(self, is_children):
        url = self.url
        match = re.search(r'[?&]adults=(\d+)', url)
        adults = int(match.group(1))
        children = 0
        if is_children:
            match = re.search(r'[?&]children=(\d+)', url)
            children = int(match.group(1))
        return adults, children


class ReservationPage:
    def __init__(self, page: Page):
        self.page = page
        self.phone_input = page.locator('#phoneInputphone-login')
        self.reservation_dates = page.locator("div", has_text=re.compile(r"^[A-Z][a-z]{2} \d{1,2}\s*–\s*\d{1,2}$"))

    def set_phone_input(self, phone):
        self.phone_input.fill(phone[1:])

    def get_phone_input(self):
        return self.phone_input.input_value()

    def get_reservation_details(self, is_children):
        url = self.page.url
        match = re.search(r'[?&]numberOfAdults=(\d+)', url)
        adults = int(match.group(1))
        match = re.search(r"checkin=(\d{4}-\d{2}-\d{2})", url)
        checkin = match.group(1)
        match = re.search(r"checkout=(\d{4}-\d{2}-\d{2})", url)
        checkout = match.group(1)
        children = 0
        if is_children:
            match = re.search(r'[?&]numberOfChildren=(\d+)', url)
            children = int(match.group(1))
        return adults, checkin, checkout, children
