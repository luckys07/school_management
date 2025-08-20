# library_module.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget,
    QLabel, QMessageBox
)
import db

class LibraryModule(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Library Management")
        self.setMinimumSize(500, 500)

        db.setup_tables()
        layout = QVBoxLayout()

        # Input: Book Title
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Book Title")
        layout.addWidget(self.title_input)

        # Input: Author
        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")
        layout.addWidget(self.author_input)

        # Input: ISBN
        self.isbn_input = QLineEdit()
        self.isbn_input.setPlaceholderText("ISBN")
        layout.addWidget(self.isbn_input)

        # Input: Quantity
        self.quantity_input = QLineEdit()
        self.quantity_input.setPlaceholderText("Quantity")
        layout.addWidget(self.quantity_input)

        # Add Book Button
        add_btn = QPushButton("Add Book")
        add_btn.clicked.connect(self.add_book)
        layout.addWidget(add_btn)

        # Book List
        self.book_list = QListWidget()
        layout.addWidget(QLabel("📚 All Books:"))
        layout.addWidget(self.book_list)

        self.setLayout(layout)
        self.load_books()

    def add_book(self):
        title = self.title_input.text().strip()
        author = self.author_input.text().strip()
        isbn = self.isbn_input.text().strip()
        try:
            quantity = int(self.quantity_input.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Quantity must be a number.")
            return

        if not title:
            QMessageBox.warning(self, "Missing Info", "Title is required.")
            return

        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO books (title, author, isbn, quantity)
            VALUES (?, ?, ?, ?)
        """, (title, author, isbn, quantity))
        conn.commit()
        conn.close()

        self.title_input.clear()
        self.author_input.clear()
        self.isbn_input.clear()
        self.quantity_input.clear()
        self.load_books()
        QMessageBox.information(self, "Success", "Book added successfully.")

    def load_books(self):
        self.book_list.clear()
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT title, author, quantity FROM books")
        for title, author, qty in cursor.fetchall():
            self.book_list.addItem(f"{title} by {author} (Qty: {qty})")
        conn.close()
