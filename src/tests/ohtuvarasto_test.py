import unittest
from ohtuvarasto import Ohtuvarasto


class TestOhtuvarasto(unittest.TestCase):

    def setUp(self):
        self.manager = Ohtuvarasto()

    def test_create_warehouse_returns_id(self):
        warehouse_id = self.manager.create_warehouse("Test Warehouse")
        self.assertEqual(warehouse_id, 1)

    def test_create_multiple_warehouses_returns_unique_ids(self):
        id1 = self.manager.create_warehouse("Warehouse 1")
        id2 = self.manager.create_warehouse("Warehouse 2")
        self.assertEqual(id1, 1)
        self.assertEqual(id2, 2)

    def test_get_warehouse_returns_warehouse_data(self):
        warehouse_id = self.manager.create_warehouse("Test")
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertEqual(warehouse["name"], "Test")
        self.assertEqual(warehouse["products"], {})

    def test_get_nonexistent_warehouse_returns_none(self):
        warehouse = self.manager.get_warehouse(999)
        self.assertIsNone(warehouse)

    def test_get_all_warehouses(self):
        self.manager.create_warehouse("A")
        self.manager.create_warehouse("B")
        warehouses = self.manager.get_all_warehouses()
        self.assertEqual(len(warehouses), 2)

    def test_update_warehouse_name(self):
        warehouse_id = self.manager.create_warehouse("Old Name")
        result = self.manager.update_warehouse_name(warehouse_id, "New Name")
        self.assertTrue(result)
        warehouse = self.manager.get_warehouse(warehouse_id)
        self.assertEqual(warehouse["name"], "New Name")

    def test_update_nonexistent_warehouse_returns_false(self):
        result = self.manager.update_warehouse_name(999, "Name")
        self.assertFalse(result)

    def test_delete_warehouse(self):
        warehouse_id = self.manager.create_warehouse("Delete Me")
        result = self.manager.delete_warehouse(warehouse_id)
        self.assertTrue(result)
        self.assertIsNone(self.manager.get_warehouse(warehouse_id))

    def test_delete_nonexistent_warehouse_returns_false(self):
        result = self.manager.delete_warehouse(999)
        self.assertFalse(result)

    def test_add_product(self):
        warehouse_id = self.manager.create_warehouse("Test")
        result = self.manager.add_product(warehouse_id, "Apple", 10)
        self.assertTrue(result)
        products = self.manager.get_products(warehouse_id)
        self.assertEqual(products["Apple"], 10)

    def test_add_product_increases_existing_quantity(self):
        warehouse_id = self.manager.create_warehouse("Test")
        self.manager.add_product(warehouse_id, "Apple", 10)
        self.manager.add_product(warehouse_id, "Apple", 5)
        products = self.manager.get_products(warehouse_id)
        self.assertEqual(products["Apple"], 15)

    def test_add_product_to_nonexistent_warehouse_returns_false(self):
        result = self.manager.add_product(999, "Apple", 10)
        self.assertFalse(result)

    def test_add_product_with_negative_quantity_returns_false(self):
        warehouse_id = self.manager.create_warehouse("Test")
        result = self.manager.add_product(warehouse_id, "Apple", -5)
        self.assertFalse(result)

    def test_get_products_returns_copy(self):
        warehouse_id = self.manager.create_warehouse("Test")
        self.manager.add_product(warehouse_id, "Apple", 10)
        products = self.manager.get_products(warehouse_id)
        products["Apple"] = 999
        original_products = self.manager.get_products(warehouse_id)
        self.assertEqual(original_products["Apple"], 10)

    def test_get_products_from_nonexistent_warehouse_returns_none(self):
        products = self.manager.get_products(999)
        self.assertIsNone(products)

    def test_remove_product(self):
        warehouse_id = self.manager.create_warehouse("Test")
        self.manager.add_product(warehouse_id, "Apple", 10)
        result = self.manager.remove_product(warehouse_id, "Apple")
        self.assertTrue(result)
        products = self.manager.get_products(warehouse_id)
        self.assertNotIn("Apple", products)

    def test_remove_nonexistent_product_returns_false(self):
        warehouse_id = self.manager.create_warehouse("Test")
        result = self.manager.remove_product(warehouse_id, "Nonexistent")
        self.assertFalse(result)

    def test_remove_product_from_nonexistent_warehouse_returns_false(self):
        result = self.manager.remove_product(999, "Apple")
        self.assertFalse(result)

    def test_update_product_quantity(self):
        warehouse_id = self.manager.create_warehouse("Test")
        self.manager.add_product(warehouse_id, "Apple", 10)
        result = self.manager.update_product_quantity(warehouse_id, "Apple", 20)
        self.assertTrue(result)
        products = self.manager.get_products(warehouse_id)
        self.assertEqual(products["Apple"], 20)

    def test_update_product_quantity_with_negative_returns_false(self):
        warehouse_id = self.manager.create_warehouse("Test")
        self.manager.add_product(warehouse_id, "Apple", 10)
        result = self.manager.update_product_quantity(warehouse_id, "Apple", -5)
        self.assertFalse(result)

    def test_update_nonexistent_product_quantity_returns_false(self):
        warehouse_id = self.manager.create_warehouse("Test")
        result = self.manager.update_product_quantity(warehouse_id, "Nonexistent", 10)
        self.assertFalse(result)

    def test_update_product_in_nonexistent_warehouse_returns_false(self):
        result = self.manager.update_product_quantity(999, "Apple", 10)
        self.assertFalse(result)

    def test_clear_warehouse(self):
        warehouse_id = self.manager.create_warehouse("Test")
        self.manager.add_product(warehouse_id, "Apple", 10)
        self.manager.add_product(warehouse_id, "Banana", 5)
        result = self.manager.clear_warehouse(warehouse_id)
        self.assertTrue(result)
        products = self.manager.get_products(warehouse_id)
        self.assertEqual(products, {})

    def test_clear_nonexistent_warehouse_returns_false(self):
        result = self.manager.clear_warehouse(999)
        self.assertFalse(result)
