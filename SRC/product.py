import json
import os

class Product:
    def __init__(self, product_id, name, price, quantity):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f'{self.name} (ID: {self.product_id}) - Price: {self.price}, Stock: {self.quantity}'