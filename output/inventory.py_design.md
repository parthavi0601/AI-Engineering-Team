```markdown
# Inventory and Order Management System Design

This document outlines the design for an inventory and order management system implemented in a single Python module named `inventory.py`. The system will contain multiple classes which encapsulate the various functionalities as specified in the high-level requirements.

## Classes and Methods

### Class: `Product`
This class represents a product in the inventory.

#### Attributes:
- `name` (str): The name of the product.
- `price` (float): The price of the product. Must be a non-negative value.
- `stock_quantity` (int): The current stock quantity of the product. Must be a non-negative value.

#### Methods:
- `__init__(name: str, price: float, stock_quantity: int)`: Initializes a product instance.
- `update_price(new_price: float)`: Updates the product's price. Ensures price is non-negative.
- `update_stock(new_stock: int)`: Updates the product's stock quantity. Ensures stock is non-negative.

### Class: `Order`
This class represents a customer order.

#### Attributes:
- `order_id` (str): A unique identifier for the order.
- `items` (dict): A dictionary holding product names as keys and their quantities as values.
- `total_cost` (float): The total cost of the order. Calculated dynamically.
- `is_completed` (bool): Status indicating if order is completed.
- `is_cancelled` (bool): Status indicating if order is cancelled.

#### Methods:
- `__init__(order_id: str, items: dict)`: Initializes an order instance.
- `calculate_total_inventory(inventory_manager: InventoryManager) -> float`: Calculates total cost based on current stock and prices in the inventory.
- `complete_order(inventory_manager: InventoryManager)`: Marks order as completed and reduces stock in the inventory.
- `cancel_order(inventory_manager: InventoryManager)`: Marks order as cancelled and restores stock in the inventory.

### Class: `InventoryManager`
This class is responsible for managing inventory and customer orders.

#### Attributes:
- `products` (dict): A dictionary storing all products with their names as keys.
- `orders` (dict): A dictionary storing all orders with their order IDs as keys.
- `low_stock_threshold` (int): A threshold for low stock alerts.
- `sales_total` (float): Total sales amount calculated from completed orders.

#### Methods:
- `__init__(low_stock_threshold: int)`: Initializes the inventory manager.
- `add_product(name: str, price: float, stock_quantity: int)`: Adds a new product to the inventory. Validates input values.
- `update_product(name: str, price: float = None, stock_quantity: int = None)`: Updates product details (price and/or stock).
- `remove_product(name: str)`: Safely removes a product if it’s not part of active orders.
- `create_order(items: dict) -> str`: Creates a new order with the given products and quantities. Validates stock levels and returns a unique order ID.
- `cancel_order(order_id: str)`: Cancels an existing order and restores stock.
- `generate_inventory_report() -> dict`: Generates a report of all products and stock levels.
- `check_low_stock() -> list`: Checks for products below the low stock threshold and returns list.
- `get_total_sales() -> float`: Returns the total sales from completed orders.
- `get_order_details(order_id: str) -> Order`: Retrieves details of a specific order by ID.

### Usage
The designed classes can be instantiated and utilized within a single Python module. Unit tests for order placement and stock validation can be implemented in a separate test file.

## Frontend (Gradio UI)
A minimal Gradio UI will be created in a file named `app.py` to allow users to:
- Add products to the inventory.
- Place orders by specifying products and quantities.
- Display the current inventory status.
- Show a summary of orders with their total cost.

The UI will serve as a prototype and help in demonstrating the system's functionality without extensive development.

## Testing
- A test file named `test_inventory.py` will be created containing unit tests to cover critical functionalities like:
  - Successful placement of an order with sufficient stock.
  - Prevention of order placement when stock is insufficient.

This design summary establishes a structured and organized approach to implementing the inventory and order management system in Python, focusing on clean object-oriented design principles.
```