import math
from model_objects import ProductQuantity, SpecialOfferType, Discount

class ShoppingCart:

    def __init__(self):
        self._items = []
        self._product_quantities = {}

    @property
    def items(self):
        return self._items

    def add_item(self, product):
        self.add_item_quantity(product, 1.0)

    def add_item_quantity(self, product, quantity):
        self._items.append(ProductQuantity(product, quantity))
        if product in self._product_quantities.keys():
            self._product_quantities[product] += quantity
        else:
            self._product_quantities[product] = quantity

    def handle_offers(self, receipt, offers, catalog):
        for p in self._product_quantities.keys():
            quantity = self._product_quantities[p]
            if p in offers.keys():
                offer = offers[p]
                unit_price = catalog.unit_price(p)
                quantity_as_int = int(quantity)
                discount = None


                # Handling Three for Two Offer
                # Handling Three for Two Offer
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:

                    if quantity_as_int >= 3:
                        number_of_offers = quantity_as_int // 3  # Full 3-for-2 offers
                        price_to_pay = (quantity_as_int - number_of_offers) * unit_price  # Only pay for non-free items
                        discount_amount = quantity_as_int * unit_price - price_to_pay  # Calculate the discount amount
                        print(f" this is the  number of offer{ number_of_offers} and here is the price to pay {price_to_pay} and here is the discount_amount {discount_amount}")
                        discount = Discount(p, "3 for 2", -round(discount_amount, 2))  # Apply discount

                        # Apply the discount to the receipt items
                        for item in receipt.items:
                            if item.product == p:
                                print(
                                    f"Original total: {item.total_price}, Discounted total: {item.quantity * unit_price - discount_amount}")
                                item.total_price = round(item.quantity * unit_price - discount_amount, 2)



                # Other offer types...
                elif offer.offer_type == SpecialOfferType.TWO_FOR_AMOUNT:
                    # Apply discount for every two items
                    if quantity_as_int >= 2:
                        number_of_pairs = quantity_as_int // 2  # Calculate number of pairs
                        price_to_pay = number_of_pairs * offer.argument  # Apply offer price to each pair
                        discount_amount = (unit_price * quantity_as_int) - price_to_pay  # Calculate total discount
                        discount = Discount(p, "2 for " + str(offer.argument), -round(discount_amount, 2))

                        # Apply the discount to the receipt items
                        for item in receipt.items:
                            if item.product == p:
                                # Update the total price to reflect the discounted price
                                item.total_price = round(price_to_pay, 2)  # Set total price to the price for pairs



                elif offer.offer_type == SpecialOfferType.FIVE_FOR_AMOUNT:
                    x = 5
                    number_of_x = math.floor(quantity_as_int / x)
                    if quantity_as_int >= 5:
                        discount_total = unit_price * quantity - (
                                offer.argument * number_of_x + quantity_as_int % 5 * unit_price)
                        discount = Discount(p, str(x) + " for " + str(offer.argument), -round(discount_total, 2))

                elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount_amount = -round(quantity * unit_price * offer.argument / 100.0, 2)
                    discount = Discount(p, str(offer.argument) + "% off", discount_amount)

                if discount:
                    receipt.add_discount(discount)

    def total_price(self):
        total = 0
        for item in self.items:
            print(f"Item: {item.product.name}, Quantity: {item.quantity}, Price: {item.total_price}")
            total += item.total_price  # Assuming item.total_price is updated
        return round(total, 2)
