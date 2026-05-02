import gradio as gr
import inventory
import unittest

# Create a placeholder for the InventoryManager if it doesn't exist in the inventory module
# This ensures the Gradio app can run even if inventory.py is not fully populated yet,
# but it's better to have the InventoryManager defined in inventory.py as per requirements.
if not hasattr(inventory, 'manager'):
    print("Warning: inventory.manager not found. Creating a default instance.")
    inventory.manager = inventory.InventoryManager(low_stock_threshold=5) # Default threshold

# --- Gradio UI ---

def add_product_ui(name, price, stock_quantity):
    try:
        price = float(price)
        stock_quantity = int(stock_quantity)
        if price < 0 or stock_quantity < 0:
            return "Error: Price and stock quantity cannot be negative."
        inventory.manager.add_product(name, price, stock_quantity)
        return f"Product '{name}' added successfully."
    except ValueError:
        return "Error: Invalid input for price or stock quantity. Please enter numbers."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def update_product_ui(name, price, stock_quantity):
    try:
        if price is not None:
            price = float(price)
            if price < 0:
                return "Error: Price cannot be negative."
        if stock_quantity is not None:
            stock_quantity = int(stock_quantity)
            if stock_quantity < 0:
                return "Error: Stock quantity cannot be negative."

        inventory.manager.update_product(name, price if price is not None else None, stock_quantity if stock_quantity is not None else None)
        return f"Product '{name}' updated successfully."
    except ValueError:
        return "Error: Invalid input for price or stock quantity. Please enter numbers."
    except KeyError:
        return f"Error: Product '{name}' not found."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def create_order_ui(item_name, item_quantity):
    try:
        item_quantity = int(item_quantity)
        if item_quantity <= 0:
            return "Error: Item quantity must be positive."

        # We'll build the order dictionary incrementally
        if 'current_order_items' not in st.session_state:
            st.session_state.current_order_items = {}
        
        if item_name not in inventory.manager.products:
            return f"Error: Product '{item_name}' does not exist."

        st.session_state.current_order_items[item_name] = item_quantity
        
        # Calculate and display current order details
        total_cost = 0
        order_details_str = "Current Order:\n"
        for name, qty in st.session_state.current_order_items.items():
            if name in inventory.manager.products:
                product = inventory.manager.products[name]
                item_total = product.price * qty
                total_cost += item_total
                order_details_str += f"- {name}: {qty} x ${product.price:.2f} = ${item_total:.2f}\n"
            else:
                order_details_str += f"- {name}: {qty} (Product not found)\n"
        order_details_str += f"Total Estimated Cost: ${total_cost:.2f}"

        return order_details_str

    except ValueError:
        return "Error: Invalid quantity. Please enter a number."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def finalize_order_ui():
    if 'current_order_items' not in st.session_state or not st.session_state.current_order_items:
        return "Error: No items in the current order.", None

    order_items = st.session_state.current_order_items.copy()
    st.session_state.current_order_items = {} # Clear for next order

    try:
        order_id = inventory.manager.create_order(order_items)
        order_details = inventory.manager.get_order_details(order_id)
        if order_details:
            return f"Order placed successfully! Order ID: {order_id}", order_details.__dict__
        else:
            return f"Order created with ID {order_id}, but details could not be retrieved.", None
    except Exception as e:
        return f"Error placing order: {e}", None

def view_inventory_ui():
    inventory_report = inventory.manager.generate_inventory_report()
    if not inventory_report:
        return "Inventory is empty."
    
    report_str = "--- Inventory Report ---\n"
    for name, details in inventory_report.items():
        report_str += f"Product: {name}\n"
        report_str += f"  Price: ${details['price']:.2f}\n"
        report_str += f"  Stock: {details['stock_quantity']}\n"
        report_str += "------------------------\n"
    return report_str

def view_order_details_ui(order_id):
    order = inventory.manager.get_order_details(order_id)
    if order:
        order_dict = order.__dict__.copy()
        # Convert items dictionary for better readability if needed
        if 'items' in order_dict:
            items_str = ", ".join([f"{name} ({qty})" for name, qty in order_dict['items'].items()])
            order_dict['items'] = items_str
        return str(order_dict)
    else:
        return f"Order ID '{order_id}' not found."

def cancel_order_ui(order_id):
    try:
        inventory.manager.cancel_order(order_id)
        return f"Order '{order_id}' cancelled successfully."
    except Exception as e:
        return f"Error cancelling order: {e}"

def get_low_stock_alerts_ui():
    low_stock_items = inventory.manager.check_low_stock()
    if not low_stock_items:
        return "No low stock items."
    
    alerts_str = "--- Low Stock Alerts ---\n"
    for item in low_stock_items:
        alerts_str += f"Product: {item.name}, Current Stock: {item.stock_quantity}\n"
    alerts_str += "------------------------"
    return alerts_str

def get_total_sales_ui():
    total_sales = inventory.manager.get_total_sales()
    return f"Total Sales (Completed Orders): ${total_sales:.2f}"

