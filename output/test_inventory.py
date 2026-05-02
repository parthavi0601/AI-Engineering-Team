import unittest
from inventory import Product, Order, InventoryManager


class TestProduct(unittest.TestCase):
    def setUp(self):
        self.product = Product("Test Product", 10.0, 100)

    def test_initialize_product(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.price, 10.0)
        self.assertEqual(self.product.stock_quantity, 100)

    def test_update_price(self):
        self.product.update_price(12.0)
        self.assertEqual(self.product.price, 12.0)

    def test_update_price_negative(self):
        self.product.update_price(-5.0)
        self.assertEqual(self.product.price, 10.0)

    def test_update_stock(self):
        self.product.update_stock(150)
        self.assertEqual(self.product.stock_quantity, 150)

    def test_update_stock_negative(self):
        self.product.update_stock(-10)
        self.assertEqual(self.product.stock_quantity, 100)


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.product = Product("Test Product", 10.0, 100)
        self.order_items = {self.product: 5}
        self.order = Order("1", self.order_items)

    def test_calculate_total_cost(self):
        self.assertEqual(self.order.total_cost, 50.0)

    def test_complete_order(self):
        inventory_manager = InventoryManager(10)
        inventory_manager.add_product("Test Product", 10.0, 100)
        self.order.complete_order(inventory_manager)
        self.assertTrue(self.order.is_completed)
        self.assertEqual(inventory_manager.products["Test Product"].stock_quantity, 95)

    def test_complete_order_insufficient_stock(self):
        inventory_manager = InventoryManager(10)
        inventory_manager.add_product("Test Product", 10.0, 3)
        self.order.complete_order(inventory_manager)
        self.assertFalse(self.order.is_completed)

    def test_cancel_order(self):
        inventory_manager = InventoryManager(10)
        inventory_manager.add_product("Test Product", 10.0, 100)
        self.order.complete_order(inventory_manager)
        self.order.cancel_order(inventory_manager)
        self.assertTrue(self.order.is_cancelled)
        self.assertEqual(inventory_manager.products["Test Product"].stock_quantity, 100)


class TestInventoryManager(unittest.TestCase):
    def setUp(self):
        self.inventory_manager = InventoryManager(10)
        self.inventory_manager.add_product("Test Product", 10.0, 100)

    def test_add_product(self):
        self.inventory_manager.add_product("New Product", 20.0, 50)
        self.assertIn("New Product", self.inventory_manager.products)

    def test_update_product(self):
        self.inventory_manager.update_product("Test Product", 15.0, 80)
        self.assertEqual(self.inventory_manager.products["Test Product"].price, 15.0)
        self.assertEqual(self.inventory_manager.products["Test Product"].stock_quantity, 80)

    def test_remove_product(self):
        self.inventory_manager.remove_product("Test Product")
        self.assertNotIn("Test Product", self.inventory_manager.products)

    def test_create_order(self):
        order_id = self.inventory_manager.create_order({"Test Product": 5})
        self.assertIn(order_id, self.inventory_manager.orders)

    def test_cancel_order(self):
        order_id = self.inventory_manager.create_order({"Test Product": 5})
        self.inventory_manager.cancel_order(order_id)
        self.assertTrue(self.inventory_manager.orders[order_id].is_cancelled)

    def test_generate_inventory_report(self):
        report = self.inventory_manager.generate_inventory_report()
        self.assertEqual(len(report), 1)
        self.assertEqual(report["Test Product"]["price"], 10.0)

    def test_check_low_stock(self):
        self.inventory_manager.update_product("Test Product", stock_quantity=5)
        low_stock_products = self.inventory_manager.check_low_stock()
        self.assertIn(self.inventory_manager.products["Test Product"], low_stock_products)


if __name__ == '__main__':
    unittest.main()