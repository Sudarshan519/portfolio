class Invoice:
    def __init__(self, invoice_number, billing_date, due_date, company_info, customer_info, items, tax_rate=0):
        self.invoice_number = invoice_number
        self.billing_date = billing_date
        self.due_date = due_date
        self.company_info = company_info
        self.customer_info = customer_info
        self.items = items
        self.tax_rate = tax_rate

    def calculate_subtotal(self):
        subtotal = sum(item['quantity'] * item['price'] for item in self.items)
        return subtotal

    def calculate_tax(self):
        return self.calculate_subtotal() * self.tax_rate

    def calculate_total(self):
        total = self.calculate_subtotal() + self.calculate_tax()
        return total

    def generate_invoice(self):
        invoice_lines = []

        invoice_lines.append("Invoice Number: {}".format(self.invoice_number))
        invoice_lines.append("Billing Date: {}".format(self.billing_date))
        invoice_lines.append("Due Date: {}".format(self.due_date))
        invoice_lines.append("\n")
        
        # Company Information
        invoice_lines.append("From:")
        invoice_lines.append(self.company_info)
        invoice_lines.append("\n")
        
        # Customer Information
        invoice_lines.append("To:")
        invoice_lines.append(self.customer_info)
        invoice_lines.append("\n")
        
        # Itemized List
        invoice_lines.append("Item Description\tQuantity\tUnit Price\tTotal")
        for item in self.items:
            line = "{}\t{}\t{}\t{}".format(
                item['description'],
                item['quantity'],
                item['price'],
                item['quantity'] * item['price']
            )
            invoice_lines.append(line)
        invoice_lines.append("\n")
        
        # Totals
        invoice_lines.append("Subtotal: {}".format(self.calculate_subtotal()))
        invoice_lines.append("Tax ({}%): {}".format(self.tax_rate * 100, self.calculate_tax()))
        invoice_lines.append("Total Amount: {}".format(self.calculate_total()))

        return "\n".join(invoice_lines)


# Sample data
company_info = "Your Company Name\n123 Main Street\nCity, State, Zip\nPhone: (123) 456-7890"
customer_info = "Customer Name\n456 Customer Street\nCity, State, Zip\nEmail: customer@example.com"
invoice_data = {
    'invoice_number': 'INV12345',
    'billing_date': '2023-08-13',
    'due_date': '2023-09-13',
    'items': [
        {'description': 'Product A', 'quantity': 2, 'price': 50},
        {'description': 'Product B', 'quantity': 1, 'price': 75},
        {'description': 'Service C', 'quantity': 5, 'price': 20},
    ],
    'tax_rate': 0.1  # 10%
}

# Create an Invoice instance
invoice = Invoice(
    invoice_number=invoice_data['invoice_number'],
    billing_date=invoice_data['billing_date'],
    due_date=invoice_data['due_date'],
    company_info=company_info,
    customer_info=customer_info,
    items=invoice_data['items'],
    tax_rate=invoice_data['tax_rate']
)

# Generate and print the invoice
generated_invoice = invoice.generate_invoice()
print(generated_invoice)

# 30 4 * * * /path/to/python /path/to/daily_job_script.py
