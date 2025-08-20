import sys, os, traceback
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout,
    QVBoxLayout, QPushButton, QLabel, QSizePolicy, QScrollArea, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt


class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("School Management System")
        self.setMinimumSize(1000, 600)

        central_widget = QWidget()
        main_layout = QHBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Sidebar
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(10)

        title_label = QLabel("📋 Dashboard Menu")
        title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(title_label)

        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(theme_btn)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Features: (text, module file, class, icon path)
        features = [
            ("Learning Management System", "lms_module", "LMSModule", "icons/lms.png"),
            ("Library Management",         "library_module", "LibraryModule", "icons/library.png"),
            ("Transport Management",       "transport_module", "TransportModule", "icons/bus.png"),
            ("Hostel Management",          "hostel_module", "HostelModule", "icons/hostel.png"),
            ("Inventory Management",       "inventory_module", "InventoryModule", "icons/inventory.png"),
            ("HR Management",              "hr_module", "HRModule", "icons/hr.png"),
            ("Biometrics/RFID",            "biometric_module", "BiometricModule", "icons/biometric.png"),
        ]

        for text, module_name, class_name, icon_path in features:
            btn = QPushButton(f"  {text}")
            # Load icon or fallback
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
            else:
                btn.setIcon(QIcon("icons/default.png"))
            btn.setIconSize(QSize(24, 24))
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.clicked.connect(lambda _, m=module_name, c=class_name, t=text: self.load_module(m, c, t))
            scroll_layout.addWidget(btn)

        scroll_layout.addStretch()
        scroll_area.setWidget(scroll_widget)
        sidebar_layout.addWidget(scroll_area)

        sidebar_container = QWidget()
        sidebar_container.setLayout(sidebar_layout)
        sidebar_container.setFixedWidth(350)  # Increased width
        main_layout.addWidget(sidebar_container, 1)

        # Content area placeholder
        self.content_area = QWidget()
        self.content_area.setMinimumWidth(600)
        main_layout.addWidget(self.content_area, 3)

        self.is_dark_theme = False

    def toggle_theme(self):
        if self.is_dark_theme:
            self.setStyleSheet("")
            self.is_dark_theme = False
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #2C3E50; }
                QPushButton { background-color: #34495E; color: white; padding: 8px; border-radius: 4px; }
                QPushButton:hover { background-color: #1ABC9C; }
                QLabel { color: white; }
                QScrollArea { background-color: transparent; }
            """)
            self.is_dark_theme = True

    def load_module(self, module_name, class_name, display_name):
        try:
            module = __import__(module_name)
            module_class = getattr(module, class_name)
            widget = module_class()
        except Exception as e:
            tb = traceback.format_exc()
            QMessageBox.critical(self, "Load Error",
                                 f"Failed to load {class_name} from {module_name}.\n\n{e}\n\n{tb}")
            return

        # Create container with title + module
        container = QWidget()
        v_layout = QVBoxLayout(container)

        title_label = QLabel(display_name)
        title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        v_layout.addWidget(title_label)

        v_layout.addWidget(widget)

        layout = self.centralWidget().layout()
        layout.removeWidget(self.content_area)
        self.content_area.deleteLater()
        self.content_area = container
        layout.addWidget(self.content_area, 3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec_())













# import sys, os, traceback
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QWidget, QHBoxLayout,
#     QVBoxLayout, QPushButton, QLabel, QSizePolicy, QScrollArea, QMessageBox
# )
# from PyQt5.QtGui import QFont, QIcon
# from PyQt5.QtCore import QSize, Qt


# class Dashboard(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("School Management System")
#         self.setMinimumSize(1000, 600)

#         central_widget = QWidget()
#         main_layout = QHBoxLayout(central_widget)
#         self.setCentralWidget(central_widget)

#         # Sidebar
#         sidebar_layout = QVBoxLayout()
#         sidebar_layout.setContentsMargins(10, 10, 10, 10)
#         sidebar_layout.setSpacing(10)

#         title_label = QLabel("📋 Dashboard Menu")
#         title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
#         title_label.setAlignment(Qt.AlignCenter)
#         sidebar_layout.addWidget(title_label)

#         theme_btn = QPushButton("Toggle Theme")
#         theme_btn.clicked.connect(self.toggle_theme)
#         sidebar_layout.addWidget(theme_btn)

#         scroll_area = QScrollArea()
#         scroll_area.setWidgetResizable(True)
#         scroll_widget = QWidget()
#         scroll_layout = QVBoxLayout(scroll_widget)

#         # Features: (text, module file, class, icon path)
#         features = [
#             ("Learning Management System", "lms_module", "LMSModule", "icons/lms.png"),
#             ("Library Management",         "library_module", "LibraryModule", "icons/library.png"),
#             ("Transport Management",       "transport_module", "TransportModule", "icons/bus.png"),
#             ("Hostel Management",          "hostel_module", "HostelModule", "icons/hostel.png"),
#             ("Inventory Management",       "inventory_module", "InventoryModule", "icons/inventory.png"),
#             ("HR Management",              "hr_module", "HRModule", "icons/hr.png"),
#             ("Biometrics/RFID",            "biometric_module", "BiometricModule", "icons/biometric.png"),
#         ]

#         for text, module_name, class_name, icon_path in features:
#             btn = QPushButton(f"  {text}")
#             # Load icon or fallback
#             if os.path.exists(icon_path):
#                 btn.setIcon(QIcon(icon_path))
#             else:
#                 btn.setIcon(QIcon("icons/default.png"))
#             btn.setIconSize(QSize(24, 24))
#             btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#             btn.clicked.connect(lambda _, m=module_name, c=class_name, t=text: self.load_module(m, c, t))
#             scroll_layout.addWidget(btn)

#         scroll_layout.addStretch()
#         scroll_area.setWidget(scroll_widget)
#         sidebar_layout.addWidget(scroll_area)

#         sidebar_container = QWidget()
#         sidebar_container.setLayout(sidebar_layout)
#         sidebar_container.setFixedWidth(350)  # Increased width
#         main_layout.addWidget(sidebar_container, 1)

#         # Content area placeholder
#         self.content_area = QWidget()
#         self.content_area.setMinimumWidth(600)
#         main_layout.addWidget(self.content_area, 3)

#         self.is_dark_theme = False

#     def toggle_theme(self):
#         if self.is_dark_theme:
#             self.setStyleSheet("")
#             self.is_dark_theme = False
#         else:
#             self.setStyleSheet("""
#                 QMainWindow { background-color: #2C3E50; }
#                 QPushButton { background-color: #34495E; color: white; padding: 8px; border-radius: 4px; }
#                 QPushButton:hover { background-color: #1ABC9C; }
#                 QLabel { color: white; }
#                 QScrollArea { background-color: transparent; }
#             """)
#             self.is_dark_theme = True

#     def load_module(self, module_name, class_name, display_name):
#         try:
#             module = __import__(module_name)
#             module_class = getattr(module, class_name)
#             widget = module_class()
#         except Exception as e:
#             tb = traceback.format_exc()
#             QMessageBox.critical(self, "Load Error",
#                                  f"Failed to load {class_name} from {module_name}.\n\n{e}\n\n{tb}")
#             return

#         # Create container with title + module
#         container = QWidget()
#         v_layout = QVBoxLayout(container)

#         title_label = QLabel(display_name)
#         title_label.setFont(QFont("Segoe UI", 22, QFont.Bold))
#         title_label.setAlignment(Qt.AlignCenter)
#         v_layout.addWidget(title_label)

#         v_layout.addWidget(widget)

#         layout = self.centralWidget().layout()
#         layout.removeWidget(self.content_area)
#         self.content_area.deleteLater()
#         self.content_area = container
#         layout.addWidget(self.content_area, 3)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = Dashboard()
#     window.show()
#     sys.exit(app.exec_())











# # import sys, os, traceback
# # from PyQt5.QtWidgets import (
# #     QApplication, QMainWindow, QWidget, QHBoxLayout,
# #     QVBoxLayout, QPushButton, QLabel, QSizePolicy, QScrollArea, QMessageBox
# # )
# # from PyQt5.QtGui import QFont, QIcon
# # from PyQt5.QtCore import QSize, Qt


# # class Dashboard(QMainWindow):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("School Management System")
# #         self.setMinimumSize(1000, 600)

# #         central_widget = QWidget()
# #         main_layout = QHBoxLayout(central_widget)
# #         self.setCentralWidget(central_widget)

# #         # Sidebar
# #         sidebar_layout = QVBoxLayout()
# #         sidebar_layout.setContentsMargins(10, 10, 10, 10)
# #         sidebar_layout.setSpacing(10)

# #         title_label = QLabel("📋 Dashboard Menu")
# #         title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
# #         title_label.setAlignment(Qt.AlignCenter)
# #         sidebar_layout.addWidget(title_label)

# #         theme_btn = QPushButton("Toggle Theme")
# #         theme_btn.clicked.connect(self.toggle_theme)
# #         sidebar_layout.addWidget(theme_btn)

# #         scroll_area = QScrollArea()
# #         scroll_area.setWidgetResizable(True)
# #         scroll_widget = QWidget()
# #         scroll_layout = QVBoxLayout(scroll_widget)

# #         # Explicit mapping: (button text, module file, class name, icon path)
# #         features = [
# #             ("Learning Management System", "lms_module", "LMSModule", "icons/lms.png"),
# #             ("Library Management",         "library_module", "LibraryModule", "icons/library.png"),
# #             ("Transport Management",       "transport_module", "TransportModule", "icons/bus.png"),
# #             ("Hostel Management",          "hostel_module", "HostelModule", "icons/hostel.png"),
# #             ("Inventory Management",       "inventory_module", "InventoryModule", "icons/inventory.png"),
# #             ("HR Management",              "hr_module", "HRModule", "icons/hr.png"),
# #             ("Biometrics/RFID",            "biometric_module", "BiometricModule", "icons/biometric.png"),
# #         ]

# #         for text, module_name, class_name, icon_path in features:
# #             btn = QPushButton(f"  {text}")
# #             # QIcon is safe if file is missing (will render empty), so no try/except needed.
# #             if os.path.exists(icon_path):
# #                 btn.setIcon(QIcon(icon_path))
# #             btn.setIconSize(QSize(24, 24))
# #             btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
# #             btn.clicked.connect(lambda _, m=module_name, c=class_name: self.load_module(m, c))
# #             scroll_layout.addWidget(btn)

# #         scroll_layout.addStretch()
# #         scroll_area.setWidget(scroll_widget)
# #         sidebar_layout.addWidget(scroll_area)

# #         sidebar_container = QWidget()
# #         sidebar_container.setLayout(sidebar_layout)
# #         sidebar_container.setFixedWidth(300)
# #         main_layout.addWidget(sidebar_container, 1)

# #         # Content area placeholder
# #         self.content_area = QWidget()
# #         self.content_area.setMinimumWidth(600)
# #         main_layout.addWidget(self.content_area, 3)

# #         self.is_dark_theme = False

# #     def toggle_theme(self):
# #         if self.is_dark_theme:
# #             self.setStyleSheet("")  # Light/default
# #             self.is_dark_theme = False
# #         else:
# #             self.setStyleSheet("""
# #                 QMainWindow { background-color: #2C3E50; }
# #                 QPushButton { background-color: #34495E; color: white; padding: 8px; border-radius: 4px; }
# #                 QPushButton:hover { background-color: #1ABC9C; }
# #                 QLabel { color: white; }
# #                 QScrollArea { background-color: transparent; }
# #             """)
# #             self.is_dark_theme = True

# #     def load_module(self, module_name, class_name):
# #         try:
# #             module = __import__(module_name)
# #             module_class = getattr(module, class_name)
# #             widget = module_class()
# #         except Exception as e:
# #             # Show a friendly error instead of crashing the whole app
# #             tb = traceback.format_exc()
# #             QMessageBox.critical(self, "Load Error",
# #                                  f"Failed to load {class_name} from {module_name}.\n\n{e}\n\n{tb}")
# #             return

# #         # Replace right-side content area
# #         layout = self.centralWidget().layout()
# #         layout.removeWidget(self.content_area)
# #         self.content_area.deleteLater()
# #         self.content_area = widget
# #         layout.addWidget(self.content_area, 3)


# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = Dashboard()
# #     window.show()
# #     sys.exit(app.exec_())






















# # # import sys
# # # from PyQt5.QtWidgets import (
# # #     QApplication, QMainWindow, QWidget, QHBoxLayout,
# # #     QVBoxLayout, QPushButton, QLabel, QSizePolicy, QScrollArea
# # # )
# # # from PyQt5.QtGui import QFont, QIcon
# # # from PyQt5.QtCore import QSize, Qt  # ✅ Fixed import

# # # class Dashboard(QMainWindow):
# # #     def __init__(self):
# # #         super().__init__()
# # #         self.setWindowTitle("School Management System")
# # #         self.setMinimumSize(1000, 600)

# # #         # Central widget and main layout
# # #         central_widget = QWidget()
# # #         main_layout = QHBoxLayout(central_widget)
# # #         self.setCentralWidget(central_widget)

# # #         # Sidebar layout
# # #         sidebar_layout = QVBoxLayout()
# # #         sidebar_layout.setContentsMargins(10, 10, 10, 10)
# # #         sidebar_layout.setSpacing(10)

# # #         title_label = QLabel("📋 Dashboard Menu")
# # #         title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
# # #         title_label.setAlignment(Qt.AlignCenter)
# # #         sidebar_layout.addWidget(title_label)

# # #         theme_btn = QPushButton("Toggle Theme")
# # #         theme_btn.clicked.connect(self.toggle_theme)
# # #         sidebar_layout.addWidget(theme_btn)

# # #         # Scroll area for menu buttons
# # #         scroll_area = QScrollArea()
# # #         scroll_area.setWidgetResizable(True)
# # #         scroll_widget = QWidget()
# # #         scroll_layout = QVBoxLayout(scroll_widget)

# # #         # ✅ Explicit icon mapping for safety
# # #         features = [
# # #             ("Learning Management System", "lms_module", "LMSModule", "icons/lms.png"),
# # #             ("Library Management", "library_module", "LibraryModule", "icons/library.png"),
# # #             ("Transport Management", "transport_module", "TransportModule", "icons/bus.png"),
# # #             ("Hostel Management", "hostel_module", "HostelModule", "icons/hostel.png"),
# # #             ("Inventory Management", "inventory_module", "InventoryModule", "icons/inventory.png"),
# # #             ("HR Management", "hr_module", "HRModule", "icons/hr.png"),
# # #             ("Biometrics/RFID", "biometric_module", "BiometricModule", "icons/biometric.png"),
# # #         ]

# # #         for text, module_name, class_name, icon_path in features:
# # #             btn = QPushButton(f"  {text}")
# # #             btn.setIcon(QIcon(icon_path))
# # #             btn.setIconSize(QSize(24, 24))
# # #             btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
# # #             btn.clicked.connect(lambda _, m=module_name, c=class_name: self.load_module(m, c))
# # #             scroll_layout.addWidget(btn)

# # #         scroll_layout.addStretch()
# # #         scroll_area.setWidget(scroll_widget)
# # #         sidebar_layout.addWidget(scroll_area)

# # #         # Add sidebar to main layout
# # #         sidebar_container = QWidget()
# # #         sidebar_container.setLayout(sidebar_layout)
# # #         sidebar_container.setFixedWidth(300)
# # #         main_layout.addWidget(sidebar_container, 1)

# # #         # Content area
# # #         self.content_area = QWidget()
# # #         self.content_area.setMinimumWidth(600)
# # #         main_layout.addWidget(self.content_area, 3)

# # #         self.is_dark_theme = False

# # #     def toggle_theme(self):
# # #         if self.is_dark_theme:
# # #             self.setStyleSheet("")  # Light theme
# # #             self.is_dark_theme = False
# # #         else:
# # #             # Dark theme
# # #             self.setStyleSheet("""
# # #                 QMainWindow { background-color: #2C3E50; }
# # #                 QPushButton { background-color: #34495E; color: white; padding: 8px; border-radius: 4px; }
# # #                 QPushButton:hover { background-color: #1ABC9C; }
# # #                 QLabel { color: white; }
# # #             """)
# # #             self.is_dark_theme = True

# # #     def load_module(self, module_name, class_name):
# # #         module = __import__(module_name)
# # #         module_class = getattr(module, class_name)
# # #         widget = module_class()

# # #         # ✅ Safer widget replacement
# # #         layout = self.centralWidget().layout()
# # #         layout.removeWidget(self.content_area)
# # #         self.content_area.deleteLater()
# # #         self.content_area = widget
# # #         layout.addWidget(self.content_area, 3)

# # # if __name__ == "__main__":
# # #     app = QApplication(sys.argv)
# # #     window = Dashboard()
# # #     window.show()
# # #     sys.exit(app.exec_())




















# # # # import sys
# # # # from PyQt5.QtWidgets import (
# # # #     QApplication, QMainWindow, QWidget, QHBoxLayout,
# # # #     QVBoxLayout, QPushButton, QLabel, QSizePolicy, QScrollArea
# # # # )
# # # # from PyQt5.QtGui import QFont, QIcon
# # # # from PyQt5.QtCore import QSize


# # # # class Dashboard(QMainWindow):
# # # #     def __init__(self):
# # # #         super().__init__()
# # # #         self.setWindowTitle("School Management System")
# # # #         self.setMinimumSize(1000, 600)

# # # #         # Central widget and main layout
# # # #         central_widget = QWidget()
# # # #         main_layout = QHBoxLayout(central_widget)
# # # #         self.setCentralWidget(central_widget)

# # # #         # Sidebar layout
# # # #         sidebar_layout = QVBoxLayout()
# # # #         sidebar_layout.setContentsMargins(10, 10, 10, 10)
# # # #         sidebar_layout.setSpacing(10)

# # # #         title_label = QLabel("📋 Dashboard Menu")
# # # #         title_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
# # # #         title_label.setAlignment(Qt.AlignCenter)
# # # #         sidebar_layout.addWidget(title_label)

# # # #         theme_btn = QPushButton("Toggle Theme")
# # # #         theme_btn.clicked.connect(self.toggle_theme)
# # # #         sidebar_layout.addWidget(theme_btn)

# # # #         # Scroll area for menu buttons
# # # #         scroll_area = QScrollArea()
# # # #         scroll_area.setWidgetResizable(True)
# # # #         scroll_widget = QWidget()
# # # #         scroll_layout = QVBoxLayout(scroll_widget)

# # # #         # Sidebar buttons
# # # #         features = [
# # # #             ("Learning Management System", "lms_module", "LMSModule"),
# # # #             ("Library Management", "library_module", "LibraryModule"),
# # # #             ("Transport Management", "transport_module", "TransportModule"),
# # # #             ("Hostel Management", "hostel_module", "HostelModule"),
# # # #             ("Inventory Management", "inventory_module", "InventoryModule"),
# # # #             ("HR Management", "hr_module", "HRModule"),
# # # #             ("Biometrics/RFID", "biometric_module", "BiometricModule"),
# # # #         ]

# # # #         for text, module_name, class_name in features:
# # # #             btn = QPushButton(f"  {text}")
# # # #             btn.setIcon(QIcon(f"icons/{module_name.split('_')[0]}.png"))
# # # #             btn.setIconSize(QSize(24, 24))
# # # #             btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
# # # #             btn.clicked.connect(lambda _, m=module_name, c=class_name: self.load_module(m, c))
# # # #             scroll_layout.addWidget(btn)

# # # #         scroll_layout.addStretch()
# # # #         scroll_area.setWidget(scroll_widget)
# # # #         sidebar_layout.addWidget(scroll_area)

# # # #         # Add sidebar to main layout
# # # #         sidebar_container = QWidget()
# # # #         sidebar_container.setLayout(sidebar_layout)
# # # #         sidebar_container.setFixedWidth(300)
# # # #         main_layout.addWidget(sidebar_container, 1)

# # # #         # Content area
# # # #         self.content_area = QWidget()
# # # #         self.content_area.setMinimumWidth(600)
# # # #         main_layout.addWidget(self.content_area, 3)

# # # #         self.is_dark_theme = False

# # # #     def toggle_theme(self):
# # # #         if self.is_dark_theme:
# # # #             self.setStyleSheet("")
# # # #             self.is_dark_theme = False
# # # #         else:
# # # #             self.setStyleSheet("""
# # # #                 QMainWindow { background-color: #2C3E50; }
# # # #                 QPushButton { background-color: #34495E; color: white; padding: 8px; border-radius: 4px; }
# # # #                 QPushButton:hover { background-color: #1ABC9C; }
# # # #                 QLabel { color: white; }
# # # #             """)
# # # #             self.is_dark_theme = True

# # # #     def load_module(self, module_name, class_name):
# # # #         module = __import__(module_name)
# # # #         module_class = getattr(module, class_name)
# # # #         widget = module_class()

# # # #         # Replace the right-side content area with the new widget
# # # #         self.centralWidget().layout().replaceWidget(self.content_area, widget)
# # # #         self.content_area.deleteLater()
# # # #         self.content_area = widget

# # # # if __name__ == "__main__":
# # # #     app = QApplication(sys.argv)
# # # #     window = Dashboard()
# # # #     window.show()
# # # #     sys.exit(app.exec_())

























# # # # # # main.py
# # # # # import sys
# # # # # from PyQt5.QtWidgets import (
# # # # #     QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
# # # # #     QLabel, QHBoxLayout
# # # # # )
# # # # # from PyQt5.QtGui import QFont, QIcon
# # # # # from PyQt5.QtCore import QSize, QPropertyAnimation, QRect
# # # # # import db

# # # # # class SchoolDashboard(QMainWindow):
# # # # #     def __init__(self):
# # # # #         super().__init__()
# # # # #         self.setWindowTitle("School Management System")
# # # # #         self.setGeometry(200, 100, 1000, 600)
# # # # #         self.light_theme()

# # # # #         db.setup_tables()

# # # # #         # Main widget and layout
# # # # #         main_widget = QWidget()
# # # # #         self.setCentralWidget(main_widget)
# # # # #         main_layout = QHBoxLayout()
# # # # #         main_widget.setLayout(main_layout)

# # # # #         # Sidebar
# # # # #         sidebar = QVBoxLayout()
# # # # #         sidebar.setSpacing(15)

# # # # #         title = QLabel("📚 Dashboard Menu")
# # # # #         title.setFont(QFont("Segoe UI", 16, QFont.Bold))
# # # # #         title.setStyleSheet("color: white; padding: 10px;")
# # # # #         sidebar.addWidget(title)

# # # # #         # Theme toggle button
# # # # #         theme_btn = QPushButton("Toggle Theme")
# # # # #         theme_btn.clicked.connect(self.toggle_theme)
# # # # #         sidebar.addWidget(theme_btn)

# # # # #         # Sidebar buttons
# # # # #         buttons = [
# # # # #             ("Learning Management System", "icons/lms.png", "lms_module", "LMSModule"),
# # # # #             ("Library Management", "icons/library.png", "library_module", "LibraryModule"),
# # # # #             ("Transport Management", "icons/bus.png", "transport_module", "TransportModule"),
# # # # #             ("Hostel Management", "icons/hostel.png", "hostel_module", "HostelModule"),
# # # # #             ("Inventory Management", "icons/inventory.png", "inventory_module", "InventoryModule"),
# # # # #             ("HR Management", "icons/hr.png", "hr_module", "HRModule"),
# # # # #             ("Biometrics/RFID", "icons/biometric.png", "biometric_module", "BiometricModule")
# # # # #         ]

# # # # #         self.windows = {}

# # # # #         for btn_text, icon_path, module_name, class_name in buttons:
# # # # #             btn = QPushButton(f"  {btn_text}")
# # # # #             btn.setIcon(QIcon(icon_path))
# # # # #             btn.setIconSize(QSize(24, 24))
# # # # #             btn.setFixedHeight(45)
# # # # #             btn.setStyleSheet(self.button_style)
# # # # #             btn.clicked.connect(lambda checked, m=module_name, c=class_name: self.load_module(m, c))
# # # # #             sidebar.addWidget(btn)

# # # # #         sidebar.addStretch()

# # # # #         # Sidebar widget
# # # # #         sidebar_widget = QWidget()
# # # # #         sidebar_widget.setLayout(sidebar)
# # # # #         sidebar_widget.setStyleSheet(self.sidebar_style)

# # # # #         # Main content area
# # # # #         self.content_area = QLabel("Select a feature from the menu")
# # # # #         self.content_area.setFont(QFont("Segoe UI", 14))
# # # # #         self.content_area.setStyleSheet("padding: 20px; background-color: white; border-radius: 8px;")
# # # # #         self.content_area.setMinimumWidth(600)

# # # # #         # Add to main layout
# # # # #         main_layout.addWidget(sidebar_widget, 1)
# # # # #         main_layout.addWidget(self.content_area, 3)

# # # # #     def load_module(self, module_name, class_name):
# # # # #         module = __import__(module_name)
# # # # #         module_class = getattr(module, class_name)
# # # # #         window = module_class()
# # # # #         window.show()
# # # # #         self.windows[class_name] = window  # Keep reference so window stays open

# # # # #     def toggle_theme(self):
# # # # #         if self.theme == "light":
# # # # #             self.dark_theme()
# # # # #         else:
# # # # #             self.light_theme()
# # # # #         self.repaint()

# # # # #     def light_theme(self):
# # # # #         self.theme = "light"
# # # # #         self.sidebar_style = """
# # # # #             background-color: qlineargradient(
# # # # #                 spread:pad, x1:0, y1:0, x2:1, y2:0,
# # # # #                 stop:0 #4CAF50, stop:1 #2E7D32
# # # # #             );
# # # # #             border-radius: 8px;
# # # # #         """
# # # # #         self.button_style = """
# # # # #             QPushButton {
# # # # #                 background-color: rgba(255, 255, 255, 0.2);
# # # # #                 color: white;
# # # # #                 font-size: 14px;
# # # # #                 border-radius: 6px;
# # # # #                 padding-left: 10px;
# # # # #                 text-align: left;
# # # # #             }
# # # # #             QPushButton:hover {
# # # # #                 background-color: rgba(255, 255, 255, 0.4);
# # # # #             }
# # # # #         """

# # # # #     def dark_theme(self):
# # # # #         self.theme = "dark"
# # # # #         self.sidebar_style = """
# # # # #             background-color: qlineargradient(
# # # # #                 spread:pad, x1:0, y1:0, x2:1, y2:0,
# # # # #                 stop:0 #1E1E1E, stop:1 #333333
# # # # #             );
# # # # #             border-radius: 8px;
# # # # #         """
# # # # #         self.button_style = """
# # # # #             QPushButton {
# # # # #                 background-color: rgba(255, 255, 255, 0.1);
# # # # #                 color: white;
# # # # #                 font-size: 14px;
# # # # #                 border-radius: 6px;
# # # # #                 padding-left: 10px;
# # # # #                 text-align: left;
# # # # #             }
# # # # #             QPushButton:hover {
# # # # #                 background-color: rgba(255, 255, 255, 0.3);
# # # # #             }
# # # # #         """

# # # # # if __name__ == "__main__":
# # # # #     app = QApplication(sys.argv)
# # # # #     window = SchoolDashboard()
# # # # #     window.show()
# # # # #     sys.exit(app.exec_())



























# # # # # # import sys
# # # # # # from PyQt5.QtWidgets import (
# # # # # #     QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
# # # # # # )
# # # # # # from PyQt5.QtGui import QFont, QIcon
# # # # # # from PyQt5.QtCore import QSize, QPropertyAnimation, QRect

# # # # # # class SchoolDashboard(QMainWindow):
# # # # # #    def show_feature(self, feature_name):
# # # # # #     if feature_name == "Learning Management System":
# # # # # #         from lms_module import LMSModule
# # # # # #         lms_screen = LMSModule()
# # # # # #         lms_screen.show()
# # # # # #         self.lms_window = lms_screen
# # # # # #     else:
# # # # # #         self.content_area.setText(f"You selected: {feature_name}")
# # # # # #         anim = QPropertyAnimation(self.content_area, b"geometry")
# # # # # #         anim.setDuration(300)
# # # # # #         anim.setStartValue(QRect(self.content_area.x() - 50, self.content_area.y(),
# # # # # #                                  self.content_area.width(), self.content_area.height()))
# # # # # #         anim.setEndValue(QRect(self.content_area.x(), self.content_area.y(),
# # # # # #                                self.content_area.width(), self.content_area.height()))
# # # # # #         anim.start()
# # # # # #         self.anim = anim

        
# # # # # #         # Main widget and layout
# # # # # #         main_widget = QWidget()
# # # # # #         self.setCentralWidget(main_widget)
# # # # # #         main_layout = QHBoxLayout()
# # # # # #         main_widget.setLayout(main_layout)

# # # # # #         # Sidebar menu
# # # # # #         sidebar = QVBoxLayout()
# # # # # #         sidebar.setSpacing(15)

# # # # # #         title = QLabel("📚 Dashboard Menu")
# # # # # #         title.setFont(QFont("Segoe UI", 16, QFont.Bold))
# # # # # #         title.setStyleSheet("color: white; padding: 10px;")
# # # # # #         sidebar.addWidget(title)

# # # # # #         # Theme toggle button
# # # # # #         theme_btn = QPushButton("Toggle Theme")
# # # # # #         theme_btn.clicked.connect(self.toggle_theme)
# # # # # #         sidebar.addWidget(theme_btn)

# # # # # #         # Sidebar buttons
# # # # # #         buttons = [
# # # # # #             ("Learning Management System", "icons/lms.png"),
# # # # # #             ("Library Management", "icons/library.png"),
# # # # # #             ("Transport Management", "icons/bus.png"),
# # # # # #             ("Hostel Management", "icons/hostel.png"),
# # # # # #             ("Inventory Management", "icons/inventory.png"),
# # # # # #             ("HR Management", "icons/hr.png"),
# # # # # #             ("Biometrics/RFID", "icons/biometric.png")
# # # # # #         ]

# # # # # #         for btn_text, icon_path in buttons:
# # # # # #             btn = QPushButton(f"  {btn_text}")
# # # # # #             btn.setIcon(QIcon(icon_path))
# # # # # #             btn.setIconSize(QSize(24, 24))
# # # # # #             btn.setFixedHeight(45)
# # # # # #             btn.setStyleSheet(self.button_style)
# # # # # #             btn.clicked.connect(lambda checked, b=btn_text: self.show_feature(b))
# # # # # #             sidebar.addWidget(btn)

# # # # # #         sidebar.addStretch()

# # # # # #         # Sidebar widget
# # # # # #         sidebar_widget = QWidget()
# # # # # #         sidebar_widget.setLayout(sidebar)
# # # # # #         sidebar_widget.setStyleSheet(self.sidebar_style)

# # # # # #         # Main content area
# # # # # #         self.content_area = QLabel("Select a feature from the menu")
# # # # # #         self.content_area.setFont(QFont("Segoe UI", 14))
# # # # # #         self.content_area.setStyleSheet("padding: 20px; background-color: white; border-radius: 8px;")
# # # # # #         self.content_area.setMinimumWidth(600)

# # # # # #         # Add layouts
# # # # # #         main_layout.addWidget(sidebar_widget, 1)
# # # # # #         main_layout.addWidget(self.content_area, 3)

# # # # # #     def show_feature(self, feature_name):
# # # # # #         self.content_area.setText(f"You selected: {feature_name}")
# # # # # #         anim = QPropertyAnimation(self.content_area, b"geometry")
# # # # # #         anim.setDuration(300)
# # # # # #         anim.setStartValue(QRect(self.content_area.x() - 50, self.content_area.y(),
# # # # # #                                  self.content_area.width(), self.content_area.height()))
# # # # # #         anim.setEndValue(QRect(self.content_area.x(), self.content_area.y(),
# # # # # #                                self.content_area.width(), self.content_area.height()))
# # # # # #         anim.start()
# # # # # #         self.anim = anim  # Keep reference so animation works

# # # # # #     def toggle_theme(self):
# # # # # #         if self.theme == "light":
# # # # # #             self.dark_theme()
# # # # # #         else:
# # # # # #             self.light_theme()
# # # # # #         self.repaint()

# # # # # #     def light_theme(self):
# # # # # #         self.theme = "light"
# # # # # #         self.sidebar_style = """
# # # # # #             background-color: qlineargradient(
# # # # # #                 spread:pad, x1:0, y1:0, x2:1, y2:0, 
# # # # # #                 stop:0 #4CAF50, stop:1 #2E7D32
# # # # # #             );
# # # # # #             border-radius: 8px;
# # # # # #         """
# # # # # #         self.button_style = """
# # # # # #             QPushButton {
# # # # # #                 background-color: rgba(255, 255, 255, 0.2);
# # # # # #                 color: white;
# # # # # #                 font-size: 14px;
# # # # # #                 border-radius: 6px;
# # # # # #                 padding-left: 10px;
# # # # # #                 text-align: left;
# # # # # #             }
# # # # # #             QPushButton:hover {
# # # # # #                 background-color: rgba(255, 255, 255, 0.4);
# # # # # #             }
# # # # # #         """

# # # # # #     def dark_theme(self):
# # # # # #         self.theme = "dark"
# # # # # #         self.sidebar_style = """
# # # # # #             background-color: qlineargradient(
# # # # # #                 spread:pad, x1:0, y1:0, x2:1, y2:0, 
# # # # # #                 stop:0 #1E1E1E, stop:1 #333333
# # # # # #             );
# # # # # #             border-radius: 8px;
# # # # # #         """
# # # # # #         self.button_style = """
# # # # # #             QPushButton {
# # # # # #                 background-color: rgba(255, 255, 255, 0.1);
# # # # # #                 color: white;
# # # # # #                 font-size: 14px;
# # # # # #                 border-radius: 6px;
# # # # # #                 padding-left: 10px;
# # # # # #                 text-align: left;
# # # # # #             }
# # # # # #             QPushButton:hover {
# # # # # #                 background-color: rgba(255, 255, 255, 0.3);
# # # # # #             }
# # # # # #         """

# # # # # # if __name__ == "__main__":
# # # # # #     app = QApplication(sys.argv)
# # # # # #     window = SchoolDashboard()
# # # # # #     window.show()
# # # # # #     sys.exit(app.exec_())

































# # # # # # # import sys
# # # # # # # from PyQt5.QtWidgets import (
# # # # # # #     QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
# # # # # # # )
# # # # # # # from PyQt5.QtGui import QFont, QIcon
# # # # # # # from PyQt5.QtCore import QSize, QPropertyAnimation, QRect

# # # # # # # class SchoolDashboard(QMainWindow):
# # # # # # #     def __init__(self):
# # # # # # #         super().__init__()
# # # # # # #         self.setWindowTitle("School Management System")
# # # # # # #         self.setGeometry(200, 100, 1000, 600)
# # # # # # #         self.light_theme()
        
# # # # # # #         # Main widget and layout
# # # # # # #         main_widget = QWidget()
# # # # # # #         self.setCentralWidget(main_widget)
# # # # # # #         main_layout = QHBoxLayout()
# # # # # # #         main_widget.setLayout(main_layout)

# # # # # # #         # Sidebar menu
# # # # # # #         sidebar = QVBoxLayout()
# # # # # # #         sidebar.setSpacing(15)

# # # # # # #         title = QLabel("📚 Dashboard Menu")
# # # # # # #         title.setFont(QFont("Segoe UI", 16, QFont.Bold))
# # # # # # #         title.setStyleSheet("color: white; padding: 10px;")
# # # # # # #         sidebar.addWidget(title)

# # # # # # #         # Theme toggle button
# # # # # # #         theme_btn = QPushButton("Toggle Theme")
# # # # # # #         theme_btn.clicked.connect(self.toggle_theme)
# # # # # # #         sidebar.addWidget(theme_btn)

# # # # # # #         buttons = [
# # # # # # #             ("Learning Management System", "icons/lms.png"),
# # # # # # #             ("Library Management", "icons/library.png"),
# # # # # # #             ("Transport Management", "icons/bus.png"),
# # # # # # #             ("Hostel Management", "icons/hostel.png"),
# # # # # # #             ("Inventory Management", "icons/inventory.png"),
# # # # # # #             ("HR Management", "icons/hr.png"),
# # # # # # #             ("Biometrics/RFID", "icons/biometric.png")
# # # # # # #         ]

# # # # # # #         for btn_text, icon_path in buttons:
# # # # # # #             btn = QPushButton(f"  {btn_text}")
# # # # # # #             btn.setIcon(QIcon(icon_path))
# # # # # # #             btn.setIconSize(QSize(24, 24))
# # # # # # #             btn.setFixedHeight(45)
# # # # # # #             btn.setStyleSheet(self.button_style)
# # # # # # #             btn.clicked.connect(lambda checked, b=btn_text: self.show_feature(b))
# # # # # # #             sidebar.addWidget(btn)

# # # # # # #         sidebar.addStretch()

# # # # # # #         # Sidebar widget
# # # # # # #         sidebar_widget = QWidget()
# # # # # # #         sidebar_widget.setLayout(sidebar)
# # # # # # #         sidebar_widget.setStyleSheet(self.sidebar_style)

# # # # # # #         # Main content area
# # # # # # #         self.content_area = QLabel("Select a feature from the menu")
# # # # # # #         self.content_area.setFont(QFont("Segoe UI", 14))
# # # # # # #         self.content_area.setStyleSheet("padding: 20px; background-color: white; border-radius: 8px;")
# # # # # # #         self.content_area.setMinimumWidth(600)

# # # # # # #         # Add layouts
# # # # # # #         main_layout.addWidget(sidebar_widget, 1)
# # # # # # #         main_layout.addWidget(self.content_area, 3)

# # # # # # #     def show_feature(self, feature_name):
# # # # # # #         self.content_area.setText(f"You selected: {feature_name}")
# # # # # # #         anim = QPropertyAnimation(self.content_area, b"geometry")
# # # # # # #         anim.setDuration(300)
# # # # # # #         anim.setStartValue(QRect(self.content_area.x() - 50, self.content_area.y(), self.content_area.width(), self.content_area.height()))
# # # # # # #         anim.setEndValue(QRect(self.content_area.x(), self.content_area.y(), self.content_area.width(), self.content_area.height()))
# # # # # # #         anim.start()
# # # # # # #         self.anim = anim

# # # # # # #     def toggle_theme(self):
# # # # # # #         if self.theme == "light":
# # # # # # #             self.dark_theme()
# # # # # # #         else:
# # # # # # #             self.light_theme()
# # # # # # #         self.repaint()

# # # # # # #     def light_theme(self):
# # # # # # #         self.theme = "light"
# # # # # # #         self.sidebar_style = """
# # # # # # #             background-color: qlineargradient(
# # # # # # #                 spread:pad, x1:0, y1:0, x2:1, y2:0, 
# # # # # # #                 stop:0 #4CAF50, stop:1 #2E7D32
# # # # # # #             );
# # # # # # #             border-radius: 8px;
# # # # # # #         """
# # # # # # #         self.button_style = """
# # # # # # #             QPushButton {
# # # # # # #                 background-color: rgba(255, 255, 255, 0.2);
# # # # # # #                 color: white;
# # # # # # #                 font-size: 14px;
# # # # # # #                 border-radius: 6px;
# # # # # # #                 padding-left: 10px;
# # # # # # #                 text-align: left;
# # # # # # #             }
# # # # # # #             QPushButton:hover {
# # # # # # #                 background-color: rgba(255, 255, 255, 0.4);
# # # # # # #             }
# # # # # # #         """

# # # # # # #     def dark_theme(self):
# # # # # # #         self.theme = "dark"
# # # # # # #         self.sidebar_style = """
# # # # # # #             background-color: qlineargradient(
# # # # # # #                 spread:pad, x1:0, y1:0, x2:1, y2:0, 
# # # # # # #                 stop:0 #1E1E1E, stop:1 #333333
# # # # # # #             );
# # # # # # #             border-radius: 8px;
# # # # # # #         """
# # # # # # #         self.button_style = """
# # # # # # #             QPushButton {
# # # # # # #                 background-color: rgba(255, 255, 255, 0.1);
# # # # # # #                 color: white;
# # # # # # #                 font-size: 14px;
# # # # # # #                 border-radius: 6px;
# # # # # # #                 padding-left: 10px;
# # # # # # #                 text-align: left;
# # # # # # #             }
# # # # # # #             QPushButton:hover {
# # # # # # #                 background-color: rgba(255, 255, 255, 0.3);
# # # # # # #             }
# # # # # # #         """

# # # # # # # if __name__ == "__main__":
# # # # # # #     app = QApplication(sys.argv)
# # # # # # #     window = SchoolDashboard()
# # # # # # #     window.show()
# # # # # # #     sys.exit(app.exec_())
