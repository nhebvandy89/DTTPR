# product_dialog.py
import os
import shutil
import uuid
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_dialog = parent
        self.setAlignment(Qt.AlignCenter)
        self.setText("ចុចទ្វេដងដើម្បីជ្រើសរូបភាព")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #cccccc;
                border-radius: 5px;
                background-color: #f9f9f9;
                min-height: 200px;
                max-height: 200px;
                min-width: 200px;
                max-width: 200px;
                padding: 5px;
            }
            QLabel:hover {
                border-color: #4CAF50;
                background-color: #e8f5e8;
            }
        """)
    
    def mouseDoubleClickEvent(self, event):
        if self.parent_dialog:
            self.parent_dialog.select_image()

class ProductDialog(QDialog):
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.parent_window = parent
        self.product_data = product_data
        self.image_path = None
        
        self.setWindowTitle('បន្ថែមទំនិញថ្មី' if not product_data else 'កែប្រែទំនិញ')
        self.setModal(True)
        self.setMinimumWidth(800)
        
        self.initUI()
        
        if product_data:
            self.load_product_data()
    
    def initUI(self):
        layout = QHBoxLayout(self)
        
        # Left panel - Image
        left_panel = QWidget()
        left_panel.setMaximumWidth(250)
        left_layout = QVBoxLayout(left_panel)
        
        self.image_label = ImageLabel(self)
        left_layout.addWidget(self.image_label)
        
        # Image buttons
        image_btn_layout = QHBoxLayout()
        
        self.select_btn = QPushButton("ជ្រើសរូបភាព")
        self.select_btn.clicked.connect(self.select_image)
        image_btn_layout.addWidget(self.select_btn)
        
        self.clear_btn = QPushButton("សម្អាត")
        self.clear_btn.clicked.connect(self.clear_image)
        self.clear_btn.setEnabled(False)
        image_btn_layout.addWidget(self.clear_btn)
        
        left_layout.addLayout(image_btn_layout)
        left_layout.addStretch()
        
        # Right panel - Form
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        scroll_widget = QWidget()
        form_layout = QFormLayout(scroll_widget)
        form_layout.setSpacing(10)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("បញ្ចូលឈ្មោះទំនិញ...")
        form_layout.addRow('ឈ្មោះទំនិញ:', self.name_input)
        
        # Category
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItems(['សៀវភៅ', 'សៀវភៅកត់ត្រា', 'ប៊ិក', 'ខ្មៅដៃ', 'បន្ទាត់', 'កាបូប', 'ម៉ាស៊ីនគិតលេខ', 'ក្រដាស'])
        form_layout.addRow('ប្រភេទ:', self.category_input)
        
        # Barcode
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("បញ្ចូលកូដទំនិញ...")
        form_layout.addRow('កូដទំនិញ:', self.barcode_input)
        
        # Cost price
        cost_layout = QHBoxLayout()
        self.cost_price = QDoubleSpinBox()
        self.cost_price.setRange(0, 10000)
        self.cost_price.setPrefix("$ ")
        self.cost_price.setValue(0)
        cost_layout.addWidget(self.cost_price)
        
        self.cost_currency = QComboBox()
        self.cost_currency.addItems(['USD', 'KHR'])
        cost_layout.addWidget(self.cost_currency)
        form_layout.addRow('តម្លៃដើម:', cost_layout)
        
        # Selling price
        sell_layout = QHBoxLayout()
        self.sell_price = QDoubleSpinBox()
        self.sell_price.setRange(0, 10000)
        self.sell_price.setPrefix("$ ")
        self.sell_price.setValue(0)
        sell_layout.addWidget(self.sell_price)
        
        self.sell_currency = QComboBox()
        self.sell_currency.addItems(['USD', 'KHR'])
        sell_layout.addWidget(self.sell_currency)
        form_layout.addRow('តម្លៃលក់:', sell_layout)
        
        # Stock
        stock_layout = QHBoxLayout()
        self.stock_input = QSpinBox()
        self.stock_input.setRange(0, 999999)
        self.stock_input.setValue(0)
        self.stock_input.setSuffix(" ដុំ")
        stock_layout.addWidget(self.stock_input)
        
        self.min_stock = QSpinBox()
        self.min_stock.setRange(0, 999999)
        self.min_stock.setValue(5)
        stock_layout.addWidget(QLabel("ស្តុកអប្បបរមា:"))
        stock_layout.addWidget(self.min_stock)
        form_layout.addRow('បរិមាណស្តុក:', stock_layout)
        
        # Description
        self.desc_input = QTextEdit()
        self.desc_input.setMaximumHeight(100)
        self.desc_input.setPlaceholderText("បញ្ចូលការពិពណ៌នាបន្ថែម...")
        form_layout.addRow('បរិយាយ:', self.desc_input)
        
        # Options
        options_layout = QHBoxLayout()
        
        self.tax_check = QCheckBox("គិតពន្ធ")
        self.tax_check.setChecked(True)
        options_layout.addWidget(self.tax_check)
        
        self.discount_check = QCheckBox("អាចបញ្ចុះតម្លៃបាន")
        self.discount_check.setChecked(True)
        options_layout.addWidget(self.discount_check)
        
        self.active_check = QCheckBox("សកម្ម")
        self.active_check.setChecked(True)
        options_layout.addWidget(self.active_check)
        
        form_layout.addRow('ជម្រើស:', options_layout)
        
        scroll.setWidget(scroll_widget)
        right_layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("រក្សាទុក")
        self.save_btn.clicked.connect(self.save_product)
        
        self.cancel_btn = QPushButton("បោះបង់")
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        right_layout.addLayout(button_layout)
        
        # Add panels
        layout.addWidget(left_panel)
        layout.addWidget(right_panel, 1)
    
    def select_image(self):
        """ជ្រើសរើសរូបភាព"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self, 
            "ជ្រើសរូបភាពទំនិញ", 
            "", 
            "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        
        if file_path:
            self.load_image(file_path)
    
    def load_image(self, file_path):
        """ផ្ទុករូបភាព"""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(190, 190, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(scaled)
            self.image_path = file_path
            self.clear_btn.setEnabled(True)
    
    def clear_image(self):
        """សម្អាតរូបភាព"""
        self.image_label.clear()
        self.image_label.setText("ចុចទ្វេដងដើម្បីជ្រើសរូបភាព")
        self.image_path = None
        self.clear_btn.setEnabled(False)
    
    def save_product_image(self):
        """រក្សាទុករូបភាព"""
        if self.image_path and os.path.exists(self.image_path):
            # Generate unique filename
            ext = os.path.splitext(self.image_path)[1]
            new_filename = f"{uuid.uuid4().hex}{ext}"
            new_path = os.path.join('product_images', new_filename)
            
            # Create directory if not exists
            if not os.path.exists('product_images'):
                os.makedirs('product_images')
            
            # Copy image
            shutil.copy2(self.image_path, new_path)
            return new_path
        
        return None
    
    def save_product(self):
        """រក្សាទុកទំនិញ"""
        # Validate
        if not self.name_input.text().strip():
            QMessageBox.warning(self, 'ព្រមាន', 'សូមបញ្ចូលឈ្មោះទំនិញ!')
            return
        
        try:
            # Save image
            image_path = self.save_product_image()
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if self.product_data:  # Update
                # Prepare update data
                update_data = [
                    self.name_input.text().strip(),
                    self.category_input.currentText(),
                    self.barcode_input.text().strip() or None,
                    self.cost_price.value(),
                    self.cost_currency.currentText(),
                    self.sell_price.value(),
                    self.sell_currency.currentText(),
                    self.stock_input.value(),
                    self.min_stock.value(),
                    self.desc_input.toPlainText().strip(),
                    image_path if image_path else self.product_data[11],
                    1 if self.tax_check.isChecked() else 0,
                    1 if self.discount_check.isChecked() else 0,
                    1 if self.active_check.isChecked() else 0,
                    current_time
                ]
                
                self.parent_window.db.update_product(self.product_data[0], update_data)
                QMessageBox.information(self, 'ជោគជ័យ', 'កែប្រែទំនិញរួចរាល់!')
                
            else:  # Insert
                # Prepare insert data
                insert_data = [
                    self.name_input.text().strip(),
                    self.category_input.currentText(),
                    self.barcode_input.text().strip() or None,
                    self.cost_price.value(),
                    self.cost_currency.currentText(),
                    self.sell_price.value(),
                    self.sell_currency.currentText(),
                    self.stock_input.value(),
                    self.min_stock.value(),
                    self.desc_input.toPlainText().strip(),
                    image_path,
                    1 if self.tax_check.isChecked() else 0,
                    1 if self.discount_check.isChecked() else 0,
                    1 if self.active_check.isChecked() else 0,
                    current_time,
                    current_time
                ]
                
                self.parent_window.db.insert_product(insert_data)
                QMessageBox.information(self, 'ជោគជ័យ', 'បន្ថែមទំនិញថ្មីរួចរាល់!')
            
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, 'កំហុស', str(e))
    
    def load_product_data(self):
        """ផ្ទុកទិន្នន័យទំនិញសម្រាប់កែប្រែ"""
        if self.product_data:
            self.name_input.setText(self.product_data[1])
            self.category_input.setCurrentText(self.product_data[2] or '')
            self.barcode_input.setText(self.product_data[3] or '')
            self.cost_price.setValue(self.product_data[4])
            self.cost_currency.setCurrentText(self.product_data[5])
            self.sell_price.setValue(self.product_data[6])
            self.sell_currency.setCurrentText(self.product_data[7])
            self.stock_input.setValue(self.product_data[8])
            self.min_stock.setValue(self.product_data[9])
            self.desc_input.setText(self.product_data[10] or '')
            
            if self.product_data[11] and os.path.exists(self.product_data[11]):
                self.load_image(self.product_data[11])
            
            self.tax_check.setChecked(bool(self.product_data[12]))
            self.discount_check.setChecked(bool(self.product_data[13]))
            self.active_check.setChecked(bool(self.product_data[14]))