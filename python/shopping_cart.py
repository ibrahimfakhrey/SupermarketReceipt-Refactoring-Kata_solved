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
                if offer.offer_type == SpecialOfferType.THREE_FOR_TWO:
                    if quantity_as_int >= 3:
                        number_of_offers = quantity_as_int // 3  # Full 3-for-2 offers
                        price_to_pay = (quantity_as_int - number_of_offers) * unit_price  # Only pay for non-free items
                        discount_amount = quantity_as_int * unit_price - price_to_pay  # Calculate the discount amount
                        print(
                            f"Three for Two offer: {number_of_offers} offers, price to pay: {price_to_pay}, discount amount: {discount_amount}")
                        discount = Discount(p, "3 for 2", -round(discount_amount, 2))

                        # Apply the discount to the receipt items
                        for item in receipt.items:
                            if item.product == p:
                                item.total_price = round(item.quantity * unit_price - discount_amount, 2)

                # Handling Two for Amount Offer (e.g., Cherry tomatoes, Toothpaste)
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
                    x = 5  # The number of items needed for the special offer
                    number_of_x = quantity_as_int // x  # Number of full bundles of 5
                    if number_of_x > 0:
                        discount_total = offer.argument * number_of_x  # The price for the 5 tubes at €7.49 each bundle
                        discount = Discount(p, f"{x} for {offer.argument}", -round(discount_total, 2))

                        # Apply the discount to the receipt items
                        for item in receipt.items:
                            if item.product == p:
                                item.total_price = round(discount_total, 2)  # Update the total price for this item


                # Handling 10% Discount Offer (e.g., Rice)
                elif offer.offer_type == SpecialOfferType.TEN_PERCENT_DISCOUNT:
                    discount_amount = -round(quantity * unit_price * offer.argument / 100.0, 2)
                    discount = Discount(p, str(offer.argument) + "% off", discount_amount)

                # Handling 20% Discount on Apples (New Offer)
                elif offer.offer_type == SpecialOfferType.TWENTY_PERCENT_DISCOUNT:
                    if quantity_as_int >= 1:
                        discount_amount = -round(quantity * unit_price * 0.20, 2)  # 20% discount
                        discount = Discount(p, "20% off", discount_amount)

                if discount:
                    receipt.add_discount(discount)

    def total_price(self):
        total = 0
        for item in self.items:
            print(f"Item: {item.product.name}, Quantity: {item.quantity}, Price: {item.total_price}")
            total += item.total_price  # Assuming item.total_price is updated
        return round(total, 2)
