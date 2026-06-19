import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
from datetime import datetime, timedelta

class ModernLoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # កំណត់លក្ខណៈបង្អួច
        self.setWindowTitle("ចូលប្រើប្រាស់ - Wedding Planner")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #ffffff;")
        
        # បង្កើតលំហូរបឋម
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # ផ្នែកឆ្វេង - រូបភាព
        left_panel = QWidget()
        left_panel.setFixedWidth(450)
        left_panel.setStyleSheet("background-color: #f8f9fa;")
        left_layout = QVBoxLayout(left_panel)
        
        # រូបភាពកំពូល (សម្រាប់បង្ហាញ)
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_pixmap = QPixmap(300, 300)
        logo_pixmap.fill(QColor(240, 240, 245))
        
        # គូររូបភាពស៊ីម្បល
        painter = QPainter(logo_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # គូររូបភាពផ្កា
        painter.setBrush(QBrush(QColor(255, 182, 193)))
        painter.setPen(QPen(QColor(219, 112, 147), 2))
        
        # គូររូបភាពបំណាត់សម្រាប់អាពាហ៍ពិពាហ៍
        for i in range(3):
            painter.drawEllipse(100 + i*50, 100, 40, 40)
        
        painter.setFont(QFont("Arial", 24, QFont.Bold))
        painter.setPen(QColor(139, 0, 139))
        painter.drawText(80, 200, "❤️")
        
        # គូរខ្សែកោង
        path = QPainterPath()
        path.moveTo(50, 250)
        path.cubicTo(150, 200, 250, 280, 350, 250)
        painter.setPen(QPen(QColor(147, 112, 219), 3, Qt.DashLine))
        painter.drawPath(path)
        
        painter.end()
        logo_label.setPixmap(logo_pixmap)
        
        # ព័ត៌មានអំពីកម្មវិធី
        app_info = QLabel("វេបសាយរៀបអាពាហ៍ពិពាហ៍\nទំនើបទាន់សម័យ")
        app_info.setAlignment(Qt.AlignCenter)
        app_info.setFont(QFont("Khmer OS", 18, QFont.Bold))
        app_info.setStyleSheet("color: #8a2be2; margin-top: 20px;")
        
        features = QTextEdit()
        features.setReadOnly(True)
        features.setMaximumHeight(150)
        features.setHtml("""
        <div style='font-family: "Khmer OS"; font-size: 13px; color: #555; line-height: 1.6;'>
        <p><b>លក្ខណៈពិសេស៖</b></p>
        <ul>
            <li>ផែនការអាពាហ៍ពិពាហ៍ពេញលេញ</li>
            <li>ការគ្រប់គ្រងថវិកាដោយស្វ័យប្រវត្តិ</li>
            <li>បញ្ជីអ្នកទទួលអញ្ជើញដែលងាយស្រួល</li>
            <li>ជ្រើសរើសអ្នកផ្គត់ផ្គង់សេវាកម្ម</li>
            <li>ការគ្រប់គ្រងពេលវេលាដោយស្វ័យប្រវត្តិ</li>
        </ul>
        </div>
        """)
        
        left_layout.addWidget(logo_label)
        left_layout.addWidget(app_info)
        left_layout.addWidget(features)
        left_layout.addStretch()
        
        # ផ្នែកស្តាំ - ទម្រង់ចូល
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setAlignment(Qt.AlignCenter)
        
        # ចំណងជើង
        login_title = QLabel("ចូលប្រើប្រាស់")
        login_title.setFont(QFont("Khmer OS", 28, QFont.Bold))
        login_title.setStyleSheet("color: #6a11cb; margin-bottom: 30px;")
        login_title.setAlignment(Qt.AlignCenter)
        
        # ទម្រង់ចូល
        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(20)
        
        # អ៊ីមែល
        email_label = QLabel("អាសយដ្ឋានអ៊ីមែល")
        email_label.setFont(QFont("Khmer OS", 11))
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("បញ្ចូលអ៊ីមែលរបស់អ្នក")
        self.email_input.setMinimumHeight(45)
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border-color: #6a11cb;
                background-color: #ffffff;
            }
        """)
        
        # ពាក្យសម្ងាត់
        password_label = QLabel("ពាក្យសម្ងាត់")
        password_label.setFont(QFont("Khmer OS", 11))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("បញ្ចូលពាក្យសម្ងាត់")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 10px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 14px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border-color: #6a11cb;
                background-color: #ffffff;
            }
        """)
        
        # ជម្រើសចងចាំ
        remember_widget = QWidget()
        remember_layout = QHBoxLayout(remember_widget)
        self.remember_check = QCheckBox("ចងចាំខ្ញុំ")
        self.remember_check.setFont(QFont("Khmer OS", 10))
        forgot_password = QPushButton("ភ្លេចពាក្យសម្ងាត់?")
        forgot_password.setFont(QFont("Khmer OS", 10))
        forgot_password.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #6a11cb;
                border: none;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #2575fc;
            }
        """)
        remember_layout.addWidget(self.remember_check)
        remember_layout.addStretch()
        remember_layout.addWidget(forgot_password)
        
        # ប៊ូតុងចូល
        login_button = QPushButton("ចូលប្រើប្រាស់")
        login_button.setMinimumHeight(50)
        login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #6a11cb, stop:1 #2575fc);
                color: white;
                border: none;
                border-radius: 8px;
                font-family: 'Khmer OS';
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #2575fc, stop:1 #6a11cb);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #5a0cb9, stop:1 #1a65ec);
            }
        """)
        login_button.clicked.connect(self.login)
        
        # ការចូលប្រើប្រាស់ផ្សេងទៀត
        social_label = QLabel("ឬចូលប្រើប្រាស់ជាមួយ")
        social_label.setAlignment(Qt.AlignCenter)
        social_label.setFont(QFont("Khmer OS", 10))
        social_label.setStyleSheet("color: #666; margin: 20px 0 10px 0;")
        
        # ប៊ូតុងសង្គម
        social_widget = QWidget()
        social_layout = QHBoxLayout(social_widget)
        
        google_btn = QPushButton("Google")
        facebook_btn = QPushButton("Facebook")
        
        for btn in [google_btn, facebook_btn]:
            btn.setMinimumHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ffffff;
                    color: #333;
                    border: 2px solid #e0e0e0;
                    border-radius: 8px;
                    font-family: 'Khmer OS';
                    padding: 8px 20px;
                    margin: 0 5px;
                }
                QPushButton:hover {
                    border-color: #6a11cb;
                    background-color: #f9f5ff;
                }
            """)
            social_layout.addWidget(btn)
        
        # សួរពីគណនី
        register_widget = QWidget()
        register_layout = QHBoxLayout(register_widget)
        register_label = QLabel("មិនទាន់មានគណនីទេ?")
        register_label.setFont(QFont("Khmer OS", 10))
        register_btn = QPushButton("ចុះឈ្មោះឥឡូវនេះ")
        register_btn.setFont(QFont("Khmer OS", 10, QFont.Bold))
        register_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #6a11cb;
                border: none;
            }
            QPushButton:hover {
                color: #2575fc;
                text-decoration: underline;
            }
        """)
        register_btn.clicked.connect(self.show_register)
        
        register_layout.addStretch()
        register_layout.addWidget(register_label)
        register_layout.addWidget(register_btn)
        register_layout.addStretch()
        
        # បន្ថែមទាំងអស់ទៅក្នុងទម្រង់
        form_layout.addWidget(email_label)
        form_layout.addWidget(self.email_input)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        form_layout.addWidget(remember_widget)
        form_layout.addWidget(login_button)
        form_layout.addWidget(social_label)
        form_layout.addWidget(social_widget)
        form_layout.addWidget(register_widget)
        
        # បន្ថែមទាំងអស់ទៅក្នុងផ្នែកស្តាំ
        right_layout.addWidget(login_title)
        right_layout.addWidget(form_widget)
        right_layout.addStretch()
        
        # បន្ថែមផ្នែកទាំងពីរទៅក្នុងលំហូរបឋម
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        
    def login(self):
        email = self.email_input.text()
        password = self.password_input.text()
        
        if not email or not password:
            QMessageBox.warning(self, "ព័ត៌មានមិនគ្រប់គ្រាន់", 
                                "សូមបញ្ចូលអ៊ីមែល និងពាក្យសម្ងាត់!")
            return
        
        # នៅទីនេះអ្នកអាចបន្ថែមការផ្ទៀងផ្ទាត់ជាមួយមូលដ្ឋានទិន្នន័យ
        if email == "demo@wedding.kh" and password == "123456":
            self.accept_login()
        else:
            # ក្លែងធ្វើជាការចូលប្រើប្រាស់ជោគជ័យសម្រាប់ការបង្ហាញ
            self.accept_login()
    
    def accept_login(self):
        self.main_window = ModernWeddingWebsiteUI()
        self.main_window.show()
        self.close()
    
    def show_register(self):
        QMessageBox.information(self, "ចុះឈ្មោះ", 
                                "លក្ខណៈពិសេសនៃការចុះឈ្មោះនឹងមកដល់ឆាប់ៗនេះ!")

class ModernWeddingWebsiteUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.guest_list = []
        self.budget_items = []
        self.payment_methods = ["ធនាគា", "ABA", "ACLEDA", "WING", "តាមរយៈទូរស័ព្ទ", "សាច់ប្រាក់"]
        self.currency_types = ["ដុល្លា ($)", "រៀល (៛)"]
        self.currency_rate = 4100  # 1 USD = 4100៛
        self.initUI()
        self.load_sample_data()
        
    def load_sample_data(self):
        # ទិន្នន័យឧទាហរណ៍សម្រាប់ភ្ញៀវ
        sample_guests = [
            ["លី សុផល", "ភ្ញៀវខាងស្រី", "១២៣៤៥៦៧៨៩", "បានរួលរួម", "២ នាក់", "៥០០០០៛"],
            ["គាត់ សំណាង", "ភ្ញៀវខាងប្រុស", "០១២៣៤៥៦៧៨", "រង់ចាំ", "១ នាក់", "២០០០០៛"],
            ["ម៉ាន់ សុខា", "មិត្តភក្តិ", "០៩៨៧៦៥៤៣២", "បានរួលរួម", "៣ នាក់", "១០០០០០៛"],
            ["ណារ៉ុង សោភា", "ក្រុមគ្រួសារ", "០១១២២៣៣៤៤", "មិនអាចមកបាន", "០ នាក់", "០៛"],
            ["វ៉ាន់ ស្រីណាត", "មិត្តភក្តិការងារ", "០៧៧៨៨៩៩០០", "បានរួលរួម", "២ នាក់", "៦០០០០៛"]
        ]
        
        for guest in sample_guests:
            self.guest_list.append(guest)
        
        # ទិន្នន័យឧទាហរណ៍សម្រាប់ថវិកា
        sample_budget = [
            ["កន្លែងរៀបអាពាហ៍ពិពាហ៍", "២,៥០០", "ដុល្លា ($)", "១,២០០", "ដុល្លា ($)", "ធនាគា", "១៥ មករា ២០២៤"],
            ["អាហារ", "៣,០០០", "ដុល្លា ($)", "១,៥០០", "ដុល្លា ($)", "ABA", "២០ មករា ២០២៤"],
            ["ថតរូប", "២,០០០,០០០", "រៀល (៛)", "១,០០០,០០០", "រៀល (៛)", "ACLEDA", "៥ កុម្ភៈ ២០២៤"],
            ["ផ្កា", "៦០០", "ដុល្លា ($)", "៣០០", "ដុល្លា ($)", "សាច់ប្រាក់", "១០ កុម្ភៈ ២០២៤"]
        ]
        
        for item in sample_budget:
            self.budget_items.append(item)
        
    def initUI(self):
        # កំណត់លក្ខណៈបង្អួច
        self.setWindowTitle("វេបសាយរៀបអាពាហ៍ពិពាហ៍ - Wedding Planner Pro")
        self.setGeometry(50, 50, 1400, 850)
        
        # បង្កើតផ្ទាំងកណ្តាល
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # បង្កើតលំហូរបឋម
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # បង្កើតរចនាសម្ព័ន្ធបង្អួចទំនើប
        self.create_modern_header()
        self.create_main_content()
        
        # បង្ហាញបង្អួច
        self.show()
    
    def create_modern_header(self):
        # ផ្នែកផ្ទៃលើទំនើប
        header_widget = QWidget()
        header_widget.setFixedHeight(70)
        header_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                      stop:0 #6a11cb, stop:1 #2575fc);
        """)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # ឈ្មោះកម្មវិធី
        app_name = QLabel("❤️ Wedding Planner Pro")
        app_name.setFont(QFont("Khmer OS", 18, QFont.Bold))
        app_name.setStyleSheet("color: white;")
        
        # របារស្វែងរក
        search_widget = QWidget()
        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(0, 0, 0, 0)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ស្វែងរក...")
        self.search_input.setMinimumWidth(250)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 15px;
                border: none;
                border-radius: 20px;
                background-color: rgba(255, 255, 255, 0.9);
                font-family: 'Khmer OS';
                font-size: 14px;
            }
            QLineEdit:focus {
                background-color: white;
            }
        """)
        
        search_btn = QPushButton("🔍")
        search_btn.setFixedSize(40, 40)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: none;
                border-radius: 20px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_btn)
        
        # របារឧបករណ៍
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setSpacing(15)
        
        # ប៊ូតុងផ្សេងៗ
        notifications_btn = QPushButton("🔔")
        notifications_btn.setToolTip("ដំណឹង")
        messages_btn = QPushButton("✉️")
        messages_btn.setToolTip("សារ")
        profile_btn = QPushButton("👤")
        profile_btn.setToolTip("គណនី")
        
        for btn in [notifications_btn, messages_btn, profile_btn]:
            btn.setFixedSize(40, 40)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.2);
                    border: none;
                    border-radius: 20px;
                    color: white;
                    font-size: 16px;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.3);
                }
            """)
            toolbar_layout.addWidget(btn)
        
        # បន្ថែមទាំងអស់ទៅក្នុងផ្ទៃលើ
        header_layout.addWidget(app_name)
        header_layout.addStretch()
        header_layout.addWidget(search_widget)
        header_layout.addStretch()
        header_layout.addWidget(toolbar_widget)
        
        self.main_layout.addWidget(header_widget)
    
    def create_main_content(self):
        # ខ្លឹមសារបឋម
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # ផ្នែកឆ្វេង - របារចំហៀង
        sidebar = self.create_modern_sidebar()
        
        # ផ្នែកស្តាំ - ខ្លឹមសារ
        content_area = self.create_content_area()
        
        content_layout.addWidget(sidebar, 1)
        content_layout.addWidget(content_area, 3)
        
        self.main_layout.addWidget(content_widget)
    
    def create_modern_sidebar(self):
        # របារចំហៀងទំនើប
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 15px;
                padding: 20px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setSpacing(15)
        
        # ព័ត៌មានអ្នកប្រើប្រាស់
        user_widget = QWidget()
        user_layout = QHBoxLayout(user_widget)
        
        avatar = QLabel("👰")
        avatar.setStyleSheet("""
            QLabel {
                font-size: 40px;
                padding: 10px;
            }
        """)
        
        user_info = QWidget()
        user_info_layout = QVBoxLayout(user_info)
        user_name = QLabel("ស្រី ស្រីធីតា")
        user_name.setFont(QFont("Khmer OS", 14, QFont.Bold))
        user_name.setStyleSheet("color: #333;")
        user_date = QLabel("ថ្ងៃរៀបអាពាហ៍ពិពាហ៍: ១២ មេសា ២០២៤")
        user_date.setFont(QFont("Khmer OS", 10))
        user_date.setStyleSheet("color: #666;")
        
        user_info_layout.addWidget(user_name)
        user_info_layout.addWidget(user_date)
        
        user_layout.addWidget(avatar)
        user_layout.addWidget(user_info)
        
        # ប៊ូតុងរហ័ស
        quick_actions = QLabel("សកម្មភាពរហ័ស")
        quick_actions.setFont(QFont("Khmer OS", 12, QFont.Bold))
        quick_actions.setStyleSheet("color: #6a11cb; margin-top: 10px;")
        
        # បង្កើតប៊ូតុងរហ័ស
        add_guest_btn = self.create_sidebar_button("👥 បន្ថែមភ្ញៀវថ្មី", "#e3f2fd")
        add_guest_btn.clicked.connect(self.show_add_guest_dialog)
        
        add_budget_btn = self.create_sidebar_button("💰 បន្ថែមចំណាយ", "#f3e5f5")
        add_budget_btn.clicked.connect(self.show_add_budget_dialog)
        
        view_calendar_btn = self.create_sidebar_button("📅 មើលប្រតិទិន", "#e8f5e9")
        
        # តារាងអង្គីកររបស់វិធីសាស្រ្ត
        nav_label = QLabel("ការរុករក")
        nav_label.setFont(QFont("Khmer OS", 12, QFont.Bold))
        nav_label.setStyleSheet("color: #6a11cb; margin-top: 20px;")
        
        # បង្កើតប៊ូតុងវិធីសាស្រ្ត
        nav_items = [
            ("🏠", "ទំព័រដើម", self.show_home),
            ("📋", "ផែនការពេញលេញ", self.show_planning),
            ("👥", "អ្នកទទួលអញ្ជើញ", self.show_guests_tab),
            ("💰", "ថវិកា", self.show_budget_tab),
            ("🏢", "អ្នកផ្គត់ផ្គង់", self.show_vendors),
            ("🎨", "ការរចនា", self.show_design),
            ("📊", "របាយការណ៍", self.show_reports),
            ("⚙️", "ការកំណត់", self.show_settings)
        ]
        
        # បន្ថែមទាំងអស់ទៅក្នុងរបារចំហៀង
        sidebar_layout.addWidget(user_widget)
        sidebar_layout.addWidget(quick_actions)
        sidebar_layout.addWidget(add_guest_btn)
        sidebar_layout.addWidget(add_budget_btn)
        sidebar_layout.addWidget(view_calendar_btn)
        sidebar_layout.addWidget(nav_label)
        
        for icon, text, handler in nav_items:
            btn = self.create_nav_button(icon, text)
            btn.clicked.connect(handler)
            sidebar_layout.addWidget(btn)
        
        sidebar_layout.addStretch()
        
        # ព័ត៌មានកាលបរិច្ឆេទ
        date_widget = QWidget()
        date_layout = QVBoxLayout(date_widget)
        date_layout.setContentsMargins(10, 10, 10, 10)
        
        current_date = QLabel(datetime.now().strftime("%d/%m/%Y"))
        current_date.setAlignment(Qt.AlignCenter)
        current_date.setFont(QFont("Khmer OS", 12, QFont.Bold))
        current_date.setStyleSheet("""
            color: #6a11cb;
            padding: 10px;
            background-color: #f3f3f3;
            border-radius: 10px;
        """)
        
        countdown = QLabel("នៅសល់ ៧៥ ថ្ងៃទៀត")
        countdown.setAlignment(Qt.AlignCenter)
        countdown.setFont(QFont("Khmer OS", 10))
        countdown.setStyleSheet("color: #ff6b6b;")
        
        date_layout.addWidget(current_date)
        date_layout.addWidget(countdown)
        
        sidebar_layout.addWidget(date_widget)
        
        return sidebar
    
    def create_sidebar_button(self, text, color):
        btn = QPushButton(text)
        btn.setFont(QFont("Khmer OS", 11))
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border: none;
                border-radius: 10px;
                padding: 12px 15px;
                text-align: left;
                color: #333;
            }}
            QPushButton:hover {{
                background-color: #e0e0e0;
            }}
        """)
        return btn
    
    def create_nav_button(self, icon, text):
        btn = QPushButton(f"{icon}  {text}")
        btn.setFont(QFont("Khmer OS", 11))
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 10px;
                padding: 12px 15px;
                text-align: left;
                color: #555;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
                color: #6a11cb;
            }
        """)
        return btn
    
    def create_content_area(self):
        # តំបន់ខ្លឹមសារ
        content_area = QWidget()
        content_layout = QVBoxLayout(content_area)
        
        # ចំណងជើង
        welcome_label = QLabel("សូមស្វាគមន៍មកកាន់ផែនការអាពាហ៍ពិពាហ៍របស់អ្នក!")
        welcome_label.setFont(QFont("Khmer OS", 20, QFont.Bold))
        welcome_label.setStyleSheet("color: #333; margin-bottom: 10px;")
        
        subtitle = QLabel("ចាប់ផ្តើមធ្វើឱ្យថ្ងៃពិសេសរបស់អ្នកក្លាយជាការចងចាំដ៏ស្រស់ស្អាត")
        subtitle.setFont(QFont("Khmer OS", 12))
        subtitle.setStyleSheet("color: #666; margin-bottom: 30px;")
        
        # កាតស្ថិតិ
        stats_widget = self.create_stats_cards()
        
        # តារាងអង្គីករខ្លឹមសារ
        self.content_tabs = QTabWidget()
        self.content_tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                padding: 12px 25px;
                margin-right: 5px;
                border-radius: 8px 8px 0 0;
                font-family: 'Khmer OS';
                font-size: 13px;
                color: #666;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #6a11cb;
                font-weight: bold;
                border-bottom: 3px solid #6a11cb;
            }
            QTabBar::tab:hover {
                background-color: #e0e0e0;
            }
        """)
        
        # បង្កើតផ្ទាំងផ្សេងៗ
        self.create_dashboard_tab()
        self.create_guests_tab()
        self.create_budget_tab()
        self.create_tasks_tab()
        
        content_layout.addWidget(welcome_label)
        content_layout.addWidget(subtitle)
        content_layout.addWidget(stats_widget)
        content_layout.addWidget(self.content_tabs)
        
        return content_area
    
    def create_stats_cards(self):
        # កាតស្ថិតិ
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        stats_layout.setSpacing(15)
        
        # គណនាស្ថិតិពីទិន្នន័យ
        total_guests = len(self.guest_list)
        confirmed_guests = sum(1 for guest in self.guest_list if guest[3] == "បានរួលរួម")
        
        # គណនាថវិកាសរុប
        total_budget = 0
        spent_budget = 0
        
        for item in self.budget_items:
            amount = float(item[1].replace(",", "").replace("១", "1").replace("២", "2").replace("៣", "3")
                          .replace("៤", "4").replace("៥", "5").replace("៦", "6").replace("៧", "7")
                          .replace("៨", "8").replace("៩", "9").replace("០", "0"))
            
            if item[2] == "រៀល (៛)":
                amount = amount / self.currency_rate  # បំលែងទៅជាដុល្លា
            
            total_budget += amount
            
            spent_amount = float(item[3].replace(",", "").replace("១", "1").replace("២", "2").replace("៣", "3")
                               .replace("៤", "4").replace("៥", "5").replace("៦", "6").replace("៧", "7")
                               .replace("៨", "8").replace("៩", "9").replace("០", "0"))
            
            if item[4] == "រៀល (៛)":
                spent_amount = spent_amount / self.currency_rate
            
            spent_budget += spent_amount
        
        # គណនាប្រាក់ចងដៃសរុប
        total_gifts = 0
        for guest in self.guest_list:
            gift_amount = guest[5].replace("៛", "").replace(",", "").strip()
            if gift_amount and gift_amount != "០":
                amount = float(gift_amount.replace("១", "1").replace("២", "2").replace("៣", "3")
                              .replace("៤", "4").replace("៥", "5").replace("៦", "6").replace("៧", "7")
                              .replace("៨", "8").replace("៩", "9").replace("០", "0"))
                total_gifts += amount / self.currency_rate  # បំលែងទៅជាដុល្លា
        
        stats_data = [
            ("ថវិកាសរុប", f"${total_budget:,.0f}", "#6a11cb", "💰"),
            ("បានប្រើប្រាស់", f"${spent_budget:,.0f}", "#2575fc", "📊"),
            ("ភ្ញៀវសរុប", f"{total_guests} នាក់", "#00b09b", "👥"),
            ("ប្រាក់ចងដៃ", f"${total_gifts:,.0f}", "#ff6b6b", "🎁")
        ]
        
        for title, value, color, icon in stats_data:
            card = self.create_stat_card(title, value, color, icon)
            stats_layout.addWidget(card)
        
        return stats_widget
    
    def create_stat_card(self, title, value, color, icon):
        card = QWidget()
        card.setFixedHeight(120)
        card.setStyleSheet(f"""
            QWidget {{
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
                padding: 15px;
            }}
        """)
        
        card_layout = QVBoxLayout(card)
        
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Khmer OS", 11))
        title_label.setStyleSheet("color: #666;")
        
        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        top_layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Khmer OS", 22, QFont.Bold))
        value_label.setStyleSheet(f"color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        
        card_layout.addWidget(top_widget)
        card_layout.addWidget(value_label)
        card_layout.addStretch()
        
        return card
    
    def create_dashboard_tab(self):
        # ផ្ទាំងផ្ទាំងគ្រប់គ្រង
        dashboard_tab = QWidget()
        layout = QVBoxLayout(dashboard_tab)
        
        # របារវឌ្ឍនភាព
        progress_label = QLabel("វឌ្ឍនភាពសរុប: ៤៥%")
        progress_label.setFont(QFont("Khmer OS", 14, QFont.Bold))
        
        self.overall_progress = QProgressBar()
        self.overall_progress.setValue(45)
        self.overall_progress.setFormat("%p%")
        self.overall_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                text-align: center;
                height: 25px;
                font-family: 'Khmer OS';
                font-size: 14px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #6a11cb, stop:1 #2575fc);
                border-radius: 6px;
            }
        """)
        
        # កាតភារកិច្ចសំខាន់ៗ
        tasks_label = QLabel("ភារកិច្ចសំខាន់ៗ")
        tasks_label.setFont(QFont("Khmer OS", 16, QFont.Bold))
        
        tasks_widget = QWidget()
        tasks_layout = QVBoxLayout(tasks_widget)
        
        important_tasks = [
            ("ជ្រើសរើសកន្លែងរៀបអាពាហ៍ពិពាហ៍", "កំពុងធ្វើ", "🏢"),
            ("បង់ថ្លៃរៀបអាពាហ៍ពិពាហ៍ ៥០%", "រង់ចាំ", "💰"),
            ("ជ្រើសរើសសម្លៀកបំពាក់", "មិនទាន់ចាប់ផ្តើម", "👗"),
            ("បញ្ជូលបញ្ជីអ្នកទទួលអញ្ជើញ", "កំពុងធ្វើ", "📋")
        ]
        
        for task, status, icon in important_tasks:
            task_widget = self.create_task_item(task, status, icon)
            tasks_layout.addWidget(task_widget)
        
        layout.addWidget(progress_label)
        layout.addWidget(self.overall_progress)
        layout.addSpacing(20)
        layout.addWidget(tasks_label)
        layout.addWidget(tasks_widget)
        layout.addStretch()
        
        self.content_tabs.addTab(dashboard_tab, "ផ្ទាំងគ្រប់គ្រង")
    
    def create_task_item(self, task, status, icon):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        icon_label = QLabel(icon)
        
        task_label = QLabel(task)
        task_label.setFont(QFont("Khmer OS", 11))
        
        status_label = QLabel(status)
        status_label.setFont(QFont("Khmer OS", 10))
        
        if status == "កំពុងធ្វើ":
            status_label.setStyleSheet("color: #ffa500; background-color: #fff3cd; padding: 5px 10px; border-radius: 5px;")
        elif status == "រង់ចាំ":
            status_label.setStyleSheet("color: #6c757d; background-color: #e2e3e5; padding: 5px 10px; border-radius: 5px;")
        else:
            status_label.setStyleSheet("color: #dc3545; background-color: #f8d7da; padding: 5px 10px; border-radius: 5px;")
        
        layout.addWidget(icon_label)
        layout.addWidget(task_label, 1)
        layout.addWidget(status_label)
        
        widget.setStyleSheet("""
            QWidget {
                padding: 10px;
                border-bottom: 1px solid #f0f0f0;
            }
            QWidget:hover {
                background-color: #f9f9f9;
                border-radius: 8px;
            }
        """)
        
        return widget
    
    def create_guests_tab(self):
        # ផ្ទាំងគ្រប់គ្រងភ្ញៀវ
        guests_tab = QWidget()
        layout = QVBoxLayout(guests_tab)
        
        # បង្កើតរបារឧបករណ៍
        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout(toolbar_widget)
        
        # ប៊ូតុងបន្ថែមភ្ញៀវ
        add_guest_btn = QPushButton("➕ បន្ថែមភ្ញៀវថ្មី")
        add_guest_btn.setStyleSheet("""
            QPushButton {
                background-color: #6a11cb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-family: 'Khmer OS';
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2575fc;
            }
        """)
        add_guest_btn.clicked.connect(self.show_add_guest_dialog)
        
        # ប៊ូតុងនាំចូល/នាំចេញ
        import_btn = QPushButton("📥 នាំចូល")
        export_btn = QPushButton("📤 នាំចេញ")
        
        for btn in [import_btn, export_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #f8f9fa;
                    color: #333;
                    border: 1px solid #dee2e6;
                    border-radius: 8px;
                    padding: 10px 15px;
                    font-family: 'Khmer OS';
                    font-size: 13px;
                    margin-left: 5px;
                }
                QPushButton:hover {
                    background-color: #e9ecef;
                }
            """)
        
        # ស្ថិតិភ្ញៀវ
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        
        total = sum(int(guest[4].replace("នាក់", "").strip()) for guest in self.guest_list if guest[3] != "មិនអាចមកបាន")
        confirmed = sum(int(guest[4].replace("នាក់", "").strip()) for guest in self.guest_list if guest[3] == "បានរួលរួម")
        
        # គណនាប្រាក់ចងដៃសរុប
        total_gifts = 0
        for guest in self.guest_list:
            gift_amount = guest[5].replace("៛", "").replace(",", "").strip()
            if gift_amount and gift_amount != "០":
                amount = float(gift_amount.replace("១", "1").replace("២", "2").replace("៣", "3")
                              .replace("៤", "4").replace("៥", "5").replace("៦", "6").replace("៧", "7")
                              .replace("៨", "8").replace("៩", "9").replace("០", "0"))
                total_gifts += amount
        
        stats_labels = [
            f"សរុប: {len(self.guest_list)} គ្រួសារ",
            f"បានរួលរួម: {sum(1 for g in self.guest_list if g[3] == 'បានរួលរួម')}",
            f"រង់ចាំ: {sum(1 for g in self.guest_list if g[3] == 'រង់ចាំ')}",
            f"មិនអាចមកបាន: {sum(1 for g in self.guest_list if g[3] == 'មិនអាចមកបាន')}",
            f"ប្រាក់ចងដៃ: {total_gifts:,.0f}៛"
        ]
        
        for stat in stats_labels:
            label = QLabel(stat)
            label.setFont(QFont("Khmer OS", 10))
            label.setStyleSheet("""
                padding: 8px 12px;
                background-color: #f8f9fa;
                border-radius: 6px;
                margin-right: 10px;
            """)
            stats_layout.addWidget(label)
        
        stats_layout.addStretch()
        
        # តារាងភ្ញៀវ
        self.guests_table = QTableWidget()
        self.guests_table.setColumnCount(7)
        self.guests_table.setHorizontalHeaderLabels(["លេខ", "ឈ្មោះភ្ញៀវ", "ប្រភេទ", "លេខទូរស័ព្ទ", "ស្ថានភាព", "ចំនួន", "ប្រាក់ចងដៃ"])
        self.guests_table.setAlternatingRowColors(True)
        self.guests_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                font-family: 'Khmer OS';
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #6a11cb;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
        """)
        
        self.update_guests_table()
        
        # បន្ថែមទាំងអស់ទៅក្នុងលំហូរ
        toolbar_layout.addWidget(add_guest_btn)
        toolbar_layout.addWidget(import_btn)
        toolbar_layout.addWidget(export_btn)
        toolbar_layout.addStretch()
        
        layout.addWidget(toolbar_widget)
        layout.addWidget(stats_widget)
        layout.addWidget(self.guests_table)
        
        self.content_tabs.addTab(guests_tab, "គ្រប់គ្រងភ្ញៀវ")
    
    def update_guests_table(self):
        self.guests_table.setRowCount(len(self.guest_list))
        
        for row, guest in enumerate(self.guest_list):
            # បន្ថែមលេខរៀង
            self.guests_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            
            # បន្ថែមទិន្នន័យផ្សេងៗ
            for col in range(6):
                self.guests_table.setItem(row, col + 1, QTableWidgetItem(guest[col]))
            
            # បង្កើតប៊ូតុងសកម្មភាព
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 2, 5, 2)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 30)
            edit_btn.setToolTip("កែសម្រួល")
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_guest(r))
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(30, 30)
            delete_btn.setToolTip("លុប")
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_guest(r))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            # បន្ថែមសកម្មភាពក្នុងជួរទី 7
            action_widget2 = QWidget()
            action_layout2 = QHBoxLayout(action_widget2)
            action_layout2.setContentsMargins(5, 2, 5, 2)
            
            action_layout2.addWidget(edit_btn)
            action_layout2.addWidget(delete_btn)
            
            # ដោយសារយើងបានបន្ថែមជួរប្រាក់ចងដៃ ឥឡូវយើងត្រូវការជួរទី 8 សម្រាប់សកម្មភាព
            # ដូច្នេះយើងត្រូវបន្ថែមជួរមួយទៀត
            self.guests_table.setColumnCount(8)
            self.guests_table.setHorizontalHeaderLabels(["លេខ", "ឈ្មោះភ្ញៀវ", "ប្រភេទ", "លេខទូរស័ព្ទ", "ស្ថានភាព", "ចំនួន", "ប្រាក់ចងដៃ", "សកម្មភាព"])
            
            self.guests_table.setCellWidget(row, 7, action_widget2)
        
        self.guests_table.resizeColumnsToContents()
    
    def create_budget_tab(self):
        # ផ្ទាំងគ្រប់គ្រងថវិកា
        budget_tab = QWidget()
        layout = QVBoxLayout(budget_tab)
        
        # ស្ថិតិថវិកា
        stats_widget = QWidget()
        stats_layout = QHBoxLayout(stats_widget)
        
        total_budget_usd = 0
        total_budget_riel = 0
        spent_budget_usd = 0
        spent_budget_riel = 0
        
        for item in self.budget_items:
            amount = float(item[1].replace(",", "").replace("១", "1").replace("២", "2").replace("៣", "3")
                          .replace("៤", "4").replace("៥", "5").replace("៦", "6").replace("៧", "7")
                          .replace("៨", "8").replace("៩", "9").replace("០", "0"))
            
            spent_amount = float(item[3].replace(",", "").replace("១", "1").replace("២", "2").replace("៣", "3")
                               .replace("៤", "4").replace("៥", "5").replace("៦", "6").replace("៧", "7")
                               .replace("៨", "8").replace("៩", "9").replace("០", "0"))
            
            if item[2] == "ដុល្លា ($)":
                total_budget_usd += amount
            else:
                total_budget_riel += amount
            
            if item[4] == "ដុល្លា ($)":
                spent_budget_usd += spent_amount
            else:
                spent_budget_riel += spent_amount
        
        # បំលែងទៅជាដុល្លាសរុប
        total_budget = total_budget_usd + (total_budget_riel / self.currency_rate)
        spent_budget = spent_budget_usd + (spent_budget_riel / self.currency_rate)
        remaining = total_budget - spent_budget
        
        budget_stats = [
            f"ថវិកាសរុប: ${total_budget:,.0f}",
            f"បានចំណាយ: ${spent_budget:,.0f}",
            f"នៅសល់: ${remaining:,.0f}",
            f"ភាគរយ: {(spent_budget/total_budget*100 if total_budget > 0 else 0):.1f}%"
        ]
        
        for stat in budget_stats:
            label = QLabel(stat)
            label.setFont(QFont("Khmer OS", 11, QFont.Bold))
            label.setStyleSheet("""
                padding: 10px 15px;
                background-color: #f8f9fa;
                border-radius: 8px;
                margin-right: 15px;
                color: #333;
            """)
            stats_layout.addWidget(label)
        
        stats_layout.addStretch()
        
        # របារវឌ្ឍនភាព
        progress_label = QLabel("ការចំណាយប្រាក់")
        progress_label.setFont(QFont("Khmer OS", 14))
        
        self.budget_progress = QProgressBar()
        self.budget_progress.setValue(int((spent_budget/total_budget*100) if total_budget > 0 else 0))
        self.budget_progress.setFormat("%p%")
        self.budget_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                text-align: center;
                height: 25px;
                font-family: 'Khmer OS';
                font-size: 14px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                          stop:0 #00b09b, stop:1 #96c93d);
                border-radius: 6px;
            }
        """)
        
        # ប៊ូតុងបន្ថែមថវិកា
        add_budget_btn = QPushButton("➕ បន្ថែមចំណាយថ្មី")
        add_budget_btn.setStyleSheet("""
            QPushButton {
                background-color: #00b09b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-family: 'Khmer OS';
                font-size: 14px;
                font-weight: bold;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #96c93d;
            }
        """)
        add_budget_btn.clicked.connect(self.show_add_budget_dialog)
        
        # តារាងថវិកា
        self.budget_table = QTableWidget()
        self.budget_table.setColumnCount(9)
        self.budget_table.setHorizontalHeaderLabels(["លេខ", "ធាតុចំណាយ", "ថវិកា", "រូបិយប័ណ្ណ", "បានចំណាយ", "រូបិយប័ណ្ណ", "កន្លែងបញ្ជូលប្រាក់", "កាលបរិច្ឆេទ", "សកម្មភាព"])
        self.budget_table.setAlternatingRowColors(True)
        self.budget_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                font-family: 'Khmer OS';
                font-size: 12px;
            }
            QHeaderView::section {
                background-color: #00b09b;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
        """)
        
        self.update_budget_table()
        
        # បន្ថែមទាំងអស់ទៅក្នុងលំហូរ
        layout.addWidget(stats_widget)
        layout.addWidget(progress_label)
        layout.addWidget(self.budget_progress)
        layout.addWidget(add_budget_btn)
        layout.addWidget(self.budget_table)
        
        self.content_tabs.addTab(budget_tab, "គ្រប់គ្រងថវិកា")
    
    def update_budget_table(self):
        self.budget_table.setRowCount(len(self.budget_items))
        
        for row, item in enumerate(self.budget_items):
            # បន្ថែមលេខរៀង
            self.budget_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
            
            # បន្ថែមទិន្នន័យផ្សេងៗ
            for col in range(7):
                self.budget_table.setItem(row, col + 1, QTableWidgetItem(item[col]))
            
            # បង្កើតប៊ូតុងសកម្មភាព
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 2, 5, 2)
            
            edit_btn = QPushButton("✏️")
            edit_btn.setFixedSize(30, 30)
            edit_btn.setToolTip("កែសម្រួល")
            edit_btn.clicked.connect(lambda checked, r=row: self.edit_budget_item(r))
            
            delete_btn = QPushButton("🗑️")
            delete_btn.setFixedSize(30, 30)
            delete_btn.setToolTip("លុប")
            delete_btn.clicked.connect(lambda checked, r=row: self.delete_budget_item(r))
            
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)
            
            self.budget_table.setCellWidget(row, 8, action_widget)
        
        self.budget_table.resizeColumnsToContents()
    
    def create_tasks_tab(self):
        # ផ្ទាំងភារកិច្ច
        tasks_tab = QWidget()
        layout = QVBoxLayout(tasks_tab)
        
        # ប៊ូតុងបន្ថែមភារកិច្ច
        add_task_btn = QPushButton("➕ បន្ថែមភារកិច្ចថ្មី")
        add_task_btn.setStyleSheet("""
            QPushButton {
                background-color: #6a11cb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-family: 'Khmer OS';
                font-size: 14px;
                font-weight: bold;
                max-width: 200px;
            }
            QPushButton:hover {
                background-color: #2575fc;
            }
        """)
        
        # តារាងភារកិច្ច
        tasks_table = QTableWidget()
        tasks_table.setColumnCount(5)
        tasks_table.setHorizontalHeaderLabels(["ភារកិច្ច", "ថ្ងៃត្រូវបំពេញ", "ស្ថានភាព", "អ្នកទទួលខុសត្រូវ", "សកម្មភាព"])
        
        tasks_data = [
            ["ជួបអ្នកផ្គត់ផ្គង់ផ្កា", "១៥ មករា ២០២៤", "កំពុងធ្វើ", "ស្រី ស្រីធីតា", "✏️ ❌"],
            ["ទិញសម្លៀកបំពាក់", "៣០ មករា ២០២៤", "រង់ចាំ", "គាត់ សំណាង", "✏️ ❌"],
            ["បង្កើតបញ្ជីតន្ត្រី", "១០ កុម្ភៈ ២០២៤", "បានបញ្ចប់", "ស្រី ស្រីធីតា", "✏️ ❌"],
            ["ជ្រើសរើសម៉ូត", "២០ កុម្ភៈ ២០២៤", "កំពុងធ្វើ", "ស្រី ស្រីធីតា", "✏️ ❌"],
        ]
        
        tasks_table.setRowCount(len(tasks_data))
        for row, data in enumerate(tasks_data):
            for col, value in enumerate(data):
                tasks_table.setItem(row, col, QTableWidgetItem(value))
        
        tasks_table.horizontalHeader().setStretchLastSection(True)
        tasks_table.resizeColumnsToContents()
        
        layout.addWidget(add_task_btn)
        layout.addWidget(tasks_table)
        
        self.content_tabs.addTab(tasks_tab, "ភារកិច្ច")
    
    def show_add_guest_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("បន្ថែមភ្ញៀវថ្មី")
        dialog.setFixedSize(500, 500)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("បន្ថែមភ្ញៀវថ្មី")
        title.setFont(QFont("Khmer OS", 16, QFont.Bold))
        title.setStyleSheet("color: #6a11cb; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setSpacing(15)
        
        # ឈ្មោះភ្ញៀវ
        name_input = QLineEdit()
        name_input.setPlaceholderText("ឈ្មោះពេញ")
        name_input.setMinimumHeight(40)
        
        # ប្រភេទភ្ញៀវ
        type_combo = QComboBox()
        type_combo.addItems(["ភ្ញៀវខាងស្រី", "ភ្ញៀវខាងប្រុស", "មិត្តភក្តិ", "ក្រុមគ្រួសារ", "ក្រុមការងារ", "ផ្សេងៗ"])
        
        # លេខទូរស័ព្ទ
        phone_input = QLineEdit()
        phone_input.setPlaceholderText("លេខទូរស័ព្ទ")
        phone_input.setMinimumHeight(40)
        
        # ស្ថានភាព (បានកែពី "បានបញ្ជាក់" ទៅ "បានរួលរួម")
        status_combo = QComboBox()
        status_combo.addItems(["បានរួលរួម", "រង់ចាំ", "មិនអាចមកបាន"])
        
        # ចំនួន
        count_input = QLineEdit()
        count_input.setPlaceholderText("ចំនួននាក់")
        count_input.setMinimumHeight(40)
        
        # ប្រាក់ចងដៃ (បន្ថែមថ្មី)
        gift_input = QLineEdit()
        gift_input.setPlaceholderText("ចំនួនប្រាក់ចងដៃ (៛)")
        gift_input.setMinimumHeight(40)
        
        # បន្ថែមទៅក្នុងទម្រង់
        form_layout.addRow("ឈ្មោះភ្ញៀវ:", name_input)
        form_layout.addRow("ប្រភេទ:", type_combo)
        form_layout.addRow("លេខទូរស័ព្ទ:", phone_input)
        form_layout.addRow("ស្ថានភាព:", status_combo)
        form_layout.addRow("ចំនួននាក់:", count_input)
        form_layout.addRow("ប្រាក់ចងដៃ:", gift_input)
        
        # ប៊ូតុង
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        save_btn = QPushButton("រក្សាទុក")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #6a11cb;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-family: 'Khmer OS';
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2575fc;
            }
        """)
        
        cancel_btn = QPushButton("បោះបង់")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-family: 'Khmer OS';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        # បន្ថែមទាំងអស់ទៅក្នុងលំហូរ
        layout.addWidget(title)
        layout.addWidget(form_widget)
        layout.addWidget(button_widget)
        
        def save_guest():
            name = name_input.text().strip()
            guest_type = type_combo.currentText()
            phone = phone_input.text().strip()
            status = status_combo.currentText()
            count = count_input.text().strip()
            gift = gift_input.text().strip()
            
            if not name or not count:
                QMessageBox.warning(dialog, "ព័ត៌មានមិនគ្រប់គ្រាន់", "សូមបញ្ចូលឈ្មោះ និងចំនួននាក់!")
                return
            
            if not gift:
                gift = "០៛"
            elif not gift.endswith("៛"):
                gift = f"{gift}៛"
            
            self.guest_list.append([name, guest_type, phone, status, f"{count} នាក់", gift])
            self.update_guests_table()
            
            # ធ្វើបច្ចុប្បន្នភាពស្ថិតិ
            self.content_tabs.setCurrentIndex(0)  # ទៅកាន់ dashboard
            self.content_tabs.setCurrentIndex(1)  # ត្រឡប់ទៅកាន់ភ្ញៀវ
            
            QMessageBox.information(dialog, "ជោគជ័យ", "បានបន្ថែមភ្ញៀវថ្មីដោយជោគជ័យ!")
            dialog.close()
        
        def cancel():
            dialog.close()
        
        save_btn.clicked.connect(save_guest)
        cancel_btn.clicked.connect(cancel)
        
        dialog.exec_()
    
    def show_add_budget_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("បន្ថែមចំណាយថ្មី")
        dialog.setFixedSize(600, 550)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 10px;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        
        title = QLabel("បន្ថែមចំណាយថ្មី")
        title.setFont(QFont("Khmer OS", 16, QFont.Bold))
        title.setStyleSheet("color: #00b09b; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        
        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setSpacing(15)
        
        # ធាតុចំណាយ
        item_input = QLineEdit()
        item_input.setPlaceholderText("ឧទាហរណ៍៖ កន្លែងរៀបអាពាហ៍ពិពាហ៍")
        item_input.setMinimumHeight(40)
        
        # ថវិកា - ចំនួន
        budget_input = QLineEdit()
        budget_input.setPlaceholderText("ចំនួនទឹកប្រាក់")
        budget_input.setMinimumHeight(40)
        
        # ថវិកា - រូបិយប័ណ្ណ
        budget_currency_combo = QComboBox()
        budget_currency_combo.addItems(self.currency_types)
        
        # បានចំណាយ - ចំនួន
        spent_input = QLineEdit()
        spent_input.setPlaceholderText("ចំនួនដែលបានចំណាយ")
        spent_input.setMinimumHeight(40)
        
        # បានចំណាយ - រូបិយប័ណ្ណ
        spent_currency_combo = QComboBox()
        spent_currency_combo.addItems(self.currency_types)
        
        # កន្លែងបញ្ជូលប្រាក់
        payment_combo = QComboBox()
        payment_combo.addItems(self.payment_methods)
        
        # កាលបរិច្ឆេទ
        date_input = QDateEdit()
        date_input.setCalendarPopup(True)
        date_input.setDate(QDate.currentDate())
        date_input.setMinimumHeight(40)
        
        # បន្ថែមទៅក្នុងទម្រង់
        form_layout.addRow("ធាតុចំណាយ:", item_input)
        
        # បង្កើត layout សម្រាប់ថវិកា
        budget_widget = QWidget()
        budget_layout = QHBoxLayout(budget_widget)
        budget_layout.setContentsMargins(0, 0, 0, 0)
        budget_layout.addWidget(budget_input)
        budget_layout.addWidget(budget_currency_combo)
        form_layout.addRow("ថវិកា:", budget_widget)
        
        # បង្កើត layout សម្រាប់បានចំណាយ
        spent_widget = QWidget()
        spent_layout = QHBoxLayout(spent_widget)
        spent_layout.setContentsMargins(0, 0, 0, 0)
        spent_layout.addWidget(spent_input)
        spent_layout.addWidget(spent_currency_combo)
        form_layout.addRow("បានចំណាយ:", spent_widget)
        
        form_layout.addRow("កន្លែងបញ្ជូលប្រាក់:", payment_combo)
        form_layout.addRow("កាលបរិច្ឆេទ:", date_input)
        
        # ប៊ូតុងបំលែងរូបិយប័ណ្ណ
        convert_btn = QPushButton("🔄 បំលែងរូបិយប័ណ្ណ")
        convert_btn.setStyleSheet("""
            QPushButton {
                background-color: #ffc107;
                color: #333;
                border: none;
                border-radius: 8px;
                padding: 10px 15px;
                font-family: 'Khmer OS';
                font-size: 12px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #e0a800;
            }
        """)
        convert_btn.clicked.connect(lambda: self.convert_currency(budget_input, budget_currency_combo, spent_input, spent_currency_combo))
        
        # ប៊ូតុង
        button_widget = QWidget()
        button_layout = QHBoxLayout(button_widget)
        
        save_btn = QPushButton("រក្សាទុក")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #00b09b;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-family: 'Khmer OS';
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #96c93d;
            }
        """)
        
        cancel_btn = QPushButton("បោះបង់")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 30px;
                font-family: 'Khmer OS';
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        # បន្ថែមទាំងអស់ទៅក្នុងលំហូរ
        layout.addWidget(title)
        layout.addWidget(form_widget)
        layout.addWidget(convert_btn)
        layout.addWidget(button_widget)
        
        def save_budget():
            item = item_input.text().strip()
            budget = budget_input.text().strip()
            budget_currency = budget_currency_combo.currentText()
            spent = spent_input.text().strip()
            spent_currency = spent_currency_combo.currentText()
            payment = payment_combo.currentText()
            date = date_input.date().toString("dd/MM/yyyy")
            
            if not item or not budget or not spent:
                QMessageBox.warning(dialog, "ព័ត៌មានមិនគ្រប់គ្រាន់", "សូមបញ្ចូលព័ត៌មានទាំងអស់!")
                return
            
            self.budget_items.append([item, budget, budget_currency, spent, spent_currency, payment, date])
            self.update_budget_table()
            
            # ធ្វើបច្ចុប្បន្នភាពស្ថិតិ
            self.content_tabs.setCurrentIndex(0)  # ទៅកាន់ dashboard
            self.content_tabs.setCurrentIndex(2)  # ត្រឡប់ទៅកាន់ថវិកា
            
            QMessageBox.information(dialog, "ជោគជ័យ", "បានបន្ថែមចំណាយថ្មីដោយជោគជ័យ!")
            dialog.close()
        
        def cancel():
            dialog.close()
        
        save_btn.clicked.connect(save_budget)
        cancel_btn.clicked.connect(cancel)
        
        dialog.exec_()
    
    def convert_currency(self, budget_input, budget_currency_combo, spent_input, spent_currency_combo):
        # បំលែងរូបិយប័ណ្ណ
        try:
            budget_amount = float(budget_input.text().strip())
            budget_currency = budget_currency_combo.currentText()
            
            if budget_currency == "ដុល្លា ($)":
                # បំលែងពីដុល្លាទៅរៀល
                converted_amount = budget_amount * self.currency_rate
                spent_currency_combo.setCurrentText("រៀល (៛)")
                spent_input.setText(f"{converted_amount:,.0f}")
            else:
                # បំលែងពីរៀលទៅដុល្លា
                converted_amount = budget_amount / self.currency_rate
                spent_currency_combo.setCurrentText("ដុល្លា ($)")
                spent_input.setText(f"{converted_amount:,.2f}")
                
        except ValueError:
            QMessageBox.warning(self, "កំហុស", "សូមបញ្ចូលលេខត្រឹមត្រូវ!")
    
    def edit_guest(self, row):
        # កែសម្រួលភ្ញៀវ (សាមញ្ញ)
        QMessageBox.information(self, "កែសម្រួល", f"ការកែសម្រួលភ្ញៀវ លេខ {row+1} នឹងមកដល់នៅក្នុងកំណែបន្ទាប់!")
    
    def delete_guest(self, row):
        reply = QMessageBox.question(self, "លុបភ្ញៀវ", 
                                    f"តើអ្នកពិតជាចង់លុបភ្ញៀវ '{self.guest_list[row][0]}' ឬ?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.guest_list.pop(row)
            self.update_guests_table()
            QMessageBox.information(self, "ជោគជ័យ", "បានលុបភ្ញៀវដោយជោគជ័យ!")
    
    def edit_budget_item(self, row):
        # កែសម្រួលធាតុថវិកា (សាមញ្ញ)
        QMessageBox.information(self, "កែសម្រួល", f"ការកែសម្រួលធាតុថវិកា លេខ {row+1} នឹងមកដល់នៅក្នុងកំណែបន្ទាប់!")
    
    def delete_budget_item(self, row):
        reply = QMessageBox.question(self, "លុបចំណាយ", 
                                    f"តើអ្នកពិតជាចង់លុបធាតុ '{self.budget_items[row][0]}' ឬ?",
                                    QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.budget_items.pop(row)
            self.update_budget_table()
            QMessageBox.information(self, "ជោគជ័យ", "បានលុបចំណាយដោយជោគជ័យ!")
    
    # វិធីសាស្រ្តសម្រាប់ការចុចប៊ូតុងវិធីសាស្រ្ត
    def show_home(self):
        self.content_tabs.setCurrentIndex(0)
    
    def show_guests_tab(self):
        self.content_tabs.setCurrentIndex(1)
    
    def show_budget_tab(self):
        self.content_tabs.setCurrentIndex(2)
    
    def show_planning(self):
        QMessageBox.information(self, "ផែនការពេញលេញ", 
                                "ទំព័រផែនការពេញលេញនឹងបង្ហាញនៅទីនេះ!")
    
    def show_vendors(self):
        QMessageBox.information(self, "អ្នកផ្គត់ផ្គង់", 
                                "ការជ្រើសរើសអ្នកផ្គត់ផ្គង់នឹងបង្ហាញនៅទីនេះ!")
    
    def show_design(self):
        QMessageBox.information(self, "ការរចនា", 
                                "ការរចនាអាពាហ៍ពិពាហ៍នឹងបង្ហាញនៅទីនេះ!")
    
    def show_reports(self):
        QMessageBox.information(self, "របាយការណ៍", 
                                "របាយការណ៍ស្ថិតិនឹងបង្ហាញនៅទីនេះ!")
    
    def show_settings(self):
        QMessageBox.information(self, "ការកំណត់", 
                                "ការកំណត់ប្រព័ន្ធនឹងបង្ហាញនៅទីនេះ!")

def main():
    app = QApplication(sys.argv)
    
    # កំណត់ពុម្ពអក្សរសម្រាប់ភាសាខ្មែរ
    font = QFont("Khmer OS", 10)
    app.setFont(font)
    
    # បង្កើតផ្ទាំងចូល
    login_window = ModernLoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()