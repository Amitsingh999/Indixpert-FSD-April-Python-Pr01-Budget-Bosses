import json
import os
from .product import Product

class InventoryManagementSystem:
    def __init__(self, username):
        self.path = f'data/products/products.{username}.json'
        self.products = {}
        self.max_quantity = 200
        self.product_id_counter = 1
        self.load_products()

    def load_products(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as file:
                    data = json.load(file)
                    for product in data:
                        self.products[product['id']] = Product(
                            product['id'], product['name'], product['price'], product['quantity']
                        )
                        self.product_id_counter = max(self.product_id_counter, int(product['id'][4:]) + 1)
            except json.JSONDecodeError:
                print("Error loading product data. Starting with an empty inventory.")
                self.products = {}
        else:
            self.products = {}

    def save_products(self):
        products = [
            {'id': p.product_id, 'name': p.name, 'price': p.price, 'quantity': p.quantity}
            for p in self.products.values()
        ]
        with open(self.path, 'w') as file:
            json.dump(products, file, indent=2)

    def add_product(self, name, price, quantity):
        if any(p.name.lower() == name.lower() for p in self.products.values()):
            print(f"A product with the name '{name}' already exists.")
            return

        if len(self.products) >= 20:
            print("Maximum number of products reached.")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            print("Invalid price or quantity.")
            return

        product_id = f"PD10{self.product_id_counter:04d}"
        self.products[product_id] = Product(product_id, name, price, quantity)
        self.product_id_counter += 1

        self.save_products()
        print(f"Product {name} added successfully with ID: {product_id}")

    def update_stock(self, name):
        product = next((p for p in self.products.values() if p.name.lower() == name.lower()), None)
        if not product:
            print("Product not found.")
            return

        action = input("What would you like to update? (1: Price, 2: Quantity): ")
        if action == "1":
            try:
                product.price = float(input("Enter new price: "))
                print(f"Product price updated to {product.price}.")
            except ValueError:
                print("Invalid price entered.")
        elif action == "2":
            self.update_quantity(product)
        else:
            print("Invalid option.")

    def update_quantity(self, product):
        action = input("Enter action (+ for restock, - for sell): ")
        try:
            quantity = int(input("Enter quantity: "))
        except ValueError:
            print("Invalid quantity entered.")
            return

        if action == "-":
            if product.quantity >= quantity:
                product.quantity -= quantity
                print(f"Sold {quantity} of {product.name}. Updated stock: {product.quantity}")
            else:
                print("Not enough stock to sell!")
        elif action == "+":
            if 0 < product.quantity + quantity <= self.max_quantity:
                product.quantity += quantity
                print(f"Restocked {quantity} of {product.name}. Updated stock: {product.quantity}")
            else:
                print(f"Error: Total quantity cannot exceed {self.max_quantity}.")
        else:
            print("Invalid action.")

    def check_stock(self, name):
        product = next((p for p in self.products.values() if p.name.lower() == name.lower()), None)
        if product:
            print(f"Current stock for {product.name}: {product.quantity}")
        else:
            print("Product not found.")

    def delete_product(self, name):
        product = next((p for p in self.products.values() if p.name.lower() == name.lower()), None)
        if product:
            confirmation = input(f"Are you sure you want to delete the product '{product.name}'? (yes/no): ")
            if confirmation.lower() == 'yes':
                del self.products[product.product_id]
                self.save_products()
                print(f"Product {name} deleted successfully.")
            else:
                print("Product deletion canceled.")
        else:
            print("Product not found.")

    def display_inventory(self):
        if not self.products:
            print("Inventory is empty.")
            return

        show_details = input("Do you want to show product details? (yes/no): ").strip().lower()
        if show_details == 'yes':
            for product in self.products.values():
                print(product)

    def search_product(self):
        search_term = input("Enter at least 3 letters of the product name: ")

        if len(search_term) < 3:
            print("Please enter at least 3 letters to search.")
            return

        matching_products = [product for product in self.products.values() if search_term.lower() in product.name.lower()]

        if matching_products:
            print("Search Results:")
            for product in matching_products:
                print(product)
        else:
            print("No products found matching your search.")