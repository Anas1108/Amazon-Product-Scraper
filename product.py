class Product:
    def __init__(self, title, price, image_url, reviews, timestamp):
        self.title = title
        self.price = price
        self.image_url = image_url
        self.reviews = reviews
        self.timestamp = timestamp

    def __str__(self):
        return f"Title: {self.title}\nPrice: {self.price}\nImage URL: {self.image_url}\nReviews: {self.reviews}\nTimestamp: {self.timestamp}"
