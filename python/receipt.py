class ReceiptItem:
    def __init__(self, product, quantity, price, total_price):
        self.product = product
        self.quantity = quantity
        self.price = price
        self.total_price = total_price

class Receipt:
    def __init__(self):
        self._items = []
        self._discounts = []

    def total_price(self):
        total = sum(item.total_price for item in self.items) + sum(discount.discount_amount for discount in self.discounts)
        return total

    def add_product(self, product, quantity, price, total_price):
        self._items.append(ReceiptItem(product, quantity, price, total_price))

    def add_discount(self, discount):
        self._discounts.append(discount)

    @property
    def items(self):
        return self._items[:]

    @property
    def discounts(self):
        return self._discounts[:]

    def total_price(self):
        total = 0
        for item in self.items:
            total += item.total_price  # Assuming item.total_price is updated with the discount
        for discount in self.discounts:
            total += discount.discount_amount  # Subtract discount amounts
        return round(total, 2)
