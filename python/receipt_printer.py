from model_objects import ProductUnit

class ReceiptPrinter:
    def __init__(self, columns=40):
        self.columns = columns

    def print_receipt(self, receipt):
        result = ""
        for item in receipt.items:
            result += self.print_receipt_item(item)

        for discount in receipt.discounts:
            result += self.print_discount(discount)

        result += "\n" + self.present_total(receipt)
        return str(result)

    def print_receipt_item(self, item):
        total_price_printed = self.print_price(item.total_price)
        name = item.product.name
        line = self.format_line_with_whitespace(name, total_price_printed)
        if item.quantity != 1:
            line += f"  {self.print_price(item.price)} * {self.print_quantity(item)}\n"
        return line

    def format_line_with_whitespace(self, name, value):
        whitespace_size = self.columns - len(name) - len(value)
        line = f"{name}{' ' * whitespace_size}{value}\n"
        return line

    def print_price(self, price):
        return "%.2f" % price

    def print_quantity(self, item):
        return str(item.quantity) if ProductUnit.EACH == item.product.unit else '%.3f' % item.quantity

    def print_discount(self, discount):
        name = f"{discount.description} ({discount.product.name})"
        value = self.print_price(discount.discount_amount)
        return self.format_line_with_whitespace(name, value)

    def present_total(self, receipt):
        name = "Total: "
        value = self.print_price(receipt.total_price())
        return self.format_line_with_whitespace(name, value)
