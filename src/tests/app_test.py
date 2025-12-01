import unittest
from app import app, warehouse_manager
from ohtuvarasto import Ohtuvarasto


class TestFlaskApp(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.client = app.test_client()
        # Reset the warehouse manager before each test
        warehouse_manager._warehouses.clear()
        warehouse_manager._next_id = 1

    def test_index_page_loads(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Warehouses", response.data)

    def test_index_shows_no_warehouses_message(self):
        response = self.client.get("/")
        self.assertIn(b"No warehouses found", response.data)

    def test_create_warehouse_page_loads(self):
        response = self.client.get("/warehouse/new")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Create New Warehouse", response.data)

    def test_create_warehouse_post(self):
        response = self.client.post(
            "/warehouse/new", data={"name": "Test Warehouse"}, follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Warehouse", response.data)

    def test_create_warehouse_empty_name_shows_error(self):
        response = self.client.post(
            "/warehouse/new", data={"name": ""}, follow_redirects=True
        )
        self.assertIn(b"Warehouse name cannot be empty", response.data)

    def test_view_warehouse(self):
        warehouse_id = warehouse_manager.create_warehouse("Test Warehouse")
        response = self.client.get(f"/warehouse/{warehouse_id}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Warehouse", response.data)

    def test_view_nonexistent_warehouse_redirects(self):
        response = self.client.get("/warehouse/999", follow_redirects=True)
        self.assertIn(b"Warehouse not found", response.data)

    def test_edit_warehouse_page_loads(self):
        warehouse_id = warehouse_manager.create_warehouse("Test Warehouse")
        response = self.client.get(f"/warehouse/{warehouse_id}/edit")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Edit Warehouse", response.data)

    def test_edit_warehouse_post(self):
        warehouse_id = warehouse_manager.create_warehouse("Old Name")
        response = self.client.post(
            f"/warehouse/{warehouse_id}/edit",
            data={"name": "New Name"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"New Name", response.data)

    def test_delete_warehouse(self):
        warehouse_id = warehouse_manager.create_warehouse("Delete Me")
        response = self.client.post(
            f"/warehouse/{warehouse_id}/delete", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"deleted", response.data)
        self.assertIsNone(warehouse_manager.get_warehouse(warehouse_id))

    def test_add_product(self):
        warehouse_id = warehouse_manager.create_warehouse("Test Warehouse")
        response = self.client.post(
            f"/warehouse/{warehouse_id}/product/add",
            data={"product_name": "Apple", "quantity": "10"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        products = warehouse_manager.get_products(warehouse_id)
        self.assertEqual(products["Apple"], 10)

    def test_add_product_empty_name_shows_error(self):
        warehouse_id = warehouse_manager.create_warehouse("Test Warehouse")
        response = self.client.post(
            f"/warehouse/{warehouse_id}/product/add",
            data={"product_name": "", "quantity": "10"},
            follow_redirects=True,
        )
        self.assertIn(b"Invalid product name or quantity", response.data)

    def test_remove_product(self):
        warehouse_id = warehouse_manager.create_warehouse("Test Warehouse")
        warehouse_manager.add_product(warehouse_id, "Apple", 10)
        response = self.client.post(
            f"/warehouse/{warehouse_id}/product/Apple/remove", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        products = warehouse_manager.get_products(warehouse_id)
        self.assertNotIn("Apple", products)

    def test_update_product_quantity(self):
        warehouse_id = warehouse_manager.create_warehouse("Test Warehouse")
        warehouse_manager.add_product(warehouse_id, "Apple", 10)
        response = self.client.post(
            f"/warehouse/{warehouse_id}/product/Apple/update",
            data={"quantity": "20"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        products = warehouse_manager.get_products(warehouse_id)
        self.assertEqual(products["Apple"], 20)

    def test_clear_warehouse(self):
        warehouse_id = warehouse_manager.create_warehouse("Test Warehouse")
        warehouse_manager.add_product(warehouse_id, "Apple", 10)
        warehouse_manager.add_product(warehouse_id, "Banana", 5)
        response = self.client.post(
            f"/warehouse/{warehouse_id}/clear", follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        products = warehouse_manager.get_products(warehouse_id)
        self.assertEqual(products, {})
