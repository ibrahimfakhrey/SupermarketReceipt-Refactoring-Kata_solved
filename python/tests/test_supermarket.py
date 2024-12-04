import pytest
from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from receipt import Receipt
from tests.fake_catalog import FakeCatalog

from receipt_printer import ReceiptPrinter

# Test to verify correct receipt calculation without any special offers
# Updated test_simple_receipt method
def test_simple_receipt():
    catalog = FakeCatalog()
    apple = Product("Apple", ProductUnit.KILO)
    catalog.add_product(apple, 1.99)

    cart = ShoppingCart()
    cart.add_item(apple)  # Using add_item method instead of add_item_quantity

    teller = Teller(catalog)
    receipt = teller.checks_out_articles_from(cart)

    # Test total price
    assert receipt.total_price() == pytest.approx(1.99, 0.01)  # Adjusted for 1 item only
    assert len(receipt.items) == 1  # Only one product in the receipt
    assert receipt.items[0].product == apple
    assert receipt.items[0].quantity == 1  # Quantity is 1 since add_item adds 1 by default
    assert receipt.items[0].price == 1.99
    assert receipt.items[0].total_price == pytest.approx(1.99, 0.01)


# Test applying a 10% discount on apples
def test_ten_percent_discount():
    catalog = FakeCatalog()
    apple = Product("Apple", ProductUnit.KILO)
    catalog.add_product(apple, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apple, 10)

    cart = ShoppingCart()
    cart.add_item_quantity(apple, 2)

    receipt = teller.checks_out_articles_from(cart)

    # Check if discount is applied correctly
    assert receipt.total_price() == pytest.approx(2 * 1.99 * 0.9, 0.01)
    assert len(receipt.discounts) == 1  # Only one discount applied
    assert receipt.discounts[0].description == "10% off"
    assert receipt.discounts[0].discount_amount == pytest.approx(-0.4, 0.01)  # Update expected value to -0.4


def test_three_for_two_offer():
    catalog = FakeCatalog()
    toothbrush = Product("Toothbrush", ProductUnit.EACH)
    catalog.add_product(toothbrush, 0.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.THREE_FOR_TWO, toothbrush, 3)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 3)

    receipt = teller.checks_out_articles_from(cart)

    print("Items in receipt before final total calculation:")
    totla = 0
    for item in receipt.items:
        print(f"Product: {item.product.name}, Quantity: {item.quantity}, Total Price: {item.total_price}")
        totla+=item.total_price



    # The total price should reflect the "Three for Two" offer (pay for 2 items)
    # The correct total price should be 2 * 0.99
    assert totla == pytest.approx(2 * 0.99, 0.01)  # Total price should be 2 * 0.99
    assert len(receipt.items) == 1  # Only one product in the receipt
    assert receipt.items[0].product == toothbrush
    assert receipt.items[0].quantity == 3
    assert receipt.items[0].total_price == pytest.approx(2 * 0.99, 0.01)  # Total price should be 2 * 0.99


# Test the "2 for amount" special offer
def test_two_for_amount_offer():
    catalog = FakeCatalog()
    toothpaste = Product("Toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, toothpaste, 3.50)

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 4)

    receipt = teller.checks_out_articles_from(cart)
    totla = 0
    for item in receipt.items:
        print(f"Product: {item.product.name}, Quantity: {item.quantity}, Total Price: {item.total_price}")
        totla += item.total_price
    print(f"this offer two and here is the total {totla}")
    # Price should be discounted for every 2 items
    assert totla == pytest.approx(3.50 * 2, 0.01)  # Two sets of "2 for amount"
    assert len(receipt.items) == 1  # Only one product in the receipt
    assert receipt.items[0].product == toothpaste
    assert receipt.items[0].quantity == 4
    assert receipt.items[0].total_price == pytest.approx(3.50 * 2, 0.01)


# Test a bundle offer (e.g., 1 toothbrush + 1 toothpaste)
def test_bundle_offer():
    catalog = FakeCatalog()
    toothbrush = Product("Toothbrush", ProductUnit.EACH)
    toothpaste = Product("Toothpaste", ProductUnit.EACH)

    catalog.add_product(toothbrush, 0.99)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothbrush, 10)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, toothpaste, 10)

    cart = ShoppingCart()
    cart.add_item_quantity(toothbrush, 1)
    cart.add_item_quantity(toothpaste, 1)

    receipt = teller.checks_out_articles_from(cart)

    # Total should have 10% discount for both items in the bundle
    expected_total = (0.99 + 1.79) * 0.9
    assert receipt.total_price() == pytest.approx(expected_total, 0.01)


