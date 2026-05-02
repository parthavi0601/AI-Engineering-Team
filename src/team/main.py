#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from team.crew import Team

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
requirements = """
Build a backend module for an inventory and order management system.

The system should allow:
- Adding products with name, price, and stock quantity
- Updating product details (price, stock)
- Removing products safely (only if not part of active orders)

The system should support:
- Creating customer orders with multiple products and quantities
- Generating unique order IDs
- Calculating total order cost dynamically
- Reducing stock when an order is placed

The system should:
- Prevent orders if stock is insufficient
- Validate all inputs (no negative price, stock, or quantity)
- Support order cancellation (restores stock correctly)
- Maintain complete order history (including cancelled orders)

The system should provide:
- Inventory reports (all products + stock levels)
- Low stock alerts (configurable threshold)
- Total sales tracking (based only on completed orders)
- Ability to fetch order details by ID

Technical constraints:
- Everything must be implemented in a SINGLE Python module
- Use clean object-oriented design (classes like Product, InventoryManager, Order)
- No external database (in-memory storage only)
- Code must be modular, readable, and testable

Testing:
- Include 1–2 simple unit tests covering:
  - Order placement
  - Stock validation

Frontend:
- ALSO generate a simple Gradio UI (app.py) that:
  - Allows adding products
  - Allows placing orders
  - Displays inventory
  - Shows order summary and total cost
- Keep UI minimal (prototype/demo level)

Output requirements:
- Backend module (.py)
- Test file (test_*.py)
- Simple Gradio UI (app.py)
- Design explanation (markdown)
"""
module_name = "inventory.py"
class_name = "InventoryManager"
def run():
    inputs={
        'requirements': requirements,
        'module_name': module_name,
        'class_name': class_name,
    }

    try:
        Team().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"Error during crew execution: {e}")