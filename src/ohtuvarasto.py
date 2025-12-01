"""Ohtuvarasto - A warehouse manager for managing multiple warehouses with products."""


class Ohtuvarasto:
    """Manages multiple warehouses, each containing products with quantities."""

    def __init__(self):
        self._warehouses = {}  # {warehouse_id: {"name": str, "products": {product_name: quantity}}}
        self._next_id = 1

    def create_warehouse(self, name):
        """Create a new warehouse with the given name. Returns warehouse ID."""
        warehouse_id = self._next_id
        self._warehouses[warehouse_id] = {"name": name, "products": {}}
        self._next_id += 1
        return warehouse_id

    def get_warehouse(self, warehouse_id):
        """Get warehouse details by ID. Returns None if not found."""
        return self._warehouses.get(warehouse_id)

    def get_all_warehouses(self):
        """Get all warehouses as a list of (id, warehouse_data) tuples."""
        return [(wid, data) for wid, data in self._warehouses.items()]

    def update_warehouse_name(self, warehouse_id, new_name):
        """Update the name of a warehouse. Returns True if successful."""
        if warehouse_id in self._warehouses:
            self._warehouses[warehouse_id]["name"] = new_name
            return True
        return False

    def delete_warehouse(self, warehouse_id):
        """Delete a warehouse. Returns True if successful."""
        if warehouse_id in self._warehouses:
            del self._warehouses[warehouse_id]
            return True
        return False

    def add_product(self, warehouse_id, product_name, quantity):
        """Add a product to a warehouse. Returns True if successful."""
        if warehouse_id not in self._warehouses:
            return False
        if quantity < 0:
            return False
        products = self._warehouses[warehouse_id]["products"]
        if product_name in products:
            products[product_name] += quantity
        else:
            products[product_name] = quantity
        return True

    def get_products(self, warehouse_id):
        """Get all products in a warehouse. Returns dict of {name: quantity}."""
        warehouse = self._warehouses.get(warehouse_id)
        if warehouse:
            return warehouse["products"].copy()
        return None

    def remove_product(self, warehouse_id, product_name):
        """Remove a product from a warehouse. Returns True if successful."""
        if warehouse_id not in self._warehouses:
            return False
        products = self._warehouses[warehouse_id]["products"]
        if product_name in products:
            del products[product_name]
            return True
        return False

    def update_product_quantity(self, warehouse_id, product_name, new_quantity):
        """Update the quantity of a product. Returns True if successful."""
        if warehouse_id not in self._warehouses:
            return False
        if new_quantity < 0:
            return False
        products = self._warehouses[warehouse_id]["products"]
        if product_name in products:
            products[product_name] = new_quantity
            return True
        return False

    def clear_warehouse(self, warehouse_id):
        """Clear all products from a warehouse. Returns True if successful."""
        if warehouse_id in self._warehouses:
            self._warehouses[warehouse_id]["products"] = {}
            return True
        return False
