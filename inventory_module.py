# inventory_module.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox
)
import db

class InventoryModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setMinimumSize(500, 500)

        db.setup_tables()
        layout = QVBoxLayout()

        # Input: Item Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Item Name")
        layout.addWidget(self.name_input)

        # Input: Quantity
        self.qty_input = QLineEdit()
        self.qty_input.setPlaceholderText("Quantity")
        layout.addWidget(self.qty_input)

        # Input: Location
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Storage Location")
        layout.addWidget(self.location_input)

        # Add Item Button
        add_btn = QPushButton("Add Inventory Item")
        add_btn.clicked.connect(self.add_item)
        layout.addWidget(add_btn)

        # Inventory List
        self.inventory_list = QListWidget()
        layout.addWidget(QLabel("📦 Inventory Items:"))
        layout.addWidget(self.inventory_list)

        self.setLayout(layout)
        self.load_items()

    def add_item(self):
        name = self.name_input.text().strip()
        location = self.location_input.text().strip()
        try:
            qty = int(self.qty_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Quantity must be a number.")
            return

        if not name:
            QMessageBox.warning(self, "Input Error", "Item name is required.")
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO inventory_items (name, quantity, location)
            VALUES (?, ?, ?)
        """, (name, qty, location))
        conn.commit()
        conn.close()

        self.name_input.clear()
        self.qty_input.clear()
        self.location_input.clear()
        self.load_items()
        QMessageBox.information(self, "Success", "Item added successfully.")

    def load_items(self):
        self.inventory_list.clear()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, quantity, location FROM inventory_items")
        for name, qty, loc in cursor.fetchall():
            self.inventory_list.addItem(f"{name} - Qty: {qty} ({loc})")
        conn.close()
