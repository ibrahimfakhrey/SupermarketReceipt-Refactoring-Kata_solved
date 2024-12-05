Setup Instructions
Clone the Repository


git clone <https://github.com/emilybache/SupermarketReceipt-Refactoring-Kata.git>
cd python
Activate the Virtual Environment Ensure the venv folder exists in the project directory.

On Windows:


venv\Scripts\activate
On macOS/Linux:


source venv/bin/activate
Install Dependencies Install all necessary dependencies from the requirements.txt file:


pip install -r requirements.txt
Run Tests Verify the functionality of the application by running the test suite:


pytest
Run the Application The application itself doesn't include a user interface but can be run by interacting with the provided classes and functions. For example, you can:

Create a FakeCatalog to manage products.
Use ShoppingCart to add items.
Add special offers via the Teller.
Generate and print a receipt.
Refer to the test cases in the tests directory for usage examples.
____________________________________________________________________
Example Usage
____________________________________________________________________
Here’s a simple example of how to use the system:

from model_objects import Product, ProductUnit, SpecialOfferType
from shopping_cart import ShoppingCart
from teller import Teller
from receipt_printer import ReceiptPrinter
from tests.fake_catalog import FakeCatalog

# Set up catalog and products
catalog = FakeCatalog()
apple = Product("Apple", ProductUnit.KILO)
catalog.add_product(apple, 1.99)

# Set up cart
cart = ShoppingCart()
cart.add_item_quantity(apple, 2)

# Set up offers
teller = Teller(catalog)
teller.add_special_offer(SpecialOfferType.TEN_PERCENT_DISCOUNT, apple, 10)

# Generate receipt
receipt = teller.checks_out_articles_from(cart)
printer = ReceiptPrinter()
print(printer.print_receipt(receipt))
Project Structure
catalog.py: Manages product pricing (placeholder implementation for simplicity).
model_objects.py: Defines core data structures like Product, Offer, Discount, etc.
receipt.py: Handles receipt creation and calculations.
receipt_printer.py: Formats and prints the receipt.
shopping_cart.py: Manages items and applies offers.
teller.py: Acts as the controller for checkout operations.
tests/: Contains unit tests for all core functionalities.
Dependencies
The application uses the following dependencies, managed via requirements.txt:
____________________________________________________________________
pytest for testing.
Notes
Ensure you activate the venv environment every time before running or testing the application.
____________________________________________________________________
This command runs the full test suite to ensure all features are functioning as expected.
pytest tests/ --maxfail=1 --disable-warnings -q
____________________________________________________________________

If you want to test specific features, you can specify the test file or function:
If you encounter issues, verify that Python 3.10+ is installed and the venv is properly set up.
License
This project is licensed under the MIT License.

