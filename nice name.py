import csv

# Load product data from CSV file
products = {}
with open('products.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        products[row['Product_id']] = {
            'Name': row['Name'],
            'Price': float(row['Price']),
            'Currency': row['Currency'],
            'Quantity': int(row['Quantity'])
        }

# Load currency data from CSV file
currency = {}
with open('currency.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        currency[row['currency_code']] = {
            'Name': row['Name'],
            'Symbol': row['Symbol']
        }

# Initialize vending machine state
vending_machine = {
    'balance': 0.0,
    'selected_product': None
}

def display_products():
    print("Available products:")
    for Product_id, product in products.items():
        print(f"  {Product_id}: {product['Name']} - {product['Price']} {currency[product['Currency']]['Symbol']} - Quantity: {product['Quantity']}")


def display_balance():
    if vending_machine['selected_product'] is not None:
        product = products[vending_machine['selected_product']]
        print(f"Your current balance is: {vending_machine['balance']} {currency[product['Currency']]['Symbol']}")
    else:
        print("Please select a product first.")

def select_product():
    Product_id = input("Enter product ID: ")
    if Product_id not in products:
        print("Invalid product ID.")
        return

    vending_machine['selected_product'] = Product_id

def insert_money():
    amount = float(input("Enter amount to insert: "))
    vending_machine['balance'] += amount


def purchase_product():
    if vending_machine['selected_product'] is None:
        print("Please select a product first.")
        return

    product = products[vending_machine['selected_product']]
    if product['Quantity'] <= 0:
        print("Product is out of stock.")
        return

    if vending_machine['balance'] < product['Price']:
        print("Insufficient balance.")
        return

    vending_machine['balance'] -= product['Price']
    product['Quantity'] -= 1
    print(f"You have purchased {product['Name']} for {product['Price']} {currency[product['Currency']]['Symbol']}. Remaining Quantity: {product['Quantity']}.")
    vending_machine['selected_product'] = None


def main():
    while True:
        display_balance()
        display_products()

        option = input("(S)elect product, (I)nsert money, (P)urchase, (Q)uit: ")
        if option.upper() == 'S':
            select_product()
        elif option.upper() == 'I':
            insert_money()
        elif option.upper() == 'P':
            purchase_product()
        elif option.upper() == 'Q':
            print("Thank you for using our vending machine!")
            break

if __name__ == '__main__':
    main()