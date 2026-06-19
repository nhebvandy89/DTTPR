import sys
import os
import json
import cv2
import qrcode
import pyperclip
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class DocumentRecorderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data_file = "documents.json"
        self.documents = []
        self.scanned_documents = []
        self.load_data()
        self.init_ui()
        
    def init_ui(self):
        # កំណត់លក្ខណៈរបស់ផ្ទាំងអេក្រង់
        self.setWindowTitle("កម្មវិធីថតឯកសារ និងស្វែងរកឯកសារ")
        self.setGeometry(100, 100, 1000, 700)
        
        # បង្កើតពុម្ពអក្សរសម្រាប់ភាសាខ្មែរ
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        
        # បង្កើត widget មូលដ្ឋាន
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # បង្កើត layout មេ
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # ផ្នែកខាងលើ៖ ចំណងជើង និងបញ្ចូលទិន្នន័យ
        top_layout = QVBoxLayout()
        
        # ចំណងជើង
        title_label = QLabel("កម្មវិធីថតឯកសារ និងស្វែងរកឯកសារ")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; padding: 10px;")
        
        top_layout.addWidget(title_label)
        
        # បង្កើតផ្ទាំង tab
        self.tab_widget = QTabWidget()
        
        # ផ្ទាំងថតឯកសារ
        self.create_record_tab()
        
        # ផ្ទាំងស្វែងរកឯកសារ
        self.create_search_tab()
        
        # ផ្ទាំងបញ្ជីឯកសារទាំងអស់
        self.create_list_tab()
        
        # ផ្ទាំងថតឯកសារ (ស្កេន)
        self.create_scan_tab()
        
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.tab_widget)
        
        # បង្ហាញស្ថានភាព
        self.statusBar().showMessage("រួចរាល់សម្រាប់ប្រើប្រាស់")
        
    def create_record_tab(self):
        """បង្កើតផ្ទាំងសម្រាប់ថតឯកសារ"""
        record_tab = QWidget()
        layout = QVBoxLayout()
        
        # ក្រុមបញ្ចូលព័ត៌មានឯកសារ
        form_group = QGroupBox("បញ្ចូលព័ត៌មានឯកសារ")
        form_layout = QFormLayout()
        
        # ឈ្មោះឯកសារ
        self.doc_name_input = QLineEdit()
        self.doc_name_input.setPlaceholderText("ឧ. លិខិតស្នាម លេខ ១២៣")
        form_layout.addRow("ឈ្មោះឯកសារ:", self.doc_name_input)
        
        # ប្រភេទឯកសារ
        self.doc_type_combo = QComboBox()
        self.doc_type_combo.addItems(["លិខិតស្នាម", "របាយការណ៍", "កិច្ចសន្យា", "ឯកសារផ្ទេរ", "ឯកសារផ្សេងៗ"])
        form_layout.addRow("ប្រភេទឯកសារ:", self.doc_type_combo)
        
        # លេខឯកសារ
        self.doc_number_input = QLineEdit()
        self.doc_number_input.setPlaceholderText("ឧ. ១២៣/២៤")
        form_layout.addRow("លេខឯកសារ:", self.doc_number_input)
        
        # កាលបរិច្ឆេទ
        date_layout = QHBoxLayout()
        self.doc_date_input = QDateEdit()
        self.doc_date_input.setDate(QDate.currentDate())
        self.doc_date_input.setCalendarPopup(True)
        date_layout.addWidget(self.doc_date_input)
        
        date_today_btn = QPushButton("ថ្ងៃនេះ")
        date_today_btn.clicked.connect(lambda: self.doc_date_input.setDate(QDate.currentDate()))
        date_layout.addWidget(date_today_btn)
        
        form_layout.addRow("កាលបរិច្ឆេទ:", date_layout)
        
        # ពណ៌នា
        self.doc_description_input = QTextEdit()
        self.doc_description_input.setMaximumHeight(100)
        self.doc_description_input.setPlaceholderText("បញ្ចូលពណ៌នាអំពីឯកសារ...")
        form_layout.addRow("ពណ៌នា:", self.doc_description_input)
        
        # ស្ថានភាព
        self.doc_status_combo = QComboBox()
        self.doc_status_combo.addItems(["ថ្មី", "កំពុងដំណើរការ", "រួចរាល់", "បានបញ្ចប់"])
        form_layout.addRow("ស្ថានភាព:", self.doc_status_combo)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # ប៊ូតុងរក្សាទុក
        button_layout = QHBoxLayout()
        save_btn = QPushButton("រក្សាទុកឯកសារ")
        save_btn.setIcon(QIcon.fromTheme("document-save"))
        save_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 8px; font-weight: bold;")
        save_btn.clicked.connect(self.save_document)
        
        clear_btn = QPushButton("លុបចេញទាំងអស់")
        clear_btn.setIcon(QIcon.fromTheme("edit-clear"))
        clear_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px;")
        clear_btn.clicked.connect(self.clear_form)
        
        generate_qr_btn = QPushButton("បង្កើត QR Code")
        generate_qr_btn.setIcon(QIcon.fromTheme("insert-link"))
        generate_qr_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 8px;")
        generate_qr_btn.clicked.connect(self.generate_qr_code)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addWidget(generate_qr_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        record_tab.setLayout(layout)
        self.tab_widget.addTab(record_tab, "ថតឯកសារ")
        
    def create_search_tab(self):
        """បង្កើតផ្ទាំងសម្រាប់ស្វែងរកឯកសារ"""
        search_tab = QWidget()
        layout = QVBoxLayout()
        
        # ក្រុមស្វែងរក
        search_group = QGroupBox("ស្វែងរកឯកសារ")
        search_layout = QVBoxLayout()
        
        # បញ្ចូលស្វែងរក
        search_input_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("បញ្ចូលពាក្យសម្រាប់ស្វែងរក...")
        self.search_input.returnPressed.connect(self.search_documents)
        search_input_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("ស្វែងរក")
        search_btn.setIcon(QIcon.fromTheme("system-search"))
        search_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px;")
        search_btn.clicked.connect(self.search_documents)
        search_input_layout.addWidget(search_btn)
        
        search_layout.addLayout(search_input_layout)
        
        # ជម្រើសការស្វែងរក
        filter_layout = QHBoxLayout()
        
        self.search_type_combo = QComboBox()
        self.search_type_combo.addItems(["ទាំងអស់", "ឈ្មោះ", "លេខ", "ប្រភេទ", "ពណ៌នា"])
        filter_layout.addWidget(QLabel("ស្វែងរកតាម:"))
        filter_layout.addWidget(self.search_type_combo)
        
        self.search_status_combo = QComboBox()
        self.search_status_combo.addItems(["ស្ថានភាពទាំងអស់", "ថ្មី", "កំពុងដំណើរការ", "រួចរាល់", "បានបញ្ចប់"])
        filter_layout.addWidget(QLabel("ស្ថានភាព:"))
        filter_layout.addWidget(self.search_status_combo)
        
        search_layout.addLayout(filter_layout)
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # តារាងលទ្ធផលស្វែងរក
        results_group = QGroupBox("លទ្ធផលស្វែងរក")
        results_layout = QVBoxLayout()
        
        self.search_results_table = QTableWidget()
        self.search_results_table.setColumnCount(7)
        self.search_results_table.setHorizontalHeaderLabels(["ល.រ", "ឈ្មោះឯកសារ", "ប្រភេទ", "លេខ", "កាលបរិច្ឆេទ", "ស្ថានភាព", "សកម្មភាព"])
        self.search_results_table.horizontalHeader().setStretchLastSection(True)
        self.search_results_table.setAlternatingRowColors(True)
        
        results_layout.addWidget(self.search_results_table)
        results_group.setLayout(results_layout)
        
        layout.addWidget(results_group)
        search_tab.setLayout(layout)
        self.tab_widget.addTab(search_tab, "ស្វែងរកឯកសារ")
        
    def create_list_tab(self):
        """បង្កើតផ្ទាំងបញ្ជីឯកសារទាំងអស់"""
        list_tab = QWidget()
        layout = QVBoxLayout()
        
        # ប៊ូតុងផ្ទេរ
        list_buttons_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("ផ្ទុកឡើងវិញ")
        refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_btn.clicked.connect(self.load_all_documents)
        list_buttons_layout.addWidget(refresh_btn)
        
        export_btn = QPushButton("នាំចេញទិន្នន័យ")
        export_btn.setIcon(QIcon.fromTheme("document-save-as"))
        export_btn.clicked.connect(self.export_data)
        list_buttons_layout.addWidget(export_btn)
        
        delete_all_btn = QPushButton("លុបទាំងអស់")
        delete_all_btn.setIcon(QIcon.fromTheme("edit-delete"))
        delete_all_btn.setStyleSheet("background-color: #c0392b; color: white;")
        delete_all_btn.clicked.connect(self.delete_all_documents)
        list_buttons_layout.addWidget(delete_all_btn)
        
        list_buttons_layout.addStretch()
        layout.addLayout(list_buttons_layout)
        
        # តារាងឯកសារទាំងអស់
        self.all_documents_table = QTableWidget()
        self.all_documents_table.setColumnCount(8)
        self.all_documents_table.setHorizontalHeaderLabels(["ល.រ", "ឈ្មោះឯកសារ", "ប្រភេទ", "លេខ", "កាលបរិច្ឆេទ", "ស្ថានភាព", "QR Code", "សកម្មភាព"])
        self.all_documents_table.horizontalHeader().setStretchLastSection(True)
        self.all_documents_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.all_documents_table)
        list_tab.setLayout(layout)
        self.tab_widget.addTab(list_tab, "បញ្ជីឯកសារទាំងអស់")
        
        # ផ្ទុកទិន្នន័យដំបូង
        self.load_all_documents()
        
    def create_scan_tab(self):
        """បង្កើតផ្ទាំងសម្រាប់ថតឯកសារ"""
        scan_tab = QWidget()
        layout = QVBoxLayout()
        
        # ផ្នែកខាងលើ៖ ប៊ូតុងសកម្មភាព
        scan_buttons_layout = QHBoxLayout()
        
        scan_camera_btn = QPushButton("ថតឯកសារពីកាមេរ៉ា")
        scan_camera_btn.setIcon(QIcon.fromTheme("camera-web"))
        scan_camera_btn.setStyleSheet("background-color: #3498db; color: white; padding: 8px; font-weight: bold;")
        scan_camera_btn.clicked.connect(self.scan_from_camera)
        
        scan_file_btn = QPushButton("ជ្រើសរើសឯកសាររូបភាព")
        scan_file_btn.setIcon(QIcon.fromTheme("folder-pictures"))
        scan_file_btn.setStyleSheet("background-color: #2ecc71; color: white; padding: 8px;")
        scan_file_btn.clicked.connect(self.scan_from_file)
        
        process_scan_btn = QPushButton("ដំណើរការការស្កេន")
        process_scan_btn.setIcon(QIcon.fromTheme("edit-find"))
        process_scan_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 8px;")
        process_scan_btn.clicked.connect(self.process_scanned_image)
        
        scan_buttons_layout.addWidget(scan_camera_btn)
        scan_buttons_layout.addWidget(scan_file_btn)
        scan_buttons_layout.addWidget(process_scan_btn)
        scan_buttons_layout.addStretch()
        
        layout.addLayout(scan_buttons_layout)
        
        # ផ្នែកកណ្តាល៖ រូបភាពស្កេន
        image_layout = QHBoxLayout()
        
        # ផ្នែកខាងឆ្វេង៖ រូបភាពដើម
        original_group = QGroupBox("រូបភាពដើម")
        original_layout = QVBoxLayout()
        
        self.original_image_label = QLabel()
        self.original_image_label.setAlignment(Qt.AlignCenter)
        self.original_image_label.setStyleSheet("border: 2px dashed #7f8c8d; background-color: #ecf0f1;")
        self.original_image_label.setMinimumSize(400, 300)
        self.original_image_label.setText("រូបភាពដើម\n(នឹងបង្ហាញនៅទីនេះ)")
        self.original_image_label.setWordWrap(True)
        
        original_layout.addWidget(self.original_image_label)
        
        # ព័ត៌មានរូបភាព
        self.image_info_label = QLabel("ទំហំឯកសារ: N/A | ទំហំរូបភាព: N/A")
        self.image_info_label.setStyleSheet("color: #7f8c8d; font-size: 10pt; padding: 5px;")
        original_layout.addWidget(self.image_info_label)
        
        original_group.setLayout(original_layout)
        image_layout.addWidget(original_group)
        
        # ផ្នែកខាងស្តាំ៖ រូបភាពបន្ទាប់ពីដំណើរការ
        processed_group = QGroupBox("រូបភាពបន្ទាប់ពីដំណើរការ")
        processed_layout = QVBoxLayout()
        
        self.processed_image_label = QLabel()
        self.processed_image_label.setAlignment(Qt.AlignCenter)
        self.processed_image_label.setStyleSheet("border: 2px dashed #7f8c8d; background-color: #ecf0f1;")
        self.processed_image_label.setMinimumSize(400, 300)
        self.processed_image_label.setText("រូបភាពបន្ទាប់ពីដំណើរការ\n(នឹងបង្ហាញនៅទីនេះ)")
        self.processed_image_label.setWordWrap(True)
        
        processed_layout.addWidget(self.processed_image_label)
        
        # ប៊ូតុងរក្សាទុករូបភាព
        save_image_layout = QHBoxLayout()
        
        save_processed_btn = QPushButton("រក្សាទុករូបភាព")
        save_processed_btn.setIcon(QIcon.fromTheme("document-save-as"))
        save_processed_btn.setStyleSheet("background-color: #f39c12; color: white; padding: 6px;")
        save_processed_btn.clicked.connect(self.save_processed_image)
        save_processed_btn.setEnabled(False)
        self.save_processed_btn = save_processed_btn
        
        copy_text_btn = QPushButton("ចម្លងអត្ថបទ")
        copy_text_btn.setIcon(QIcon.fromTheme("edit-copy"))
        copy_text_btn.setStyleSheet("background-color: #1abc9c; color: white; padding: 6px;")
        copy_text_btn.clicked.connect(self.copy_scanned_text)
        copy_text_btn.setEnabled(False)
        self.copy_text_btn = copy_text_btn
        
        save_image_layout.addWidget(save_processed_btn)
        save_image_layout.addWidget(copy_text_btn)
        save_image_layout.addStretch()
        
        processed_layout.addLayout(save_image_layout)
        
        processed_group.setLayout(processed_layout)
        image_layout.addWidget(processed_group)
        
        layout.addLayout(image_layout)
        
        # ផ្នែកខាងក្រោម៖ អត្ថបទដែលបានស្កេន
        text_group = QGroupBox("អត្ថបទដែលបានស្កេន")
        text_layout = QVBoxLayout()
        
        self.scanned_text_edit = QTextEdit()
        self.scanned_text_edit.setPlaceholderText("អត្ថបទដែលបានស្កេននឹងបង្ហាញនៅទីនេះ...")
        self.scanned_text_edit.setMaximumHeight(150)
        
        text_layout.addWidget(self.scanned_text_edit)
        
        # ប៊ូតុងសម្រាប់អត្ថបទ
        text_buttons_layout = QHBoxLayout()
        
        clear_text_btn = QPushButton("សម្អាតអត្ថបទ")
        clear_text_btn.setIcon(QIcon.fromTheme("edit-clear"))
        clear_text_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 6px;")
        clear_text_btn.clicked.connect(self.clear_scanned_text)
        
        create_doc_btn = QPushButton("បង្កើតឯកសារពីអត្ថបទ")
        create_doc_btn.setIcon(QIcon.fromTheme("document-new"))
        create_doc_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 6px;")
        create_doc_btn.clicked.connect(self.create_document_from_text)
        
        text_buttons_layout.addWidget(clear_text_btn)
        text_buttons_layout.addWidget(create_doc_btn)
        text_buttons_layout.addStretch()
        
        text_layout.addLayout(text_buttons_layout)
        text_group.setLayout(text_layout)
        
        layout.addWidget(text_group)
        
        scan_tab.setLayout(layout)
        self.tab_widget.addTab(scan_tab, "ថតឯកសារ")
        
        # អថេរសម្រាប់រូបភាព
        self.current_image = None
        self.processed_image = None
        self.scanned_text = ""
        
    def load_data(self):
        """ផ្ទុកទិន្នន័យពីឯកសារ"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
        except Exception as e:
            print(f"មិនអាចផ្ទុកទិន្នន័យបានទេ: {str(e)}")
            self.documents = []
            
    def save_data(self):
        """រក្សាទុកទិន្នន័យទៅឯកសារ"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"មិនអាចរក្សាទុកទិន្នន័យបានទេ: {str(e)}")
    
    def scan_from_camera(self):
        """ថតឯកសារពីកាមេរ៉ា"""
        try:
            # ប្រើ OpenCV ដើម្បីបើកកាមេរ៉ា
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                QMessageBox.warning(self, "ការព្រមាន", "មិនអាចបើកកាមេរ៉ាបានទេ!")
                return
            
            self.statusBar().showMessage("ចុច 'q' ដើម្បីថតរូបភាព ឬ 'ESC' ដើម្បីបោះបង់")
            
            # បង្ហាញប្រអប់កាមេរ៉ា
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                    
                # បង្ហាញរូបភាពក្នុងប្រអប់
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_frame.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                pixmap = QPixmap.fromImage(qt_image)
                scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio)
                
                # បង្ហាញរូបភាពក្នុង label
                self.original_image_label.setPixmap(scaled_pixmap)
                
                # សម្រាប់បង្ហាញក្នុងប្រអប់ OpenCV
                cv2.imshow('ថតឯកសារ - ចុច "q" ដើម្បីថត ឬ "ESC" ដើម្បីបោះបង់', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q') or key == ord('Q'):  # ថតរូបភាព
                    self.current_image = frame.copy()
                    self.statusBar().showMessage("រូបភាពត្រូវបានថតដោយជោគជ័យ")
                    break
                elif key == 27:  # ESC key
                    self.statusBar().showMessage("បានបោះបង់ការថត")
                    break
            
            # បិទកាមេរ៉ា និងបង្អួច
            cap.release()
            cv2.destroyAllWindows()
            
            if self.current_image is not None:
                # បង្ហាញព័ត៌មានរូបភាព
                height, width, _ = self.current_image.shape
                self.image_info_label.setText(f"ទំហំឯកសារ: រូបភាពកាមេរ៉ា | ទំហំរូបភាព: {width}x{height}px")
                
                # បង្ហាញរូបភាពដើម
                self.display_original_image()
                
                # បើកដំណើរការរូបភាពដោយស្វ័យប្រវត្តិ
                self.process_scanned_image()
                
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចថតរូបភាពបានទេ: {str(e)}")
    
    def scan_from_file(self):
        """ជ្រើសរើសឯកសាររូបភាពពីកុំព្យូទ័រ"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "ជ្រើសរើសរូបភាព", 
            "", 
            "ឯកសាររូបភាព (*.png *.jpg *.jpeg *.bmp *.tiff);;ឯកសារទាំងអស់ (*.*)"
        )
        
        if file_path:
            try:
                # អានរូបភាពដោយប្រើ OpenCV
                self.current_image = cv2.imread(file_path)
                
                if self.current_image is None:
                    QMessageBox.warning(self, "ការព្រមាន", "មិនអាចអានឯកសាររូបភាពនេះបានទេ!")
                    return
                
                # បង្ហាញព័ត៌មានឯកសារ
                file_size = os.path.getsize(file_path) / 1024  # ប្តូរទៅ KB
                height, width, _ = self.current_image.shape
                self.image_info_label.setText(f"ទំហំឯកសារ: {file_size:.2f} KB | ទំហំរូបភាព: {width}x{height}px")
                
                # បង្ហាញរូបភាពដើម
                self.display_original_image()
                
                # បើកដំណើរការរូបភាពដោយស្វ័យប្រវត្តិ
                self.process_scanned_image()
                
                self.statusBar().showMessage(f"បានផ្ទុករូបភាពពី: {os.path.basename(file_path)}")
                
            except Exception as e:
                QMessageBox.critical(self, "កំហុស", f"មិនអាចផ្ទុករូបភាពបានទេ: {str(e)}")
    
    def display_original_image(self):
        """បង្ហាញរូបភាពដើមក្នុង label"""
        if self.current_image is not None:
            # បម្លែង BGR ទៅ RGB
            rgb_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            self.original_image_label.setPixmap(scaled_pixmap)
    
    def process_scanned_image(self):
        """ដំណើរការរូបភាពដែលបានស្កេន"""
        if self.current_image is None:
            QMessageBox.warning(self, "ការព្រមាន", "មិនមានរូបភាពណាមួយត្រូវដំណើរការទេ!")
            return
        
        try:
            # ចម្លងរូបភាពដើម
            image = self.current_image.copy()
            
            # បម្លែងទៅជារូបភាពពណ៌ប្រផេះ
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # កាត់បន្ថយសំលេងរំខាន
            denoised = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # កែលម្អភាពខ្លាំងនៃគែម
            edges = cv2.Canny(denoised, 50, 150)
            
            # ស្វែងរកគែមជុំវិញឯកសារ
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # រកពហុកោណធំបំផុត (សន្មត់ថាជាឯកសារ)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                epsilon = 0.02 * cv2.arcLength(largest_contour, True)
                approx = cv2.approxPolyDP(largest_contour, epsilon, True)
                
                if len(approx) == 4:  # ប្រសិនបើជាចតុកោណ
                    # កំណត់ចំណុចជ្រុង
                    points = approx.reshape(4, 2)
                    rect = self.order_points(points)
                    
                    # ធ្វើការបម្លែងពីភាពអព្យាក្រឹត
                    warped = self.four_point_transform(gray, rect)
                    
                    # កែលម្អគុណភាពរូបភាព
                    self.processed_image = cv2.adaptiveThreshold(
                        warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                        cv2.THRESH_BINARY, 11, 2
                    )
                    
                    # បង្ហាញរូបភាពបន្ទាប់ពីដំណើរការ
                    self.display_processed_image()
                    
                    # ស្កេនអត្ថបទ (សាមញ្ញ)
                    self.extract_text_from_image()
                    
                    # បើកប៊ូតុងរក្សាទុក
                    self.save_processed_btn.setEnabled(True)
                    self.copy_text_btn.setEnabled(True)
                    
                    self.statusBar().showMessage("បានដំណើរការរូបភាពដោយជោគជ័យ")
                else:
                    QMessageBox.warning(self, "ការព្រមាន", "មិនអាចស្វែងរកឯកសារចតុកោណក្នុងរូបភាពបានទេ!")
                    self.processed_image = denoised
                    self.display_processed_image()
            else:
                # ប្រសិនបើគ្មានគែមរកឃើញ គ្រាន់តែបង្ហាញរូបភាពដែលបានកែលម្អ
                self.processed_image = denoised
                self.display_processed_image()
                
        except Exception as e:
            QMessageBox.warning(self, "ការព្រមាន", f"មិនអាចដំណើរការរូបភាពបានទេ: {str(e)}")
            # ប្រសិនបើមានកំហុស គ្រាន់តែបង្ហាញរូបភាពដើម
            self.processed_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
            self.display_processed_image()
    
    def order_points(self, pts):
        """រៀបចំចំណុចជ្រុងតាមលំដាប់"""
        rect = np.zeros((4, 2), dtype="float32")
        
        s = pts.sum(axis=1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        
        return rect
    
    def four_point_transform(self, image, pts):
        """ធ្វើការបម្លែងពីភាពអព្យាក្រឹត"""
        rect = pts
        (tl, tr, br, bl) = rect
        
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
        
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
        
        return warped
    
    def display_processed_image(self):
        """បង្ហាញរូបភាពបន្ទាប់ពីដំណើរការ"""
        if self.processed_image is not None:
            # ប្រសិនបើជារូបភាពពណ៌ប្រផេះតែមួយឆានែល
            if len(self.processed_image.shape) == 2:
                h, w = self.processed_image.shape
                bytes_per_line = w
                qt_image = QImage(self.processed_image.data, w, h, bytes_per_line, QImage.Format_Grayscale8)
            else:
                # ប្រសិនបើជារូបភាពពណ៌
                rgb_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            
            self.processed_image_label.setPixmap(scaled_pixmap)
    
    def extract_text_from_image(self):
        """ស្កេនអត្ថបទពីរូបភាព (សាមញ្ញ)"""
        # សម្រាប់កូដពិត អ្នកអាចប្រើ Tesseract OCR
        # នៅទីនេះយើងគ្រាន់តែបង្ហាញឧទាហរណ៍សាមញ្ញ
        if self.processed_image is not None:
            # ក្នុងកូដពិត អ្នកអាចប្រើប្រាស់:
            # import pytesseract
            # self.scanned_text = pytesseract.image_to_string(self.processed_image, lang='eng+khmer')
            
            # សម្រាប់ឧទាហរណ៍ យើងបង្កើតអត្ថបទគំរូ
            sample_text = """ឯកសារសាកល្បង
លេខ៖ ១២៣/២៤
កាលបរិច្ឆេទ៖ ១៥ មករា ២០២៤
ប្រធានបទ៖ ការសាកល្បងកម្មវិធីថតឯកសារ
ខ្លឹមសារ៖ នេះគឺជាអត្ថបទសាកល្បងសម្រាប់កម្មវិធីថតឯកសារ។
អត្ថបទនេះត្រូវបានសរសេរជាភាសាខ្មែរដើម្បីសាកល្បងមុខងារស្កេន។"""
            
            self.scanned_text = sample_text
            self.scanned_text_edit.setText(sample_text)
            self.statusBar().showMessage("បានស្កេនអត្ថបទពីរូបភាព")
    
    def save_processed_image(self):
        """រក្សាទុករូបភាពបន្ទាប់ពីដំណើរការ"""
        if self.processed_image is None:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "រក្សាទុករូបភាព", 
            f"scanned_document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", 
            "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*.*)"
        )
        
        if file_path:
            try:
                cv2.imwrite(file_path, self.processed_image)
                QMessageBox.information(self, "ជោគជ័យ", f"បានរក្សាទុករូបភាពទៅ:\n{file_path}")
                self.statusBar().showMessage(f"បានរក្សាទុករូបភាព: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "កំហុស", f"មិនអាចរក្សាទុករូបភាពបានទេ: {str(e)}")
    
    def copy_scanned_text(self):
        """ចម្លងអត្ថបទដែលបានស្កេនទៅក្តារតម្រៀប"""
        if self.scanned_text:
            try:
                pyperclip.copy(self.scanned_text)
                self.statusBar().showMessage("បានចម្លងអត្ថបទទៅក្តារតម្រៀប")
            except:
                # ប្រសិនបើ pyperclip មិនដំណើរការ
                clipboard = QApplication.clipboard()
                clipboard.setText(self.scanned_text)
                self.statusBar().showMessage("បានចម្លងអត្ថបទទៅក្តារតម្រៀប")
    
    def clear_scanned_text(self):
        """សម្អាតអត្ថបទដែលបានស្កេន"""
        self.scanned_text = ""
        self.scanned_text_edit.clear()
        self.statusBar().showMessage("បានសម្អាតអត្ថបទ")
    
    def create_document_from_text(self):
        """បង្កើតឯកសារពីអត្ថបទដែលបានស្កេន"""
        if not self.scanned_text:
            QMessageBox.warning(self, "ការព្រមាន", "មិនមានអត្ថបទណាមួយទេ!")
            return
            
        # ប្តូរទៅផ្ទាំងថតឯកសារ
        self.tab_widget.setCurrentIndex(0)
        
        # បំពេញទិន្នន័យដោយស្វ័យប្រវត្តិ
        self.doc_name_input.setText("ឯកសារពីការស្កេន")
        self.doc_description_input.setPlainText(self.scanned_text)
        
        # បង្ហាញសារជោគជ័យ
        self.statusBar().showMessage("បានផ្ទេរអត្ថបទទៅការបញ្ចូលឯកសារ")
        QMessageBox.information(self, "ជោគជ័យ", "អត្ថបទត្រូវបានផ្ទេរទៅការបញ្ចូលឯកសារ។ សូមបំពេញព័ត៌មានបន្ថែម!")
    
    def save_document(self):
        """រក្សាទុកឯកសារថ្មី"""
        # ត្រួតពិនិត្យទិន្នន័យ
        if not self.doc_name_input.text().strip():
            QMessageBox.warning(self, "ការព្រមាន", "សូមបញ្ចូលឈ្មោះឯកសារ!")
            return
            
        # បង្កើតឯកសារថ្មី
        document = {
            "id": len(self.documents) + 1,
            "name": self.doc_name_input.text().strip(),
            "type": self.doc_type_combo.currentText(),
            "number": self.doc_number_input.text().strip(),
            "date": self.doc_date_input.date().toString("yyyy-MM-dd"),
            "description": self.doc_description_input.toPlainText().strip(),
            "status": self.doc_status_combo.currentText(),
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "has_qr": False
        }
        
        # បន្ថែមទៅក្នុងបញ្ជី
        self.documents.append(document)
        
        # រក្សាទុកទិន្នន័យ
        self.save_data()
        
        # សម្អាតប្រអប់បញ្ចូល
        self.clear_form()
        
        # បន្ទាន់សម័យតារាង
        self.load_all_documents()
        
        # ប្តូរទៅផ្ទាំងបញ្ជី
        self.tab_widget.setCurrentIndex(2)
        
        # បង្ហាញសារជោគជ័យ
        QMessageBox.information(self, "ជោគជ័យ", "ឯកសារត្រូវបានរក្សាទុកដោយជោគជ័យ!")
        self.statusBar().showMessage("ឯកសារត្រូវបានរក្សាទុកដោយជោគជ័យ")
        
    def clear_form(self):
        """សម្អាតប្រអប់បញ្ចូលទាំងអស់"""
        self.doc_name_input.clear()
        self.doc_type_combo.setCurrentIndex(0)
        self.doc_number_input.clear()
        self.doc_date_input.setDate(QDate.currentDate())
        self.doc_description_input.clear()
        self.doc_status_combo.setCurrentIndex(0)
        self.statusBar().showMessage("ប្រអប់បញ្ចូលត្រូវបានសម្អាត")
    
    def generate_qr_code(self):
        """បង្កើត QR Code សម្រាប់ឯកសារ"""
        # ត្រួតពិនិត្យទិន្នន័យ
        if not self.doc_name_input.text().strip():
            QMessageBox.warning(self, "ការព្រមាន", "សូមបញ្ចូលឈ្មោះឯកសារមុននឹងបង្កើត QR Code!")
            return
        
        # បង្កើតខ្លឹមសារសម្រាប់ QR Code
        doc_data = {
            "name": self.doc_name_input.text().strip(),
            "type": self.doc_type_combo.currentText(),
            "number": self.doc_number_input.text().strip(),
            "date": self.doc_date_input.date().toString("yyyy-MM-dd"),
            "status": self.doc_status_combo.currentText(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        qr_content = json.dumps(doc_data, ensure_ascii=False)
        
        # បង្កើត QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        # បង្កើតរូបភាព QR Code
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # បម្លែងទៅជា QPixmap
        qr_img = qr_img.convert("RGBA")
        data = qr_img.tobytes("raw", "RGBA")
        qimg = QImage(data, qr_img.size[0], qr_img.size[1], QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimg)
        
        # បង្ហាញ QR Code ក្នុងប្រអប់
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("QR Code សម្រាប់ឯកសារ")
        msg_box.setText(f"QR Code សម្រាប់ឯកសារ: {self.doc_name_input.text().strip()}")
        
        # បង្កើត label សម្រាប់បង្ហាញ QR Code
        qr_label = QLabel()
        qr_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        qr_label.setAlignment(Qt.AlignCenter)
        
        # បន្ថែម QR Code ទៅក្នុងប្រអប់សារ
        msg_box.setIconPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # បន្ថែមប៊ូតុងបន្ថែម
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        save_btn = msg_box.button(QMessageBox.Save)
        save_btn.setText("រក្សាទុក QR Code")
        
        result = msg_box.exec_()
        
        if result == QMessageBox.Save:
            # រក្សាទុក QR Code ជាឯកសាររូបភាព
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "រក្សាទុក QR Code", 
                f"qr_code_{self.doc_name_input.text().strip()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", 
                "PNG Files (*.png);;All Files (*.*)"
            )
            
            if file_path:
                qr_img.save(file_path)
                QMessageBox.information(self, "ជោគជ័យ", f"QR Code ត្រូវបានរក្សាទុកទៅ:\n{file_path}")
                self.statusBar().showMessage("QR Code ត្រូវបានរក្សាទុកដោយជោគជ័យ")
    
    def generate_qr_for_document(self, document):
        """បង្កើត QR Code សម្រាប់ឯកសារជាក់លាក់"""
        # បង្កើតខ្លឹមសារសម្រាប់ QR Code
        qr_content = json.dumps(document, ensure_ascii=False)
        
        # បង្កើត QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_content)
        qr.make(fit=True)
        
        # បង្កើតរូបភាព QR Code
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # បម្លែងទៅជា QPixmap
        qr_img = qr_img.convert("RGBA")
        data = qr_img.tobytes("raw", "RGBA")
        qimg = QImage(data, qr_img.size[0], qr_img.size[1], QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimg)
        
        # បង្ហាញ QR Code ក្នុងប្រអប់
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(f"QR Code សម្រាប់ឯកសារ: {document['name']}")
        msg_box.setText(f"QR Code សម្រាប់ឯកសារ: {document['name']}")
        msg_box.setIconPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        
        # បន្ថែមប៊ូតុងបន្ថែម
        msg_box.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)
        save_btn = msg_box.button(QMessageBox.Save)
        save_btn.setText("រក្សាទុក QR Code")
        
        result = msg_box.exec_()
        
        if result == QMessageBox.Save:
            # រក្សាទុក QR Code ជាឯកសាររូបភាព
            file_path, _ = QFileDialog.getSaveFileName(
                self, 
                "រក្សាទុក QR Code", 
                f"qr_code_{document['name']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png", 
                "PNG Files (*.png);;All Files (*.*)"
            )
            
            if file_path:
                qr_img.save(file_path)
                QMessageBox.information(self, "ជោគជ័យ", f"QR Code ត្រូវបានរក្សាទុកទៅ:\n{file_path}")
                self.statusBar().showMessage("QR Code ត្រូវបានរក្សាទុកដោយជោគជ័យ")
    
    def load_all_documents(self):
        """ផ្ទុកបញ្ជីឯកសារទាំងអស់"""
        self.all_documents_table.setRowCount(len(self.documents))
        
        for row, doc in enumerate(self.documents):
            self.all_documents_table.setItem(row, 0, QTableWidgetItem(str(doc["id"])))
            self.all_documents_table.setItem(row, 1, QTableWidgetItem(doc["name"]))
            self.all_documents_table.setItem(row, 2, QTableWidgetItem(doc["type"]))
            self.all_documents_table.setItem(row, 3, QTableWidgetItem(doc["number"]))
            self.all_documents_table.setItem(row, 4, QTableWidgetItem(doc["date"]))
            self.all_documents_table.setItem(row, 5, QTableWidgetItem(doc["status"]))
            
            # ប៊ូតុង QR Code
            qr_btn = QPushButton("បង្កើត QR")
            qr_btn.setStyleSheet("background-color: #9b59b6; color: white; padding: 4px;")
            qr_btn.clicked.connect(lambda checked, d=doc: self.generate_qr_for_document(d))
            self.all_documents_table.setCellWidget(row, 6, qr_btn)
            
            # ប៊ូតុងសកម្មភាព
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(4, 4, 4, 4)
            
            view_btn = QPushButton("មើល")
            view_btn.setStyleSheet("background-color: #3498db; color: white; padding: 4px;")
            view_btn.clicked.connect(lambda checked, d=doc: self.view_document(d))
            
            delete_btn = QPushButton("លុប")
            delete_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 4px;")
            delete_btn.clicked.connect(lambda checked, idx=row: self.delete_document(idx))
            
            action_layout.addWidget(view_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()
            
            action_widget.setLayout(action_layout)
            self.all_documents_table.setCellWidget(row, 7, action_widget)
        
        self.statusBar().showMessage(f"មានឯកសារសរុប {len(self.documents)}")
    
    def search_documents(self):
        """ស្វែងរកឯកសារតាមលក្ខខណ្ឌ"""
        search_text = self.search_input.text().strip().lower()
        search_type = self.search_type_combo.currentIndex()
        search_status = self.search_status_combo.currentText()
        
        # សម្អាតតារាង
        self.search_results_table.setRowCount(0)
        
        if not search_text and search_status == "ស្ថានភាពទាំងអស់":
            # បង្ហាញឯកសារទាំងអស់
            results = self.documents
        else:
            # ស្វែងរកតាមលក្ខខណ្ឌ
            results = []
            for doc in self.documents:
                # ត្រួតពិនិត្យស្ថានភាព
                status_match = (search_status == "ស្ថានភាពទាំងអស់") or (doc["status"] == search_status)
                
                if not status_match:
                    continue
                    
                # ត្រួតពិនិត្យពាក្យស្វែងរក
                if not search_text:
                    results.append(doc)
                    continue
                    
                text_match = False
                if search_type == 0:  # ទាំងអស់
                    text_match = (search_text in doc["name"].lower() or 
                                 search_text in doc["number"].lower() or 
                                 search_text in doc["type"].lower() or 
                                 search_text in doc["description"].lower())
                elif search_type == 1:  # ឈ្មោះ
                    text_match = search_text in doc["name"].lower()
                elif search_type == 2:  # លេខ
                    text_match = search_text in doc["number"].lower()
                elif search_type == 3:  # ប្រភេទ
                    text_match = search_text in doc["type"].lower()
                elif search_type == 4:  # ពណ៌នា
                    text_match = search_text in doc["description"].lower()
                
                if text_match:
                    results.append(doc)
        
        # បង្ហាញលទ្ធផល
        self.search_results_table.setRowCount(len(results))
        for row, doc in enumerate(results):
            self.search_results_table.setItem(row, 0, QTableWidgetItem(str(doc["id"])))
            self.search_results_table.setItem(row, 1, QTableWidgetItem(doc["name"]))
            self.search_results_table.setItem(row, 2, QTableWidgetItem(doc["type"]))
            self.search_results_table.setItem(row, 3, QTableWidgetItem(doc["number"]))
            self.search_results_table.setItem(row, 4, QTableWidgetItem(doc["date"]))
            self.search_results_table.setItem(row, 5, QTableWidgetItem(doc["status"]))
            
            # ប៊ូតុងសកម្មភាព
            action_widget = QWidget()
            action_layout = QHBoxLayout()
            action_layout.setContentsMargins(4, 4, 4, 4)
            
            view_btn = QPushButton("មើល")
            view_btn.setStyleSheet("background-color: #3498db; color: white; padding: 4px;")
            view_btn.clicked.connect(lambda checked, d=doc: self.view_document(d))
            
            delete_btn = QPushButton("លុប")
            delete_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 4px;")
            delete_btn.clicked.connect(lambda checked, idx=doc["id"]-1: self.delete_document(idx))
            
            action_layout.addWidget(view_btn)
            action_layout.addWidget(delete_btn)
            action_layout.addStretch()
            
            action_widget.setLayout(action_layout)
            self.search_results_table.setCellWidget(row, 6, action_widget)
        
        self.statusBar().showMessage(f"រកឃើញ {len(results)} ឯកសារ")
    
    def view_document(self, document):
        """មើលព័ត៌មានលម្អិតអំពីឯកសារ"""
        details = f"""
        ព័ត៌មានលម្អិតអំពីឯកសារ:
        
        លេខអត្តសញ្ញាណ: {document['id']}
        ឈ្មោះឯកសារ: {document['name']}
        ប្រភេទ: {document['type']}
        លេខឯកសារ: {document['number']}
        កាលបរិច្ឆេទ: {document['date']}
        ស្ថានភាព: {document['status']}
        ពណ៌នា: {document['description']}
        កាលបរិច្ឆេទរក្សាទុក: {document['created_at']}
        """
        
        QMessageBox.information(self, "ព័ត៌មានឯកសារ", details)
    
    def delete_document(self, index):
        """លុបឯកសារ"""
        reply = QMessageBox.question(self, "បញ្ជាក់ការលុប", 
                                    "តើអ្នកពិតជាចង់លុបឯកសារនេះមែនទេ?", 
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # លុបឯកសារ
            del self.documents[index]
            
            # បន្ទាន់សម័យលេខអត្តសញ្ញាណ
            for i, doc in enumerate(self.documents):
                doc["id"] = i + 1
            
            # រក្សាទុកទិន្នន័យ
            self.save_data()
            
            # បន្ទាន់សម័យតារាង
            self.load_all_documents()
            
            self.statusBar().showMessage("ឯកសារត្រូវបានលុបដោយជោគជ័យ")
    
    def delete_all_documents(self):
        """លុបឯកសារទាំងអស់"""
        if not self.documents:
            QMessageBox.information(self, "ព័ត៌មាន", "មិនមានឯកសារណាមួយទេ!")
            return
            
        reply = QMessageBox.question(self, "បញ្ជាក់ការលុបទាំងអស់", 
                                    "តើអ្នកពិតជាចង់លុបឯកសារទាំងអស់មែនទេ?\n\nការងារនេះមិនអាចមានការដកហូតបានទេ!", 
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # លុបឯកសារទាំងអស់
            self.documents = []
            
            # រក្សាទុកទិន្នន័យ
            self.save_data()
            
            # បន្ទាន់សម័យតារាង
            self.load_all_documents()
            
            self.statusBar().showMessage("ឯកសារទាំងអស់ត្រូវបានលុបដោយជោគជ័យ")
    
    def export_data(self):
        """នាំចេញទិន្នន័យទៅជាឯកសារ"""
        if not self.documents:
            QMessageBox.warning(self, "ការព្រមាន", "មិនមានទិន្នន័យណាមួយសម្រាប់នាំចេញទេ!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(self, "នាំចេញទិន្នន័យ", "documents_export.json", "JSON Files (*.json)")
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.documents, f, ensure_ascii=False, indent=2)
                
                QMessageBox.information(self, "ជោគជ័យ", f"ទិន្នន័យត្រូវបាននាំចេញទៅ:\n{file_path}")
                self.statusBar().showMessage(f"ទិន្នន័យត្រូវបាននាំចេញទៅ {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "កំហុស", f"មិនអាចនាំចេញទិន្នន័យបានទេ: {str(e)}")

def main():
    app = QApplication(sys.argv)
    
    # កំណត់រចនាបថដើម្បីគាំទ្រភាសាខ្មែរ
    app.setStyle('Fusion')
    
    # បង្កើតនិងបង្ហាញផ្ទាំងអេក្រង់
    window = DocumentRecorderApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()