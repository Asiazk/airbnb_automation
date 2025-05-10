class ListingResult:
    def __init__(self, url="", price=10000000, rating=0.0, title=""):
        self.url = url
        self.price_per_night = price
        self.rating = rating
        self.title = title


class BookingBox:
    def __init__(self, dates, adults, children):
        self.dates = dates
        self.adults = adults
        self.children = children
        # self.infants = None
        # self.pets = None

    def __str__(self):
        return (f"Dates: {self.dates}, "
                f"Adults: {self.adults}, Children: {self.children}")
