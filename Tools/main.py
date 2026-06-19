# main.py
import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from database_manager import DatabaseManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # បង្កើតថតរូបភាពបើមិនទាន់មាន
        if not os.path.exists('product_images'):
            os.makedirs('product_images')
        
        # ភ្ជាប់ database
        self.db = DatabaseManager('study_materials.db')
        
        self.cart = []
        self.exchange_rate = 4000
        self.current_user = None
        
        self.initUI()
        self.load_products()
        self.update_statistics()
        
        # បង្ហាញសារស្វាគមន៍
        self.statusBar().showMessage(f"✅ ភ្ជាប់ database រួចរាល់: {self.db.db_name}", 5000)
    
    def initUI(self):
        self.setWindowTitle('ប្រព័ន្ធគ្រប់គ្រងការលក់សម្ភារៈសិក្សា')
        self.setGeometry(100, 100, 1400, 800)
        
        # កំណត់រចនាប័ទ្ម
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #e0e0e0;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton[type="danger"] {
                background-color: #f44336;
            }
            QPushButton[type="danger"]:hover {
                background-color: #da190b;
            }
            QPushButton[type="warning"] {
                background-color: #ff9800;
            }
            QPushButton[type="warning"]:hover {
                background-color: #e68900;
            }
            QTableWidget {
                gridline-color: #d0d0d0;
                selection-background-color: #e3f2fd;
                alternate-background-color: #f9f9f9;
                font-size: 13px;
            }
            QHeaderView::section {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
                padding: 6px;
                border: 1px solid #cccccc;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
                border: 2px solid #4CAF50;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QStatusBar {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
        """)
        
        # បង្កើត toolbar
        self.create_toolbar()
        
        # បង្កើត central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # បង្កើត tabs
        tabs = QTabWidget()
        tabs.addTab(self.create_dashboard_tab(), "🏠 ផ្ទាំងគ្រប់គ្រង")
        tabs.addTab(self.create_sales_tab(), "🏪 លក់ទំនិញ")
        tabs.addTab(self.create_inventory_tab(), "📦 ស្តុកទំនិញ")
        tabs.addTab(self.create_reports_tab(), "📊 របាយការណ៍")
        
        layout.addWidget(tabs)
        
        # Status bar
        self.statusBar().showMessage('រួចរាល់')
    
    def create_toolbar(self):
        toolbar = self.addToolBar('Tools')
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #4CAF50;
                spacing: 10px;
                padding: 5px;
            }
            QToolButton {
                color: white;
                background-color: transparent;
                padding: 5px 10px;
                border-radius: 3px;
            }
            QToolButton:hover {
                background-color: #45a049;
            }
        """)
        
        # Database info
        db_label = QLabel(f"📀 {self.db.db_name}")
        db_label.setStyleSheet("color: white; font-weight: bold; padding: 5px;")
        toolbar.addWidget(db_label)
        
        toolbar.addSeparator()
        
        # Refresh action
        refresh_action = QAction(QIcon.fromTheme("view-refresh"), "ធ្វើឱ្យថ្មី", self)
        refresh_action.triggered.connect(self.refresh_all)
        toolbar.addAction(refresh_action)
        
        # Backup action
        backup_action = QAction(QIcon.fromTheme("document-save"), "បម្រុងទុក", self)
        backup_action.triggered.connect(self.backup_database)
        toolbar.addAction(backup_action)
        
        # Statistics
        self.stats_label = QLabel("")
        self.stats_label.setStyleSheet("color: white; padding: 5px;")
        toolbar.addWidget(self.stats_label)
    
    def create_dashboard_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Welcome message
        welcome_label = QLabel("សូមស្វាគមន៍មកកាន់ប្រព័ន្ធគ្រប់គ្រងការលក់")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50; padding: 20px;")
        welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome_label)
        
        # Statistics cards
        stats_layout = QHBoxLayout()
        
        # Product stats
        self.product_card = self.create_stat_card(
            "📦 ទំនិញសរុប", 
            "0", 
            "ចំនួនទំនិញក្នុងប្រព័ន្ធ",
            "#4CAF50"
        )
        stats_layout.addWidget(self.product_card)
        
        # Stock stats
        self.stock_card = self.create_stat_card(
            "📊 ស្តុកសរុប", 
            "0", 
            "បរិមាណទំនិញទាំងអស់",
            "#2196F3"
        )
        stats_layout.addWidget(self.stock_card)
        
        # Low stock stats
        self.low_stock_card = self.create_stat_card(
            "⚠️ ស្តុកជិតអស់", 
            "0", 
            "ទំនិញដែលត្រូវបញ្ជាទិញបន្ថែម",
            "#FF9800"
        )
        stats_layout.addWidget(self.low_stock_card)
        
        # Today sales stats
        self.today_sales_card = this.create_stat_card(
            "💰 លក់ថ្ងៃនេះ", 
            "$0.00", 
            "ចំណូលសរុបថ្ងៃនេះ",
            "#9C27B0"
        )
        stats_layout.addWidget(self.today_sales_card)
        
        layout.addLayout(stats_layout)
        
        # Low stock products table
        low_stock_group = QGroupBox("ទំនិញជិតអស់ស្តុក")
        low_stock_layout = QVBoxLayout()
        
        self.low_stock_table = QTableWidget()
        self.low_stock_table.setColumnCount(4)
        self.low_stock_table.setHorizontalHeaderLabels(['ឈ្មោះទំនិញ', 'ប្រភេទ', 'ស្តុកបច្ចុប្បន្ន', 'ស្តុកអប្បបរមា'])
        self.low_stock_table.horizontalHeader().setStretchLastSection(True)
        low_stock_layout.addWidget(self.low_stock_table)
        
        low_stock_group.setLayout(low_stock_layout)
        layout.addWidget(low_stock_group)
        
        # Recent activities
        recent_group = QGroupBox("សកម្មភាពថ្មីៗ")
        recent_layout = QVBoxLayout()
        
        self.recent_text = QTextEdit()
        self.recent_text.setReadOnly(True)
        self.recent_text.setMaximumHeight(150)
        recent_layout.addWidget(self.recent_text)
        
        recent_group.setLayout(recent_layout)
        layout.addWidget(recent_group)
        
        return widget
    
    def create_stat_card(self, title, value, subtitle, color):
        card = QFrame()
        card.setFrameStyle(QFrame.Box)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 10px;
                padding: 15px;
                margin: 10px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 16px; color: #666;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 32px; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)
        
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("font-size: 12px; color: #999;")
        subtitle_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle_label)
        
        return card
    
    def create_sales_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # Left panel - Product list
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # Search bar
        search_group = QGroupBox("ស្វែងរកទំនិញ")
        search_layout = QGridLayout()
        
        search_layout.addWidget(QLabel("ឈ្មោះ/កូដ:"), 0, 0)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("បញ្ចូលឈ្មោះ ឬកូដទំនិញ...")
        self.search_input.textChanged.connect(self.search_products)
        search_layout.addWidget(self.search_input, 0, 1)
        
        search_layout.addWidget(QLabel("ប្រភេទ:"), 1, 0)
        self.category_filter = QComboBox()
        self.category_filter.addItem("ទាំងអស់")
        self.category_filter.addItems(['សៀវភៅ', 'សៀវភៅកត់ត្រា', 'ប៊ិក', 'ខ្មៅដៃ', 'បន្ទាត់', 'កាបូប', 'ម៉ាស៊ីនគិតលេខ', 'ក្រដាស'])
        self.category_filter.currentTextChanged.connect(self.search_products)
        search_layout.addWidget(self.category_filter, 1, 1)
        
        search_btn = QPushButton("ស្វែងរក")
        search_btn.clicked.connect(self.search_products)
        search_layout.addWidget(search_btn, 0, 2, 2, 1)
        
        search_group.setLayout(search_layout)
        left_layout.addWidget(search_group)
        
        # Product table
        self.product_table = QTableWidget()
        self.product_table.setColumnCount(6)
        self.product_table.setHorizontalHeaderLabels(['ID', 'កូដ', 'ឈ្មោះទំនិញ', 'ប្រភេទ', 'តម្លៃ', 'ស្តុក'])
        self.product_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.product_table.setAlternatingRowColors(True)
        self.product_table.doubleClicked.connect(self.add_to_cart)
        
        # Set column widths
        self.product_table.setColumnWidth(0, 50)
        self.product_table.setColumnWidth(1, 100)
        self.product_table.setColumnWidth(2, 200)
        self.product_table.setColumnWidth(3, 100)
        self.product_table.setColumnWidth(4, 100)
        self.product_table.setColumnWidth(5, 80)
        
        left_layout.addWidget(self.product_table)
        
        # Quick add by barcode
        barcode_layout = QHBoxLayout()
        barcode_layout.addWidget(QLabel("Barcode:"))
        self.barcode_scanner = QLineEdit()
        self.barcode_scanner.setPlaceholderText("ស្កេន Barcode...")
        self.barcode_scanner.returnPressed.connect(self.add_by_barcode)
        barcode_layout.addWidget(self.barcode_scanner)
        left_layout.addLayout(barcode_layout)
        
        # Right panel - Cart
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Cart title
        cart_title = QLabel("🛒 កន្ត្រកទំនិញ")
        cart_title.setStyleSheet("font-size: 18px; font-weight: bold; color: #4CAF50; padding: 10px;")
        right_layout.addWidget(cart_title)
        
        # Cart table
        self.cart_table = QTableWidget()
        self.cart_table.setColumnCount(6)
        self.cart_table.setHorizontalHeaderLabels(['ID', 'ឈ្មោះ', 'តម្លៃ', 'បរិមាណ', 'សរុប', ''])
        self.cart_table.setAlternatingRowColors(True)
        
        # Set column widths
        self.cart_table.setColumnWidth(0, 50)
        self.cart_table.setColumnWidth(1, 150)
        self.cart_table.setColumnWidth(2, 80)
        self.cart_table.setColumnWidth(3, 80)
        self.cart_table.setColumnWidth(4, 100)
        self.cart_table.setColumnWidth(5, 50)
        
        right_layout.addWidget(self.cart_table)
        
        # Total amount
        total_widget = QWidget()
        total_widget.setStyleSheet("background-color: #e8f5e8; border-radius: 5px; padding: 10px;")
        total_layout = QHBoxLayout(total_widget)
        
        total_layout.addWidget(QLabel("សរុប:"))
        total_layout.addStretch()
        
        self.total_amount_label = QLabel("$0.00")
        self.total_amount_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #4CAF50;")
        total_layout.addWidget(self.total_amount_label)
        
        self.total_currency = QComboBox()
        self.total_currency.addItems(['ដុល្លារ ($)', 'រៀល (៛)'])
        self.total_currency.currentTextChanged.connect(self.update_total_display)
        total_layout.addWidget(self.total_currency)
        
        right_layout.addWidget(total_widget)
        
        # Customer info
        customer_group = QGroupBox("ព័ត៌មានអតិថិជន")
        customer_layout = QFormLayout()
        
        self.customer_name = QLineEdit()
        self.customer_name.setPlaceholderText("បញ្ចូលឈ្មោះអតិថិជន...")
        customer_layout.addRow("ឈ្មោះ:", self.customer_name)
        
        self.customer_phone = QLineEdit()
        self.customer_phone.setPlaceholderText("លេខទូរស័ព្ទ...")
        customer_layout.addRow("ទូរស័ព្ទ:", self.customer_phone)
        
        customer_group.setLayout(customer_layout)
        right_layout.addWidget(customer_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.remove_btn = QPushButton("❌ ដកចេញ")
        self.remove_btn.setProperty("type", "danger")
        self.remove_btn.clicked.connect(self.remove_from_cart)
        
        self.clear_btn = QPushButton("🔄 សម្អាត")
        self.clear_btn.setProperty("type", "warning")
        self.clear_btn.clicked.connect(self.clear_cart)
        
        self.checkout_btn = QPushButton("💵 បញ្ចប់ការលក់")
        self.checkout_btn.clicked.connect(self.checkout)
        
        button_layout.addWidget(self.remove_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.checkout_btn)
        
        right_layout.addLayout(button_layout)
        
        # Add panels to main layout
        layout.addWidget(left_panel, 2)
        layout.addWidget(right_panel, 1)
        
        return widget
    
    def create_inventory_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Button toolbar
        toolbar = QHBoxLayout()
        
        add_btn = QPushButton("➕ បន្ថែមទំនិញថ្មី")
        add_btn.clicked.connect(self.add_product_dialog)
        
        edit_btn = QPushButton("✏️ កែប្រែទំនិញ")
        edit_btn.clicked.connect(self.edit_product_dialog)
        
        delete_btn = QPushButton("🗑️ លុបទំនិញ")
        delete_btn.setProperty("type", "danger")
        delete_btn.clicked.connect(self.delete_product)
        
        refresh_btn = QPushButton("🔄 ធ្វើឱ្យថ្មី")
        refresh_btn.clicked.connect(self.load_inventory)
        
        export_btn = QPushButton("📥 នាំចេញ")
        export_btn.clicked.connect(self.export_inventory)
        
        toolbar.addWidget(add_btn)
        toolbar.addWidget(edit_btn)
        toolbar.addWidget(delete_btn)
        toolbar.addWidget(refresh_btn)
        toolbar.addWidget(export_btn)
        toolbar.addStretch()
        
        layout.addLayout(toolbar)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("ស្វែងរក:"))
        self.inventory_search = QLineEdit()
        self.inventory_search.setPlaceholderText("បញ្ចូលឈ្មោះ ឬកូដទំនិញ...")
        self.inventory_search.textChanged.connect(self.filter_inventory)
        search_layout.addWidget(self.inventory_search)
        layout.addLayout(search_layout)
        
        # Inventory table
        self.inventory_table = QTableWidget()
        self.inventory_table.setColumnCount(13)
        self.inventory_table.setHorizontalHeaderLabels([
            'ID', 'កូដ', 'ឈ្មោះ', 'ប្រភេទ', 'តម្លៃដើម', 'រូបិយប័ណ្ណ',
            'តម្លៃលក់', 'រូបិយប័ណ្ណ', 'ស្តុក', 'ស្តុកអប្បបរមា', 'ស្ថានភាព', 'រូបភាព', 'កែប្រែចុងក្រោយ'
        ])
        self.inventory_table.setAlternatingRowColors(True)
        self.inventory_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Set column widths
        self.inventory_table.setColumnWidth(0, 50)
        self.inventory_table.setColumnWidth(1, 100)
        self.inventory_table.setColumnWidth(2, 200)
        self.inventory_table.setColumnWidth(3, 100)
        self.inventory_table.setColumnWidth(4, 80)
        self.inventory_table.setColumnWidth(5, 80)
        self.inventory_table.setColumnWidth(6, 80)
        self.inventory_table.setColumnWidth(7, 80)
        self.inventory_table.setColumnWidth(8, 80)
        self.inventory_table.setColumnWidth(9, 80)
        self.inventory_table.setColumnWidth(10, 80)
        self.inventory_table.setColumnWidth(11, 80)
        self.inventory_table.setColumnWidth(12, 150)
        
        layout.addWidget(self.inventory_table)
        
        # Summary
        summary_layout = QHBoxLayout()
        summary_layout.addWidget(QLabel("សង្ខេប:"))
        
        self.total_products_label = QLabel("ទំនិញសរុប: 0")
        self.total_products_label.setStyleSheet("font-weight: bold;")
        summary_layout.addWidget(self.total_products_label)
        
        self.low_stock_label = QLabel("ស្តុកជិតអស់: 0")
        self.low_stock_label.setStyleSheet("color: #f44336; font-weight: bold;")
        summary_layout.addWidget(self.low_stock_label)
        
        self.out_of_stock_label = QLabel("អស់ស្តុក: 0")
        self.out_of_stock_label.setStyleSheet("color: #ff9800; font-weight: bold;")
        summary_layout.addWidget(self.out_of_stock_label)
        
        summary_layout.addStretch()
        layout.addLayout(summary_layout)
        
        return widget
    
    def create_reports_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Report controls
        controls_group = QGroupBox("ជ្រើសរើសរបាយការណ៍")
        controls_layout = QGridLayout()
        
        controls_layout.addWidget(QLabel("ប្រភេទរបាយការណ៍:"), 0, 0)
        self.report_type = QComboBox()
        self.report_type.addItems(['របាយការណ៍លក់ប្រចាំថ្ងៃ', 'របាយការណ៍លក់ប្រចាំខែ', 
                                  'របាយការណ៍ស្តុក', 'របាយការណ៍ប្រាក់ចំណេញ'])
        controls_layout.addWidget(self.report_type, 0, 1)
        
        controls_layout.addWidget(QLabel("ចាប់ពីថ្ងៃ:"), 1, 0)
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        self.start_date.setCalendarPopup(True)
        controls_layout.addWidget(self.start_date, 1, 1)
        
        controls_layout.addWidget(QLabel("ដល់ថ្ងៃ:"), 2, 0)
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        self.end_date.setCalendarPopup(True)
        controls_layout.addWidget(self.end_date, 2, 1)
        
        generate_btn = QPushButton("📊 បង្កើតរបាយការណ៍")
        generate_btn.clicked.connect(self.generate_report)
        controls_layout.addWidget(generate_btn, 3, 0, 1, 2)
        
        controls_group.setLayout(controls_layout)
        layout.addWidget(controls_group)
        
        # Report display
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setStyleSheet("""
            QTextEdit {
                font-family: 'Khmer OS', monospace;
                font-size: 14px;
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout.addWidget(self.report_text)
        
        # Export buttons
        export_layout = QHBoxLayout()
        export_layout.addStretch()
        
        pdf_btn = QPushButton("📄 នាំចេញជា PDF")
        pdf_btn.clicked.connect(self.export_report_pdf)
        export_layout.addWidget(pdf_btn)
        
        excel_btn = QPushButton("📊 នាំចេញជា Excel")
        excel_btn.clicked.connect(self.export_report_excel)
        export_layout.addWidget(excel_btn)
        
        layout.addLayout(export_layout)
        
        return widget
    
    def load_products(self):
        """ផ្ទុកទំនិញពី database"""
        try:
            products = self.db.get_all_products()
            
            self.product_table.setRowCount(len(products))
            for row, product in enumerate(products):
                self.product_table.setItem(row, 0, QTableWidgetItem(str(product[0])))
                self.product_table.setItem(row, 1, QTableWidgetItem(str(product[3] or '')))
                self.product_table.setItem(row, 2, QTableWidgetItem(product[1]))
                self.product_table.setItem(row, 3, QTableWidgetItem(product[2] or ''))
                self.product_table.setItem(row, 4, QTableWidgetItem(f"${product[6]:.2f}"))
                self.product_table.setItem(row, 5, QTableWidgetItem(str(product[8])))
            
            self.statusBar().showMessage(f"✅ បានផ្ទុកទំនិញ {len(products)} មុខ", 3000)
            
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចផ្ទុកទំនិញ: {str(e)}")
    
    def load_inventory(self):
        """ផ្ទុកស្តុកទំនិញ"""
        try:
            products = self.db.get_all_products()
            
            self.inventory_table.setRowCount(len(products))
            total_products = 0
            low_stock = 0
            out_of_stock = 0
            
            for row, product in enumerate(products):
                # ID
                self.inventory_table.setItem(row, 0, QTableWidgetItem(str(product[0])))
                # Barcode
                self.inventory_table.setItem(row, 1, QTableWidgetItem(str(product[3] or '')))
                # Name
                self.inventory_table.setItem(row, 2, QTableWidgetItem(product[1]))
                # Category
                self.inventory_table.setItem(row, 3, QTableWidgetItem(product[2] or ''))
                # Cost price
                self.inventory_table.setItem(row, 4, QTableWidgetItem(f"${product[4]:.2f}"))
                # Cost currency
                self.inventory_table.setItem(row, 5, QTableWidgetItem(product[5]))
                # Selling price
                self.inventory_table.setItem(row, 6, QTableWidgetItem(f"${product[6]:.2f}"))
                # Selling currency
                self.inventory_table.setItem(row, 7, QTableWidgetItem(product[7]))
                # Stock
                stock = product[8]
                stock_item = QTableWidgetItem(str(stock))
                if stock <= 0:
                    stock_item.setBackground(QColor(255, 200, 200))
                    out_of_stock += 1
                elif stock <= product[9]:
                    stock_item.setBackground(QColor(255, 255, 200))
                    low_stock += 1
                self.inventory_table.setItem(row, 8, stock_item)
                # Min stock
                self.inventory_table.setItem(row, 9, QTableWidgetItem(str(product[9])))
                # Status
                status = "សកម្ម" if product[14] else "មិនសកម្ម"
                self.inventory_table.setItem(row, 10, QTableWidgetItem(status))
                # Image
                if product[11]:
                    self.inventory_table.setItem(row, 11, QTableWidgetItem("✅ មាន"))
                else:
                    self.inventory_table.setItem(row, 11, QTableWidgetItem("❌ គ្មាន"))
                # Updated at
                self.inventory_table.setItem(row, 12, QTableWidgetItem(str(product[16] or '')))
                
                total_products += 1
            
            # Update summary
            self.total_products_label.setText(f"ទំនិញសរុប: {total_products}")
            self.low_stock_label.setText(f"ស្តុកជិតអស់: {low_stock}")
            self.out_of_stock_label.setText(f"អស់ស្តុក: {out_of_stock}")
            
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចផ្ទុកស្តុក: {str(e)}")
    
    def update_statistics(self):
        """ធ្វើបច្ចុប្បន្នភាពស្ថិតិ"""
        try:
            stats = self.db.get_statistics()
            
            # Update dashboard cards if they exist
            if hasattr(self, 'product_card'):
                product_value = stats.get('total_products', 0)
                self.product_card.findChild(QLabel, "", Qt.FindChildrenRecursively).setText(str(product_value))
            
            if hasattr(self, 'stock_card'):
                stock_value = stats.get('total_stock', 0)
                self.stock_card.findChild(QLabel, "", Qt.FindChildrenRecursively).setText(str(stock_value))
            
            if hasattr(self, 'low_stock_card'):
                low_stock_value = stats.get('low_stock', 0)
                self.low_stock_card.findChild(QLabel, "", Qt.FindChildrenRecursively).setText(str(low_stock_value))
            
            if hasattr(self, 'today_sales_card'):
                today_revenue = stats.get('today_revenue', 0)
                self.today_sales_card.findChild(QLabel, "", Qt.FindChildrenRecursively).setText(f"${today_revenue:.2f}")
            
            # Update low stock table
            if hasattr(self, 'low_stock_table'):
                low_stock_products = self.db.get_low_stock_products()
                self.low_stock_table.setRowCount(len(low_stock_products))
                for row, product in enumerate(low_stock_products):
                    self.low_stock_table.setItem(row, 0, QTableWidgetItem(product[0]))
                    self.low_stock_table.setItem(row, 1, QTableWidgetItem(""))
                    self.low_stock_table.setItem(row, 2, QTableWidgetItem(str(product[1])))
                    self.low_stock_table.setItem(row, 3, QTableWidgetItem(str(product[2])))
            
            # Update recent activities
            if hasattr(self, 'recent_text'):
                self.recent_text.append(f"[{datetime.now().strftime('%H:%M:%S')}] បានធ្វើបច្ចុប្បន្នភាពស្ថិតិ")
            
            # Update toolbar stats
            self.stats_label.setText(f"📊 {stats.get('total_products', 0)} ទំនិញ | {stats.get('total_stock', 0)} ស្តុក")
            
        except Exception as e:
            print(f"Error updating statistics: {e}")
    
    def search_products(self):
        """ស្វែងរកទំនិញ"""
        search_term = self.search_input.text()
        category = self.category_filter.currentText()
        
        try:
            if search_term:
                products = self.db.search_products(search_term)
            else:
                products = self.db.get_all_products()
            
            # Filter by category if needed
            if category != "ទាំងអស់":
                products = [p for p in products if p[2] == category]
            
            self.product_table.setRowCount(len(products))
            for row, product in enumerate(products):
                self.product_table.setItem(row, 0, QTableWidgetItem(str(product[0])))
                self.product_table.setItem(row, 1, QTableWidgetItem(str(product[3] or '')))
                self.product_table.setItem(row, 2, QTableWidgetItem(product[1]))
                self.product_table.setItem(row, 3, QTableWidgetItem(product[2] or ''))
                self.product_table.setItem(row, 4, QTableWidgetItem(f"${product[6]:.2f}"))
                self.product_table.setItem(row, 5, QTableWidgetItem(str(product[8])))
            
            self.statusBar().showMessage(f"✅ បានរកឃើញ {len(products)} មុខ", 2000)
            
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចស្វែងរក: {str(e)}")
    
    def filter_inventory(self):
        """ត្រងស្តុកទំនិញ"""
        search_term = self.inventory_search.text().lower()
        
        for row in range(self.inventory_table.rowCount()):
            match = False
            for col in [1, 2]:  # Search in barcode and name columns
                item = self.inventory_table.item(row, col)
                if item and search_term in item.text().lower():
                    match = True
                    break
            self.inventory_table.setRowHidden(row, not match)
    
    def add_to_cart(self):
        """បន្ថែមទំនិញទៅកន្ត្រក"""
        current_row = self.product_table.currentRow()
        if current_row >= 0:
            try:
                product_id = int(self.product_table.item(current_row, 0).text())
                name = self.product_table.item(current_row, 2).text()
                price_text = self.product_table.item(current_row, 4).text().replace('$', '')
                price = float(price_text)
                stock = int(self.product_table.item(current_row, 5).text())
                
                # Check if product already in cart
                for item in self.cart:
                    if item['id'] == product_id:
                        if item['quantity'] < stock:
                            item['quantity'] += 1
                            self.update_cart_display()
                            self.statusBar().showMessage(f"✅ បានបន្ថែម {name} មួយទៀត", 2000)
                        else:
                            QMessageBox.warning(self, "ព្រមាន", 
                                              f"{name}\nទំនិញមិនគ្រប់គ្រាន់ក្នុងស្តុក!")
                        return
                
                # Add new item to cart
                self.cart.append({
                    'id': product_id,
                    'name': name,
                    'price': price,
                    'quantity': 1,
                    'stock': stock
                })
                self.update_cart_display()
                self.statusBar().showMessage(f"✅ បានបន្ថែម {name} ទៅកន្ត្រក", 2000)
                
            except Exception as e:
                QMessageBox.critical(self, "កំហុស", f"មិនអាចបន្ថែមទំនិញ: {str(e)}")
    
    def add_by_barcode(self):
        """បន្ថែមទំនិញតាម Barcode"""
        barcode = self.barcode_scanner.text()
        if not barcode:
            return
        
        try:
            product = self.db.get_product_by_barcode(barcode)
            
            if product:
                # Check if product already in cart
                for item in self.cart:
                    if item['id'] == product[0]:
                        if item['quantity'] < product[8]:
                            item['quantity'] += 1
                            self.update_cart_display()
                            self.barcode_scanner.clear()
                            self.statusBar().showMessage(f"✅ បានបន្ថែម {product[1]} មួយទៀត", 2000)
                        else:
                            QMessageBox.warning(self, "ព្រមាន", 
                                              f"{product[1]}\nទំនិញមិនគ្រប់គ្រាន់ក្នុងស្តុក!")
                        return
                
                # Add new item to cart
                self.cart.append({
                    'id': product[0],
                    'name': product[1],
                    'price': product[6],
                    'quantity': 1,
                    'stock': product[8]
                })
                self.update_cart_display()
                self.barcode_scanner.clear()
                self.statusBar().showMessage(f"✅ បានបន្ថែម {product[1]} ទៅកន្ត្រក", 2000)
            else:
                QMessageBox.warning(self, "មិនមានទំនិញ", 
                                   f"រកមិនឃើញទំនិញដែលមានកូដ: {barcode}")
                self.barcode_scanner.clear()
                
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចស្វែងរក Barcode: {str(e)}")
    
    def update_cart_display(self):
        """ធ្វើបច្ចុប្បន្នភាពតារាងកន្ត្រក"""
        self.cart_table.setRowCount(len(self.cart))
        total_usd = 0
        
        for row, item in enumerate(self.cart):
            # ID
            self.cart_table.setItem(row, 0, QTableWidgetItem(str(item['id'])))
            
            # Name
            self.cart_table.setItem(row, 1, QTableWidgetItem(item['name']))
            
            # Price
            price_item = QTableWidgetItem(f"${item['price']:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 2, price_item)
            
            # Quantity with spinbox
            spinbox = QSpinBox()
            spinbox.setMinimum(1)
            spinbox.setMaximum(item['stock'])
            spinbox.setValue(item['quantity'])
            spinbox.valueChanged.connect(lambda v, r=row: self.update_cart_quantity(r, v))
            self.cart_table.setCellWidget(row, 3, spinbox)
            
            # Subtotal
            subtotal = item['price'] * item['quantity']
            total_usd += subtotal
            subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 4, subtotal_item)
            
            # Remove button
            remove_btn = QPushButton("❌")
            remove_btn.setProperty("type", "danger")
            remove_btn.setMaximumWidth(30)
            remove_btn.clicked.connect(lambda checked, r=row: self.remove_cart_item(r))
            self.cart_table.setCellWidget(row, 5, remove_btn)
        
        # Update totals
        self.total_usd = total_usd
        self.update_total_display()
    
    def update_cart_quantity(self, row, quantity):
        """ធ្វើបច្ចុប្បន្នភាពបរិមាណក្នុងកន្ត្រក"""
        if row < len(self.cart):
            self.cart[row]['quantity'] = quantity
            subtotal = self.cart[row]['price'] * quantity
            subtotal_item = QTableWidgetItem(f"${subtotal:.2f}")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.cart_table.setItem(row, 4, subtotal_item)
            
            # Update total
            total_usd = sum(item['price'] * item['quantity'] for item in self.cart)
            self.total_usd = total_usd
            self.update_total_display()
    
    def remove_cart_item(self, row):
        """ដកទំនិញចេញពីកន្ត្រក"""
        if row < len(self.cart):
            removed_item = self.cart.pop(row)
            self.update_cart_display()
            self.statusBar().showMessage(f"✅ បានដក {removed_item['name']} ចេញពីកន្ត្រក", 2000)
    
    def remove_from_cart(self):
        """ដកទំនិញដែលបានជ្រើសចេញពីកន្ត្រក"""
        current_row = self.cart_table.currentRow()
        if current_row >= 0:
            self.remove_cart_item(current_row)
    
    def clear_cart(self):
        """សម្អាតកន្ត្រកទាំងមូល"""
        if self.cart:
            reply = QMessageBox.question(self, 'បញ្ជាក់', 
                                        'តើអ្នកពិតជាចង់សម្អាតកន្ត្រកទាំងមូលមែនទេ?',
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.cart.clear()
                self.update_cart_display()
                self.statusBar().showMessage("✅ បានសម្អាតកន្ត្រក", 2000)
    
    def update_total_display(self):
        """ធ្វើបច្ចុប្បន្នភាពបង្ហាញតម្លៃសរុប"""
        currency = self.total_currency.currentText()
        if 'ដុល្លារ' in currency:
            self.total_amount_label.setText(f"${self.total_usd:.2f}")
        else:
            total_khr = self.total_usd * self.exchange_rate
            self.total_amount_label.setText(f"{total_khr:,.0f}៛")
    
    def checkout(self):
        """បញ្ចប់ការលក់"""
        if not self.cart:
            QMessageBox.warning(self, 'ព្រមាន', 'សូមបន្ថែមទំនិញទៅកន្ត្រកមុនពេលបញ្ចប់ការលក់!')
            return
        
        # Open payment dialog
        from payment_dialog import PaymentDialog
        dialog = PaymentDialog(self, self.total_usd, self.cart, self.customer_name.text(), self.customer_phone.text())
        
        if dialog.exec_() == QDialog.Accepted:
            # Clear cart and refresh
            self.cart.clear()
            self.update_cart_display()
            self.customer_name.clear()
            self.customer_phone.clear()
            self.load_products()
            self.load_inventory()
            self.update_statistics()
    
    def add_product_dialog(self):
        """បើក dialog បន្ថែមទំនិញថ្មី"""
        from product_dialog import ProductDialog
        dialog = ProductDialog(self)
        
        if dialog.exec_() == QDialog.Accepted:
            self.load_products()
            self.load_inventory()
            self.update_statistics()
    
    def edit_product_dialog(self):
        """បើក dialog កែប្រែទំនិញ"""
        current_row = self.inventory_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'ព្រមាន', 'សូមជ្រើសរើសទំនិញដែលចង់កែប្រែ!')
            return
        
        product_id = int(self.inventory_table.item(current_row, 0).text())
        product = self.db.get_product_by_id(product_id)
        
        if product:
            from product_dialog import ProductDialog
            dialog = ProductDialog(self, product_data=product)
            
            if dialog.exec_() == QDialog.Accepted:
                self.load_products()
                self.load_inventory()
                self.update_statistics()
    
    def delete_product(self):
        """លុបទំនិញ"""
        current_row = self.inventory_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, 'ព្រមាន', 'សូមជ្រើសរើសទំនិញដែលចង់លុប!')
            return
        
        product_name = self.inventory_table.item(current_row, 2).text()
        product_id = int(self.inventory_table.item(current_row, 0).text())
        
        reply = QMessageBox.question(self, 'បញ្ជាក់ការលុប',
                                   f'តើអ្នកពិតជាចង់លុបទំនិញ "{product_name}" មែនទេ?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.db.delete_product(product_id)
                self.load_products()
                self.load_inventory()
                self.update_statistics()
                QMessageBox.information(self, 'ជោគជ័យ', 'លុបទំនិញរួចរាល់!')
            except Exception as e:
                QMessageBox.critical(self, 'កំហុស', f'មិនអាចលុបទំនិញ: {str(e)}')
    
    def export_inventory(self):
        """នាំចេញស្តុកទំនិញ"""
        try:
            import csv
            
            filename, _ = QFileDialog.getSaveFileName(self, 'រក្សាទុកឯកសារ', 
                                                      f'inventory_{datetime.now().strftime("%Y%m%d")}.csv', 
                                                      'CSV Files (*.csv)')
            
            if filename:
                products = self.db.get_all_products()
                
                with open(filename, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    
                    # Write headers
                    headers = ['ID', 'ឈ្មោះ', 'ប្រភេទ', 'បាកូដ', 'តម្លៃដើម', 'តម្លៃលក់', 'ស្តុក', 'ស្តុកអប្បបរមា']
                    writer.writerow(headers)
                    
                    # Write data
                    for p in products:
                        writer.writerow([p[0], p[1], p[2], p[3], p[4], p[6], p[8], p[9]])
                
                QMessageBox.information(self, 'ជោគជ័យ', f'បាននាំចេញទិន្នន័យទៅ {filename}')
                
        except Exception as e:
            QMessageBox.critical(self, 'កំហុស', f'មិនអាចនាំចេញទិន្នន័យ: {str(e)}')
    
    def generate_report(self):
        """បង្កើតរបាយការណ៍"""
        report_type = self.report_type.currentText()
        start = self.start_date.date().toString('yyyy-MM-dd')
        end = self.end_date.date().toString('yyyy-MM-dd')
        
        try:
            if report_type == 'របាយការណ៍លក់ប្រចាំថ្ងៃ':
                self.generate_daily_sales_report(start, end)
            elif report_type == 'របាយការណ៍លក់ប្រចាំខែ':
                self.generate_monthly_sales_report(start, end)
            elif report_type == 'របាយការណ៍ស្តុក':
                self.generate_stock_report()
            elif report_type == 'របាយការណ៍ប្រាក់ចំណេញ':
                self.generate_profit_report(start, end)
                
        except Exception as e:
            QMessageBox.critical(self, 'កំហុស', f'មិនអាចបង្កើតរបាយការណ៍: {str(e)}')
    
    def generate_daily_sales_report(self, start, end):
        """បង្កើតរបាយការណ៍លក់ប្រចាំថ្ងៃ"""
        sales = self.db.get_sales_report(start, end)
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║                 របាយការណ៍លក់ប្រចាំថ្ងៃ                      ║
╠════════════════════════════════════════════════════════════════╣
║ ចាប់ពីថ្ងៃទី: {start}                                   
║ ដល់ថ្ងៃទី: {end}                                         
╠════════════════════════════════════════════════════════════════╣
"""
        
        if sales:
            for sale in sales:
                report += f"""
║ {sale[0]}: {sale[1]} ប្រតិបត្តិការ, ${sale[2]:.2f}, មធ្យម ${sale[3]:.2f}
"""
        else:
            report += "\n║ គ្មានទិន្នន័យលក់ក្នុងអំឡុងពេលនេះ"
        
        report += """
╚════════════════════════════════════════════════════════════════╝
"""
        
        self.report_text.setText(report)
    
    def generate_monthly_sales_report(self, start, end):
        """បង្កើតរបាយការណ៍លក់ប្រចាំខែ"""
        # This would need a different query
        self.report_text.setText("មុខងារនេះកំពុងអភិវឌ្ឍន៍...")
    
    def generate_stock_report(self):
        """បង្កើតរបាយការណ៍ស្តុក"""
        low_stock = self.db.get_low_stock_products()
        out_of_stock = self.db.get_out_of_stock_products()
        stats = self.db.get_statistics()
        
        report = f"""
╔════════════════════════════════════════════════════════════════╗
║                    របាយការណ៍ស្តុកទំនិញ                        ║
╠════════════════════════════════════════════════════════════════╣
║ ស្ថិតិទូទៅ:                                                
║   • ទំនិញសរុប: {stats.get('total_products', 0)} មុខ
║   • ស្តុកសរុប: {stats.get('total_stock', 0)} ដុំ
║   • ទំនិញមានរូបភាព: {stats.get('products_with_image', 0)} មុខ
╠════════════════════════════════════════════════════════════════╣
║ ទំនិញជិតអស់ស្តុក ({len(low_stock)} មុខ):                              
"""
        
        if low_stock:
            for item in low_stock:
                report += f"║   • {item[0][:30]:30} : {item[1]}/{item[2]}\n"
        else:
            report += "║   គ្មានទំនិញជិតអស់ស្តុក\n"
        
        report += f"""
╠════════════════════════════════════════════════════════════════╣
║ ទំនិញអស់ស្តុក ({len(out_of_stock)} មុខ):                                   
"""
        
        if out_of_stock:
            for item in out_of_stock:
                report += f"║   • {item[0][:30]:30}\n"
        else:
            report += "║   គ្មានទំនិញអស់ស្តុក\n"
        
        report += """
╚════════════════════════════════════════════════════════════════╝
"""
        
        self.report_text.setText(report)
    
    def generate_profit_report(self, start, end):
        """បង្កើតរបាយការណ៍ប្រាក់ចំណេញ"""
        self.report_text.setText("មុខងារនេះកំពុងអភិវឌ្ឍន៍...")
    
    def export_report_pdf(self):
        """នាំចេញរបាយការណ៍ជា PDF"""
        QMessageBox.information(self, 'ព័ត៌មាន', 'មុខងារនាំចេញ PDF កំពុងអភិវឌ្ឍន៍')
    
    def export_report_excel(self):
        """នាំចេញរបាយការណ៍ជា Excel"""
        QMessageBox.information(self, 'ព័ត៌មាន', 'មុខងារនាំចេញ Excel កំពុងអភិវឌ្ឍន៍')
    
    def backup_database(self):
        """បម្រុងទុក database"""
        backup_file = self.db.backup_database()
        if backup_file:
            QMessageBox.information(self, 'ជោគជ័យ', f'បានបម្រុងទុក database ទៅ:\n{backup_file}')
        else:
            QMessageBox.critical(self, 'កំហុស', 'មិនអាចបម្រុងទុក database បានទេ')
    
    def refresh_all(self):
        """ធ្វើឱ្យទិន្នន័យទាំងអស់ថ្មី"""
        self.load_products()
        self.load_inventory()
        self.update_statistics()
        self.statusBar().showMessage("✅ បានធ្វើឱ្យទិន្នន័យថ្មី", 2000)
    
    def closeEvent(self, event):
        """បិទការភ្ជាប់ database ពេលបិទកម្មវិធី"""
        reply = QMessageBox.question(self, 'បញ្ជាក់',
                                    'តើអ្នកចង់បិទកម្មវិធីមែនទេ?',
                                    QMessageBox.Yes | QMessageBox.No,
                                    QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.db.close()
            event.accept()
        else:
            event.ignore()

def main():
    app = QApplication(sys.argv)
    
    # កំណត់រចនាប័ទ្ម
    app.setStyle('Fusion')
    
    # កំណត់ font សម្រាប់ភាសាខ្មែរ
    font = QFont('Khmer OS', 10)
    app.setFont(font)
    
    # បង្កើត MainWindow
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()