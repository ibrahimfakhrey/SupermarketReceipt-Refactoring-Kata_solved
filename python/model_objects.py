from enum import Enum

class Product:
    def __init__(self, name, unit):
        self.name = name
        self.unit = unit

    def __repr__(self):
        return f"Product(name={self.name}, unit={self.unit})"

class ProductQuantity:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

class ProductUnit(Enum):
    EACH = 1
    KILO = 2
    BAG = 4  # Add BAG to the enum


class SpecialOfferType(Enum):
    THREE_FOR_TWO = 1
    TEN_PERCENT_DISCOUNT = 2
    TWO_FOR_AMOUNT = 3
    FIVE_FOR_AMOUNT = 4
    TWENTY_PERCENT_DISCOUNT = 5  # New Offer for 20% discount on apples

class Offer:
    def __init__(self, offer_type, product, argument):
        self.offer_type = offer_type
        self.product = product
        self.argument = argument

class Discount:
    def __init__(self, product, description, discount_amount):
        self.product = product
        self.description = description
        self.discount_amount = discount_amount