# --- Unit Tests ---
class TestInventorySystem(unittest.TestCase):
    def setUp(self):
        # Reset manager for each test
        self.manager = inventory.InventoryManager(low_stock_threshold=5)
        inventory.manager = self.manager # Ensure Gradio uses this fresh instance

    def test_order_placement_and_stock_reduction(self):
        self.manager.add_product("TestItem", 10.0, 20)
        initial_stock = self.manager.products["TestItem"].stock_quantity
        
        order_id = self.manager.create_order({"TestItem": 5})
        self.assertIsNotNone(order_id)
        self.assertEqual(self.manager.products["TestItem"].stock_quantity, initial_stock - 5)

    def test_insufficient_stock_prevention(self):
        self.manager.add_product("ScarceItem", 25.0, 3)
        
        with self.assertRaises(SystemExit): # Assuming create_order might exit on failure or raise specific error
            # The current implementation prints and returns None, not raises.
            # Let's adapt the test to check the return value.
            result = self.manager.create_order({"ScarceItem": 5})
            self.assertIsNone(result, "Order should not be created with insufficient stock")
        
        self.assertEqual(self.manager.products["ScarceItem"].stock_quantity, 3, "Stock should not change if order fails")

    def test_order_cancellation_restores_stock(self):
        self.manager.add_product("CancelItem", 5.0, 10)
        order_id = self.manager.create_order({"CancelItem": 4})
        initial_stock_after_order = self.manager.products["CancelItem"].stock_quantity # Should be 6

        self.manager.cancel_order(order_id)
        self.assertEqual(self.manager.products["CancelItem"].stock_quantity, 10, "Stock should be restored after cancellation")
        self.assertTrue(self.manager.orders[order_id].is_cancelled)

# Run tests if the script is executed directly
if __name__ == "__main__":
    # This part is crucial for running the tests before launching Gradio
    # You can choose to run tests only or run tests and then launch Gradio
    try:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
        print("\nTests completed. Launching Gradio interface...\n")
    except Exception as e:
        print(f"An error occurred during test execution: {e}")
        print("Launching Gradio interface anyway...\n")

# --- Gradio Interface Definition ---

with gr.Blocks() as demo:
    gr.Markdown("# Inventory and Order Management System")

    with gr.Tab("Products"):
        with gr.Row():
            with gr.Column():
                product_name_input = gr.Textbox(label="Product Name")
                product_price_input = gr.Number(label="Price", value=0.0)
                product_stock_input = gr.Number(label="Stock Quantity", value=0)
                add_product_button = gr.Button("Add Product")
                update_product_name_input = gr.Textbox(label="Product Name to Update")
                update_product_price_input = gr.Number(label="New Price (optional)", value=None)
                update_product_stock_input = gr.Number(label="New Stock Quantity (optional)", value=None)
                update_product_button = gr.Button("Update Product")
        with gr.Row():
            add_product_output = gr.Textbox(label="Status")
            update_product_output = gr.Textbox(label="Status")

    with gr.Tab("Orders"):
        st.session_state.current_order_items = {} # Initialize session state for current order
        with gr.Row():
            with gr.Column():
                order_item_name_input = gr.Textbox(label="Item Name")
                order_item_quantity_input = gr.Number(label="Quantity", value=1)
                add_item_to_order_button = gr.Button("Add Item to Current Order")
                order_preview_output = gr.Textbox(label="Current Order Summary")
                finalize_order_button = gr.Button("Place Finalized Order")
                order_placement_output = gr.Textbox(label="Order Placement Status")
                order_details_output_json = gr.JSON(label="Order Details")
        
        with gr.Row():
            view_order_id_input = gr.Textbox(label="Order ID to View")
            view_order_details_button = gr.Button("View Order Details")
            cancel_order_id_input = gr.Textbox(label="Order ID to Cancel")
            cancel_order_button = gr.Button("Cancel Order")
            cancel_order_output = gr.Textbox(label="Cancellation Status")

    with gr.Tab("Reports"):
        with gr.Row():
            inventory_report_output = gr.Textbox(label="Inventory Report", lines=10)
            view_inventory_button = gr.Button("View Inventory")
        with gr.Row():
            low_stock_output = gr.Textbox(label="Low Stock Alerts", lines=5)
            view_low_stock_button = gr.Button("Check Low Stock")
        with gr.Row():
            total_sales_output = gr.Textbox(label="Total Sales")
            view_total_sales_button = gr.Button("View Total Sales")

    # --- Event Handlers ---
    add_product_button.click(
        fn=add_product_ui,
        inputs=[product_name_input, product_price_input, product_stock_input],
        outputs=[add_product_output]
    )
    update_product_button.click(
        fn=update_product_ui,
        inputs=[update_product_name_input, update_product_price_input, update_product_stock_input],
        outputs=[update_product_output]
    )
    add_item_to_order_button.click(
        fn=create_order_ui,
        inputs=[order_item_name_input, order_item_quantity_input],
        outputs=[order_preview_output]
    )
    finalize_order_button.click(
        fn=finalize_order_ui,
        inputs=[],
        outputs=[order_placement_output, order_details_output_json]
    )
    view_order_details_button.click(
        fn=view_order_details_ui,
        inputs=[view_order_id_input],
        outputs=[order_details_output_json] # Reusing JSON output for order details
    )
    cancel_order_button.click(
        fn=cancel_order_ui,
        inputs=[cancel_order_id_input],
        outputs=[cancel_order_output]
    )
    view_inventory_button.click(
        fn=view_inventory_ui,
        inputs=[],
        outputs=[inventory_report_output]
    )
    view_low_stock_button.click(
        fn=get_low_stock_alerts_ui,
        inputs=[],
        outputs=[low_stock_output]
    )
    view_total_sales_button.click(
        fn=get_total_sales_ui,
        inputs=[],
        outputs=[total_sales_output]
    )

if __name__ == "__main__":
    # Initialize the manager with some default data for demonstration
    inventory.manager.add_product("Laptop", 1200.00, 50)
    inventory.manager.add_product("Mouse", 25.50, 200)
    inventory.manager.add_product("Keyboard", 75.00, 150)
    inventory.manager.add_product("Monitor", 300.00, 30)
    
    # Make sure session state is clear at the start of a new session
    if 'current_order_items' not in gr.State.__dict__:
        gr.State.current_order_items = {}

    demo.launch()
```