# Test that HTML receipt generation works
def test_html_receipt_generation():
    catalog = FakeCatalog()
    apple = Product("Apple", ProductUnit.KILO)
    catalog.add_product(apple, 1.99)

    cart = ShoppingCart()
    cart.add_item_quantity(apple, 2)

    teller = Teller(catalog)
    receipt = teller.checks_out_articles_from(cart)

    receipt_printer = ReceiptPrinter(columns=50)
    html_receipt = receipt_printer.print_receipt(receipt)

    # Check if HTML contains the total
    assert "Total: " in html_receipt
    assert "Apple" in html_receipt
    assert "2" in html_receipt  # Quantity should be printed
    assert "1.99" in html_receipt  # Price should be printed


# Test with no special offers applied
def test_no_special_offers():
    catalog = FakeCatalog()
    rice = Product("Rice", ProductUnit.KILO)
    catalog.add_product(rice, 2.49)

    cart = ShoppingCart()
    cart.add_item_quantity(rice, 3)

    teller = Teller(catalog)
    receipt = teller.checks_out_articles_from(cart)

    # Total price without discounts
    assert receipt.total_price() == pytest.approx(3 * 2.49, 0.01)
    assert len(receipt.items) == 1  # Only one product in the receipt
    assert receipt.items[0].product == rice
    assert receipt.items[0].quantity == 3
    assert receipt.items[0].total_price == pytest.approx(3 * 2.49, 0.01)


# Test the 20% discount on apples
def test_twenty_percent_discount_on_apples():
    catalog = FakeCatalog()
    apple = Product("Apple", ProductUnit.KILO)
    catalog.add_product(apple, 1.99)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apple, 20)  # 20% discount

    cart = ShoppingCart()
    cart.add_item_quantity(apple, 2)

    receipt = teller.checks_out_articles_from(cart)

    # Check if discount is applied correctly (20% off)
    assert receipt.total_price() == pytest.approx(2 * 1.99 * 0.8, 0.01)  # 20% off should be 2 * 1.99 * 0.8


# Test the 10% discount on rice
def test_ten_percent_discount_on_rice():
    catalog = FakeCatalog()
    rice = Product("Rice", ProductUnit.BAG)
    catalog.add_product(rice, 2.49)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, rice, 10)  # 10% discount

    cart = ShoppingCart()
    cart.add_item_quantity(rice, 3)

    receipt = teller.checks_out_articles_from(cart)

    # Check if discount is applied correctly (10% off)
    assert receipt.total_price() == pytest.approx(3 * 2.49 * 0.9, 0.01)  # 10% off


def test_five_for_seven_forty_nine_toothpaste():
    catalog = FakeCatalog()
    toothpaste = Product("Toothpaste", ProductUnit.EACH)
    catalog.add_product(toothpaste, 1.79)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.FIVE_FOR_AMOUNT, toothpaste, 7.49)  # Correct offer type

    cart = ShoppingCart()
    cart.add_item_quantity(toothpaste, 5)

    receipt = teller.checks_out_articles_from(cart)
    totla = 0
    for item in receipt.items:
        print(f"Product: {item.product.name}, Quantity: {item.quantity}, Total Price: {item.total_price}")
        totla += item.total_price
    print(f"this offer two and here is the total {totla}")

    # Ensure that the total price is €7.49 for 5 tubes
    assert totla == pytest.approx(7.49, 0.01)


# Test the "Two boxes of cherry tomatoes for €0.99" offer
def test_two_for_ninety_nine_cherry_tomatoes():
    catalog = FakeCatalog()
    cherry_tomatoes = Product("Cherry Tomatoes", ProductUnit.EACH)
    catalog.add_product(cherry_tomatoes, 0.69)

    teller = Teller(catalog)
    teller.add_special_offer(SpecialOfferType.TWO_FOR_AMOUNT, cherry_tomatoes, 0.99)  # 2 boxes for 0.99

    cart = ShoppingCart()
    cart.add_item_quantity(cherry_tomatoes, 2)

    receipt = teller.checks_out_articles_from(cart)
    totla = 0
    for item in receipt.items:
        print(f"Product: {item.product.name}, Quantity: {item.quantity}, Total Price: {item.total_price}")
        totla += item.total_price
    print(f"this offer two and here is the total {totla}")
    # Price should be €0.99 for 2 boxes
    assert totla== pytest.approx(0.99, 0.01)
    assert len(receipt.items) == 1  # Only one product in the receipt
    assert receipt.items[0].product == cherry_tomatoes
    assert receipt.items[0].quantity == 2
    assert receipt.items[0].total_price == pytest.approx(0.99, 0.01)
