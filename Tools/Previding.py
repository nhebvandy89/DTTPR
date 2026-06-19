import sys
import os
import tempfile
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from datetime import datetime, timedelta
import json
import qrcode
from PIL import Image
import io
import random

class DSMPOSSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DSM-Shop Electronics - POS System")
        self.setGeometry(100, 100, 1400, 800)
        
        # ទិន្នន័យទំនិញក្នុងរទេះ
        self.cart_items = []
        self.total_amount = 0.0
        
        # ទិន្នន័យប្រតិបត្តិការ
        self.transactions = []
        self.quick_order_items = []  # បញ្ជីទំនិញសម្រាប់បញ្ជាទិញរហ័ស
        
        # ផ្ទាំងរូបភាពបណ្តោះអាសន្ន
        self.temp_image_files = []
        
        # បង្កើតទម្រង់ផ្ទាំងពណ៌
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # បង្កើតទំព័រដំបូង (ទំព័រដើម)
        self.main_page = self.create_main_page()
        self.stacked_widget.addWidget(self.main_page)
        
        # បង្កើតទំព័របន្ថែមទំនិញ
        self.add_product_page = self.create_add_product_page()
        self.stacked_widget.addWidget(self.add_product_page)
        
        # បង្កើតទំព័រផ្សេងៗទៀត
        self.dashboard_page = self.create_dashboard_page()
        self.stacked_widget.addWidget(self.dashboard_page)
        
        self.stock_page = self.create_stock_page()
        self.reports_page = self.create_reports_page()
        self.customers_page = self.create_customers_page()
        self.suppliers_page = self.create_suppliers_page()
        self.users_page = self.create_users_page()
        self.settings_page = self.create_settings_page()
        
        self.stacked_widget.addWidget(self.stock_page)
        self.stacked_widget.addWidget(self.reports_page)
        self.stacked_widget.addWidget(self.customers_page)
        self.stacked_widget.addWidget(self.suppliers_page)
        self.stacked_widget.addWidget(self.users_page)
        self.stacked_widget.addWidget(self.settings_page)
        
        # អនុវត្តរចនាបទ
        self.apply_style()
        
        # ផ្ទុកទិន្នន័យឧទាហរណ៍
        self.load_sample_data()
        
    def load_sample_data(self):
        # បង្កើតទិន្នន័យឧទាហរណ៍សម្រាប់ផ្ទាំងគ្រប់គ្រង
        today = datetime.now()
        
        # ប្រតិបត្តិការថ្ងៃនេះ
        for i in range(5):
            transaction_time = today.replace(hour=random.randint(9, 17), minute=random.randint(0, 59))
            self.transactions.append({
                'id': 1000 + i,
                'customer': f'អតិថិជន {i+1}',
                'total': round(random.uniform(50, 500), 2),
                'payment_method': random.choice(['សាច់ប្រាក់', 'កាត', 'QR Code']),
                'date': transaction_time,
                'status': 'ជោគជ័យ'
            })
        
        # បញ្ជីទំនិញសម្រាប់បញ្ជាទិញរហ័ស
        self.quick_order_items = [
            {'id': 1, 'name': 'Samsung TV 55"', 'price': 450.00, 'image': None},
            {'id': 2, 'name': 'iPhone 13 Pro', 'price': 999.00, 'image': None},
            {'id': 3, 'name': 'HP Laptop', 'price': 850.00, 'image': None},
            {'id': 4, 'name': 'Coca Cola Can', 'price': 0.75, 'image': None},
            {'id': 5, 'name': 'Lays Chips', 'price': 1.50, 'image': None},
            {'id': 6, 'name': 'Logitech Mouse', 'price': 29.99, 'image': None},
        ]
        
    def apply_style(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                border-radius: 4px;
                padding: 10px;
                cursor: pointer;
            }
            QLabel {
                color: #2c3e50;
            }
            QLineEdit, QTextEdit, QSpinBox, QComboBox {
                padding: 8px;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
                min-height: 35px;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QListWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                font-size: 14px;
            }
            QGroupBox {
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                font-weight: bold;
                color: #2c3e50;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
    def create_main_page(self):
        main_page = QWidget()
        main_layout = QHBoxLayout(main_page)
        
        # ផ្នែកខាងឆ្វេង - ម៉ឺនុយ
        left_sidebar = self.create_left_sidebar()
        main_layout.addWidget(left_sidebar, 1)
        
        # ផ្នែកកណ្តាល - បញ្ជីផលិតផល
        center_content = self.create_center_content()
        main_layout.addWidget(center_content, 3)
        
        # ផ្នែកខាងស្តាំ - ទំនិញក្នុងរទេះ
        right_sidebar = self.create_right_sidebar()
        main_layout.addWidget(right_sidebar, 2)
        
        return main_page
        
    def create_left_sidebar(self):
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet("""
            QWidget#sidebar {
                background-color: #2c3e50;
            }
            QLabel {
                color: white;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton {
                background-color: transparent;
                color: white;
                text-align: left;
                padding: 15px 20px;
                font-size: 14px;
                border: none;
                border-radius: 0;
                border-left: 4px solid transparent;
            }
            QPushButton:hover {
                background-color: #34495e;
                border-left: 4px solid #3498db;
            }
            QPushButton#active {
                background-color: #1a252f;
                border-left: 4px solid #3498db;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # ចំណងជើងហាង
        title = QLabel("DSM-Shop Electronics")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                background-color: #1a252f;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 25px 10px;
                border-bottom: 2px solid #34495e;
            }
        """)
        layout.addWidget(title)
        
        # ស្លាក POS System
        pos_label = QLabel("POS System")
        pos_label.setAlignment(Qt.AlignCenter)
        pos_label.setStyleSheet("""
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                padding: 15px;
                background-color: #34495e;
                border-bottom: 1px solid #2c3e50;
            }
        """)
        layout.addWidget(pos_label)
        
        # ប៊ូតុងម៉ឺនុយ
        menu_items = [
            ("📊 ផ្ទាំងគ្រប់គ្រង", "dashboard"),
            ("🛒 ការលក់", "pos"),
            ("📦 ស្តុកទំនិញ", "stock"),
            ("📈 របាយការណ៍", "reports"),
            ("👥 អតិថិជន", "customers"),
            ("🏢 អ្នកផ្គត់ផ្គង់", "suppliers"),
            ("👤 អ្នកប្រើប្រាស់", "users"),
            ("⚙️ ការកំណត់", "settings")
        ]
        
        self.menu_buttons = {}
        
        for text, page_id in menu_items:
            btn = QPushButton(text)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("page_id", page_id)
            if page_id == "pos":
                btn.setObjectName("active")
            btn.clicked.connect(self.on_menu_clicked)
            layout.addWidget(btn)
            self.menu_buttons[page_id] = btn
            
        # ប៊ូតុងបន្ថែមទំនិញ
        add_product_btn = QPushButton("➕ បន្ថែមទំនិញ")
        add_product_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                margin: 20px;
                padding: 12px;
                border-radius: 4px;
                border-left: 4px solid #2980b9;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        add_product_btn.setCursor(Qt.PointingHandCursor)
        add_product_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(add_product_btn)
        
        # ប៊ូតុងបញ្ជាទិញរហ័ស
        quick_order_btn = QPushButton("⚡ បញ្ជាទិញរហ័ស")
        quick_order_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                font-weight: bold;
                margin: 0 20px 20px 20px;
                padding: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #d68910;
            }
        """)
        quick_order_btn.setCursor(Qt.PointingHandCursor)
        quick_order_btn.clicked.connect(self.show_quick_order_dialog)
        layout.addWidget(quick_order_btn)
        
        # បន្ថែមទំហំដែលអាចបត់បែនបាន
        layout.addStretch(1)
        
        # ប៊ូតុងចាក់ចេញ
        logout_btn = QPushButton("🚪 ចាក់ចេញ")
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-weight: bold;
                margin: 20px;
                padding: 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        return sidebar
        
    def on_menu_clicked(self):
        sender = self.sender()
        page_id = sender.property("page_id")
        
        # កំណត់ប៊ូតុងសកម្ម
        for btn in self.menu_buttons.values():
            btn.setObjectName("")
        sender.setObjectName("active")
        
        # ប្តូរទំព័រ
        page_map = {
            "dashboard": 2,
            "pos": 0,
            "stock": 3,
            "reports": 4,
            "customers": 5,
            "suppliers": 6,
            "users": 7,
            "settings": 8
        }
        
        self.stacked_widget.setCurrentIndex(page_map[page_id])
        
    def logout(self):
        reply = QMessageBox.question(self, 'ផ្ទៀងផ្ទាត់', 
                                     'តើអ្នកពិតជាចង់ចាកចេញមែនទេ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # សម្អាតឯកសារបណ្តោះអាសន្ន
            for temp_file in self.temp_image_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass
            
            QMessageBox.information(self, "ចាកចេញ", "អ្នកបានចាកចេញដោយជោគជ័យ!")
            # self.close()
        
    def create_center_content(self):
        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # ក្បាលទំព័រ
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        date_label = QLabel(datetime.now().strftime("%d %B, %Y"))
        date_label.setStyleSheet("font-size: 16px; color: #7f8c8d; font-weight: bold;")
        
        time_label = QLabel(datetime.now().strftime("%I:%M %p"))
        time_label.setStyleSheet("font-size: 16px; color: #2c3e50; font-weight: bold;")
        
        header_layout.addWidget(date_label)
        header_layout.addStretch()
        header_layout.addWidget(time_label)
        
        layout.addWidget(header)
        
        # បន្ទាត់ដែលបំបែក
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setStyleSheet("color: #ddd; margin: 15px 0;")
        layout.addWidget(line)
        
        # របារស្វែងរក
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        
        search_label = QLabel("Scan Barcode / Search Name (F1)")
        search_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("សូមបញ្ចូលឈ្មោះផលិតផល ឬលេខបាកូដ...")
        self.search_input.setMinimumHeight(40)
        self.search_input.returnPressed.connect(self.search_products)
        
        search_btn = QPushButton("🔍 ស្វែងរក")
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 12px 24px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        search_btn.clicked.connect(self.search_products)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input, 1)
        search_layout.addWidget(search_btn)
        
        layout.addWidget(search_container)
        
        # ប៊ូតុងតម្រៀប
        sort_widget = QWidget()
        sort_layout = QHBoxLayout(sort_widget)
        
        sort_label = QLabel("តម្រៀបតាម:")
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["ឈ្មោះ (ក-អ)", "ឈ្មោះ (អ-ក)", "តម្លៃ (ទាប→ខ្ពស់)", "តម្លៃ (ខ្ពស់→ទាប)", "ស្តុក (ច្រើន→តិច)", "ស្តុក (តិច→ច្រើន)"])
        self.sort_combo.currentTextChanged.connect(self.sort_products)
        
        sort_layout.addWidget(sort_label)
        sort_layout.addWidget(self.sort_combo)
        sort_layout.addStretch()
        
        layout.addWidget(sort_widget)
        
        # ប៊ូតុងបញ្ជាទិញច្រើន
        multi_select_widget = QWidget()
        multi_select_layout = QHBoxLayout(multi_select_widget)
        
        self.multi_select_checkbox = QCheckBox("✅ ជ្រើសរើសច្រើន")
        self.multi_select_checkbox.stateChanged.connect(self.toggle_multi_select_mode)
        
        self.add_selected_btn = QPushButton("➕ បញ្ចូលដោយជ្រើសរើស")
        self.add_selected_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.add_selected_btn.clicked.connect(self.add_selected_to_cart)
        self.add_selected_btn.setVisible(False)
        
        multi_select_layout.addWidget(self.multi_select_checkbox)
        multi_select_layout.addWidget(self.add_selected_btn)
        multi_select_layout.addStretch()
        
        layout.addWidget(multi_select_widget)
        
        # បណ្តាញផលិតផល
        self.products_scroll = QScrollArea()
        self.products_scroll.setWidgetResizable(True)
        self.products_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.products_widget = QWidget()
        self.products_grid = QGridLayout(self.products_widget)
        self.products_grid.setSpacing(15)
        
        # បញ្ជីផលិតផល
        self.products = [
            {
                "id": 1,
                "name": "Samsung TV 55\"",
                "price": 450.00,
                "discount": 50.00,
                "discount_percent": 10,
                "final_price": 400.00,
                "info": "Smart TV 4K",
                "stock": 15,
                "category": "អេឡិចត្រូនិញ",
                "barcode": "8801234567890",
                "image": None,
                "image_path": None,
                "has_discount": True
            },
            {
                "id": 2,
                "name": "Coca Cola Can",
                "price": 0.75,
                "discount": 0.10,
                "discount_percent": 13,
                "final_price": 0.65,
                "info": "330ml",
                "stock": 94,
                "category": "ភេសជ្ជៈ",
                "barcode": "4901234567890",
                "image": None,
                "image_path": None,
                "has_discount": True
            },
            {
                "id": 3,
                "name": "Lays Chips",
                "price": 1.50,
                "discount": 0.00,
                "discount_percent": 0,
                "final_price": 1.50,
                "info": "Original Flavor",
                "stock": 30,
                "category": "អាហារសម្រន់",
                "barcode": "2840012345678",
                "image": None,
                "image_path": None,
                "has_discount": False
            },
            {
                "id": 4,
                "name": "iPhone 13 Pro",
                "price": 999.00,
                "discount": 100.00,
                "discount_percent": 10,
                "final_price": 899.00,
                "info": "128GB",
                "stock": 8,
                "category": "ទូរស័ព្ទ",
                "barcode": "8851234567890",
                "image": None,
                "image_path": None,
                "has_discount": True
            },
            {
                "id": 5,
                "name": "HP Laptop",
                "price": 850.00,
                "discount": 75.00,
                "discount_percent": 9,
                "final_price": 775.00,
                "info": "Core i7, 16GB RAM",
                "stock": 12,
                "category": "កុំព្យូទ័រ",
                "barcode": "8861234567890",
                "image": None,
                "image_path": None,
                "has_discount": True
            },
            {
                "id": 6,
                "name": "Logitech Mouse",
                "price": 29.99,
                "discount": 5.00,
                "discount_percent": 17,
                "final_price": 24.99,
                "info": "Wireless",
                "stock": 45,
                "category": "គ្រឿងបន្ថែម",
                "barcode": "097855019831",
                "image": None,
                "image_path": None,
                "has_discount": True
            },
            {
                "id": 7,
                "name": "Sony Headphones",
                "price": 199.00,
                "discount": 0.00,
                "discount_percent": 0,
                "final_price": 199.00,
                "info": "Noise Cancelling",
                "stock": 8,
                "category": "អេឡិចត្រូនិញ",
                "barcode": "4905524830192",
                "image": None,
                "image_path": None,
                "has_discount": False
            },
            {
                "id": 8,
                "name": "Samsung Refrigerator",
                "price": 1200.00,
                "discount": 150.00,
                "discount_percent": 13,
                "final_price": 1050.00,
                "info": "Double Door",
                "stock": 5,
                "category": "អេឡិចត្រូនិញ",
                "barcode": "8801234567891",
                "image": None,
                "image_path": None,
                "has_discount": True
            }
        ]
        
        self.selected_products = []  # ទំនិញដែលបានជ្រើសរើសសម្រាប់ការបញ្ជាទិញច្រើន
        
        self.display_products()
        
        self.products_grid.setRowStretch(10, 1)
        self.products_scroll.setWidget(self.products_widget)
        layout.addWidget(self.products_scroll, 1)
        
        return content
        
    def toggle_multi_select_mode(self, state):
        is_multi_select = state == Qt.Checked
        self.add_selected_btn.setVisible(is_multi_select)
        
        # បញ្ជាក់ទៅកាតផលិតផលថាត្រូវបង្ហាញ checkbox ឬមិន
        for i in range(self.products_grid.count()):
            widget = self.products_grid.itemAt(i).widget()
            if widget and hasattr(widget, 'show_checkbox'):
                widget.show_checkbox(is_multi_select)
        
    def add_selected_to_cart(self):
        selected_items = []
        for i in range(self.products_grid.count()):
            widget = self.products_grid.itemAt(i).widget()
            if widget and hasattr(widget, 'is_checked'):
                if widget.is_checked():
                    product = widget.product_data
                    selected_items.append(product)
        
        if not selected_items:
            QMessageBox.warning(self, "ការព្រមាន", "សូមជ្រើសរើសទំនិញយ៉ាងហោចណាស់មួយ!")
            return
        
        # បង្កើតទម្រង់បញ្ជូលបរិមាណសម្រាប់ទំនិញទាំងអស់
        dialog = QDialog(self)
        dialog.setWindowTitle("បញ្ចូលបរិមាណទំនិញ")
        dialog.setFixedSize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        self.quantity_inputs = {}
        
        for product in selected_items:
            product_widget = QWidget()
            product_layout = QHBoxLayout(product_widget)
            
            name_label = QLabel(f"{product['name']}")
            name_label.setStyleSheet("font-weight: bold;")
            
            price_label = QLabel(f"តម្លៃ: ${product['final_price']:.2f}")
            price_label.setStyleSheet("color: #27ae60;")
            
            quantity_spin = QSpinBox()
            quantity_spin.setMinimum(1)
            quantity_spin.setMaximum(min(product['stock'], 100))
            quantity_spin.setValue(1)
            
            product_layout.addWidget(name_label, 1)
            product_layout.addWidget(price_label)
            product_layout.addWidget(QLabel("បរិមាណ:"))
            product_layout.addWidget(quantity_spin)
            
            self.quantity_inputs[product['id']] = quantity_spin
            
            scroll_layout.addWidget(product_widget)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)
        
        # ប៊ូតុង
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.confirm_multiple_add_to_cart(selected_items, dialog))
        button_box.rejected.connect(dialog.reject)
        
        layout.addWidget(button_box)
        
        dialog.exec_()
        
    def confirm_multiple_add_to_cart(self, selected_items, dialog):
        added_count = 0
        
        for product in selected_items:
            quantity = self.quantity_inputs[product['id']].value()
            
            if quantity > 0 and quantity <= product['stock']:
                # បន្ថែមទំនិញទៅក្នុងរទេះ
                item_total = product['final_price'] * quantity
                
                # ពិនិត្យថាទំនិញមាននៅក្នុងរទេះរួចហើយឬនៅ
                found = False
                for item in self.cart_items:
                    if item['id'] == product['id']:
                        item['quantity'] += quantity
                        item['total'] += item_total
                        found = True
                        break
                
                if not found:
                    self.cart_items.append({
                        'id': product['id'],
                        'name': product['name'],
                        'price': product['final_price'],
                        'original_price': product['price'],
                        'discount': product.get('discount', 0),
                        'quantity': quantity,
                        'total': item_total,
                        'image_path': product.get('image_path'),
                        'has_discount': product.get('has_discount', False)
                    })
                
                # អាប់ដេតស្តុក
                product['stock'] -= quantity
                added_count += 1
        
        if added_count > 0:
            # អាប់ដេតការបង្ហាញ
            self.update_cart_display()
            self.display_products()
            
            QMessageBox.information(self, "ជោគជ័យ", f"បានបន្ថែម {added_count} ទំនិញទៅក្នុងរទេះ!")
            dialog.accept()
        else:
            QMessageBox.warning(self, "ការព្រមាន", "មិនមានទំនិញត្រូវបានបន្ថែមទេ!")
        
    def show_quick_order_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("⚡ បញ្ជាទិញរហ័ស")
        dialog.setFixedSize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # ចំណងជើង
        title_label = QLabel("ទំនិញដែលគេទិញញឹកញាប់")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # តារាងទំនិញ
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["ឈ្មោះ", "តម្លៃ", "បរិមាណ", ""])
        table.horizontalHeader().setStretchLastSection(True)
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        table.setRowCount(len(self.quick_order_items))
        
        self.quick_order_quantity_inputs = []
        
        for row, item in enumerate(self.quick_order_items):
            table.setItem(row, 0, QTableWidgetItem(item['name']))
            table.setItem(row, 1, QTableWidgetItem(f"${item['price']:.2f}"))
            
            quantity_spin = QSpinBox()
            quantity_spin.setMinimum(1)
            quantity_spin.setMaximum(100)
            quantity_spin.setValue(1)
            self.quick_order_quantity_inputs.append(quantity_spin)
            
            table.setCellWidget(row, 2, quantity_spin)
            
            # ប៊ូតុងបញ្ចូល
            add_btn = QPushButton("➕")
            add_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    padding: 5px 10px;
                    font-size: 12px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)
            add_btn.clicked.connect(lambda checked, r=row: self.add_quick_order_item(r, dialog))
            table.setCellWidget(row, 3, add_btn)
        
        layout.addWidget(table)
        
        # ប៊ូតុងបញ្ចូលទាំងអស់
        add_all_btn = QPushButton("➕ បញ្ចូលទំនិញទាំងអស់")
        add_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-weight: bold;
                padding: 12px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        add_all_btn.clicked.connect(lambda: self.add_all_quick_order_items(dialog))
        layout.addWidget(add_all_btn)
        
        # ប៊ូតុងបិទ
        close_btn = QPushButton("បិទ")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        close_btn.clicked.connect(dialog.reject)
        layout.addWidget(close_btn)
        
        dialog.exec_()
        
    def add_quick_order_item(self, row, dialog):
        item = self.quick_order_items[row]
        quantity = self.quick_order_quantity_inputs[row].value()
        
        # រកផលិតផលពេញលេញពីបញ្ជីផលិតផល
        product = None
        for p in self.products:
            if p['id'] == item['id']:
                product = p
                break
        
        if product and quantity <= product['stock']:
            # បន្ថែមទំនិញទៅក្នុងរទេះ
            item_total = product['final_price'] * quantity
            
            found = False
            for cart_item in self.cart_items:
                if cart_item['id'] == product['id']:
                    cart_item['quantity'] += quantity
                    cart_item['total'] += item_total
                    found = True
                    break
            
            if not found:
                self.cart_items.append({
                    'id': product['id'],
                    'name': product['name'],
                    'price': product['final_price'],
                    'original_price': product['price'],
                    'discount': product.get('discount', 0),
                    'quantity': quantity,
                    'total': item_total,
                    'image_path': product.get('image_path'),
                    'has_discount': product.get('has_discount', False)
                })
            
            # អាប់ដេតស្តុក
            product['stock'] -= quantity
            
            # អាប់ដេតការបង្ហាញ
            self.update_cart_display()
            self.display_products()
            
            QMessageBox.information(dialog, "ជោគជ័យ", f"បានបន្ថែម {product['name']} ចំនួន {quantity} ទៅក្នុងរទេះ!")
        else:
            QMessageBox.warning(dialog, "ការព្រមាន", "បរិមាណស្តុកមិនគ្រប់គ្រាន់!")
        
    def add_all_quick_order_items(self, dialog):
        added_count = 0
        
        for row, item in enumerate(self.quick_order_items):
            quantity = self.quick_order_quantity_inputs[row].value()
            
            # រកផលិតផលពេញលេញពីបញ្ជីផលិតផល
            product = None
            for p in self.products:
                if p['id'] == item['id']:
                    product = p
                    break
            
            if product and quantity > 0 and quantity <= product['stock']:
                item_total = product['final_price'] * quantity
                
                found = False
                for cart_item in self.cart_items:
                    if cart_item['id'] == product['id']:
                        cart_item['quantity'] += quantity
                        cart_item['total'] += item_total
                        found = True
                        break
                
                if not found:
                    self.cart_items.append({
                        'id': product['id'],
                        'name': product['name'],
                        'price': product['final_price'],
                        'original_price': product['price'],
                        'discount': product.get('discount', 0),
                        'quantity': quantity,
                        'total': item_total,
                        'image_path': product.get('image_path'),
                        'has_discount': product.get('has_discount', False)
                    })
                
                product['stock'] -= quantity
                added_count += 1
        
        if added_count > 0:
            self.update_cart_display()
            self.display_products()
            
            QMessageBox.information(dialog, "ជោគជ័យ", f"បានបន្ថែម {added_count} ទំនិញទៅក្នុងរទេះ!")
            dialog.accept()
        else:
            QMessageBox.warning(dialog, "ការព្រមាន", "មិនមានទំនិញត្រូវបានបន្ថែមទេ!")
        
    def sort_products(self, sort_by):
        if sort_by == "ឈ្មោះ (ក-អ)":
            self.products.sort(key=lambda x: x['name'])
        elif sort_by == "ឈ្មោះ (អ-ក)":
            self.products.sort(key=lambda x: x['name'], reverse=True)
        elif sort_by == "តម្លៃ (ទាប→ខ្ពស់)":
            self.products.sort(key=lambda x: x['final_price'])
        elif sort_by == "តម្លៃ (ខ្ពស់→ទាប)":
            self.products.sort(key=lambda x: x['final_price'], reverse=True)
        elif sort_by == "ស្តុក (ច្រើន→តិច)":
            self.products.sort(key=lambda x: x['stock'], reverse=True)
        elif sort_by == "ស្តុក (តិច→ច្រើន)":
            self.products.sort(key=lambda x: x['stock'])
        
        self.display_products()
        
    def display_products(self, products_to_display=None):
        # សម្អាតផលិតផលចាស់
        for i in reversed(range(self.products_grid.count())): 
            widget = self.products_grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        
        products = products_to_display if products_to_display else self.products
        
        row, col = 0, 0
        for product in products:
            product_card = self.create_product_card(product)
            self.products_grid.addWidget(product_card, row, col)
            col += 1
            if col > 2:  # 3 ជួរក្នុងមួយជួរឈរ
                col = 0
                row += 1
        
    def search_products(self):
        search_text = self.search_input.text().lower()
        if not search_text:
            self.display_products()
            return
            
        filtered_products = []
        for product in self.products:
            if (search_text in product["name"].lower() or 
                search_text in product["category"].lower() or
                search_text in product["info"].lower() or
                search_text in str(product["barcode"])):
                filtered_products.append(product)
        
        self.display_products(filtered_products)
        
    def create_product_card(self, product):
        card = ProductCard(product)
        card.add_to_cart_signal.connect(self.add_to_cart)
        card.selection_changed_signal.connect(self.product_selection_changed)
        
        # បង្ហាញ checkbox ប្រសិនបើកំពុងនៅក្នុងរបៀបជ្រើសរើសច្រើន
        is_multi_select = self.multi_select_checkbox.isChecked()
        card.show_checkbox(is_multi_select)
        
        return card
        
    def product_selection_changed(self, product_id, is_selected):
        if is_selected:
            self.selected_products.append(product_id)
        else:
            if product_id in self.selected_products:
                self.selected_products.remove(product_id)
        
    def add_to_cart(self, product):
        # បង្កើតទម្រង់ដើម្បីសួរបរិមាណ
        dialog = QDialog(self)
        dialog.setWindowTitle("បញ្ចូលទំនិញ")
        dialog.setFixedSize(350, 300)
        
        layout = QVBoxLayout(dialog)
        
        # រូបភាពផលិតផល
        image_label = QLabel()
        if product.get("image_path") and os.path.exists(product["image_path"]):
            pixmap = QPixmap(product["image_path"])
        else:
            pixmap = self.create_default_product_image(product["name"])
        
        pixmap = pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        
        product_label = QLabel(f"ផលិតផល: {product['name']}")
        product_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        # តម្លៃ
        price_layout = QHBoxLayout()
        if product.get("has_discount", False) and product["discount"] > 0:
            original_price = QLabel(f"តម្លៃដើម: ${product['price']:.2f}")
            original_price.setStyleSheet("font-size: 12px; color: #95a5a6; text-decoration: line-through;")
            
            final_price = QLabel(f"តម្លៃបញ្ចុះ: ${product['final_price']:.2f}")
            final_price.setStyleSheet("font-size: 14px; color: #27ae60; font-weight: bold;")
            
            price_layout.addWidget(original_price)
            price_layout.addWidget(final_price)
        else:
            price_label = QLabel(f"តម្លៃ: ${product['price']:.2f}")
            price_label.setStyleSheet("font-size: 14px; color: #27ae60;")
            price_layout.addWidget(price_label)
        
        layout.addWidget(image_label)
        layout.addWidget(product_label)
        layout.addLayout(price_layout)
        
        # បញ្ចូលបរិមាណ
        quantity_layout = QHBoxLayout()
        quantity_label = QLabel("បរិមាណ:")
        quantity_spin = QSpinBox()
        quantity_spin.setMinimum(1)
        quantity_spin.setMaximum(min(product['stock'], 100))
        quantity_spin.setValue(1)
        
        quantity_layout.addWidget(quantity_label)
        quantity_layout.addWidget(quantity_spin)
        layout.addLayout(quantity_layout)
        
        # សរុប
        total_label = QLabel(f"សរុប: ${product['final_price'] * quantity_spin.value():.2f}")
        total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        
        # អាប់ដេតសរុបនៅពេលប្តូរបរិមាណ
        def update_total():
            total = product['final_price'] * quantity_spin.value()
            total_label.setText(f"សរុប: ${total:.2f}")
        
        quantity_spin.valueChanged.connect(update_total)
        
        layout.addWidget(total_label)
        
        # ប៊ូតុងបញ្ជាក់
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.confirm_add_to_cart(product, quantity_spin.value(), dialog))
        button_box.rejected.connect(dialog.reject)
        
        layout.addWidget(button_box)
        
        dialog.exec_()
        
    def confirm_add_to_cart(self, product, quantity, dialog):
        # ពិនិត្យបរិមាណស្តុក
        if quantity > product['stock']:
            QMessageBox.warning(self, "ការព្រមាន", "បរិមាណស្តុកមិនគ្រប់គ្រាន់!")
            return
            
        # បន្ថែមទំនិញទៅក្នុងរទេះ
        item_total = product['final_price'] * quantity
        
        # ពិនិត្យថាទំនិញមាននៅក្នុងរទេះរួចហើយឬនៅ
        for item in self.cart_items:
            if item['id'] == product['id']:
                item['quantity'] += quantity
                item['total'] += item_total
                break
        else:
            self.cart_items.append({
                'id': product['id'],
                'name': product['name'],
                'price': product['final_price'],
                'original_price': product['price'],
                'discount': product.get('discount', 0),
                'quantity': quantity,
                'total': item_total,
                'image_path': product.get('image_path'),
                'has_discount': product.get('has_discount', False)
            })
        
        # អាប់ដេតស្តុក
        product['stock'] -= quantity
        
        # អាប់ដេតរទេះ
        self.update_cart_display()
        
        QMessageBox.information(self, "ជោគជ័យ", f"បានបន្ថែម {product['name']} ចំនួន {quantity} ទៅក្នុងរទេះ!")
        dialog.accept()
        
    def create_default_product_image(self, product_name):
        # បង្កើតរូបភាពលំនាំដើម
        pixmap = QPixmap(150, 150)
        pixmap.fill(QColor("#ecf0f1"))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # បង្កើតរូបរាង
        rect = QRect(15, 15, 120, 120)
        painter.setBrush(QColor("#3498db"))
        painter.setPen(QPen(QColor("#2980b9"), 2))
        painter.drawRoundedRect(rect, 10, 10)
        
        # សរសេរឈ្មោះផលិតផល
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        
        # កាត់ឈ្មោះផលិតផលឱ្យសម
        text = product_name
        if len(text) > 15:
            words = text.split()
            if len(words) > 2:
                text = ' '.join(words[:2]) + '...'
            else:
                text = text[:15] + "..."
        
        painter.drawText(rect, Qt.AlignCenter | Qt.TextWordWrap, text)
        
        painter.end()
        return pixmap
        
    def create_right_sidebar(self):
        sidebar = QWidget()
        sidebar.setStyleSheet("""
            QWidget {
                background-color: white;
                border-left: 1px solid #ddd;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # ចំណងជើងរទេះ
        cart_title = QLabel("🛒 ទំនិញក្នុងរទេះ")
        cart_title.setAlignment(Qt.AlignCenter)
        cart_title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                padding-bottom: 15px;
                border-bottom: 2px solid #3498db;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(cart_title)
        
        # ព័ត៌មានអតិថិជន
        customer_widget = QWidget()
        customer_layout = QVBoxLayout(customer_widget)
        
        customer_label = QLabel("👤 អតិថិជន:")
        customer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 8px;")
        
        self.customer_input = QLineEdit()
        self.customer_input.setPlaceholderText("សូមបញ្ចូលឈ្មោះអតិថិជន...")
        self.customer_input.setMinimumHeight(40)
        
        customer_layout.addWidget(customer_label)
        customer_layout.addWidget(self.customer_input)
        layout.addWidget(customer_widget)
        
        # បញ្ជីទំនិញក្នុងរទេះ
        cart_label = QLabel("📋 ទំនិញនាពេលបច្ចុប្បន្ន:")
        cart_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin: 20px 0 10px 0;")
        layout.addWidget(cart_label)
        
        # តារាងទំនិញ
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(5)
        self.cart_table.setHorizontalHeaderLabels(["ឈ្មោះ", "បរិមាណ", "តម្លៃ", "សរុប", ""])
        self.cart_table.horizontalHeader().setStretchLastSection(True)
        self.cart_table.verticalHeader().setVisible(False)
        self.cart_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.cart_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # កំណត់ទំហំជួរឈរ
        self.cart_table.setColumnWidth(0, 180)
        self.cart_table.setColumnWidth(1, 70)
        self.cart_table.setColumnWidth(2, 90)
        self.cart_table.setColumnWidth(3, 90)
        
        layout.addWidget(self.cart_table, 1)
        
        # ផ្នែកសរុប
        self.total_widget = QWidget()
        self.total_layout = QVBoxLayout(self.total_widget)
        self.total_layout.setSpacing(10)
        
        self.subtotal_label = QLabel("💰 សរុបរង: $0.00")
        self.subtotal_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        
        self.discount_label = QLabel("🎁 បញ្ចុះតម្លៃ: $0.00")
        self.discount_label.setStyleSheet("font-size: 16px; color: #27ae60;")
        
        self.tax_label = QLabel("📊 ពន្ធ (10%): $0.00")
        self.tax_label.setStyleSheet("font-size: 16px; color: #7f8c8d;")
        
        self.total_amount_label = QLabel("💵 សរុប: $0.00")
        self.total_amount_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #27ae60;")
        
        self.currency_label = QLabel("🇰🇭 Khmer Riel: ០ ៛")
        self.currency_label.setStyleSheet("font-size: 14px; color: #7f8c8d; font-style: italic;")
        
        self.total_layout.addWidget(self.subtotal_label)
        self.total_layout.addWidget(self.discount_label)
        self.total_layout.addWidget(self.tax_label)
        self.total_layout.addWidget(self.total_amount_label)
        self.total_layout.addWidget(self.currency_label)
        
        layout.addWidget(self.total_widget)
        
        # ប៊ូតុងបង់ប្រាក់
        pay_button = QPushButton("💳 បង់ប្រាក់")
        pay_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 18px;
                border-radius: 6px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        pay_button.setCursor(Qt.PointingHandCursor)
        pay_button.clicked.connect(self.process_payment)
        layout.addWidget(pay_button)
        
        # ប៊ូតុងសម្អាតរទេះ
        clear_button = QPushButton("🗑️ សម្អាតរទេះ")
        clear_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                border-radius: 6px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_button.setCursor(Qt.PointingHandCursor)
        clear_button.clicked.connect(self.clear_cart)
        layout.addWidget(clear_button)
        
        return sidebar
        
    def update_cart_display(self):
        self.cart_table.setRowCount(len(self.cart_items))
        
        subtotal = 0.0
        total_discount = 0.0
        total_original = 0.0
        
        for row, item in enumerate(self.cart_items):
            self.cart_table.setItem(row, 0, QTableWidgetItem(item['name']))
            self.cart_table.setItem(row, 1, QTableWidgetItem(str(item['quantity'])))
            
            # បង្ហាញតម្លៃបញ្ចុះ
            if item.get('has_discount', False):
                price_text = f"${item['price']:.2f}\n(បញ្ចុះ)"
                self.cart_table.item(row, 2).setForeground(QColor("#27ae60"))
            else:
                price_text = f"${item['price']:.2f}"
            
            self.cart_table.setItem(row, 2, QTableWidgetItem(price_text))
            self.cart_table.setItem(row, 3, QTableWidgetItem(f"${item['total']:.2f}"))
            
            # ប៊ូតុងលុប
            remove_btn = QPushButton("❌")
            remove_btn.setToolTip("លុបទំនិញនេះ")
            remove_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    padding: 5px 10px;
                    font-size: 12px;
                    border-radius: 3px;
                    min-width: 40px;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
            """)
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_from_cart(r))
            self.cart_table.setCellWidget(row, 4, remove_btn)
            
            subtotal += item['total']
            if item.get('has_discount', False):
                original_item_total = item['original_price'] * item['quantity']
                total_original += original_item_total
                total_discount += (original_item_total - item['total'])
            else:
                total_original += item['total']
        
        # គណនាសរុប
        tax = subtotal * 0.10
        total = subtotal + tax
        riel = total * 4100  # អត្រាប្តូរប្រាក់ប្រហាក់ប្រហែល
        
        self.subtotal_label.setText(f"💰 សរុបរង: ${subtotal:.2f}")
        self.discount_label.setText(f"🎁 បញ្ចុះតម្លៃ: ${total_discount:.2f}")
        self.tax_label.setText(f"📊 ពន្ធ (10%): ${tax:.2f}")
        self.total_amount_label.setText(f"💵 សរុប: ${total:.2f}")
        self.currency_label.setText(f"🇰🇭 Khmer Riel: {riel:,.0f} ៛")
        
    def remove_from_cart(self, row):
        if 0 <= row < len(self.cart_items):
            removed_item = self.cart_items.pop(row)
            
            # ដាក់ស្តុកត្រឡប់មកវិញ
            for product in self.products:
                if product['id'] == removed_item['id']:
                    product['stock'] += removed_item['quantity']
                    break
            
            # អាប់ដេតការបង្ហាញ
            self.update_cart_display()
            self.display_products()  # អាប់ដេតស្តុកនៅលើកាតផលិតផល
            
            QMessageBox.information(self, "ជោគជ័យ", f"បានលុប {removed_item['name']} ចេញពីរទេះ!")
        
    def clear_cart(self):
        if not self.cart_items:
            QMessageBox.warning(self, "ការព្រមាន", "រទេះទទេ!")
            return
            
        reply = QMessageBox.question(self, 'ផ្ទៀងផ្ទាត់', 
                                     'តើអ្នកពិតជាចង់សម្អាតរទេះទាំងអស់មែនទេ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # ដាក់ស្តុកត្រឡប់មកវិញ
            for item in self.cart_items:
                for product in self.products:
                    if product['id'] == item['id']:
                        product['stock'] += item['quantity']
                        break
            
            self.cart_items.clear()
            self.update_cart_display()
            self.display_products()  # អាប់ដេតស្តុកនៅលើកាតផលិតផល
            
            QMessageBox.information(self, "ជោគជ័យ", "បានសម្អាតរទេះដោយជោគជ័យ!")
        
    def process_payment(self):
        if not self.cart_items:
            QMessageBox.warning(self, "ការព្រមាន", "រទេះទទេ! សូមបញ្ចូលទំនិញមុនពេលបង់ប្រាក់។")
            return
            
        customer_name = self.customer_input.text().strip()
        if not customer_name:
            customer_name = "អតិថិជនធម្មតា"
            
        # បង្កើតទម្រង់បង់ប្រាក់
        dialog = QDialog(self)
        dialog.setWindowTitle("ការបង់ប្រាក់")
        dialog.setFixedSize(600, 600)
        
        layout = QVBoxLayout(dialog)
        
        # ព័ត៌មានសរុប
        subtotal = sum(item['total'] for item in self.cart_items)
        total_discount = sum((item.get('original_price', item['price']) * item['quantity']) - item['total'] 
                           for item in self.cart_items if item.get('has_discount', False))
        total_with_tax = subtotal * 1.10
        
        info_label = QLabel(f"តម្លៃសរុប: ${total_with_tax:.2f}")
        info_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #27ae60;")
        
        discount_info = QLabel(f"បញ្ចុះតម្លៃ: ${total_discount:.2f}")
        discount_info.setStyleSheet("font-size: 14px; color: #27ae60;")
        
        customer_label = QLabel(f"អតិថិជន: {customer_name}")
        
        layout.addWidget(info_label)
        layout.addWidget(discount_info)
        layout.addWidget(customer_label)
        
        # វិធីសាស្រ្តបង់ប្រាក់
        payment_group = QGroupBox("ជ្រើសរើសវិធីបង់ប្រាក់")
        payment_layout = QVBoxLayout()
        
        payment_methods = [
            ("💰 សាច់ប្រាក់", "cash"),
            ("💳 កាតឥណទាន/ឥណពន្ធ", "card"),
            ("🏦 ការផ្ទេរប្រាក់", "transfer"),
            ("📱 ទូរស័ព្ទចល័ត", "mobile"),
            ("🔲 QR Code", "qrcode")
        ]
        
        self.payment_radios = {}
        for text, method_id in payment_methods:
            radio = QRadioButton(text)
            radio.setProperty("method_id", method_id)
            payment_layout.addWidget(radio)
            self.payment_radios[method_id] = radio
        
        self.payment_radios["cash"].setChecked(True)
        payment_group.setLayout(payment_layout)
        
        layout.addWidget(payment_group)
        
        # ផ្នែក QR Code (មានតែពេលជ្រើសរើស QR Code)
        self.qr_widget = QWidget()
        qr_layout = QVBoxLayout(self.qr_widget)
        
        self.qr_label = QLabel("ស្កេន QR Code ខាងក្រោមដើម្បីបង់ប្រាក់:")
        
        # QR Code Image
        self.qr_image_label = QLabel()
        self.qr_image_label.setAlignment(Qt.AlignCenter)
        self.qr_image_label.setMinimumSize(250, 250)
        
        # ប៊ូតុងទាញយក QR Code
        self.download_qr_btn = QPushButton("📥 ទាញយក QR Code")
        self.download_qr_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.download_qr_btn.clicked.connect(self.download_qr_code)
        
        qr_layout.addWidget(self.qr_label)
        qr_layout.addWidget(self.qr_image_label)
        qr_layout.addWidget(self.download_qr_btn, 0, Qt.AlignCenter)
        self.qr_widget.setVisible(False)
        
        layout.addWidget(self.qr_widget)
        
        # ផ្នែកសាច់ប្រាក់ (មានតែពេលជ្រើសរើសសាច់ប្រាក់)
        self.cash_widget = QWidget()
        cash_layout = QVBoxLayout(self.cash_widget)
        
        cash_amount_label = QLabel("ចំនួនទឹកប្រាក់:")
        self.cash_amount_input = QLineEdit()
        self.cash_amount_input.setText(f"{total_with_tax:.2f}")
        self.cash_amount_input.setValidator(QDoubleValidator(0.01, 1000000.00, 2))
        
        cash_layout.addWidget(cash_amount_label)
        cash_layout.addWidget(self.cash_amount_input)
        self.cash_widget.setVisible(True)
        
        layout.addWidget(self.cash_widget)
        
        # តភ្ជាប់សញ្ញាសម្រាប់ប្តូរវិធីសាស្រ្តបង់ប្រាក់
        for radio in self.payment_radios.values():
            radio.toggled.connect(self.on_payment_method_changed)
        
        # ប៊ូតុង
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.confirm_payment(dialog, customer_name))
        button_box.rejected.connect(dialog.reject)
        
        layout.addWidget(button_box)
        
        dialog.exec_()
        
    def on_payment_method_changed(self):
        selected_method = None
        for method_id, radio in self.payment_radios.items():
            if radio.isChecked():
                selected_method = method_id
                break
        
        # បង្ហាញ/លាក់ផ្នែកដែលត្រូវការ
        self.qr_widget.setVisible(selected_method == "qrcode")
        self.cash_widget.setVisible(selected_method == "cash")
        
        if selected_method == "qrcode":
            self.generate_qr_code()
        
    def generate_qr_code(self):
        # បង្កើត QR Code សម្រាប់ការបង់ប្រាក់
        subtotal = sum(item['total'] for item in self.cart_items)
        total_with_tax = subtotal * 1.10
        customer_name = self.customer_input.text().strip() or "អតិថិជនធម្មតា"
        transaction_id = f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # ព័ត៌មានសម្រាប់ QR Code
        qr_data = f"""
        DSM-Shop Electronics
        Transaction ID: {transaction_id}
        Customer: {customer_name}
        Amount: ${total_with_tax:.2f}
        Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        Payment Method: QR Code
        
        ស្កេន QR Code នេះដើម្បីបង់ប្រាក់
        """
        
        # រក្សាទុក QR Code data
        self.current_qr_data = qr_data
        self.current_transaction_id = transaction_id
        
        # បង្កើត QR Code
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # បង្កើតរូបភាព QR Code
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # បំលែងទៅជា QPixmap
            buffer = io.BytesIO()
            qr_image.save(buffer, format="PNG")
            
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            
            # កំណត់ទំហំ
            pixmap = pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.qr_image_label.setPixmap(pixmap)
            
        except:
            # ប្រសិនបើមានបញ្ហា បង្កើត QR Code សាមញ្ញ
            self.qr_image_label.setText("QR Code\nមិនអាចបង្កើតបាន")
            self.qr_image_label.setStyleSheet("font-size: 16px; color: #e74c3c; font-weight: bold;")
        
    def download_qr_code(self):
        if not hasattr(self, 'current_qr_data'):
            QMessageBox.warning(self, "ការព្រមាន", "សូមជ្រើសរើស QR Code មុនពេលទាញយក!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "រក្សាទុក QR Code",
            f"qrcode_{self.current_transaction_id}.png",
            "PNG Files (*.png);;All Files (*)"
        )
        
        if file_path:
            try:
                # បង្កើត QR Code
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(self.current_qr_data)
                qr.make(fit=True)
                
                qr_image = qr.make_image(fill_color="black", back_color="white")
                qr_image.save(file_path)
                
                QMessageBox.information(self, "ជោគជ័យ", f"បានរក្សាទុក QR Code នៅ: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "កំហុស", f"មិនអាចរក្សាទុក QR Code: {str(e)}")
        
    def confirm_payment(self, dialog, customer_name):
        try:
            # ទាញយកវិធីសាស្រ្តបង់ប្រាក់ដែលបានជ្រើសរើស
            selected_method = None
            for method_id, radio in self.payment_radios.items():
                if radio.isChecked():
                    selected_method = method_id
                    break
            
            subtotal = sum(item['total'] for item in self.cart_items)
            total_with_tax = subtotal * 1.10
            
            if selected_method == "cash":
                amount = float(self.cash_amount_input.text())
                if amount < total_with_tax:
                    QMessageBox.warning(dialog, "ការព្រមាន", "ចំនួនទឹកប្រាក់មិនគ្រប់គ្រាន់!")
                    return
                change = amount - total_with_tax
                payment_details = f"សាច់ប្រាក់: ${amount:.2f}, លុយអាប់: ${change:.2f}"
            elif selected_method == "qrcode":
                payment_details = "បង់តាម QR Code"
                change = 0
                amount = total_with_tax
            else:
                payment_details = f"បង់តាម {selected_method}"
                change = 0
                amount = total_with_tax
            
            # បង្កើតប្រតិបត្តិការ
            transaction = {
                'id': f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'customer': customer_name,
                'amount': total_with_tax,
                'payment_method': selected_method,
                'date': datetime.now(),
                'items': self.cart_items.copy(),
                'status': 'ជោគជ័យ'
            }
            
            self.transactions.append(transaction)
            
            # បង្កើតបង្កាន់ដៃ
            receipt = self.generate_receipt(customer_name, amount, change, selected_method)
            
            # បង្ហាញបង្កាន់ដៃ
            self.show_receipt(receipt)
            
            # សម្អាតរទេះបន្ទាប់ពីបង់ប្រាក់
            self.cart_items.clear()
            self.customer_input.clear()
            self.update_cart_display()
            self.display_products()
            
            # អាប់ដេតផ្ទាំងគ្រប់គ្រង
            if hasattr(self, 'dashboard_widget'):
                self.update_dashboard()
            
            dialog.accept()
            
        except ValueError:
            QMessageBox.warning(dialog, "កំហុស", "សូមបញ្ចូលចំនួនទឹកប្រាក់ដែលត្រឹមត្រូវ!")
            
    def generate_receipt(self, customer_name, amount, change, payment_method):
        subtotal = sum(item['total'] for item in self.cart_items)
        total_discount = sum((item.get('original_price', item['price']) * item['quantity']) - item['total'] 
                           for item in self.cart_items if item.get('has_discount', False))
        total_with_tax = subtotal * 1.10
        
        receipt = f"""
        {'='*40}
            DSM-Shop Electronics
            បង្កាន់ដៃទទួលប្រាក់
        {'='*40}
        កាលបរិច្ឆេទ: {datetime.now().strftime('%Y-%m-%d %H:%M')}
        អតិថិជន: {customer_name}
        {'='*40}
        ទំនិញ:
        """
        
        for item in self.cart_items:
            item_name = item['name']
            if len(item_name) > 18:
                item_name = item_name[:15] + "..."
            
            if item.get('has_discount', False):
                original_price = item['original_price']
                discount_amount = (original_price - item['price']) * item['quantity']
                receipt += f"\n{item_name:18} x{item['quantity']:3} ${item['total']:8.2f}"
                receipt += f"\n{'បញ្ចុះ':22} ${discount_amount:8.2f}"
            else:
                receipt += f"\n{item_name:18} x{item['quantity']:3} ${item['total']:8.2f}"
        
        receipt += f"""
        {'='*40}
        សរុបរង: ${subtotal:30.2f}
        បញ្ចុះតម្លៃ: ${total_discount:26.2f}
        សរុបក្រោយបញ្ចុះ: ${subtotal:19.2f}
        ពន្ធ (10%): ${total_with_tax - subtotal:26.2f}
        {'='*40}
        សរុប: ${total_with_tax:33.2f}
        បង់: ${amount:32.2f}
        លុយអាប់: ${change:30.2f}
        វិធីបង់ប្រាក់: {payment_method:>19}
        {'='*40}
        សូមអរគុណសម្រាប់ការទិញ!
        {'='*40}
        """
        
        return receipt
        
    def show_receipt(self, receipt_text):
        # បង្កើតផ្ទាំងបង្កាន់ដៃ
        dialog = QDialog(self)
        dialog.setWindowTitle("បង្កាន់ដៃទទួលប្រាក់")
        dialog.setFixedSize(500, 600)
        
        layout = QVBoxLayout(dialog)
        
        # តំបន់អត្ថបទបង្កាន់ដៃ
        receipt_text_edit = QTextEdit()
        receipt_text_edit.setText(receipt_text)
        receipt_text_edit.setReadOnly(True)
        receipt_text_edit.setStyleSheet("""
            QTextEdit {
                font-family: 'Courier New';
                font-size: 12px;
                background-color: white;
                border: 1px solid #ddd;
            }
        """)
        
        layout.addWidget(receipt_text_edit)
        
        # ប៊ូតុង
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Save | QDialogButtonBox.Print)
        button_box.accepted.connect(dialog.accept)
        button_box.button(QDialogButtonBox.Save).clicked.connect(lambda: self.save_receipt(receipt_text))
        button_box.button(QDialogButtonBox.Print).setText("បោះពុម្ព")
        button_box.button(QDialogButtonBox.Print).clicked.connect(lambda: self.print_dialog(receipt_text_edit))
        
        layout.addWidget(button_box)
        
        dialog.exec_()
        
    def save_receipt(self, receipt_text):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "រក្សាទុកបង្កាន់ដៃ", 
            f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", 
            "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(receipt_text)
                QMessageBox.information(self, "ជោគជ័យ", "បានរក្សាទុកបង្កាន់ដៃដោយជោគជ័យ!")
            except Exception as e:
                QMessageBox.warning(self, "កំហុស", f"មិនអាចរក្សាទុកឯកសារ: {str(e)}")
                
    def print_dialog(self, text_edit):
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        
        if print_dialog.exec_() == QPrintDialog.Accepted:
            text_edit.print_(printer)
    
    # ==================== ផ្ទាំងគ្រប់គ្រង ====================
    def create_dashboard_page(self):
        self.dashboard_widget = QWidget()
        layout = QVBoxLayout(self.dashboard_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # ចំណងជើង
        title = QLabel("📊 ផ្ទាំងគ្រប់គ្រង")
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # កាតសង្ខេប
        summary_layout = QHBoxLayout()
        
        # កាតសរុបលក់
        sales_card = self.create_dashboard_card("💰 សរុបលក់", "$2,450.50", "#27ae60", "📈 +12% ពីសប្តាហ៍មុន")
        summary_layout.addWidget(sales_card)
        
        # កាតប្រតិបត្តិការ
        transactions_card = self.create_dashboard_card("📋 ប្រតិបត្តិការ", "24", "#3498db", "🔄 5 ថ្ងៃនេះ")
        summary_layout.addWidget(transactions_card)
        
        # កាតអតិថិជន
        customers_card = self.create_dashboard_card("👥 អតិថិជន", "48", "#9b59b6", "👤 3 ថ្មីថ្ងៃនេះ")
        summary_layout.addWidget(customers_card)
        
        # កាតស្តុកទំនិញ
        stock_card = self.create_dashboard_card("📦 ស្តុកទំនិញ", "156", "#f39c12", "⚠️ 8 ទំនិញតិចស្តុក")
        summary_layout.addWidget(stock_card)
        
        layout.addLayout(summary_layout)
        
        # ផ្នែក QR Code ការទូទាត់
        qr_section = QGroupBox("🔲 QR Code ការទូទាត់")
        qr_layout = QVBoxLayout()
        
        # ព័ត៌មាន QR Code
        qr_info = QLabel("ស្កេន QR Code ខាងក្រោមដើម្បីទទួលប្រាក់ពីអតិថិជន:")
        qr_info.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        
        # QR Code Display
        self.dashboard_qr_label = QLabel()
        self.dashboard_qr_label.setAlignment(Qt.AlignCenter)
        self.dashboard_qr_label.setMinimumSize(200, 200)
        self.dashboard_qr_label.setMaximumSize(250, 250)
        self.dashboard_qr_label.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px solid #3498db;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        # បង្កើត QR Code លំនាំដើមសម្រាប់ផ្ទាំងគ្រប់គ្រង
        self.generate_dashboard_qr_code()
        
        # ប៊ូតុងគ្រប់គ្រង QR Code
        qr_button_layout = QHBoxLayout()
        
        refresh_qr_btn = QPushButton("🔄 បង្កើតថ្មី")
        refresh_qr_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        refresh_qr_btn.clicked.connect(self.generate_dashboard_qr_code)
        
        download_qr_btn = QPushButton("📥 ទាញយក QR Code")
        download_qr_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        download_qr_btn.clicked.connect(self.download_dashboard_qr_code)
        
        qr_button_layout.addWidget(refresh_qr_btn)
        qr_button_layout.addStretch()
        qr_button_layout.addWidget(download_qr_btn)
        
        qr_layout.addWidget(qr_info)
        qr_layout.addWidget(self.dashboard_qr_label, 0, Qt.AlignCenter)
        qr_layout.addLayout(qr_button_layout)
        qr_section.setLayout(qr_layout)
        
        layout.addWidget(qr_section)
        
        # ប្រតិបត្តិការថ្មីៗ
        transactions_section = QGroupBox("🔄 ប្រតិបត្តិការថ្មីៗ")
        transactions_layout = QVBoxLayout()
        
        # តារាងប្រតិបត្តិការ
        self.transactions_table = QTableWidget()
        self.transactions_table.setColumnCount(5)
        self.transactions_table.setHorizontalHeaderLabels(["លេខ", "អតិថិជន", "តម្លៃ", "វិធីបង់", "កាលបរិច្ឆេទ"])
        self.transactions_table.horizontalHeader().setStretchLastSection(True)
        self.transactions_table.verticalHeader().setVisible(False)
        self.transactions_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.update_transactions_table()
        
        transactions_layout.addWidget(self.transactions_table)
        transactions_section.setLayout(transactions_layout)
        
        layout.addWidget(transactions_section)
        
        # ប៊ូតុងត្រលប់
        back_btn = QPushButton("← ត្រលប់ទៅការលក់")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 30px;
                margin-top: 20px;
                max-width: 200px;
                align-self: center;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        layout.addWidget(back_btn, 0, Qt.AlignCenter)
        
        return self.dashboard_widget
    
    def create_dashboard_card(self, title, value, color, info):
        card = QWidget()
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ddd;
                padding: 15px;
            }}
            QLabel {{
                color: #2c3e50;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 16px; font-weight: bold; color: {color};")
        
        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px 0;")
        
        info_label = QLabel(info)
        info_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(info_label)
        
        return card
    
    def generate_dashboard_qr_code(self):
        # បង្កើត QR Code សម្រាប់ទទួលប្រាក់ទូទៅ
        qr_data = f"""
        DSM-Shop Electronics
        Payment QR Code
        
        Account: DSM Electronics Co., Ltd.
        Bank: ABA Bank
        Account Number: 123 456 789
        Swift Code: ABAAKHPP
        
        Date: {datetime.now().strftime('%Y-%m-%d')}
        
        សូមបញ្ចូលលេខយោង: DASH{datetime.now().strftime('%Y%m%d')}
        """
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            buffer = io.BytesIO()
            qr_image.save(buffer, format="PNG")
            
            pixmap = QPixmap()
            pixmap.loadFromData(buffer.getvalue())
            
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.dashboard_qr_label.setPixmap(pixmap)
            
            # រក្សាទុក QR data
            self.dashboard_qr_data = qr_data
            
        except:
            self.dashboard_qr_label.setText("QR Code\nមិនអាច\nបង្កើតបាន")
            self.dashboard_qr_label.setStyleSheet("font-size: 14px; color: #e74c3c; font-weight: bold;")
    
    def download_dashboard_qr_code(self):
        if not hasattr(self, 'dashboard_qr_data'):
            QMessageBox.warning(self, "ការព្រមាន", "សូមបង្កើត QR Code មុនពេលទាញយក!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "រក្សាទុក QR Code",
            f"dashboard_qrcode_{datetime.now().strftime('%Y%m%d')}.png",
            "PNG Files (*.png);;All Files (*)"
        )
        
        if file_path:
            try:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(self.dashboard_qr_data)
                qr.make(fit=True)
                
                qr_image = qr.make_image(fill_color="black", back_color="white")
                qr_image.save(file_path)
                
                QMessageBox.information(self, "ជោគជ័យ", f"បានរក្សាទុក QR Code នៅ: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "កំហុស", f"មិនអាចរក្សាទុក QR Code: {str(e)}")
    
    def update_dashboard(self):
        # អាប់ដេតតារាងប្រតិបត្តិការ
        self.update_transactions_table()
        
        # អាប់ដេតកាតសង្ខេប
        # (នៅទីនេះអាចអាប់ដេតតម្លៃពិតប្រាកដ)
        pass
    
    def update_transactions_table(self):
        self.transactions_table.setRowCount(len(self.transactions))
        
        for row, transaction in enumerate(self.transactions):
            self.transactions_table.setItem(row, 0, QTableWidgetItem(transaction['id']))
            self.transactions_table.setItem(row, 1, QTableWidgetItem(transaction['customer']))
            self.transactions_table.setItem(row, 2, QTableWidgetItem(f"${transaction['amount']:.2f}"))
            self.transactions_table.setItem(row, 3, QTableWidgetItem(transaction['payment_method']))
            self.transactions_table.setItem(row, 4, QTableWidgetItem(transaction['date'].strftime('%Y-%m-%d %H:%M')))
    
    # ==================== ទំព័រផ្សេងៗ ====================
    
    def create_add_product_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # ចំណងជើងទំព័រ
        title = QLabel("📦 បន្ថែមទំនិញថ្មី")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 30px;
            }
        """)
        layout.addWidget(title)
        
        # ផ្នែករូបភាព
        image_group = QGroupBox("រូបភាពទំនិញ")
        image_layout = QVBoxLayout()
        
        self.product_image_label = QLabel()
        self.product_image_label.setAlignment(Qt.AlignCenter)
        self.product_image_label.setMinimumHeight(200)
        self.product_image_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px dashed #bdc3c7;
                border-radius: 8px;
                color: #7f8c8d;
                font-size: 14px;
            }
        """)
        self.product_image_label.setText("ចុចដើម្បីបញ្ចូលរូបភាព")
        self.product_image_label.setCursor(Qt.PointingHandCursor)
        self.product_image_label.mousePressEvent = self.select_product_image
        
        self.product_image_path = None
        
        # ប៊ូតុងសម្អាតរូបភាព
        clear_image_btn = QPushButton("🗑️ លុបរូបភាព")
        clear_image_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px;
                font-size: 12px;
                margin-top: 5px;
                max-width: 150px;
                align-self: center;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_image_btn.clicked.connect(self.clear_product_image)
        
        image_layout.addWidget(self.product_image_label)
        image_layout.addWidget(clear_image_btn, 0, Qt.AlignCenter)
        image_group.setLayout(image_layout)
        
        layout.addWidget(image_group)
        
        # ទម្រង់បញ្ចូលទិន្នន័យ
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        
        # ឈ្មោះទំនិញ
        self.product_name_input = QLineEdit()
        self.product_name_input.setPlaceholderText("សូមបញ្ចូលឈ្មោះទំនិញ...")
        form_layout.addRow("ឈ្មោះទំនិញ:", self.product_name_input)
        
        # តម្លៃ
        price_layout = QHBoxLayout()
        
        self.product_price_input = QLineEdit()
        self.product_price_input.setPlaceholderText("0.00")
        self.product_price_input.setValidator(QDoubleValidator(0.00, 1000000.00, 2))
        
        self.product_discount_input = QLineEdit()
        self.product_discount_input.setPlaceholderText("0.00")
        self.product_discount_input.setValidator(QDoubleValidator(0.00, 1000000.00, 2))
        self.product_discount_input.setToolTip("បញ្ចុះតម្លៃ (ទឹកប្រាក់)")
        
        self.product_discount_percent_input = QLineEdit()
        self.product_discount_percent_input.setPlaceholderText("0")
        self.product_discount_percent_input.setValidator(QDoubleValidator(0.00, 100.00, 2))
        self.product_discount_percent_input.setToolTip("បញ្ចុះតម្លៃ (%)")
        
        price_layout.addWidget(QLabel("តម្លៃ ($):"))
        price_layout.addWidget(self.product_price_input)
        price_layout.addWidget(QLabel("បញ្ចុះ ($):"))
        price_layout.addWidget(self.product_discount_input)
        price_layout.addWidget(QLabel("បញ្ចុះ (%):"))
        price_layout.addWidget(self.product_discount_percent_input)
        
        form_layout.addRow("តម្លៃ:", price_layout)
        
        # បរិមាណស្តុក
        self.product_stock_input = QSpinBox()
        self.product_stock_input.setMinimum(0)
        self.product_stock_input.setMaximum(10000)
        form_layout.addRow("បរិមាណស្តុក:", self.product_stock_input)
        
        # ប្រភេទ
        self.product_category_combo = QComboBox()
        categories = ["អេឡិចត្រូនិញ", "ទូរស័ព្ទ", "កុំព្យូទ័រ", "គ្រឿងបន្ថែម", 
                     "ភេសជ្ជៈ", "អាហារសម្រន់", "សំលៀកបំពាក់", "ផ្សេងៗ"]
        self.product_category_combo.addItems(categories)
        form_layout.addRow("ប្រភេទ:", self.product_category_combo)
        
        # លេខបាកូដ
        self.product_barcode_input = QLineEdit()
        self.product_barcode_input.setPlaceholderText("សូមបញ្ចូលលេខបាកូដ...")
        form_layout.addRow("លេខបាកូដ:", self.product_barcode_input)
        
        # ព័ត៌មានបន្ថែម
        self.product_info_input = QTextEdit()
        self.product_info_input.setMaximumHeight(100)
        self.product_info_input.setPlaceholderText("សូមបញ្ចូលព័ត៌មានបន្ថែម...")
        form_layout.addRow("ព័ត៌មានបន្ថែម:", self.product_info_input)
        
        layout.addWidget(form_widget, 1)
        
        # ប៊ូតុង
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        save_btn = QPushButton("💾 រក្សាទុកទំនិញ")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
        """)
        save_btn.clicked.connect(self.save_product)
        
        clear_btn = QPushButton("🧹 សម្អាត")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        clear_btn.clicked.connect(self.clear_product_form)
        
        back_btn = QPushButton("← ត្រលប់ទៅការលក់")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        button_layout.addWidget(back_btn)
        
        layout.addWidget(button_widget)
        
        return page
        
    def select_product_image(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "ជ្រើសរើសរូបភាព",
            "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        
        if file_path:
            # រក្សាទុករូបភាពក្នុងឯកសារបណ្តោះអាសន្ន
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            temp_file.close()
            
            # ចម្លងរូបភាពទៅឯកសារបណ្តោះអាសន្ន
            image = QImage(file_path)
            image.save(temp_file.name)
            
            self.product_image_path = temp_file.name
            self.temp_image_files.append(temp_file.name)
            
            # បង្ហាញរូបភាព
            pixmap = QPixmap(file_path)
            pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.product_image_label.setPixmap(pixmap)
            
    def clear_product_image(self):
        self.product_image_path = None
        self.product_image_label.clear()
        self.product_image_label.setText("ចុចដើម្បីបញ្ចូលរូបភាព")
        
    def save_product(self):
        # ទាញយកទិន្នន័យពីទម្រង់
        name = self.product_name_input.text().strip()
        price_text = self.product_price_input.text().strip()
        discount_text = self.product_discount_input.text().strip()
        discount_percent_text = self.product_discount_percent_input.text().strip()
        stock = self.product_stock_input.value()
        category = self.product_category_combo.currentText()
        barcode = self.product_barcode_input.text().strip()
        info = self.product_info_input.toPlainText().strip()
        
        # ពិនិត្យទិន្នន័យ
        if not name:
            QMessageBox.warning(self, "ការព្រមាន", "សូមបញ្ចូលឈ្មោះទំនិញ!")
            self.product_name_input.setFocus()
            return
            
        if not price_text:
            QMessageBox.warning(self, "ការព្រមាន", "សូមបញ្ចូលតម្លៃទំនិញ!")
            self.product_price_input.setFocus()
            return
            
        try:
            price = float(price_text)
        except ValueError:
            QMessageBox.warning(self, "កំហុស", "តម្លៃមិនត្រឹមត្រូវ! សូមបញ្ចូលលេខ។")
            self.product_price_input.setFocus()
            return
            
        # ទាញយកបញ្ចុះតម្លៃ
        discount = 0.0
        discount_percent = 0.0
        
        if discount_text:
            try:
                discount = float(discount_text)
            except ValueError:
                QMessageBox.warning(self, "កំហុស", "តម្លៃបញ្ចុះមិនត្រឹមត្រូវ!")
                self.product_discount_input.setFocus()
                return
                
        if discount_percent_text:
            try:
                discount_percent = float(discount_percent_text)
            except ValueError:
                QMessageBox.warning(self, "កំហុស", "ភាគរយបញ្ចុះមិនត្រឹមត្រូវ!")
                self.product_discount_percent_input.setFocus()
                return
        
        # គណនាតម្លៃបញ្ចុះ
        if discount > 0 and discount_percent > 0:
            # ប្រើតម្លៃបញ្ចុះ
            final_price = price - discount
            discount_percent = (discount / price) * 100
        elif discount > 0:
            # ប្រើតម្លៃបញ្ចុះ
            final_price = price - discount
            discount_percent = (discount / price) * 100
        elif discount_percent > 0:
            # ប្រើភាគរយបញ្ចុះ
            discount = price * (discount_percent / 100)
            final_price = price - discount
        else:
            final_price = price
            
        if not barcode:
            QMessageBox.warning(self, "ការព្រមាន", "សូមបញ្ចូលលេខបាកូដ!")
            self.product_barcode_input.setFocus()
            return
        
        # រក្សាទុករូបភាពក្នុងឯកសារបណ្តោះអាសន្ន
        product_image_path = None
        if self.product_image_path and os.path.exists(self.product_image_path):
            product_image_path = self.product_image_path
        
        # បង្កើតទំនិញថ្មី
        new_product = {
            "id": len(self.products) + 1,
            "name": name,
            "price": price,
            "discount": discount,
            "discount_percent": round(discount_percent, 1),
            "final_price": round(final_price, 2),
            "info": info if info else "គ្មានព័ត៌មានបន្ថែម",
            "stock": stock,
            "category": category,
            "barcode": barcode,
            "image": None,
            "image_path": product_image_path,
            "has_discount": discount > 0 or discount_percent > 0
        }
        
        # បន្ថែមទៅក្នុងបញ្ជីផលិតផល
        self.products.append(new_product)
        
        # អាប់ដេតការបង្ហាញ
        self.display_products()
        
        # សម្អាតទម្រង់
        self.clear_product_form()
        
        QMessageBox.information(self, "ជោគជ័យ", f"បានបន្ថែមទំនិញ '{name}' ដោយជោគជ័យ!")
        
        # ត្រលប់ទៅទំព័រការលក់
        self.stacked_widget.setCurrentIndex(0)
        
    def clear_product_form(self):
        self.product_name_input.clear()
        self.product_price_input.clear()
        self.product_discount_input.clear()
        self.product_discount_percent_input.clear()
        self.product_stock_input.setValue(0)
        self.product_category_combo.setCurrentIndex(0)
        self.product_barcode_input.clear()
        self.product_info_input.clear()
        self.clear_product_image()
        self.product_name_input.setFocus()
        
    # ទំព័រផ្សេងៗទៀត (សាមញ្ញ)
    def create_stock_page(self):
        return self.create_simple_page("📦 ស្តុកទំនិញ", "នេះគឺជាទំព័រគ្រប់គ្រងស្តុក")
        
    def create_reports_page(self):
        return self.create_simple_page("📈 របាយការណ៍", "នេះគឺជាទំព័ររបាយការណ៍")
        
    def create_customers_page(self):
        return self.create_simple_page("👥 អតិថិជន", "នេះគឺជាទំព័រគ្រប់គ្រងអតិថិជន")
        
    def create_suppliers_page(self):
        return self.create_simple_page("🏢 អ្នកផ្គត់ផ្គង់", "នេះគឺជាទំព័រគ្រប់គ្រងអ្នកផ្គត់ផ្គង់")
        
    def create_users_page(self):
        return self.create_simple_page("👤 អ្នកប្រើប្រាស់", "នេះគឺជាទំព័រគ្រប់គ្រងអ្នកប្រើប្រាស់")
        
    def create_settings_page(self):
        return self.create_simple_page("⚙️ ការកំណត់", "នេះគឺជាទំព័រការកំណត់ប្រព័ន្ធ")
        
    def create_simple_page(self, title, description):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        label1 = QLabel(title)
        label1.setAlignment(Qt.AlignCenter)
        label1.setStyleSheet("font-size: 32px; font-weight: bold; color: #2c3e50; margin-top: 100px;")
        
        label2 = QLabel(description)
        label2.setAlignment(Qt.AlignCenter)
        label2.setStyleSheet("font-size: 18px; color: #7f8c8d; margin-top: 20px;")
        
        back_btn = QPushButton("← ត្រលប់ទៅការលក់")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 12px 30px;
                margin-top: 50px;
                max-width: 200px;
                align-self: center;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        back_btn.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        
        layout.addWidget(label1)
        layout.addWidget(label2)
        layout.addWidget(back_btn, 0, Qt.AlignCenter)
        
        return page


class ProductCard(QWidget):
    add_to_cart_signal = pyqtSignal(dict)
    selection_changed_signal = pyqtSignal(int, bool)
    
    def __init__(self, product):
        super().__init__()
        self.product_data = product
        self.is_selected = False
        
        self.init_ui()
        
    def init_ui(self):
        bg_color = "#ffffff"
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {bg_color};
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }}
        """)
        
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(10, 10, 10, 10)
        self.card_layout.setSpacing(5)
        
        # Checkbox for multi-selection (hidden by default)
        self.checkbox = QCheckBox()
        self.checkbox.setVisible(False)
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)
        
        # រូបភាពផលិតផល
        image_container = QWidget()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_label = QLabel()
        if self.product_data.get("image_path") and os.path.exists(self.product_data["image_path"]):
            pixmap = QPixmap(self.product_data["image_path"])
        else:
            pixmap = self.create_default_product_image(self.product_data["name"])
        
        pixmap = pixmap.scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("padding: 5px;")
        
        image_layout.addWidget(self.checkbox, 0, Qt.AlignLeft)
        image_layout.addWidget(self.image_label)
        
        # ស្លាកបញ្ចុះតម្លៃ
        if self.product_data.get("has_discount", False) and self.product_data["discount_percent"] > 0:
            discount_label = QLabel(f"-{self.product_data['discount_percent']}%")
            discount_label.setAlignment(Qt.AlignCenter)
            discount_label.setStyleSheet("""
                QLabel {
                    background-color: #e74c3c;
                    color: white;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 3px 8px;
                    border-radius: 10px;
                    margin-top: 5px;
                }
            """)
            image_layout.addWidget(discount_label)
        
        self.card_layout.addWidget(image_container)
        
        # ឈ្មោះទំនិញ
        name_label = QLabel(self.product_data["name"])
        name_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50; margin-top: 5px;")
        name_label.setWordWrap(True)
        name_label.setAlignment(Qt.AlignCenter)
        self.card_layout.addWidget(name_label)
        
        # តម្លៃ
        price_widget = QWidget()
        price_layout = QVBoxLayout(price_widget)
        price_layout.setContentsMargins(0, 0, 0, 0)
        price_layout.setSpacing(2)
        
        if self.product_data.get("has_discount", False) and self.product_data["discount"] > 0:
            # បង្ហាញតម្លៃដើម និងតម្លៃបញ្ចុះ
            original_price_label = QLabel(f"${self.product_data['price']:.2f}")
            original_price_label.setStyleSheet("""
                QLabel {
                    font-size: 12px;
                    color: #95a5a6;
                    text-decoration: line-through;
                }
            """)
            original_price_label.setAlignment(Qt.AlignCenter)
            
            final_price_label = QLabel(f"${self.product_data['final_price']:.2f}")
            final_price_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #27ae60;")
            final_price_label.setAlignment(Qt.AlignCenter)
            
            price_layout.addWidget(original_price_label)
            price_layout.addWidget(final_price_label)
            
            # បង្ហាញចំនួនប្រាក់បញ្ចុះ
            discount_save_label = QLabel(f"សន្សំ ${self.product_data['discount']:.2f}")
            discount_save_label.setStyleSheet("font-size: 11px; color: #e74c3c; font-weight: bold;")
            discount_save_label.setAlignment(Qt.AlignCenter)
            price_layout.addWidget(discount_save_label)
        else:
            # បង្ហាជតម្លៃធម្មតា
            price_label = QLabel(f"${self.product_data['price']:.2f}")
            price_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
            price_label.setAlignment(Qt.AlignCenter)
            price_layout.addWidget(price_label)
        
        self.card_layout.addWidget(price_widget)
        
        # ស្តុកទំនិញ
        stock_widget = QWidget()
        stock_layout = QHBoxLayout(stock_widget)
        stock_layout.setContentsMargins(0, 0, 0, 0)
        
        stock_icon = QLabel("📦")
        stock_label = QLabel(f"ស្តុក: {self.product_data['stock']}")
        
        stock_color = "#27ae60" if self.product_data["stock"] > 10 else "#f39c12" if self.product_data["stock"] > 0 else "#e74c3c"
        stock_label.setStyleSheet(f"font-size: 12px; color: {stock_color}; font-weight: bold;")
        
        stock_layout.addWidget(stock_icon)
        stock_layout.addWidget(stock_label)
        stock_layout.addStretch()
        
        self.card_layout.addWidget(stock_widget)
        
        # ប៊ូតុងបញ្ចូលទៅក្នុងរទេះ
        add_btn = QPushButton("🛒 បញ្ចូលទៅក្នុងរទេះ")
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-weight: bold;
                padding: 8px;
                margin-top: 8px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        add_btn.setCursor(Qt.PointingHandCursor)
        add_btn.clicked.connect(self.on_add_to_cart)
        self.card_layout.addWidget(add_btn)
        
    def create_default_product_image(self, product_name):
        pixmap = QPixmap(150, 150)
        pixmap.fill(QColor("#ecf0f1"))
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        rect = QRect(15, 15, 120, 120)
        painter.setBrush(QColor("#3498db"))
        painter.setPen(QPen(QColor("#2980b9"), 2))
        painter.drawRoundedRect(rect, 10, 10)
        
        painter.setPen(QColor("white"))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        
        text = product_name
        if len(text) > 15:
            words = text.split()
            if len(words) > 2:
                text = ' '.join(words[:2]) + '...'
            else:
                text = text[:15] + "..."
        
        painter.drawText(rect, Qt.AlignCenter | Qt.TextWordWrap, text)
        
        painter.end()
        return pixmap
        
    def on_add_to_cart(self):
        self.add_to_cart_signal.emit(self.product_data)
        
    def show_checkbox(self, show):
        self.checkbox.setVisible(show)
        
    def on_checkbox_changed(self, state):
        self.is_selected = state == Qt.Checked
        self.selection_changed_signal.emit(self.product_data['id'], self.is_selected)
        
    def is_checked(self):
        return self.checkbox.isChecked()
        
    def set_checked(self, checked):
        self.checkbox.setChecked(checked)


def main():
    app = QApplication(sys.argv)
    
    # កំណត់ពុម្ពអក្សរ
    font = QFont("Khmer OS System", 10)
    app.setFont(font)
    
    window = DSMPOSSystem()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()