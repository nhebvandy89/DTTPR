import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon, QPixmap, QImage
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

class WeddingPlannerUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # កំណត់លក្ខណៈសំខាន់ៗនៃផ្ទាំង
        self.setWindowTitle('ប្រព័ន្ធគ្រប់គ្រងរៀបអាពាហ៍ពិពាហ៍')
        self.setGeometry(100, 100, 1300, 750)
        
        # បង្កើតធាតុកណ្តាល
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # បង្កើតតារាងដែលមានម៉ីនុយខាងឆ្វេង និងតំបន់ការងារ
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(10)
        
        # បង្កើតស៊ុមសម្រាប់ម៉ីនុយខាងឆ្វេង
        menu_frame = QFrame()
        menu_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8B4513, stop:1 #D2691E);
                border-right: 3px solid #A0522D;
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                color: white;
                border: 2px solid rgba(255, 255, 255, 0.3);
                border-radius: 10px;
                padding: 15px;
                margin: 8px;
                font-size: 14px;
                font-weight: bold;
                text-align: left;
                padding-left: 25px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
                border: 2px solid white;
            }
            QPushButton:pressed {
                background-color: rgba(210, 105, 30, 0.8);
            }
        """)
        menu_frame.setFixedWidth(280)
        
        # បង្កើតប៉ូតុងនៅក្នុងម៉ីនុយ
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setContentsMargins(15, 25, 15, 25)
        
        # បន្ថែមចំណងជើង
        title_label = QLabel("គ្រប់គ្រងអាពាហ៍ពិពាហ៍")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont('Arial', 18, QFont.Bold))  # Changed from 'Khmer OS'
        title_label.setStyleSheet("""
            color: white;
            background-color: rgba(139, 69, 19, 0.7);
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 25px;
            border: 2px solid white;
        """)
        menu_layout.addWidget(title_label)
        
        # បង្កើតប៉ូតុងម៉ីនុយ
        self.create_invitation_btn = QPushButton("📄 បង្កើតសំបុត្រអាពាហ៍ពិពាហ៍ថ្មី")
        self.wedding_book_btn = QPushButton("📒 សៀវភៅកត់ចំណងដៃ")
        self.settings_btn = QPushButton("⚙️ កំណត់")
        
        # បន្ថែមប៉ូតុងទៅក្នុងម៉ីនុយ
        menu_layout.addWidget(self.create_invitation_btn)
        menu_layout.addWidget(self.wedding_book_btn)
        menu_layout.addWidget(self.settings_btn)
        
        # បន្ថែមទំហំអន្តរកម្ម
        menu_layout.addStretch()
        
        # បង្កើតតំបន់ការងារសំខាន់
        self.work_area = QStackedWidget()
        self.work_area.setStyleSheet("""
            QStackedWidget, QFrame {
                background-color: #FFF8F0;
            }
        """)
        
        # បង្កើតទំព័រផ្សេងៗ
        self.create_invitation_page()
        self.create_wedding_book_page()
        self.create_settings_page()
        
        # បន្ថែមទំព័រទៅក្នុងតំបន់ការងារ
        self.work_area.addWidget(self.invitation_page)
        self.work_area.addWidget(self.wedding_book_page)
        self.work_area.addWidget(self.settings_page)
        
        # បន្ថែមម៉ីនុយ និងតំបន់ការងារទៅក្នុងតារាងចម្បង
        main_layout.addWidget(menu_frame)
        main_layout.addWidget(self.work_area, 1)
        
        # ភ្ជាប់សញ្ញាប៉ូតុង
        self.create_invitation_btn.clicked.connect(lambda: self.work_area.setCurrentIndex(0))
        self.wedding_book_btn.clicked.connect(lambda: self.work_area.setCurrentIndex(1))
        self.settings_btn.clicked.connect(lambda: self.work_area.setCurrentIndex(2))
        
        # បង្ហាញទំព័រដំបូង
        self.work_area.setCurrentIndex(0)
        
    def create_invitation_page(self):
        """បង្កើតទំព័របង្កើតសំបុត្រអាពាហ៍ពិពាហ៍"""
        self.invitation_page = QWidget()
        layout = QVBoxLayout(self.invitation_page)
        layout.setSpacing(20)
        
        # ចំណងជើងទំព័រ
        page_title = QLabel("បង្កើតសំបុត្រអាពាហ៍ពិពាហ៍ថ្មី")
        page_title.setFont(QFont('Arial', 22, QFont.Bold))  # Changed from 'Khmer OS'
        page_title.setStyleSheet("""
            color: #8B4513;
            margin: 20px;
            background-color: #FFEBCD;
            border-radius: 15px;
            padding: 20px;
            border: 2px dashed #D2691E;
        """)
        page_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(page_title)
        
        # បង្កើតស៊ុមសម្រាប់បែបបទ
        form_scroll = QScrollArea()
        form_scroll.setWidgetResizable(True)
        form_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
        """)
        
        form_widget = QWidget()
        form_scroll.setWidget(form_widget)
        
        form_layout = QGridLayout(form_widget)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)
        
        # បន្ថែមប្រអប់បញ្ចូលព័ត៌មាន
        # ព័ត៌មានអ្នករៀបការ
        info_style = """
            QLabel {
                color: #5D4037;
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
            QLineEdit, QTextEdit, QDateEdit, QComboBox {
                background-color: white;
                border: 2px solid #D2691E;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                min-height: 35px;
            }
            QLineEdit:focus, QTextEdit:focus, QDateEdit:focus {
                border: 2px solid #8B4513;
                background-color: #FFF8E1;
            }
        """
        
        # ឈ្មោះកូនប្រុស
        form_layout.addWidget(QLabel("ឈ្មោះកូនប្រុស:"), 0, 0)
        self.groom_name = QLineEdit()
        self.groom_name.setPlaceholderText("បញ្ចូលឈ្មោះកូនប្រុស")
        form_layout.addWidget(self.groom_name, 0, 1)
        
        # ឈ្មោះកូនស្រី
        form_layout.addWidget(QLabel("ឈ្មោះកូនស្រី:"), 1, 0)
        self.bride_name = QLineEdit()
        self.bride_name.setPlaceholderText("បញ្ចូលឈ្មោះកូនស្រី")
        form_layout.addWidget(self.bride_name, 1, 1)
        
        # ឈ្មោះឪពុកខាងកូនប្រុស
        form_layout.addWidget(QLabel("ឈ្មោះឪពុកខាងកូនប្រុស:"), 2, 0)
        self.groom_father = QLineEdit()
        self.groom_father.setPlaceholderText("បញ្ចូលឈ្មោះឪពុកខាងកូនប្រុស")
        form_layout.addWidget(self.groom_father, 2, 1)
        
        # ឈ្មោះម្ដាយខាងកូនប្រុស
        form_layout.addWidget(QLabel("ឈ្មោះម្ដាយខាងកូនប្រុស:"), 3, 0)
        self.groom_mother = QLineEdit()
        self.groom_mother.setPlaceholderText("បញ្ចូលឈ្មោះម្ដាយខាងកូនប្រុស")
        form_layout.addWidget(self.groom_mother, 3, 1)
        
        # ឈ្មោះឪពុកខាងកូនស្រី
        form_layout.addWidget(QLabel("ឈ្មោះឪពុកខាងកូនស្រី:"), 4, 0)
        self.bride_father = QLineEdit()
        self.bride_father.setPlaceholderText("បញ្ចូលឈ្មោះឪពុកខាងកូនស្រី")
        form_layout.addWidget(self.bride_father, 4, 1)
        
        # ឈ្មោះម្ដាយខាងកូនស្រី
        form_layout.addWidget(QLabel("ឈ្មោះម្ដាយខាងកូនស្រី:"), 5, 0)
        self.bride_mother = QLineEdit()
        self.bride_mother.setPlaceholderText("បញ្ចូលឈ្មោះម្ដាយខាងកូនស្រី")
        form_layout.addWidget(self.bride_mother, 5, 1)
        
        # កាលបរិច្ឆេទ
        form_layout.addWidget(QLabel("កាលបរិច្ឆេទរៀបការ:"), 6, 0)
        date_layout = QHBoxLayout()
        self.wedding_date = QDateEdit()
        self.wedding_date.setDate(QDate.currentDate().addDays(30))
        self.wedding_date.setCalendarPopup(True)
        self.wedding_date.setDisplayFormat("dd/MM/yyyy")
        
        self.wedding_time = QComboBox()
        self.wedding_time.addItems(["07:00 ព្រឹក", "08:00 ព្រឹក", "09:00 ព្រឹក", "10:00 ព្រឹក", 
                                    "14:00 ល្ងាច", "15:00 ល្ងាច", "16:00 ល្ងាច", "17:00 ល្ងាច"])
        
        date_layout.addWidget(self.wedding_date)
        date_layout.addWidget(QLabel("ម៉ោង:"))
        date_layout.addWidget(self.wedding_time)
        date_layout.addStretch()
        form_layout.addLayout(date_layout, 6, 1)
        
        # ទីតាំងរៀបពិធី
        form_layout.addWidget(QLabel("ទីតាំងរៀបពិធី:"), 7, 0)
        self.wedding_location = QTextEdit()
        self.wedding_location.setPlaceholderText("បញ្ចូលអាសយដ្ឋានពិស្តារ...")
        self.wedding_location.setMaximumHeight(100)
        form_layout.addWidget(self.wedding_location, 7, 1)
        
        # ប៊ូតុងបញ្ជូលរូបថតការ
        form_layout.addWidget(QLabel("រូបថតអាពាហ៍ពិពាហ៍:"), 8, 0)
        photo_layout = QHBoxLayout()
        
        self.photo_btn = QPushButton("📷 ជ្រើសរើសរូបថត")
        self.photo_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        self.photo_preview = QLabel("(មិនទាន់មានរូបថត)")
        self.photo_preview.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px dashed #888;
                border-radius: 8px;
                padding: 10px;
                color: #666;
                font-style: italic;
                min-width: 200px;
                min-height: 100px;
            }
        """)
        self.photo_preview.setAlignment(Qt.AlignCenter)
        
        photo_layout.addWidget(self.photo_btn)
        photo_layout.addWidget(self.photo_preview)
        photo_layout.addStretch()
        form_layout.addLayout(photo_layout, 8, 1)
        
        # ប៊ូតុងដាក់បញ្ជូល QR Code ចង់ដៃ
        form_layout.addWidget(QLabel("QR Code ចង់ដៃ:"), 9, 0)
        qr_layout = QHBoxLayout()
        
        self.qr_btn = QPushButton("🔗 បង្កើត QR Code")
        self.qr_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        
        self.qr_preview = QLabel("(មិនទាន់មាន QR Code)")
        self.qr_preview.setStyleSheet("""
            QLabel {
                background-color: white;
                border: 2px dashed #2196F3;
                border-radius: 8px;
                padding: 10px;
                color: #666;
                font-style: italic;
                min-width: 100px;
                min-height: 100px;
            }
        """)
        self.qr_preview.setAlignment(Qt.AlignCenter)
        
        qr_layout.addWidget(self.qr_btn)
        qr_layout.addWidget(self.qr_preview)
        qr_layout.addStretch()
        form_layout.addLayout(qr_layout, 9, 1)
        
        # អនុគមន៍បន្ថែម
        form_layout.addWidget(QLabel("សារពិសេស:"), 10, 0)
        self.special_message = QTextEdit()
        self.special_message.setPlaceholderText("បញ្ចូលសារពិសេសសម្រាប់អ្នកអញ្ជើញ...")
        self.special_message.setMaximumHeight(120)
        form_layout.addWidget(self.special_message, 10, 1)
        
        # កំណត់ស្តាយល៍សម្រាប់ទាំងអស់
        form_widget.setStyleSheet(info_style)
        
        layout.addWidget(form_scroll, 1)
        
        # បន្ថែមប៉ូតុង
        button_layout = QHBoxLayout()
        
        preview_btn = QPushButton("👁️ មើលសំបុត្រមុន")
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F57C00;
            }
        """)
        
        create_btn = QPushButton("🖨️ បង្កើតសំបុត្រ")
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 40px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6D3410;
                border: 2px solid #D2691E;
            }
        """)
        
        save_btn = QPushButton("💾 រក្សាទុក")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(preview_btn)
        button_layout.addWidget(create_btn)
        button_layout.addWidget(save_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addSpacing(20)
        
        # ភ្ជាប់សញ្ញាប៉ូតុង
        self.photo_btn.clicked.connect(self.select_photo)
        self.qr_btn.clicked.connect(self.generate_qr_code)
        create_btn.clicked.connect(self.generate_invitation)
        preview_btn.clicked.connect(self.preview_invitation)
        save_btn.clicked.connect(self.save_invitation)
        
    def select_photo(self):
        """ជ្រើសរើសរូបថត"""
        file_name, _ = QFileDialog.getOpenFileName(
            self, "ជ្រើសរើសរូបថត", "", 
            "រូបថត (*.jpg *.jpeg *.png *.bmp)"
        )
        if file_name:
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaled(200, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.photo_preview.setPixmap(pixmap)
            self.photo_preview.setText("")
            
    def generate_qr_code(self):
        """បង្កើត QR Code"""
        # ក្នុងកម្មវិធីពិត អ្នកអាចប្រើបណ្ណាល័យ qrcode
        # នេះគ្រាន់តែជាឧទាហរណ៍បង្ហាញប៉ុណ្ណោះ
        self.qr_preview.setText("QR Code\n(បង្កើតរួច)")
        self.qr_preview.setStyleSheet("""
            QLabel {
                background-color: #E3F2FD;
                border: 2px solid #2196F3;
                border-radius: 8px;
                padding: 10px;
                color: #0D47A1;
                font-weight: bold;
                min-width: 100px;
                min-height: 100px;
            }
        """)
        
    def generate_invitation(self):
        """បង្កើតសំបុត្រអញ្ជើញ"""
        # ពិនិត្យថាតើបានបញ្ចូលព័ត៌មានគ្រប់គ្រាន់ឬនៅ
        if not self.groom_name.text() or not self.bride_name.text():
            QMessageBox.warning(self, "ព្រមាន", "សូមបញ្ចូលឈ្មោះកូនប្រុស និងកូនស្រី!")
            return
            
        # បង្ហាញសារជោគជ័យ
        QMessageBox.information(
            self, "ជោគជ័យ", 
            f"សំបុត្រអញ្ជើញត្រូវបានបង្កើតជោគជ័យ!\n"
            f"កូនប្រុស: {self.groom_name.text()}\n"
            f"កូនស្រី: {self.bride_name.text()}"
        )
        
    def preview_invitation(self):
        """មើលសំបុត្រមុន"""
        # បង្ហាញការមើលមុន
        preview_text = f"""
        សំបុត្រអញ្ជើញអាពាហ៍ពិពាហ៍
        
        កូនប្រុស: {self.groom_name.text()}
        កូនស្រី: {self.bride_name.text()}
        
        ឪពុកម្តាយខាងកូនប្រុស:
        ឪពុក: {self.groom_father.text()}
        ម្តាយ: {self.groom_mother.text()}
        
        ឪពុកម្តាយខាងកូនស្រី:
        ឪពុក: {self.bride_father.text()}
        ម្តាយ: {self.bride_mother.text()}
        
        កាលបរិច្ឆេទ: {self.wedding_date.text()}
        ម៉ោង: {self.wedding_time.currentText()}
        ទីតាំង: {self.wedding_location.toPlainText()}
        """
        
        preview_dialog = QDialog(self)
        preview_dialog.setWindowTitle("មើលសំបុត្រមុន")
        preview_dialog.setGeometry(200, 200, 600, 500)
        
        layout = QVBoxLayout(preview_dialog)
        text_edit = QTextEdit()
        text_edit.setPlainText(preview_text)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        preview_dialog.exec_()
        
    def save_invitation(self):
        """រក្សាទុកសំបុត្រ"""
        file_name, _ = QFileDialog.getSaveFileName(
            self, "រក្សាទុកសំបុត្រ", 
            f"សំបុត្រអាពាហ៍ពិពាហ៍_{self.groom_name.text()}_{self.bride_name.text()}",
            "PDF Files (*.pdf);;Word Files (*.docx);;All Files (*)"
        )
        if file_name:
            QMessageBox.information(self, "ជោគជ័យ", f"សំបុត្រត្រូវបានរក្សាទុកនៅ:\n{file_name}")
    
    def create_wedding_book_page(self):
        """បង្កើតទំព័រសៀវភៅកត់ចំណងដៃ"""
        self.wedding_book_page = QWidget()
        layout = QVBoxLayout(self.wedding_book_page)
        
        # ចំណងជើងទំព័រ
        page_title = QLabel("សៀវភៅកត់ចំណងដៃ")
        page_title.setFont(QFont('Arial', 22, QFont.Bold))
        page_title.setStyleSheet("""
            color: #8B4513;
            margin: 20px;
            background-color: #FFEBCD;
            border-radius: 15px;
            padding: 20px;
            border: 2px dashed #D2691E;
        """)
        page_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(page_title)
        
        # បង្កើតតារាងសម្រាប់បង្ហាញចំណងដៃ
        self.wedding_table = QTableWidget()
        self.wedding_table.setColumnCount(6)
        self.wedding_table.setHorizontalHeaderLabels([
            "លេខចំណងដៃ", 
            "ឈ្មោះកូនប្រុស", 
            "ឈ្មោះកូនស្រី", 
            "កាលបរិច្ឆេទ", 
            "ទីតាំង",
            "ស្ថានភាព"
        ])
        self.wedding_table.horizontalHeader().setStretchLastSection(True)
        self.wedding_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 2px solid #D2691E;
                border-radius: 10px;
                alternate-background-color: #FFF8F0;
            }
            QHeaderView::section {
                background-color: #8B4513;
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 8px;
            }
        """)
        
        # បង្កើតទិន្នន័យឧទាហរណ៍
        self.populate_wedding_table()
        
        layout.addWidget(self.wedding_table)
        
        # បន្ថែមប៉ូតុងគ្រប់គ្រង
        button_layout = QHBoxLayout()
        
        buttons = [
            ("➕ បន្ថែមចំណងដៃថ្មី", "#4CAF50"),
            ("👁️ មើលព័ត៌មានលម្អិត", "#2196F3"),
            ("🖨️ បោះពុម្ពសៀវភៅ", "#FF9800"),
            ("✏️ កែសម្រួល", "#9C27B0"),
            ("🗑️ លុប", "#F44336")
        ]
        
        for text, color in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: bold;
                    margin: 5px;
                }}
                QPushButton:hover {{
                    background-color: {self.darken_color(color)};
                }}
            """)
            button_layout.addWidget(btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
    def darken_color(self, hex_color):
        """ធ្វើអោយពណ៌ងងឹតជាងមុន"""
        # ជាឧទាហរណ៍សាមញ្ញ
        return "#" + "".join([format(max(0, int(hex_color[i:i+2], 16) - 40), '02x') 
                             for i in (1, 3, 5)])
    
    def create_settings_page(self):
        """បង្កើតទំព័រកំណត់"""
        self.settings_page = QWidget()
        layout = QVBoxLayout(self.settings_page)
        
        # ចំណងជើងទំព័រ
        page_title = QLabel("កំណត់")
        page_title.setFont(QFont('Arial', 22, QFont.Bold))
        page_title.setStyleSheet("""
            color: #8B4513;
            margin: 20px;
            background-color: #FFEBCD;
            border-radius: 15px;
            padding: 20px;
            border: 2px dashed #D2691E;
        """)
        page_title.setAlignment(Qt.AlignCenter)
        layout.addWidget(page_title)
        
        # បង្កើតស៊ុមសម្រាប់កំណត់
        settings_frame = QFrame()
        settings_frame.setStyleSheet("""
            QFrame {
                background-color: #f9f5f0;
                border-radius: 10px;
                border: 2px solid #D2691E;
            }
            QLabel {
                color: #5D4037;
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QSpinBox {
                background-color: white;
                border: 2px solid #D2691E;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
            }
        """)
        settings_layout = QGridLayout(settings_frame)
        settings_layout.setSpacing(20)
        settings_layout.setContentsMargins(30, 30, 30, 30)
        
        # បន្ថែមកំណត់ផ្សេងៗ
        row = 0
        
        # កំណត់ពុម្ពសំបុត្រ
        settings_layout.addWidget(QLabel("កំណត់ពុម្ពសំបុត្រ:"), row, 0)
        self.printer_settings = QComboBox()
        self.printer_settings.addItems(["ពុម្ពអាល់ហ្វាបេត", "ពុម្ពឈី", "ពុម្ពអេហ្វោ"])
        settings_layout.addWidget(self.printer_settings, row, 1)
        row += 1
        
        # កំណត់ភាសា
        settings_layout.addWidget(QLabel("កំណត់ភាសា:"), row, 0)
        self.language_settings = QComboBox()
        self.language_settings.addItems(["ភាសាខ្មែរ", "English", "Français"])
        settings_layout.addWidget(self.language_settings, row, 1)
        row += 1
        
        # ទម្រង់កាលបរិច្ឆេទ
        settings_layout.addWidget(QLabel("ទម្រង់កាលបរិច្ឆេទ:"), row, 0)
        self.date_format = QComboBox()
        self.date_format.addItems(["dd/MM/yyyy", "MM/dd/yyyy", "yyyy-MM-dd"])
        settings_layout.addWidget(self.date_format, row, 1)
        row += 1
        
        # ទំហំពុម្ពសំបុត្រ
        settings_layout.addWidget(QLabel("ទំហំពុម្ពសំបុត្រ:"), row, 0)
        self.paper_size = QComboBox()
        self.paper_size.addItems(["A4", "A5", "Letter", "Legal"])
        settings_layout.addWidget(self.paper_size, row, 1)
        row += 1
        
        # កំណត់ស្តាយល៍
        settings_layout.addWidget(QLabel("ស្តាយល៍សំបុត្រ:"), row, 0)
        self.template_selection = QComboBox()
        self.template_selection.addItems([
            "គំរូទី១ (ប្រពៃណី)", 
            "គំរូទី២ (ទំនើប)", 
            "គំរូទី៣ (សាមញ្ញ)",
            "គំរូទី៤ (ផ្អែមល្ហែម)"
        ])
        settings_layout.addWidget(self.template_selection, row, 1)
        row += 1
        
        # កំណត់តម្លៃ
        settings_layout.addWidget(QLabel("តម្លៃសំបុត្រ (រៀល):"), row, 0)
        price_layout = QHBoxLayout()
        self.invitation_price = QSpinBox()
        self.invitation_price.setRange(0, 1000000)
        self.invitation_price.setValue(5000)
        self.invitation_price.setSuffix(" ៛")
        price_layout.addWidget(self.invitation_price)
        price_layout.addStretch()
        settings_layout.addLayout(price_layout, row, 1)
        row += 1
        
        # ផ្លូវរក្សាទុកឯកសារ
        settings_layout.addWidget(QLabel("ផ្លូវរក្សាទុកឯកសារ:"), row, 0)
        file_layout = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("C:/Wedding_Invitations/")
        browse_btn = QPushButton("រកមើល")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6D3410;
            }
        """)
        file_layout.addWidget(self.file_path)
        file_layout.addWidget(browse_btn)
        settings_layout.addLayout(file_layout, row, 1)
        
        layout.addWidget(settings_frame)
        
        # បន្ថែមប៉ូតុងរក្សាទុក
        save_layout = QHBoxLayout()
        save_btn = QPushButton("💾 រក្សាទុកកំណត់")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 15px 40px;
                font-size: 18px;
                font-weight: bold;
                margin: 20px;
            }
            QPushButton:hover {
                background-color: #1B5E20;
                border: 2px solid #4CAF50;
            }
        """)
        save_btn.setFixedSize(250, 50)
        save_layout.addStretch()
        save_layout.addWidget(save_btn)
        save_layout.addStretch()
        layout.addLayout(save_layout)
        
        layout.addStretch()
        
    def populate_wedding_table(self):
        """បំពេញតារាងដោយទិន្នន័យឧទាហរណ៍"""
        # ទិន្នន័យឧទាហរណ៍សម្រាប់សៀវភៅចំណងដៃ
        wedding_data = [
            ["001", "សុខ សារឿន", "ម៉ៅ ស្រីណាត", "១៥ កក្កដា ២០២៤", "ភ្នំពេញ", "បានចុះហត្ថលេខា"],
            ["002", "គឹម ស៊ាង", "ឡេង សុខហ៊ាន", "២២ សីហា ២០២៤", "សៀមរាប", "កំពុងរៀបចំ"],
            ["003", "ម៉ៅ សំណាង", "អៀវ សុគន្ធ", "០៥ តុលា ២០២៤", "កំពង់ចាម", "រង់ចាំការអនុម័ត"],
            ["004", "ណុប សុផល", "ផល ស្រីនី", "១២ វិច្ឆិកា ២០២៤", "បាត់ដំបង", "បានចុះហត្ថលេខា"],
            ["005", "ស៊ន វ៉ាន់ដារា", "ម៉ាលី សុផាត", "០៣ ធ្នូ ២០២៤", "ព្រះសីហនុ", "បានបញ្ចប់"],
        ]
        
        self.wedding_table.setRowCount(len(wedding_data))
        
        for row, data in enumerate(wedding_data):
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.wedding_table.setItem(row, col, item)
        
        # កំណត់ទំហំជួរឈរដោយស្វ័យប្រវត្តិ
        self.wedding_table.resizeColumnsToContents()

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    # កំណត់ពុម្ពអក្សរ (បានផ្លាស់ប្តូរពី 'Khmer OS' ទៅ 'Arial')
    font = QFont('Arial', 11)
    app.setFont(font)
    
    window = WeddingPlannerUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()