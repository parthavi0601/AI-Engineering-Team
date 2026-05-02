
class Product:
    def __init__(self, name: str, price: float, stock_quantity: int):
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    def update_price(self, new_price: float):
        if new_price < 0:
            print(f"Cannot update price to a negative value: {new_price}")
            return
        self.price = new_price

    def update_stock(self, new_stock: int):
        if new_stock < 0:
            print(f"Cannot update stock to a negative quantity: {new_stock}")
            return
        self.stock_quantity = new_stock


class Order:
    def __init__(self, order_id: str, items: dict):
        self.order_id = order_id
        self.items = items
        self.total_cost = self.calculate_total_cost(items)
        self.is_completed = False
        self.is_cancelled = False

    def calculate_total_cost(self, items: dict):
        return sum([product.price * quantity for product, quantity in items.items()])

    def complete_order(self, inventory_manager: 'InventoryManager'):
        for product_name, quantity in self.items.items():
            product = inventory_manager.products[product_name]
            if product.stock_quantity < quantity:
                print(f"Insufficient stock for order: {quantity} {product_name}(s) needed, but only {product.stock_quantity} available")
                return
        inventory_manager.reduce_stock(self.items)
        self.is_completed = True

    def cancel_order(self, inventory_manager: 'InventoryManager'):
        for product_name, quantity in self.items.items():
            product = inventory_manager.products[product_name]
            product.stock_quantity += quantity
        inventory_manager.add_order_to_history(self)
        self.is_completed = False
        self.is_cancelled = True


class InventoryManager:
    def __init__(self, low_stock_threshold: int):
        self.products = {}
        self.orders = {}
        self.low_stock_threshold = low_stock_threshold
        self.sales_total = 0
        self.order_history = []

    def add_product(self, name: str, price: float, stock_quantity: int):
        self.products[name] = Product(name, price, stock_quantity)

    def update_product(self, name: str, price: float = None, stock_quantity: int = None):
        if name in self.products:
            if price is not None:
                self.products[name].update_price(price)
            if stock_quantity is not None:
                self.products[name].update_stock(stock_quantity)

    def remove_product(self, name: str):
        if name in self.products and all(not self.orders.get(order_id).__dict__.get(f'{name}') for order_id in self.orders):
            del self.products[name]

    def create_order(self, items: dict) -> str:
        order_id = len(self.orders) + 1
        order = Order(str(order_id), items)
        for product_name, quantity in items.items():
            product = self.products[product_name]
            if product.stock_quantity - quantity < self.low_stock_threshold:
                print(f"Low-stock alert: {product_name} has {product.stock_quantity} units, only {self.low_stock_threshold} units left")
            if product.stock_quantity < quantity:
                print(f"Insufficient stock for order: {quantity} {product_name}(s) needed, but only {product.stock_quantity} available")
                return
            self.products[product_name].stock_quantity -= quantity
        self.orders[order.order_id] = order
        return order.order_id

    def cancel_order(self, order_id: str):
        if order_id in self.orders and not self.orders[order_id].is_completed:
            self.orders[order_id].cancel_order(self)
        else:
            print(f"Order {order_id} is either not found or is completed.")

    def add_order_to_history(self, order: Order):
        self.order_history.append(order)

    def generate_inventory_report(self) -> dict:
        return {product.name: product.__dict__ for product in self.products.values()}

    def check_low_stock(self) -> list:
        return [product for product in self.products.values() if product.stock_quantity <= self.low_stock_threshold]

    def get_total_sales(self) -> float:
        return sum(order.total_cost for order in self.order_history if order.is_completed)

    def get_order_details(self, order_id: str) -> Order:
        return self.orders.get(order_id)

    def reduce_stock(self, items: dict):
        for product_name, quantity in items.items():
            if product_name in self.products:
                self.products[product_name].stock_quantity -= quantity
            else:
                print(f"Product {product_name} does not exist in the product list.")


def main():
    manager = InventoryManager(10)

    manager.add_product("Item A", 10.99, 50)
    manager.add_product("Item B", 9.99, 100)
    print(manager.generate_inventory_report())

    order = manager.create_order({"Item A": 20, "Item B": 15})
    print(manager.generate_inventory_report())

    manager.cancel_order(order)
    print(manager.generate_inventory_report())
    print(manager.get_order_details(order))


if __name__ == "__main__":
    main()


import gradio as gr

manager = InventoryManager(10)

# Preload products
manager.add_product("Item A", 10.99, 50)
manager.add_product("Item B", 9.99, 100)


def add_product_ui(name, price, stock):
    manager.add_product(name, price, stock)
    return manager.generate_inventory_report()


def place_order_ui(item_a_qty, item_b_qty):
    items = {}
    if item_a_qty > 0:
        items["Item A"] = item_a_qty
    if item_b_qty > 0:
        items["Item B"] = item_b_qty

    order_id = manager.create_order(items)
    return f"Order ID: {order_id}"


def view_inventory_ui():
    return manager.generate_inventory_report()


with gr.Blocks() as demo:
    gr.Markdown("# 📦 Inventory Management System")

    with gr.Tab("Add Product"):
        name = gr.Textbox(label="Product Name")
        price = gr.Number(label="Price")
        stock = gr.Number(label="Stock")
        add_btn = gr.Button("Add Product")
        output1 = gr.JSON()

        add_btn.click(add_product_ui, [name, price, stock], output1)

    with gr.Tab("Place Order"):
        item_a = gr.Slider(0, 50, label="Item A Quantity")
        item_b = gr.Slider(0, 50, label="Item B Quantity")
        place_btn = gr.Button("Place Order")
        output2 = gr.Textbox()

        place_btn.click(place_order_ui, [item_a, item_b], output2)

    with gr.Tab("View Inventory"):
        view_btn = gr.Button("Refresh")
        output3 = gr.JSON()

        view_btn.click(view_inventory_ui, [], output3)

demo.launch()