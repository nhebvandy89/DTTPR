import sys
import sqlite3
import os
import shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import random
from datetime import datetime
import hashlib

# ================ Village Data ================
VILLAGE_NAMES = {
    1: "ភូមិទួលពង្រ",
    2: "ភូមិកោះស្នួល",
    3: "ភូមិខ្លាងាប់",
    4: "ភូមិបន្ទាយទី១",
    5: "ភូមិសន្ដិភាព",
    6: "ភូមិអូរអំពិល",
    7: "ភូមិរស្មីមានជ័យ",
    8: "ភូមិអូរកេស",
    9: "ភូមិស្រឡៅជ្រុំ",
    10: "ភូមិអភិវឌ្ឍន៍",
    11: "ភូមិទួលប្រាសាទ",
    12: "ភូមិបឹងឈូក",
    13: "ភូមិបឹងជង្រុកតេជោឈ្នះឈ្នះ",
    14: "ភូមិបឹង៧៥តេជោឈ្នះឈ្នះ",
    15: "ភូមិម៉ក់ហឺន",
    16: "ភូមិភ្នំដូនសម"
}

# ================ Color Themes ================
COLOR_THEMES = {
    "darkblue": {
        "primary": "#1C1CE7",      # ខៀវងងឹត
        "secondary": "#000066",    # ខៀវងងឹតជាងមុន
        "accent": "#0000CD",       # ខៀវមធ្យម
        "light": "#E6E6FA",        # ឡាវិនឌឺ
        "dark": "#3C3CE9"          # ខៀវងងឹតខ្លាំង
    },
    "blue": {
        "primary": "#007bff",
        "secondary": "#0056b3",
        "accent": "#3B82F6",
        "light": "#f0f8ff",
        "dark": "#002b5c"
    },
    "green": {
        "primary": "#28a745",
        "secondary": "#1e7e34",
        "accent": "#4CAF50",
        "light": "#f0fff4",
        "dark": "#155724"
    },
    "purple": {
        "primary": "#6f42c1",
        "secondary": "#7d61a7",
        "accent": "#C88AD3",
        "light": "#f8f9ff",
        "dark": "#362f78"
    },
    "orange": {
        "primary": "#fd7e14",
        "secondary": "#e36209",
        "accent": "#FF9800",
        "light": "#fff5e6",
        "dark": "#bd5d07"
    },
    "red": {
        "primary": "#dc3545",
        "secondary": "#c82333",
        "accent": "#E91E63",
        "light": "#fff5f7",
        "dark": "#b71c1c"
    },
    "teal": {
        "primary": "#20c997",
        "secondary": "#17a2b8",
        "accent": "#00BCD4",
        "light": "#e6fffa",
        "dark": "#008080"
    }
}

# Current theme - ប្រើស្បែកខៀវងងឹតជាលំនាំដើម
CURRENT_THEME = "darkblue"

def get_theme_color(name):
    """Get color from current theme"""
    return COLOR_THEMES[CURRENT_THEME].get(name, COLOR_THEMES["darkblue"][name])

# ================ Updated ImageViewer ================
class ImageViewer(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("មើលរូបភាព")
        self.setFixedSize(500, 400)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        accent_color = get_theme_color("accent")
        
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        # Display image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet(f"""
            QLabel {{
                border: 2px solid {accent_color};
                border-radius: 10px;
                background-color: {get_theme_color("light")};
                padding: 5px;
            }}
        """)
        
        self.load_image(image_path)
        
        # Image info
        info_label = QLabel(f"ឈ្មោះឯកសារ: {os.path.basename(image_path)}")
        info_label.setStyleSheet("""
            color: #6c757d; 
            margin-top: 10px; 
            font-size: 14px;
            font-weight: 500;
        """)
        info_label.setAlignment(Qt.AlignCenter)
        
        # Close button with dark blue theme
        close_btn = QPushButton("បិទ")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                margin-top: 10px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                font-weight: bold;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        
        layout.addWidget(self.image_label)
        layout.addWidget(info_label)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
    
    def load_image(self, image_path):
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # Scale image to fit
                scaled_pixmap = pixmap.scaled(450, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.image_label.setPixmap(scaled_pixmap)
            else:
                self.image_label.setText("មិនអាចបង្ហាញរូបភាព")
                self.image_label.setStyleSheet("font-size: 14px; color: #666;")
        else:
            self.image_label.setText("ឯកសាររូបភាពមិនមាន")
            self.image_label.setStyleSheet("font-size: 14px; color: #666;")

# ================ Updated UserProfileDialog ================
class UserProfileDialog(QDialog):
    def __init__(self, user_data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ផ្ទាំងអ្នកប្រើប្រាស់")
        self.setFixedSize(400, 500)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        accent_color = get_theme_color("accent")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Profile header
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {primary_color}, stop:1 {accent_color});
                border-radius: 10px;
                padding: 20px;
            }}
        """)
        
        header_layout = QVBoxLayout(header_frame)
        
        profile_icon = QLabel("👤")
        profile_icon.setStyleSheet("font-size: 48px;")
        profile_icon.setAlignment(Qt.AlignCenter)
        
        username_label = QLabel(user_data.get('username', 'អ្នកប្រើប្រាស់') if user_data else "អ្នកប្រើប្រាស់")
        username_label.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")
        username_label.setAlignment(Qt.AlignCenter)
        
        role_label = QLabel(user_data.get('role', 'អ្នកគ្រប់គ្រង') if user_data else "អ្នកគ្រប់គ្រង")
        role_label.setStyleSheet("font-size: 14px; color: rgba(255,255,255,0.8);")
        role_label.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(profile_icon)
        header_layout.addWidget(username_label)
        header_layout.addWidget(role_label)
        
        layout.addWidget(header_frame)
        
        # Profile details
        details_frame = QFrame()
        details_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        details_layout = QVBoxLayout(details_frame)
        details_layout.setSpacing(12)
        
        # User information
        info_items = [
            ("ឈ្មោះពេញ:", user_data.get('fullname', 'មិនទាន់កំណត់') if user_data else "មិនទាន់កំណត់"),
            ("អ៊ីមែល:", user_data.get('email', 'មិនទាន់កំណត់') if user_data else "មិនទាន់កំណត់"),
            ("លេខទូរស័ព្ទ:", user_data.get('phone', 'មិនទាន់កំណត់') if user_data else "មិនទាន់កំណត់"),
            ("តួនាទី:", user_data.get('role', 'អ្នកគ្រប់គ្រង') if user_data else "អ្នកគ្រប់គ្រង"),
            ("កាលបរិច្ឆេទចូលប្រើ:", user_data.get('join_date', datetime.now().strftime('%Y-%m-%d')) if user_data else datetime.now().strftime('%Y-%m-%d'))
        ]
        
        for label_text, value_text in info_items:
            item_layout = QHBoxLayout()
            
            label = QLabel(label_text)
            label.setStyleSheet(f"font-weight: bold; color: {primary_color}; font-size: 14px; min-width: 150px;")
            
            value = QLabel(value_text)
            value.setStyleSheet("color: #6c757d; font-size: 14px;")
            value.setWordWrap(True)
            
            item_layout.addWidget(label)
            item_layout.addWidget(value, 1)
            
            details_layout.addLayout(item_layout)
        
        # Stats
        stats_label = QLabel("ស្ថិតិការងារ")
        stats_label.setStyleSheet(f"font-weight: bold; color: {primary_color}; font-size: 16px; margin-top: 15px;")
        details_layout.addWidget(stats_label)
        
        stats_items = [
            ("ចំនួនទិន្នន័យបានបញ្ចូល:", user_data.get('data_entered', '0') if user_data else "0"),
            ("ចុងក្រោយធ្វើការ:", user_data.get('last_active', 'មិនទាន់មាន') if user_data else "មិនទាន់មាន")
        ]
        
        for label_text, value_text in stats_items:
            item_layout = QHBoxLayout()
            
            label = QLabel(label_text)
            label.setStyleSheet("color: #495057; font-size: 13px; min-width: 150px;")
            
            value = QLabel(value_text)
            value.setStyleSheet("color: #28a745; font-weight: bold; font-size: 13px;")
            
            item_layout.addWidget(label)
            item_layout.addWidget(value, 1)
            
            details_layout.addLayout(item_layout)
        
        details_layout.addStretch()
        layout.addWidget(details_frame)
        
        # Close button with dark blue theme
        button_layout = QHBoxLayout()
        
        close_btn = QPushButton("បិទ")
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 30px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                font-weight: bold;
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        close_btn.clicked.connect(self.accept)
        
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)

# ================ Updated SettingsDialog ================
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ការកំណត់ប្រព័ន្ធ")
        self.setFixedSize(500, 600)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        accent_color = get_theme_color("accent")
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # Settings header
        header_label = QLabel("ការកំណត់ប្រព័ន្ធ")
        header_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {primary_color};
            padding-bottom: 10px;
            border-bottom: 2px solid {primary_color};
        """)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # Settings tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #dee2e6;
                border-radius: 5px;
                background-color: white;
            }}
            QTabBar::tab {{
                background-color: {get_theme_color("light")};
                padding: 10px 15px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 14px;
                color: {primary_color};
            }}
            QTabBar::tab:selected {{
                background-color: {primary_color};
                color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: #ced4da;
            }}
        """)
        
        # General settings tab
        self.create_general_tab()
        
        # Database settings tab
        self.create_database_tab()
        
        # Export settings tab
        self.create_export_tab()
        
        # Appearance settings tab
        self.create_appearance_tab()
        
        layout.addWidget(self.tab_widget)
        
        # Save button with dark blue theme
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 រក្សាទុកការកំណត់")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        save_btn.clicked.connect(self.save_settings)
        
        cancel_btn = QPushButton("បោះបង់")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 25px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: #5a6268;
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def create_general_tab(self):
        general_tab = QWidget()
        layout = QVBoxLayout(general_tab)
        layout.setSpacing(15)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        
        # Application settings
        app_group = QGroupBox("ការកំណត់កម្មវិធី")
        app_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: {primary_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {primary_color};
            }}
        """)
        
        app_layout = QVBoxLayout()
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel("ភាសា:")
        lang_label.setStyleSheet(f"font-weight: bold; min-width: 120px; color: {primary_color};")
        
        lang_combo = QComboBox()
        lang_combo.addItems(["ភាសាខ្មែរ", "English"])
        lang_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 3px;
                font-size: 16px;
            }
        """)
        
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(lang_combo, 1)
        app_layout.addLayout(lang_layout)
        
        # Auto-save
        auto_save_check = QCheckBox("រក្សាទុកដោយស្វ័យប្រវត្តិ")
        auto_save_check.setStyleSheet("font-size: 16px;")
        app_layout.addWidget(auto_save_check)
        
        # Notification
        notif_check = QCheckBox("បង្ហាញការជូនដំណឹង")
        notif_check.setStyleSheet("font-size: 16px;")
        app_layout.addWidget(notif_check)
        
        app_group.setLayout(app_layout)
        layout.addWidget(app_group)
        
        # Data validation
        data_group = QGroupBox("ការផ្ទៀងផ្ទាត់ទិន្នន័យ")
        data_group.setStyleSheet(app_group.styleSheet())
        
        data_layout = QVBoxLayout()
        
        # Required fields
        fields = [
            ("តម្រូវអោយបំពេញលេខរៀង", True),
            ("តម្រូវអោយបំពេញឈ្មោះ", True),
            ("តម្រូវអោយបំពេញភូមិ", True),
            ("តម្រូវអោយបំពេញឯកសារ", True)
        ]
        
        for text, checked in fields:
            check = QCheckBox(text)
            check.setChecked(checked)
            check.setStyleSheet("font-size: 16px;")
            data_layout.addWidget(check)
        
        data_group.setLayout(data_layout)
        layout.addWidget(data_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(general_tab, "ទូទៅ")
    
    def create_database_tab(self):
        database_tab = QWidget()
        layout = QVBoxLayout(database_tab)
        layout.setSpacing(15)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        
        # Backup settings
        backup_group = QGroupBox("ការរក្សាទុកទិន្នន័យ")
        backup_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: {primary_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {primary_color};
            }}
        """)
        
        backup_layout = QVBoxLayout()
        
        # Auto backup
        auto_backup_check = QCheckBox("រក្សាទុកទិន្នន័យដោយស្វ័យប្រវត្តិ")
        auto_backup_check.setStyleSheet("font-size: 16px;")
        backup_layout.addWidget(auto_backup_check)
        
        # Backup frequency
        freq_layout = QHBoxLayout()
        freq_label = QLabel("ប្រេកង់រក្សាទុក:")
        freq_label.setStyleSheet(f"font-weight: bold; min-width: 120px; color: {primary_color};")
        
        freq_combo = QComboBox()
        freq_combo.addItems(["រាល់ថ្ងៃ", "រាល់សប្តាហ៍", "រាល់ខែ"])
        freq_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 3px;
                font-size: 16px;
            }
        """)
        
        freq_layout.addWidget(freq_label)
        freq_layout.addWidget(freq_combo, 1)
        backup_layout.addLayout(freq_layout)
        
        backup_group.setLayout(backup_layout)
        layout.addWidget(backup_group)
        
        # Database maintenance
        maint_group = QGroupBox("ថែទាំទិន្នន័យ")
        maint_group.setStyleSheet(backup_group.styleSheet())
        
        maint_layout = QVBoxLayout()
        
        # Optimize database button with dark blue theme
        optimize_btn = QPushButton("បង្កើនសមត្ថភាពទិន្នន័យ")
        optimize_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {get_theme_color("accent")};
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 15px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                margin-bottom: 5px;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {primary_color};
            }}
        """)
        
        # Clean old data button with dark blue theme
        clean_btn = QPushButton("សម្អាតទិន្នន័យចាស់")
        clean_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 15px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                margin-bottom: 5px;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        
        # Export all data button with green theme
        export_all_btn = QPushButton("បញ្ចេញទិន្នន័យទាំងអស់")
        export_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 3px;
                padding: 8px 15px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: #218838;
            }}
        """)
        
        maint_layout.addWidget(optimize_btn)
        maint_layout.addWidget(clean_btn)
        maint_layout.addWidget(export_all_btn)
        maint_layout.addStretch()
        
        maint_group.setLayout(maint_layout)
        layout.addWidget(maint_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(database_tab, "ទិន្នន័យ")
    
    def create_export_tab(self):
        export_tab = QWidget()
        layout = QVBoxLayout(export_tab)
        layout.setSpacing(15)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        
        # Export format
        format_group = QGroupBox("ទ្រង់ទ្រាយបញ្ចេញ")
        format_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: {primary_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {primary_color};
            }}
        """)
        
        format_layout = QVBoxLayout()
        
        formats = [
            ("CSV (ទ្រង់ទ្រាយទូទៅ)", True),
            ("Excel (.xlsx)", False),
            ("PDF (របាយការណ៍)", False),
            ("JSON (ទិន្នន័យសរសៃ)", False)
        ]
        
        for text, checked in formats:
            radio = QRadioButton(text)
            radio.setChecked(checked)
            radio.setStyleSheet("font-size: 16px;")
            format_layout.addWidget(radio)
        
        format_group.setLayout(format_layout)
        layout.addWidget(format_group)
        
        # Export options
        options_group = QGroupBox("ជម្រើសបញ្ចេញ")
        options_group.setStyleSheet(format_group.styleSheet())
        
        options_layout = QVBoxLayout()
        
        options = [
            ("បញ្ជូលរូបភាព", False),
            ("បញ្ជូលទម្រង់ពណ៌", True),
            ("បង្ហាញបញ្ជីភូមិ", True),
            ("បង្ហាញស្ថិតិសរុប", True)
        ]
        
        for text, checked in options:
            check = QCheckBox(text)
            check.setChecked(checked)
            check.setStyleSheet("font-size: 16px;")
            options_layout.addWidget(check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Default export path
        path_group = QGroupBox("ទីតាំងរក្សាទុក")
        path_group.setStyleSheet(format_group.styleSheet())
        
        path_layout = QVBoxLayout()
        
        path_layout.addWidget(QLabel("ទីតាំងរក្សាទុកលំនាំដើម:"))
        
        path_btn_layout = QHBoxLayout()
        
        path_edit = QLineEdit(os.path.expanduser("~/Desktop"))
        path_edit.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 3px;
                font-size: 16px;
            }
        """)
        
        # Browse button with dark blue theme
        browse_btn = QPushButton("រុករក...")
        browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 3px;
                padding: 6px 12px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        
        path_btn_layout.addWidget(path_edit, 1)
        path_btn_layout.addWidget(browse_btn)
        path_layout.addLayout(path_btn_layout)
        
        path_group.setLayout(path_layout)
        layout.addWidget(path_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(export_tab, "បញ្ចេញទិន្នន័យ")
    
    def create_appearance_tab(self):
        appearance_tab = QWidget()
        layout = QVBoxLayout(appearance_tab)
        layout.setSpacing(15)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        
        # Theme selection
        theme_group = QGroupBox("ស្បែកកម្មវិធី")
        theme_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
                color: {primary_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: {primary_color};
            }}
        """)
        
        theme_layout = QVBoxLayout()
        
        # Create theme radio buttons dynamically
        self.theme_buttons = []
        for theme_name, theme_data in COLOR_THEMES.items():
            radio = QRadioButton(f"ស្បែកពណ៌{theme_name} {'(លំនាំដើម)' if theme_name == CURRENT_THEME else ''}")
            radio.setChecked(theme_name == CURRENT_THEME)
            radio.setStyleSheet("font-size: 16px;")
            radio.theme_name = theme_name
            radio.clicked.connect(lambda checked, t=theme_name: self.preview_theme(t))
            self.theme_buttons.append(radio)
            theme_layout.addWidget(radio)
        
        theme_group.setLayout(theme_layout)
        layout.addWidget(theme_group)
        
        # Font settings
        font_group = QGroupBox("ការកំណត់ពុម្ពអក្សរ")
        font_group.setStyleSheet(theme_group.styleSheet())
        
        font_layout = QVBoxLayout()
        
        # Font size
        size_layout = QHBoxLayout()
        size_label = QLabel("ទំហំពុម្ពអក្សរ:")
        size_label.setStyleSheet(f"font-weight: bold; min-width: 120px; color: {primary_color};")
        
        size_combo = QComboBox()
        size_combo.addItems(["12px", "13px", "14px", "15px", "16px", "20px (លំនាំដើម)", "24px", "28px"])
        size_combo.setCurrentText("20px (លំនាំដើម)")
        size_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 3px;
                font-size: 16px;
            }
        """)
        
        size_layout.addWidget(size_label)
        size_layout.addWidget(size_combo, 1)
        font_layout.addLayout(size_layout)
        
        # Font family
        family_layout = QHBoxLayout()
        family_label = QLabel("គ្រួសារពុម្ពអក្សរ:")
        family_label.setStyleSheet(f"font-weight: bold; min-width: 120px; color: {primary_color};")
        
        family_combo = QComboBox()
        family_combo.addItems(["Arial", "Times New Roman", "Khmer OS", "Tahoma", "Microsoft Sans Serif"])
        family_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ced4da;
                border-radius: 3px;
                font-size: 16px;
            }
        """)
        
        family_layout.addWidget(family_label)
        family_layout.addWidget(family_combo, 1)
        font_layout.addLayout(family_layout)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # UI settings
        ui_group = QGroupBox("ការកំណត់ UI")
        ui_group.setStyleSheet(theme_group.styleSheet())
        
        ui_layout = QVBoxLayout()
        
        ui_options = [
            ("បង្ហាញរូបតំណាង", True),
            ("ប្រើពណ៌ផ្ទុយ", True),
            ("បង្ហាញរបារស្ថានភាព", True),
            ("បង្ហាញបន្ទាត់ជួរដេក", True)
        ]
        
        for text, checked in ui_options:
            check = QCheckBox(text)
            check.setChecked(checked)
            check.setStyleSheet("font-size: 16px;")
            ui_layout.addWidget(check)
        
        ui_group.setLayout(ui_layout)
        layout.addWidget(ui_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(appearance_tab, "រូបរាង")
    
    def preview_theme(self, theme_name):
        """Preview theme changes"""
        global CURRENT_THEME
        CURRENT_THEME = theme_name
        # Update colors in real-time
        self.update_theme_colors()
    
    def update_theme_colors(self):
        """Update dialog colors based on current theme"""
        primary_color = get_theme_color("primary")
        
        # Update header
        self.findChild(QLabel).setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {primary_color};
            padding-bottom: 10px;
            border-bottom: 2px solid {primary_color};
        """)
        
        # Update tab widget
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid #dee2e6;
                border-radius: 5px;
                background-color: white;
            }}
            QTabBar::tab {{
                background-color: {get_theme_color("light")};
                padding: 10px 15px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-size: 14px;
                color: {primary_color};
            }}
            QTabBar::tab:selected {{
                background-color: {primary_color};
                color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: #ced4da;
            }}
        """)
    
    def save_settings(self):
        QMessageBox.information(self, "ជោគជ័យ", "ការកំណត់ត្រូវបានរក្សាទុកដោយជោគជ័យ!")
        self.accept()

# ================ Modern Dashboard Tab with Updated Colors ================
class ModernDashboardTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        accent_color = get_theme_color("accent")
        light_color = get_theme_color("light")
        
        # Create scroll area for modern dashboard
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: {light_color};
            }}
            QScrollBar:vertical {{
                background-color: #f5f5f5;
                width: 10px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {primary_color};
                border-radius: 5px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {accent_color};
            }}
        """)
        
        dashboard_widget = QWidget()
        scroll_area.setWidget(dashboard_widget)
        
        dashboard_layout = QVBoxLayout(dashboard_widget)
        dashboard_layout.setContentsMargins(20, 20, 20, 20)
        dashboard_layout.setSpacing(25)
        
        # 1. Header with gradient and time
        self.create_modern_header(dashboard_layout)
        
        # 2. Quick Stats Cards (Modern Design)
        self.create_stats_cards(dashboard_layout)
        
        # 3. Charts Section
        self.create_charts_section(dashboard_layout)
        
        # 4. Recent Activity with Avatars
        self.create_activity_section(dashboard_layout)
        
        # 5. System Status
        self.create_system_status(dashboard_layout)
        
        layout.addWidget(scroll_area)
        self.setLayout(layout)
    
    def create_modern_header(self, layout):
        primary_color = get_theme_color("primary")
        accent_color = get_theme_color("accent")
        
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {primary_color}, stop:1 {accent_color});
                border-radius: 20px;
                padding: 30px;
            }}
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(10)
        
        # Welcome message with icon
        welcome_layout = QHBoxLayout()
        
        welcome_icon = QLabel("👋")
        welcome_icon.setStyleSheet("font-size: 48px; margin-right: 15px;")
        
        welcome_text = QLabel("សួស្តី, អ្នកគ្រប់គ្រង!")
        welcome_text.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: white;
        """)
        
        welcome_layout.addWidget(welcome_icon)
        welcome_layout.addWidget(welcome_text)
        welcome_layout.addStretch()
        
        # Date and time with real-time updates
        self.datetime_label = QLabel()
        self.datetime_label.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.9);
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 10px 20px;
        """)
        self.update_datetime()
        
        # Timer to update datetime every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_datetime)
        self.timer.start(1000)
        
        header_layout.addLayout(welcome_layout)
        header_layout.addWidget(self.datetime_label)
        
        layout.addWidget(header_frame)
    
    def update_datetime(self):
        current_time = datetime.now()
        time_str = current_time.strftime("%A, %d %B %Y | %I:%M:%S %p")
        
        # Khmer day names
        days_kh = {
            'Monday': 'ថ្ងៃច័ន្ទ',
            'Tuesday': 'ថ្ងៃអង្គារ',
            'Wednesday': 'ថ្ងៃពុធ',
            'Thursday': 'ថ្ងៃព្រហស្បតិ៍',
            'Friday': 'ថ្ងៃសុក្រ',
            'Saturday': 'ថ្ងៃសៅរ៍',
            'Sunday': 'ថ្ងៃអាទិត្យ'
        }
        
        # Khmer month names
        months_kh = {
            'January': 'មករា',
            'February': 'កុម្ភៈ',
            'March': 'មីនា',
            'April': 'មេសា',
            'May': 'ឧសភា',
            'June': 'មិថុនា',
            'July': 'កក្កដា',
            'August': 'សីហា',
            'September': 'កញ្ញា',
            'October': 'តុលា',
            'November': 'វិច្ឆិកា',
            'December': 'ធ្នូ'
        }
        
        # Replace English with Khmer
        for eng, kh in days_kh.items():
            if eng in time_str:
                time_str = time_str.replace(eng, kh)
                break
        
        for eng, kh in months_kh.items():
            if eng in time_str:
                time_str = time_str.replace(eng, kh)
                break
        
        self.datetime_label.setText(time_str)
    
    def create_stats_cards(self, layout):
        stats_frame = QFrame()
        stats_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
            }
        """)
        
        stats_layout = QGridLayout(stats_frame)
        stats_layout.setSpacing(20)
        
        stats = self.parent.get_statistics()
        
        # Color palette for stats cards
        card_colors = [
            ("#667eea", "#764ba2"),  # Blue-Purple
            ("#4CAF50", "#8BC34A"),  # Green
            ("#E91E63", "#FF4081"),  # Pink
            ("#FF9800", "#FF5722"),  # Orange
            ("#2196F3", "#03A9F4"),  # Blue
            ("#9C27B0", "#673AB7")   # Purple
        ]
        
        # Modern stat cards with icons and gradients
        stat_items = [
            ("សរុបអ្នកបង់ប្រាក់", stats['total'], "👥"),
            ("ប្រុស", stats['male'], "👨"),
            ("ស្រី", stats['female'], "👩"),
            ("ភូមិសកម្ម", stats['villages'], "🏘️"),
            ("បញ្ជូលថ្ងៃនេះ", stats['today'], "📅"),
            ("ប្រភេទឯកសារ", stats['doc_types'], "📋")
        ]
        
        for i, (title, value, icon) in enumerate(stat_items):
            color1, color2 = card_colors[i % len(card_colors)]
            card = self.create_modern_stat_card(title, value, icon, color1, color2, "#ffffff")
            stats_layout.addWidget(card, i // 3, i % 3)
        
        layout.addWidget(stats_frame)
    
    def create_modern_stat_card(self, title, value, icon, color1, color2, text_color):
        card = QFrame()
        card.setFixedHeight(140)
        card.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {color1}, stop:1 {color2});
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Top row with icon and title
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 40px;
            color: {text_color};
        """)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: bold;
            color: {text_color};
            opacity: 0.9;
        """)
        title_label.setWordWrap(True)
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(title_label, 1)
        
        # Value with animation effect
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"""
            font-size: 42px;
            font-weight: bold;
            color: {text_color};
        """)
        value_label.setAlignment(Qt.AlignRight)
        
        layout.addLayout(top_layout)
        layout.addWidget(value_label)
        
        # Add hover effect
        card.setGraphicsEffect(self.create_shadow_effect())
        
        return card
    
    def create_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 5)
        return shadow
    
    def create_charts_section(self, layout):
        charts_frame = QFrame()
        charts_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        charts_frame.setGraphicsEffect(self.create_shadow_effect())
        
        charts_layout = QVBoxLayout(charts_frame)
        
        # Section title
        section_title = QLabel("📊 ការវិភាគទិន្នន័យ")
        section_title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {get_theme_color("primary")};
            margin-bottom: 15px;
        """)
        charts_layout.addWidget(section_title)
        
        # Charts in grid
        charts_grid = QGridLayout()
        charts_grid.setSpacing(20)
        
        # Gender Distribution Chart
        gender_chart = self.create_gender_chart()
        charts_grid.addWidget(gender_chart, 0, 0)
        
        # Village Distribution Chart
        village_chart = self.create_village_chart()
        charts_grid.addWidget(village_chart, 0, 1)
        
        # Document Type Chart
        doc_chart = self.create_document_chart()
        charts_grid.addWidget(doc_chart, 1, 0, 1, 2)
        
        charts_layout.addLayout(charts_grid)
        layout.addWidget(charts_frame)
    
    def create_gender_chart(self):
        primary_color = get_theme_color("primary")
        
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(chart_frame)
        
        # Chart title
        title = QLabel("ការបែងចែកតាមភេទ")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {primary_color};
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Get data
        stats = self.parent.get_statistics()
        male = stats['male']
        female = stats['female']
        total = max(male + female, 1)
        
        # Create progress bars
        male_bar = self.create_progress_bar("ប្រុស", male, total, "#4CAF50")
        female_bar = self.create_progress_bar("ស្រី", female, total, "#E91E63")
        
        layout.addWidget(male_bar)
        layout.addWidget(female_bar)
        
        # Percentage labels
        percent_layout = QHBoxLayout()
        
        male_percent = QLabel(f"ប្រុស: {male} ({male/total*100:.1f}%)")
        male_percent.setStyleSheet("color: #4CAF50; font-weight: bold;")
        
        female_percent = QLabel(f"ស្រី: {female} ({female/total*100:.1f}%)")
        female_percent.setStyleSheet("color: #E91E63; font-weight: bold;")
        
        percent_layout.addWidget(male_percent)
        percent_layout.addStretch()
        percent_layout.addWidget(female_percent)
        
        layout.addLayout(percent_layout)
        
        return chart_frame
    
    def create_village_chart(self):
        primary_color = get_theme_color("primary")
        
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(chart_frame)
        
        # Chart title
        title = QLabel("សកម្មភាពតាមភូមិ")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {primary_color};
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Get village data
        try:
            self.parent.db_cursor.execute("""
                SELECT village, COUNT(*) as count 
                FROM tax_payers 
                GROUP BY village 
                ORDER BY count DESC 
                LIMIT 5
            """)
            village_data = self.parent.db_cursor.fetchall()
            
            total = sum(count for _, count in village_data)
            
            for village, count in village_data:
                village_bar = self.create_progress_bar(village, count, total if total > 0 else 1, "#2196F3")
                layout.addWidget(village_bar)
        
        except:
            error_label = QLabel("មិនមានទិន្នន័យ")
            error_label.setStyleSheet("color: #999; font-style: italic;")
            layout.addWidget(error_label)
        
        return chart_frame
    
    def create_document_chart(self):
        primary_color = get_theme_color("primary")
        
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(chart_frame)
        
        # Chart title
        title = QLabel("ប្រភេទឯកសារ")
        title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {primary_color};
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Get document type data
        try:
            self.parent.db_cursor.execute("""
                SELECT document_type, COUNT(*) as count 
                FROM tax_payers 
                GROUP BY document_type 
                ORDER BY count DESC
            """)
            doc_data = self.parent.db_cursor.fetchall()
            
            colors = ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2']
            
            for i, (doc_type, count) in enumerate(doc_data):
                doc_item = QHBoxLayout()
                
                icon_label = QLabel("📄")
                icon_label.setStyleSheet("font-size: 20px;")
                
                doc_label = QLabel(doc_type)
                doc_label.setStyleSheet("font-size: 14px; min-width: 150px;")
                
                count_label = QLabel(f"{count}")
                count_label.setStyleSheet(f"""
                    font-weight: bold;
                    color: {colors[i % len(colors)]};
                    font-size: 14px;
                """)
                
                doc_item.addWidget(icon_label)
                doc_item.addWidget(doc_label)
                doc_item.addWidget(count_label)
                doc_item.addStretch()
                
                # Progress bar
                total = sum(c for _, c in doc_data)
                progress = QProgressBar()
                progress.setMaximum(100)
                progress.setValue(int(count/total*100) if total > 0 else 0)
                progress.setTextVisible(False)
                progress.setFixedHeight(8)
                progress.setStyleSheet(f"""
                    QProgressBar {{
                        border: none;
                        background-color: #e0e0e0;
                        border-radius: 4px;
                    }}
                    QProgressBar::chunk {{
                        background-color: {colors[i % len(colors)]};
                        border-radius: 4px;
                    }}
                """)
                
                container = QWidget()
                container_layout = QVBoxLayout(container)
                container_layout.setSpacing(5)
                container_layout.addLayout(doc_item)
                container_layout.addWidget(progress)
                
                layout.addWidget(container)
        
        except:
            error_label = QLabel("មិនមានទិន្នន័យ")
            error_label.setStyleSheet("color: #999; font-style: italic;")
            layout.addWidget(error_label)
        
        return chart_frame
    
    def create_progress_bar(self, label, value, total, color):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(5)
        
        # Label and value
        label_layout = QHBoxLayout()
        
        name_label = QLabel(label)
        name_label.setStyleSheet("font-size: 14px; font-weight: 500;")
        
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"font-weight: bold; color: {color};")
        
        label_layout.addWidget(name_label)
        label_layout.addStretch()
        label_layout.addWidget(value_label)
        
        # Progress bar
        progress = QProgressBar()
        progress.setMaximum(100)
        progress.setValue(int(value/total*100) if total > 0 else 0)
        progress.setTextVisible(False)
        progress.setFixedHeight(10)
        progress.setStyleSheet(f"""
            QProgressBar {{
                border: none;
                background-color: #e0e0e0;
                border-radius: 5px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
        """)
        
        layout.addLayout(label_layout)
        layout.addWidget(progress)
        
        return widget
    
    def create_activity_section(self, layout):
        activity_frame = QFrame()
        activity_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        activity_frame.setGraphicsEffect(self.create_shadow_effect())
        
        activity_layout = QVBoxLayout(activity_frame)
        
        # Section title with refresh button
        title_layout = QHBoxLayout()
        
        title = QLabel("📝 សកម្មភាពថ្មីៗ")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {get_theme_color("primary")};
        """)
        
        # Refresh button with dark blue theme
        refresh_btn = QPushButton("🔄")
        refresh_btn.setFixedSize(50, 50)  # Increased size
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {get_theme_color("light")};
                border-radius: 25px;
                font-size: 24px;  /* ទំហំពុម្ពអក្សរ 24px */
                color: {get_theme_color("primary")};
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("accent")};
                color: white;
            }}
        """)
        refresh_btn.clicked.connect(self.refresh_activities)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(refresh_btn)
        
        activity_layout.addLayout(title_layout)
        
        # Activities list
        self.activities_list = QVBoxLayout()
        self.activities_list.setSpacing(15)
        
        self.load_recent_activities()
        
        activity_layout.addLayout(self.activities_list)
        
        layout.addWidget(activity_frame)
    
    def load_recent_activities(self):
        # Clear existing activities
        for i in reversed(range(self.activities_list.count())): 
            widget = self.activities_list.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        try:
            # Get recent activities from database
            self.parent.db_cursor.execute("""
                SELECT name, village, registration_date 
                FROM tax_payers 
                ORDER BY registration_date DESC 
                LIMIT 5
            """)
            activities = self.parent.db_cursor.fetchall()
            
            if not activities:
                empty_label = QLabel("មិនទាន់មានសកម្មភាព")
                empty_label.setStyleSheet("color: #999; font-style: italic; padding: 20px;")
                empty_label.setAlignment(Qt.AlignCenter)
                self.activities_list.addWidget(empty_label)
                return
            
            # Define avatar colors
            avatar_colors = ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2']
            
            for i, (name, village, reg_date) in enumerate(activities):
                activity_item = self.create_activity_item(
                    name, village, reg_date, 
                    avatar_colors[i % len(avatar_colors)]
                )
                self.activities_list.addWidget(activity_item)
        
        except Exception as e:
            error_label = QLabel(f"កំហុសក្នុងការផ្ទុកសកម្មភាព: {str(e)}")
            error_label.setStyleSheet("color: #FF6B6B; padding: 20px;")
            error_label.setAlignment(Qt.AlignCenter)
            self.activities_list.addWidget(error_label)
    
    def create_activity_item(self, name, village, reg_date, color):
        primary_color = get_theme_color("primary")
        
        item = QFrame()
        item.setStyleSheet(f"""
            QFrame {{
                background-color: {get_theme_color("light")};
                border-radius: 15px;
                padding: 15px;
            }}
            QFrame:hover {{
                background-color: #e9ecef;
                border-left: 4px solid {primary_color};
            }}
        """)
        
        layout = QHBoxLayout(item)
        layout.setSpacing(15)
        
        # Avatar with initial
        avatar_label = QLabel()
        avatar_label.setFixedSize(50, 50)
        avatar_label.setStyleSheet(f"""
            border-radius: 25px;
            background-color: {color};
            color: white;
            font-size: 20px;
            font-weight: bold;
        """)
        avatar_label.setAlignment(Qt.AlignCenter)
        
        # Get first letter of name for avatar
        if name and len(name.strip()) > 0:
            initial = name.strip()[0].upper()
        else:
            initial = "?"
        avatar_label.setText(initial)
        
        # Activity details
        details_layout = QVBoxLayout()
        details_layout.setSpacing(5)
        
        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #333;")
        
        village_label = QLabel(f"ភូមិ: {village}")
        village_label.setStyleSheet("color: #666; font-size: 14px;")
        
        time_label = QLabel(self.format_time_ago(reg_date))
        time_label.setStyleSheet("color: #999; font-size: 13px;")
        
        details_layout.addWidget(name_label)
        details_layout.addWidget(village_label)
        details_layout.addWidget(time_label)
        
        # Action button with dark blue theme
        view_btn = QPushButton("👁️ មើល")
        view_btn.setFixedSize(100, 40)  # Increased size
        view_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border-radius: 8px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("accent")};
            }}
        """)
        
        layout.addWidget(avatar_label)
        layout.addLayout(details_layout, 1)
        layout.addWidget(view_btn)
        
        return item
    
    def format_time_ago(self, timestamp):
        """Format timestamp to time ago in Khmer"""
        try:
            if isinstance(timestamp, str):
                # Try different date formats
                for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S']:
                    try:
                        reg_date = datetime.strptime(timestamp, fmt)
                        break
                    except:
                        continue
                else:
                    return "មិនស្គាល់ពេលវេលា"
            else:
                reg_date = datetime.fromisoformat(timestamp)
            
            now = datetime.now()
            diff = now - reg_date
            
            minutes = diff.total_seconds() / 60
            hours = minutes / 60
            days = hours / 24
            
            if minutes < 1:
                return "មុននេះបន្តិញ"
            elif minutes < 60:
                return f"{int(minutes)} នាទីមុន"
            elif hours < 24:
                return f"{int(hours)} ម៉ោងមុន"
            elif days < 7:
                return f"{int(days)} ថ្ងៃមុន"
            else:
                return reg_date.strftime("%d/%m/%Y")
        except:
            return "មិនស្គាល់ពេលវេលា"
    
    def refresh_activities(self):
        # Add refresh animation
        refresh_btn = self.sender()
        refresh_btn.setText("⏳")
        QTimer.singleShot(500, lambda: refresh_btn.setText("🔄"))
        
        self.load_recent_activities()
    
    def create_system_status(self, layout):
        status_frame = QFrame()
        status_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 20px;
                padding: 20px;
            }
        """)
        status_frame.setGraphicsEffect(self.create_shadow_effect())
        
        status_layout = QVBoxLayout(status_frame)
        
        # Section title
        title = QLabel("📈 ស្ថានភាពប្រព័ន្ធ")
        title.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {get_theme_color("primary")};
            margin-bottom: 15px;
        """)
        status_layout.addWidget(title)
        
        # Status indicators
        indicators = [
            ("ទិន្នន័យ", "ប្រើប្រាស់", "85%", "#4CAF50"),
            ("ផ្ទុកម៉ូឌុល", "ដំណើរការ", "100%", "#2196F3"),
            ("សុវត្ថិភាព", "កំពុងពិនិត្យ", "✓", "#FF9800"),
            ("ខ្ចប់ឯកសារ", "រួចរាល់", "✓", "#9C27B0")
        ]
        
        grid_layout = QGridLayout()
        grid_layout.setSpacing(15)
        
        for i, (name, status, value, color) in enumerate(indicators):
            indicator = self.create_status_indicator(name, status, value, color)
            grid_layout.addWidget(indicator, i // 2, i % 2)
        
        status_layout.addLayout(grid_layout)
        
        # Quick actions with dark blue theme
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        primary_color = get_theme_color("primary")
        
        actions = [
            ("📥 ប្រអប់ចូល", lambda: self.parent.show_input_tab()),
            ("📊 បង្កើតរបាយការណ៍", lambda: self.parent.show_report_tab()),
            ("⚙️ ការកំណត់", lambda: self.parent.show_settings())
        ]
        
        for text, handler in actions:
            btn = QPushButton(text)
            btn.setFixedHeight(55)  # Increased height
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {get_theme_color("light")};
                    border-radius: 10px;
                    font-weight: 5600;
                    font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                    color: {primary_color};
                }}
                QPushButton:hover {{
                    background-color: {primary_color};
                    color: white;
                }}
            """)
            btn.clicked.connect(handler)
            actions_layout.addWidget(btn)
        
        actions_layout.addStretch()
        status_layout.addLayout(actions_layout)
        
        layout.addWidget(status_frame)

    def create_status_indicator(self, name, status, value, color):
        indicator = QFrame()
        indicator.setFixedHeight(80)
        indicator.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 15px;
                padding: 15px;
            }
            QFrame:hover {
                background-color: #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(indicator)
        layout.setSpacing(5)
        
        # Name and status
        top_layout = QHBoxLayout()
        
        name_label = QLabel(name)
        name_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #333;")
        
        status_label = QLabel(status)
        status_label.setStyleSheet(f"color: {color}; font-weight: 500;")
        
        top_layout.addWidget(name_label)
        top_layout.addStretch()
        top_layout.addWidget(status_label)
        
        # Value with progress
        bottom_layout = QHBoxLayout()
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-weight: bold; font-size: 18px; color: {color};")
        
        bottom_layout.addWidget(value_label)
        bottom_layout.addStretch()
        
        # If it's a percentage, add progress bar
        if "%" in value:
            progress = QProgressBar()
            progress.setMaximum(100)
            progress.setValue(int(value.replace("%", "")))
            progress.setTextVisible(False)
            progress.setFixedWidth(100)
            progress.setFixedHeight(6)
            progress.setStyleSheet(f"""
                QProgressBar {{
                    background-color: #e0e0e0;
                    border-radius: 3px;
                }}
                QProgressBar::chunk {{
                    background-color: {color};
                    border-radius: 3px;
                }}
            """)
            bottom_layout.addWidget(progress)
        
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        
        return indicator

# ================ Main Application Class ================
class AdministrativeManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initDatabase()
        self.initUI()
        
    def initDatabase(self):
        """Initialize SQLite database"""
        try:
            # Create images directory
            self.images_dir = "document_images"
            if not os.path.exists(self.images_dir):
                os.makedirs(self.images_dir)
            
            self.conn = sqlite3.connect('admin_system.db', check_same_thread=False)
            self.db_cursor = self.conn.cursor()
            
            # Create main table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS tax_payers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    serial_number TEXT UNIQUE,
                    name TEXT,
                    gender TEXT,
                    document_type TEXT,
                    document_photo TEXT,
                    village TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'សកម្ម'
                )
            ''')
            
            # Create villages table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS villages (
                    id INTEGER PRIMARY KEY,
                    name TEXT UNIQUE,
                    code TEXT
                )
            ''')
            
            # Create users table
            self.db_cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    fullname TEXT,
                    email TEXT,
                    phone TEXT,
                    role TEXT DEFAULT 'user',
                    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Insert default admin user if not exists
            self.db_cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            if self.db_cursor.fetchone()[0] == 0:
                hashed_password = hashlib.sha256('admin123'.encode()).hexdigest()
                self.db_cursor.execute('''
                    INSERT INTO users (username, password, fullname, email, role)
                    VALUES (?, ?, ?, ?, ?)
                ''', ('admin', hashed_password, 'អ្នកគ្រប់គ្រង', 'admin@example.com', 'admin'))
            
            # Insert 16 villages with new names
            self.db_cursor.execute("SELECT COUNT(*) FROM villages")
            if self.db_cursor.fetchone()[0] == 0:
                villages = []
                for i in range(1, 17):
                    village_name = VILLAGE_NAMES[i]  # Use new village names
                    village_code = f"V{i:03d}"
                    villages.append((i, village_name, village_code))
                
                self.db_cursor.executemany('INSERT INTO villages VALUES (?, ?, ?)', villages)
                self.conn.commit()
            
            # Check for sample data
            self.db_cursor.execute("SELECT COUNT(*) FROM tax_payers")
            count = self.db_cursor.fetchone()[0]
            
            if count == 0:
                self.insert_sample_data()
                
            print(f"Database initialized with {count} records")
            
        except Exception as e:
            print(f"Database error: {e}")
    
    def insert_sample_data(self):
        """Insert sample data with images"""
        try:
            # Use new village names
            villages = [VILLAGE_NAMES[i] for i in range(1, 17)]
            first_names = ['វីរៈ', 'សុផល', 'រស្មី', 'សុភាព', 'មង្គល', 'សុខា', 'បញ្ញា', 'វិចិត្រ']
            last_names = ['យន់', 'ណារ', 'ទីតា', 'វណ្ណា', 'ធីតា', 'បញ្ញា', 'សុខា', 'មង្គល']
            
            # ប្រភេទឯកសារថ្មីតាមតម្រូវការ
            doc_types = ['សំបុត្រកំណើត', 'សំបុត្រអាពាហ៍ពិពាហ៍', 'សំបុត្រមរណភាព', 'ឯកសារផ្សេងៗ']
            
            for i in range(20):
                serial = f"SN-{datetime.now().year}-{i+1:04d}"
                name = f"{random.choice(first_names)} {random.choice(last_names)}"
                gender = random.choice(['ប្រុស', 'ស្រី'])
                doc_type = random.choice(doc_types)
                village = random.choice(villages)
                
                # Generate sample image filename
                image_filename = f"doc_{i+1:03d}.txt"
                image_path = os.path.join(self.images_dir, image_filename)
                
                # Create a simple sample image
                self.create_sample_image(image_path, f"{name} - {serial}")
                
                self.db_cursor.execute('''
                    INSERT INTO tax_payers (serial_number, name, gender, document_type, document_photo, village)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (serial, name, gender, doc_type, image_path, village))
            
            self.conn.commit()
            print("Sample data inserted successfully")
            
        except Exception as e:
            print(f"Error inserting sample data: {e}")
    
    def create_sample_image(self, filepath, text):
        """Create a sample image for demonstration"""
        try:
            # Create a text file as placeholder image
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"ឯកសារបញ្ជាក់អត្តសញ្ញាណ\n")
                f.write("=" * 40 + "\n")
                f.write(f"ឈ្មោះ: {text}\n")
                f.write(f"កាលបរិច្ឆេទ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("នេះគឺជាឯកសារឧទាហរណ៍សម្រាប់បង្ហាញ\n")
                f.write("=" * 40)
        except Exception as e:
            print(f"Error creating sample image: {e}")
    
    def initUI(self):
        """Initialize the user interface"""
        self.setWindowTitle("ប្រព័ន្ធគ្រប់គ្រងអត្រានុកូលដ្ឋាន")
        self.setFixedSize(1600, 1000)  # Increased size for modern design
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        accent_color = get_theme_color("accent")
        light_color = get_theme_color("light")
        
        # Set modern application style
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {light_color};
            }}
            QWidget {{
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }}
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create modern sidebar with dark blue theme
        self.create_modern_sidebar(main_layout)
        
        # Create right content area
        self.content_widget = QWidget()
        self.content_widget.setObjectName("contentWidget")
        self.content_widget.setStyleSheet(f"""
            #contentWidget {{
                background-color: {light_color};
            }}
        """)
        
        content_layout = QVBoxLayout(self.content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Main content area (tab widget)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border-top: 2px solid {primary_color};
                background-color: white;
            }}
            QTabBar::tab {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #f0f0f0, stop:1 #e0e0e0);
                border: 1px solid #c4c4c4;
                border-bottom-color: #c4c4c4;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 200px;  /* Fixed width for even spacing */
                padding: 15px 25px;  /* More padding for better appearance */
                margin-right: 1px;  /* Reduced margin for closer tabs */
                font-size: 16px;
                font-weight: 500;
                color: #333;
                text-align: center;
            }}
            QTabBar::tab:selected, QTabBar::tab:hover {{
                background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                                stop:0 #fafafa, stop:1 #f4f4f4);
            }}
            QTabBar::tab:selected {{
                border-color: #9B9B9B;
                border-bottom-color: {primary_color};
                color: {primary_color};
                font-weight: bold;
            }}
            QTabBar::tab:!selected {{
                margin-top: 2px;
            }}
            QTabBar::tab:first {{
                margin-left: 0px;
            }}
            QTabBar::tab:last {{
                margin-right: 0px;
            }}
        """)
        
        # Create modern dashboard tab
        self.create_dashboard_tab()
        self.create_input_tab()
        self.create_view_tab()
        self.create_report_tab()
        
        content_layout.addWidget(self.tab_widget)
        
        # Status bar
        self.statusBar().setStyleSheet(f"""
            QStatusBar {{
                background-color: white;
                color: #666;
                border-top: 1px solid #e0e0e0;
                padding: 5px;
            }}
        """)
        self.statusBar().showMessage("ប្រព័ន្ធរួចរាល់សម្រាប់ប្រើប្រាស់")
        
        main_layout.addWidget(self.content_widget, 1)
    
    def create_modern_sidebar(self, main_layout):
        """Create modern sidebar menu with dark blue theme"""
        primary_color = get_theme_color("primary")
        accent_color = get_theme_color("accent")
        
        sidebar = QWidget()
        sidebar.setFixedWidth(280)
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet(f"""
            #sidebar {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {primary_color}, stop:1 {accent_color});
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Sidebar header with logo
        sidebar_header = QFrame()
        sidebar_header.setFixedHeight(150)
        sidebar_header.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            }
        """)
        
        header_layout = QVBoxLayout(sidebar_header)
        header_layout.setSpacing(15)
        header_layout.setContentsMargins(5, 5, 5, 5)
        
        # Logo/Icon
        logo_label = QLabel("🏢")
        logo_label.setStyleSheet("font-size: 40px; color: white;")
        logo_label.setAlignment(Qt.AlignCenter)
        
        # App name
        app_name = QLabel("គ្រប់គ្រងអត្រានុកូលដ្ឋាន")
        app_name.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        """)
        app_name.setWordWrap(True)
        
        # Version
        version = QLabel("កំណែ 1.5")
        version.setStyleSheet("""
            color: rgba(255, 255, 255, 0.7);
            font-size: 11px;
            text-align: center;
        """)
        
        header_layout.addWidget(logo_label)
        header_layout.addWidget(app_name)
        header_layout.addWidget(version)
        
        sidebar_layout.addWidget(sidebar_header)
        
        # Menu items with icons and indicators - DARK BLUE THEME
        menu_items = [
            ("📊", "ផ្ទាំងគ្រប់គ្រង", self.show_dashboard, True),
            ("📝", "បញ្ជូលទិន្នន័យ", self.show_input_tab, False),
            ("👁️", "មើលទិន្នន័យ", self.show_view_tab, False),
            ("📈", "របាយការណ៍", self.show_report_tab, False),
            ("⚙️", "ការកំណត់", self.show_settings, False),
            ("👤", "ផ្ទាំងអ្នកប្រើ", self.show_user_profile, False),
            ("❓", "ជំនួយ", self.show_help, False)
        ]
        
        menu_frame = QFrame()
        menu_frame.setStyleSheet("""
            QFrame {
                background-color: transparent;
                padding: 20px 0;
            }
        """)
        
        menu_layout = QVBoxLayout(menu_frame)
        menu_layout.setSpacing(5)
        menu_layout.setContentsMargins(15, 0, 15, 0)
        
        for icon, text, handler, active in menu_items:
            btn = self.create_modern_menu_button(icon, text, active)
            btn.clicked.connect(handler)
            menu_layout.addWidget(btn)
        
        menu_layout.addStretch()
        sidebar_layout.addWidget(menu_frame)
        
        # User section at bottom
        user_section = QFrame()
        user_section.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.1);
                border-top: 1px solid rgba(255, 255, 255, 0.2);
                padding: 20px;
            }
        """)
        
        user_layout = QHBoxLayout(user_section)
        
        # User avatar
        avatar = QLabel("👨‍💼")
        avatar.setStyleSheet("font-size: 30px;")
        
        # User info
        user_info = QVBoxLayout()
        user_info.setSpacing(5)
        
        user_name = QLabel("អ្នកគ្រប់គ្រង")
        user_name.setStyleSheet("color: white; font-weight: bold; font-size: 12px;")
        
        user_role = QLabel("អ្នកគ្រប់គ្រងប្រព័ន្ធ")
        user_role.setStyleSheet("color: rgba(200, 200, 220, 0.7); font-size: 12px;")
        
        user_info.addWidget(user_name)
        user_info.addWidget(user_role)
        
        # Logout button with dark blue theme
        logout_btn = QPushButton("🚪")
        logout_btn.setFixedSize(40, 40)  # Increased size
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 25px;
                color: white;
                font-size: 22px;  /* ទំហំពុម្ពអក្សរ 24px */
            }}
            QPushButton:hover {{
                background-color: rgba(200, 200, 200, 0.3);
            }}
        """)
        logout_btn.clicked.connect(self.close)
        
        user_layout.addWidget(avatar)
        user_layout.addLayout(user_info, 1)
        user_layout.addWidget(logout_btn)
        
        sidebar_layout.addWidget(user_section)
        
        main_layout.addWidget(sidebar)
    
    def create_modern_menu_button(self, icon, text, active=False):
        """Create modern menu button with DARK BLUE THEME"""
        primary_color = get_theme_color("primary")
        
        btn = QPushButton()
        btn.setFixedHeight(70)  # Increased height for larger font
        
        if active:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(255, 255, 255, 0.2);
                    border-left: 4px solid white;
                    color: white;
                    text-align: left;
                    padding-left: 20px;
                    border-radius: 0px;
                    font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.3);
                }}
            """)
        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    color: rgba(255, 255, 255, 0.8);
                    text-align: left;
                    padding-left: 20px;
                    border-radius: 0px;
                    font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                    font-weight: bold;
                }}
                QPushButton:hover {{
                    background-color: rgba(255, 255, 255, 0.1);
                    color: white;
                }}
            """)
        
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(0, 0, 20, 0)
        btn_layout.setSpacing(15)
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet("font-size: 24px;")  # Increased icon size
        
        text_label = QLabel(text)
        
        btn_layout.addWidget(icon_label)
        btn_layout.addWidget(text_label, 1)
        
        return btn
    
    def create_dashboard_tab(self):
        """Create modern dashboard tab"""
        self.dashboard_tab = ModernDashboardTab(self)
        self.tab_widget.addTab(self.dashboard_tab, "📊 ផ្ទាំងគ្រប់គ្រង")
    
    def show_dashboard(self):
        """Show dashboard tab with refresh"""
        self.tab_widget.setCurrentIndex(0)
        # Refresh dashboard data
        if hasattr(self, 'dashboard_tab'):
            self.dashboard_tab.load_recent_activities()
    
    def create_input_tab(self):
        """Create input data tab"""
        input_tab = QWidget()
        layout = QVBoxLayout(input_tab)
        layout.setSpacing(15)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        
        # Form title
        form_title = QLabel("បញ្ជូលទិន្នន័យថ្មី")
        form_title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {primary_color};
            border-bottom: 2px solid {primary_color};
            padding-bottom: 8px;
        """)
        layout.addWidget(form_title)
        
        # Form container
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        form_layout = QGridLayout(form_frame)
        form_layout.setVerticalSpacing(12)
        form_layout.setHorizontalSpacing(15)
        form_layout.setColumnStretch(1, 1)
        
        # Form fields
        fields = [
            ("លេខរៀង:", QLineEdit()),
            ("ឈ្មោះពេញ:", QLineEdit()),
            ("ភេទ:", QComboBox()),
            ("ប្រភេទឯកសារ:", QComboBox()),
            ("ភូមិ:", QComboBox()),
            ("ឯកសារ:", QPushButton("📁 ជ្រើសរើសឯកសារ"))
        ]
        
        # Configure comboboxes
        gender_combo = fields[2][1]
        gender_combo.addItems(["ប្រុស", "ស្រី", "ប្ដី/ប្រពន្ធ"])
        
        doc_type_combo = fields[3][1]
        # ប្ដូរប្រភេទឯកសារតាមតម្រូវការ
        doc_type_combo.addItems(["សំបុត្រកំណើត", "សំបុត្រអាពាហ៍ពិពាហ៍", "សំបុត្រមរណភាព", "ឯកសារផ្សេងៗ"])
        
        village_combo = fields[4][1]
        # Use new village names from VILLAGE_NAMES
        village_names = [VILLAGE_NAMES[i] for i in range(1, 17)]
        village_combo.addItems(village_names)
        
        # Store references
        self.serial_input = fields[0][1]
        self.name_input = fields[1][1]
        self.gender_input = gender_combo
        self.doc_type_input = doc_type_combo
        self.village_input = village_combo
        self.image_btn = fields[5][1]
        self.selected_image_path = ""
        
        # Style form elements
        for i, (label_text, widget) in enumerate(fields):
            label = QLabel(label_text)
            label.setStyleSheet("font-weight: bold; font-size: 16px;")
            form_layout.addWidget(label, i, 0, Qt.AlignRight)
            
            if isinstance(widget, QLineEdit):
                widget.setStyleSheet("""
                    QLineEdit {
                        border: 1px solid #ced4da;
                        border-radius: 5px;
                        padding: 8px;
                        font-size: 16px;
                        min-height: 45px;
                    }
                    QLineEdit:focus {
                        border: 1px solid #007bff;
                    }
                """)
            elif isinstance(widget, QComboBox):
                widget.setStyleSheet("""
                    QComboBox {
                        border: 1px solid #ced4da;
                        border-radius: 5px;
                        padding: 8px;
                        font-size: 16px;
                        min-height: 45px;
                    }
                    QComboBox:focus {
                        border: 1px solid #007bff;
                    }
                """)
            elif isinstance(widget, QPushButton):
                widget.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {primary_color};
                        color: white;
                        border: none;
                        border-radius: 5px;
                        padding: 8px 15px;
                        font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                        min-height: 45px;
                    }}
                    QPushButton:hover {{
                        background-color: {get_theme_color("secondary")};
                    }}
                """)
                widget.clicked.connect(self.select_image)
            
            form_layout.addWidget(widget, i, 1)
        
        # Selected image label
        self.selected_image_label = QLabel("មិនទាន់ជ្រើសរើសឯកសារ")
        self.selected_image_label.setStyleSheet("color: #6c757d; font-style: italic; font-size: 14px;")
        form_layout.addWidget(QLabel(), len(fields), 0)
        form_layout.addWidget(self.selected_image_label, len(fields), 1)
        
        # Buttons with dark blue theme
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        save_btn = QPushButton("💾 រក្សាទុក")
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 55px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        save_btn.clicked.connect(self.save_data)
        
        clear_btn = QPushButton("🧹 លុបសារឡើងវិញ")
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {get_theme_color("accent")};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 30px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 55px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("dark")};
            }}
        """)
        clear_btn.clicked.connect(self.clear_form)
        
        button_layout.addStretch()
        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        
        form_layout.addLayout(button_layout, len(fields)+1, 0, 1, 2)
        
        layout.addWidget(form_frame)
        layout.addStretch()
        
        self.tab_widget.addTab(input_tab, "📝 បញ្ជូលទិន្នន័យ")
    
    def create_view_tab(self):
        """Create view data tab with search and image preview"""
        view_widget = QWidget()
        main_layout = QHBoxLayout(view_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        
        # Left panel for search and table
        left_panel = QWidget()
        left_panel.setMinimumWidth(1000)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(15)
        
        # Search bar with file search button
        search_frame = QFrame()
        search_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        search_layout = QVBoxLayout(search_frame)
        
        # Search by name
        search_name_layout = QHBoxLayout()
        
        search_name_label = QLabel("ស្វែងរកតាមឈ្មោះ:")
        search_name_label.setStyleSheet("font-weight: bold; font-size: 16px; min-width: 120px;")
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("បញ្ចូលឈ្មោះដើម្បីស្វែងរក...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #ced4da;
                border-radius: 5px;
                padding: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 1px solid #007bff;
            }
        """)
        
        # Search button with dark blue theme
        search_name_btn = QPushButton("🔍 ស្វែងរក")
        search_name_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-width: 140px;
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        search_name_btn.clicked.connect(self.perform_search_by_name)
        
        search_name_layout.addWidget(search_name_label)
        search_name_layout.addWidget(self.search_input, 1)
        search_name_layout.addWidget(search_name_btn)
        
        # Search by file button
        search_file_layout = QHBoxLayout()
        
        search_file_label = QLabel("ស្វែងរកឯកសារ:")
        search_file_label.setStyleSheet("font-weight: bold; font-size: 16px; min-width: 120px;")
        
        # Search file button with green theme
        search_file_btn = QPushButton("📁 ស្វែងរកឯកសារ")
        search_file_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: #218838;
            }}
        """)
        search_file_btn.clicked.connect(self.search_file_by_name)
        
        # Show all button with dark blue theme
        show_all_btn = QPushButton("📋 បង្ហាញទាំងអស់")
        show_all_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 45px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        show_all_btn.clicked.connect(self.show_all_data)
        
        search_file_layout.addWidget(search_file_label)
        search_file_layout.addWidget(search_file_btn)
        search_file_layout.addWidget(show_all_btn)
        search_file_layout.addStretch()
        
        search_layout.addLayout(search_name_layout)
        search_layout.addLayout(search_file_layout)
        
        left_layout.addWidget(search_frame)
        
        # Table title
        table_title = QLabel("ទិន្នន័យដែលបានរក្សាទុក")
        table_title.setStyleSheet(f"""
            font-size: 16px;
            font-weight: bold;
            color: {primary_color};
            border-bottom: 2px solid {primary_color};
            padding-bottom: 5px;
        """)
        left_layout.addWidget(table_title)
        
        # Create table
        self.data_table = QTableWidget()
        self.data_table.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                font-size: 14px;
            }}
            QHeaderView::section {{
                background-color: {primary_color};
                color: white;
                padding: 12px;
                border: none;
                font-weight: bold;
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 8px;
            }}
            QTableWidget::item:selected {{
                background-color: #cce5ff;
                color: #004085;
            }}
            QTableWidget::item:hover {{
                background-color: #f8f9fa;
            }}
        """)
        
        self.data_table.setColumnCount(7)
        self.data_table.setHorizontalHeaderLabels([
            "ល.រ", "លេខរៀង", "ឈ្មោះ", "ភេទ", "ប្រភេទឯកសារ", "ភូមិ", "ឯកសារ"
        ])
        
        self.data_table.setAlternatingRowColors(True)
        self.data_table.verticalHeader().setVisible(False)
        self.data_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.data_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Set column widths
        header = self.data_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Serial
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # Name
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Gender
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Doc Type
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Village
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # File
        
        # Load data
        self.load_table_data()
        
        # Connect row selection
        self.data_table.itemSelectionChanged.connect(self.on_row_selected)
        
        left_layout.addWidget(self.data_table, 1)
        
        # Action buttons with dark blue theme
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.view_file_btn = QPushButton("👁️ មើលឯកសារ")
        self.view_file_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
            QPushButton:disabled {{
                background-color: #6c757d;
                color: #adb5bd;
            }}
        """)
        self.view_file_btn.setEnabled(False)
        self.view_file_btn.clicked.connect(self.view_selected_file)
        
        export_btn = QPushButton("📥 បញ្ចេញទិន្នន័យ")
        export_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #20c997;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: #1aa179;
            }}
        """)
        export_btn.clicked.connect(self.export_data)
        
        self.delete_btn = QPushButton("🗑️ លុបទិន្នន័យ")
        self.delete_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {get_theme_color("accent")};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("dark")};
            }}
            QPushButton:disabled {{
                background-color: #6c757d;
                color: #adb5bd;
            }}
        """)
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_selected_row)
        
        refresh_btn = QPushButton("🔄 ផ្ទុកឡើងវិញ")
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        refresh_btn.clicked.connect(self.load_table_data)
        
        button_layout.addWidget(self.view_file_btn)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addStretch()
        
        left_layout.addLayout(button_layout)
        
        # Right panel for image preview
        right_panel = QWidget()
        right_panel.setMinimumWidth(400)
        right_panel.setStyleSheet("""
            QWidget {
                background-color: white;
                border-left: 1px solid #dee2e6;
            }
        """)
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(15)
        
        # Preview title
        preview_title = QLabel("បង្ហាញរូបភាពឯកសារ")
        preview_title.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {primary_color};
            border-bottom: 2px solid {primary_color};
            padding-bottom: 10px;
            margin-bottom: 15px;
        """)
        preview_title.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(preview_title)
        
        # Image preview area
        self.preview_frame = QFrame()
        self.preview_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {get_theme_color("light")};
                border: 2px dashed {primary_color};
                border-radius: 10px;
                min-height: 300px;
            }}
        """)
        
        preview_layout = QVBoxLayout(self.preview_frame)
        preview_layout.setAlignment(Qt.AlignCenter)
        
        self.preview_label = QLabel("ជ្រើសរើសឯកសារដើម្បីបង្ហាញ")
        self.preview_label.setStyleSheet("""
            font-size: 16px;
            color: #6c757d;
            font-style: italic;
        """)
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setWordWrap(True)
        
        self.preview_image = QLabel()
        self.preview_image.setAlignment(Qt.AlignCenter)
        self.preview_image.setStyleSheet("""
            QLabel {
                border: none;
                background-color: transparent;
            }
        """)
        self.preview_image.setScaledContents(False)
        
        preview_layout.addWidget(self.preview_label)
        preview_layout.addWidget(self.preview_image)
        
        right_layout.addWidget(self.preview_frame, 1)
        
        # File info
        self.file_info_frame = QFrame()
        self.file_info_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {get_theme_color("light")};
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 15px;
            }}
        """)
        self.file_info_frame.hide()  # Hide initially
        
        file_info_layout = QVBoxLayout(self.file_info_frame)
        
        self.file_name_label = QLabel("ឈ្មោះឯកសារ: -")
        self.file_name_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        
        self.file_size_label = QLabel("ទំហំ: -")
        self.file_size_label.setStyleSheet("color: #666; font-size: 13px;")
        
        self.file_date_label = QLabel("កាលបរិច្ឆេទ: -")
        self.file_date_label.setStyleSheet("color: #666; font-size: 13px;")
        
        self.file_path_label = QLabel("ទីតាំង: -")
        self.file_path_label.setStyleSheet("color: #666; font-size: 12px;")
        self.file_path_label.setWordWrap(True)
        
        file_info_layout.addWidget(self.file_name_label)
        file_info_layout.addWidget(self.file_size_label)
        file_info_layout.addWidget(self.file_date_label)
        file_info_layout.addWidget(self.file_path_label)
        
        right_layout.addWidget(self.file_info_frame)
        
        # Open file button with dark blue theme
        self.open_file_btn = QPushButton("📂 បើកឯកសារ")
        self.open_file_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
            QPushButton:disabled {{
                background-color: #6c757d;
                color: #adb5bd;
            }}
        """)
        self.open_file_btn.setEnabled(False)
        self.open_file_btn.clicked.connect(self.open_selected_file)
        right_layout.addWidget(self.open_file_btn)
        
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)
        
        self.tab_widget.addTab(view_widget, "👁️ មើលទិន្នន័យ")
    
    def create_report_tab(self):
        """Create beautiful report tab"""
        report_tab = QWidget()
        
        # Set theme colors
        primary_color = get_theme_color("primary")
        
        # Create scroll area for the report
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background-color: {get_theme_color("light")};
            }}
            QScrollBar:vertical {{
                background-color: #f1f1f1;
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {primary_color};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {get_theme_color("accent")};
            }}
        """)
        
        report_widget = QWidget()
        scroll_area.setWidget(report_widget)
        
        layout = QVBoxLayout(report_tab)
        layout.addWidget(scroll_area)
        
        # Report content
        report_layout = QVBoxLayout(report_widget)
        report_layout.setSpacing(20)
        report_layout.setContentsMargins(30, 30, 30, 30)
        
        # Report header
        header_frame = QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {primary_color}, stop:1 {get_theme_color("accent")});
                border-radius: 15px;
                padding: 25px;
            }}
            QLabel {{
                color: white;
            }}
        """)
        
        header_layout = QVBoxLayout(header_frame)
        
        report_title = QLabel("របាយការណ៍អត្រានុកូលដ្ឋាន")
        report_title.setStyleSheet("font-size: 28px; font-weight: bold;")
        report_title.setAlignment(Qt.AlignCenter)
        
        report_subtitle = QLabel(f"កាលបរិច្ឆេទ: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report_subtitle.setStyleSheet("font-size: 16px; opacity: 0.9;")
        report_subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(report_title)
        header_layout.addWidget(report_subtitle)
        
        report_layout.addWidget(header_frame)
        
        # Statistics section
        stats = self.get_statistics()
        
        stats_section = QLabel("ស្ថិតិទិន្នន័យ")
        stats_section.setStyleSheet(f"""
            font-size: 22px;
            font-weight: bold;
            color: {get_theme_color("dark")};
            margin-top: 10px;
            padding-bottom: 10px;
            border-bottom: 2px solid {primary_color};
        """)
        report_layout.addWidget(stats_section)
        
        # Statistics cards in grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(20)
        
        stat_items = [
            ("សរុបអ្នកបង់ប្រាក់", stats['total'], "👥", primary_color),
            ("ប្រុស", stats['male'], "👨", "#28a745"),
            ("ស្រី", stats['female'], "👩", "#e83e8c"),
            ("ភូមិសកម្ម", stats['villages'], "🏘️", "#fd7e14"),
            ("បញ្ជូលថ្ងៃនេះ", stats['today'], "📅", "#17a2b8"),
            ("ប្រភេទឯកសារ", stats['doc_types'], "📋", "#6f42c1")
        ]
        
        for i, (title, value, icon, color) in enumerate(stat_items):
            stat_card = self.create_beautiful_stat_card(title, value, icon, color)
            stats_grid.addWidget(stat_card, i // 3, i % 3)
        
        report_layout.addLayout(stats_grid)
        
        # Village distribution section
        village_section = QLabel("ការបែងចែកតាមភូមិ")
        village_section.setStyleSheet(stats_section.styleSheet())
        report_layout.addWidget(village_section)
        
        # Village distribution chart
        village_chart = self.create_village_distribution_chart()
        report_layout.addWidget(village_chart)
        
        # Gender distribution section
        gender_section = QLabel("ការបែងចែកតាមភេទ")
        gender_section.setStyleSheet(stats_section.styleSheet())
        report_layout.addWidget(gender_section)
        
        # Gender distribution
        gender_layout = QHBoxLayout()
        
        gender_frame = QFrame()
        gender_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        gender_inner_layout = QVBoxLayout(gender_frame)
        
        total = stats['total'] if stats['total'] > 0 else 1
        male_percent = (stats['male'] / total) * 100
        female_percent = (stats['female'] / total) * 100
        
        # Male stats
        male_item = QHBoxLayout()
        male_icon = QLabel("👨")
        male_icon.setStyleSheet("font-size: 24px;")
        
        male_info = QVBoxLayout()
        male_label = QLabel("ប្រុស")
        male_label.setStyleSheet("font-weight: bold; color: #28a745; font-size: 16px;")
        
        male_count = QLabel(f"{stats['male']} នាក់ ({male_percent:.1f}%)")
        male_count.setStyleSheet("font-size: 14px; color: #6c757d;")
        
        male_info.addWidget(male_label)
        male_info.addWidget(male_count)
        
        male_item.addWidget(male_icon)
        male_item.addLayout(male_info, 1)
        male_item.addStretch()
        
        gender_inner_layout.addLayout(male_item)
        
        # Female stats
        female_item = QHBoxLayout()
        female_icon = QLabel("👩")
        female_icon.setStyleSheet("font-size: 24px;")
        
        female_info = QVBoxLayout()
        female_label = QLabel("ស្រី")
        female_label.setStyleSheet("font-weight: bold; color: #e83e8c; font-size: 16px;")
        
        female_count = QLabel(f"{stats['female']} នាក់ ({female_percent:.1f}%)")
        female_count.setStyleSheet("font-size: 14px; color: #6c757d;")
        
        female_info.addWidget(female_label)
        female_info.addWidget(female_count)
        
        female_item.addWidget(female_icon)
        female_item.addLayout(female_info, 1)
        female_item.addStretch()
        
        gender_inner_layout.addLayout(female_item)
        gender_inner_layout.addStretch()
        
        gender_layout.addWidget(gender_frame, 1)
        
        # Document type distribution
        doc_frame = QFrame()
        doc_frame.setStyleSheet(gender_frame.styleSheet())
        
        doc_layout = QVBoxLayout(doc_frame)
        
        doc_title = QLabel("ប្រភេទឯកសារ")
        doc_title.setStyleSheet(f"font-weight: bold; color: {primary_color}; font-size: 16px; margin-bottom: 10px;")
        
        # Get document type distribution
        self.db_cursor.execute("""
            SELECT document_type, COUNT(*) as count 
            FROM tax_payers 
            GROUP BY document_type 
            ORDER BY count DESC
        """)
        doc_types = self.db_cursor.fetchall()
        
        for doc_type, count in doc_types:
            doc_item = QHBoxLayout()
            
            doc_type_label = QLabel(doc_type)
            doc_type_label.setStyleSheet("font-size: 14px; min-width: 150px;")
            
            doc_count = QLabel(f"{count} នាក់")
            doc_count.setStyleSheet("font-weight: bold; color: #17a2b8; font-size: 14px;")
            
            doc_percent = QLabel(f"({(count/total*100):.1f}%)")
            doc_percent.setStyleSheet("font-size: 13px; color: #6c757d;")
            
            doc_item.addWidget(doc_type_label)
            doc_item.addWidget(doc_count)
            doc_item.addWidget(doc_percent)
            doc_item.addStretch()
            
            doc_layout.addLayout(doc_item)
        
        doc_layout.addStretch()
        gender_layout.addWidget(doc_frame, 1)
        
        report_layout.addLayout(gender_layout)
        
        # Recent activity section
        activity_section = QLabel("សកម្មភាពថ្មីៗ")
        activity_section.setStyleSheet(stats_section.styleSheet())
        report_layout.addWidget(activity_section)
        
        # Recent activities
        activity_frame = QFrame()
        activity_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        activity_layout = QVBoxLayout(activity_frame)
        
        # Get recent activities
        self.db_cursor.execute("""
            SELECT name, village, registration_date 
            FROM tax_payers 
            ORDER BY registration_date DESC 
            LIMIT 5
        """)
        recent_activities = self.db_cursor.fetchall()
        
        for i, (name, village, reg_date) in enumerate(recent_activities):
            activity_item = QFrame()
            activity_item.setStyleSheet(f"""
                QFrame {{
                    background-color: {get_theme_color("light")};
                    border-radius: 8px;
                    padding: 12px;
                    margin-bottom: 8px;
                }}
            """)
            
            item_layout = QHBoxLayout(activity_item)
            
            # Number
            number_label = QLabel(str(i+1))
            number_label.setStyleSheet(f"""
                font-size: 18px;
                font-weight: bold;
                color: {primary_color};
                min-width: 30px;
            """)
            
            # Info
            info_layout = QVBoxLayout()
            
            name_label = QLabel(name)
            name_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px;")
            
            village_label = QLabel(f"ភូមិ: {village}")
            village_label.setStyleSheet("color: #6c757d; font-size: 13px;")
            
            info_layout.addWidget(name_label)
            info_layout.addWidget(village_label)
            
            # Date
            date_label = QLabel(reg_date[:10])
            date_label.setStyleSheet("color: #95a5a6; font-size: 12px; min-width: 100px;")
            
            item_layout.addWidget(number_label)
            item_layout.addLayout(info_layout, 1)
            item_layout.addWidget(date_label)
            
            activity_layout.addWidget(activity_item)
        
        activity_layout.addStretch()
        report_layout.addWidget(activity_frame)
        
        # Export buttons with dark blue theme
        export_layout = QHBoxLayout()
        
        export_pdf_btn = QPushButton("📄 បញ្ចេញជា PDF")
        export_pdf_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {get_theme_color("accent")};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 25px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("dark")};
            }}
        """)
        
        export_excel_btn = QPushButton("📊 បញ្ចេញជា Excel")
        export_excel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #28a745;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 25px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: #218838;
            }}
        """)
        
        export_csv_btn = QPushButton("📋 បញ្ចេញជា CSV")
        export_csv_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {primary_color};
                color: white;
                border: none;
                border-radius: 5px;
                padding: 12px 25px;
                font-weight: bold;
                font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                min-height: 50px;
            }}
            QPushButton:hover {{
                background-color: {get_theme_color("secondary")};
            }}
        """)
        export_csv_btn.clicked.connect(self.export_report)
        
        export_layout.addStretch()
        export_layout.addWidget(export_pdf_btn)
        export_layout.addWidget(export_excel_btn)
        export_layout.addWidget(export_csv_btn)
        export_layout.addStretch()
        
        report_layout.addLayout(export_layout)
        report_layout.addStretch()
        
        self.tab_widget.addTab(report_tab, "📈 របាយការណ៍")
    
    def create_beautiful_stat_card(self, title, value, icon, color):
        """Create a beautiful statistic card for reports"""
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        
        layout = QVBoxLayout(card)
        layout.setSpacing(10)
        
        # Top row (icon and title)
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"font-size: 32px; color: {color};")
        
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #6c757d; font-weight: bold;")
        title_label.setWordWrap(True)
        
        top_layout.addWidget(icon_label)
        top_layout.addWidget(title_label, 1)
        
        # Value
        value_label = QLabel(str(value))
        value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
        value_label.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(top_layout)
        layout.addWidget(value_label)
        
        return card
    
    def create_village_distribution_chart(self):
        """Create a beautiful village distribution chart"""
        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        chart_layout = QVBoxLayout(chart_frame)
        
        # Get village data
        self.db_cursor.execute("""
            SELECT v.name, COUNT(tp.id) as count
            FROM villages v
            LEFT JOIN tax_payers tp ON v.name = tp.village
            GROUP BY v.id, v.name
            ORDER BY v.id
        """)
        village_data = self.db_cursor.fetchall()
        
        # Colors for bars
        colors = ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d', 
                  '#17a2b8', '#6610f2', '#fd7e14', '#20c997', '#e83e8c']
        
        max_count = max(count for _, count in village_data) if village_data else 1
        
        for i, (village, count) in enumerate(village_data):
            item_frame = QFrame()
            item_layout = QHBoxLayout(item_frame)
            item_layout.setSpacing(10)
            
            # Village name
            village_label = QLabel(village)
            village_label.setStyleSheet("font-weight: bold; color: #495057; font-size: 14px; min-width: 100px;")
            
            # Progress bar
            progress_frame = QFrame()
            progress_frame.setFixedHeight(20)
            
            progress_width = int((count / max_count) * 300) if max_count > 0 else 0
            
            progress_inner = QFrame(progress_frame)
            progress_inner.setGeometry(0, 0, progress_width, 20)
            progress_inner.setStyleSheet(f"""
                background-color: {colors[i % len(colors)]};
                border-radius: 10px;
            """)
            
            # Count label
            count_label = QLabel(str(count))
            count_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px; min-width: 50px;")
            
            # Percentage
            percentage = (count / max_count * 100) if max_count > 0 else 0
            percent_label = QLabel(f"{percentage:.1f}%")
            percent_label.setStyleSheet("color: #6c757d; font-size: 13px; min-width: 50px;")
            
            item_layout.addWidget(village_label)
            item_layout.addWidget(progress_frame, 1)
            item_layout.addWidget(count_label)
            item_layout.addWidget(percent_label)
            
            chart_layout.addWidget(item_frame)
        
        return chart_frame
    
    # ================ Database and UI Methods ================
    
    def select_image(self):
        """Select any file (not just images)"""
        primary_color = get_theme_color("primary")
        
        file_name, _ = QFileDialog.getOpenFileName(
            self, "ជ្រើសរើសឯកសារ", 
            "", 
            "ឯកសារទាំងអស់ (*.*)"
        )
        
        if file_name:
            self.selected_image_path = file_name
            file_name_short = os.path.basename(file_name)
            if len(file_name_short) > 25:
                file_name_short = file_name_short[:22] + "..."
            self.selected_image_label.setText(f"បានជ្រើសរើស: {file_name_short}")
            self.selected_image_label.setStyleSheet(f"color: {primary_color}; font-weight: bold; font-size: 14px;")
    
    def save_data(self):
        """Save data to database"""
        # Validation
        if not self.serial_input.text().strip():
            QMessageBox.warning(self, "ការព្រមាន", "សូមបំពេញលេខរៀង!")
            self.serial_input.setFocus()
            return
        
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "ការព្រមាន", "សូមបំពេញឈ្មោះ!")
            self.name_input.setFocus()
            return
        
        if not self.selected_image_path:
            QMessageBox.warning(self, "ការព្រមាន", "សូមជ្រើសរើសឯកសារ!")
            return
        
        try:
            # Check for duplicate serial number
            self.db_cursor.execute(
                "SELECT id FROM tax_payers WHERE serial_number = ?",
                (self.serial_input.text().strip(),)
            )
            if self.db_cursor.fetchone():
                QMessageBox.warning(self, "ការព្រមាន", "លេខរៀងនេះមានរួចហើយ!")
                return
            
            # Copy file to application directory
            file_extension = os.path.splitext(self.selected_image_path)[1]
            file_filename = f"doc_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
            file_dest = os.path.join(self.images_dir, file_filename)
            
            try:
                shutil.copy2(self.selected_image_path, file_dest)
            except:
                # If copy fails, use original path
                file_dest = self.selected_image_path
            
            # Insert data
            self.db_cursor.execute('''
                INSERT INTO tax_payers 
                (serial_number, name, gender, document_type, document_photo, village)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                self.serial_input.text().strip(),
                self.name_input.text().strip(),
                self.gender_input.currentText(),
                self.doc_type_input.currentText(),
                file_dest,
                self.village_input.currentText()
            ))
            
            self.conn.commit()
            
            QMessageBox.information(self, "ជោគជ័យ", "ទិន្នន័យត្រូវបានរក្សាទុកដោយជោគជ័យ!")
            self.statusBar().showMessage("ទិន្នន័យត្រូវបានរក្សាទុក", 3000)
            
            # Clear form and refresh data
            self.clear_form()
            self.load_table_data()
            
            # Switch to view tab
            self.tab_widget.setCurrentIndex(2)  # View tab is now index 2
            
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចរក្សាទុកទិន្នន័យ:\n{str(e)}")
    
    def clear_form(self):
        """Clear form fields"""
        self.serial_input.clear()
        self.name_input.clear()
        self.gender_input.setCurrentIndex(0)
        self.doc_type_input.setCurrentIndex(0)
        self.village_input.setCurrentIndex(0)
        self.selected_image_path = ""
        self.selected_image_label.setText("មិនទាន់ជ្រើសរើសឯកសារ")
        self.selected_image_label.setStyleSheet("color: #6c757d; font-style: italic; font-size: 13px;")
        self.serial_input.setFocus()
    
    def load_table_data(self):
        """Load data into table"""
        try:
            self.db_cursor.execute("""
                SELECT id, serial_number, name, gender, document_type, village, document_photo
                FROM tax_payers 
                ORDER BY id DESC
            """)
            data = self.db_cursor.fetchall()
            
            self.data_table.setRowCount(len(data))
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    if col_idx == 6:  # File column
                        if cell_data and os.path.exists(cell_data):
                            file_name = os.path.basename(cell_data)
                            # Truncate long filenames
                            if len(file_name) > 20:
                                display_name = file_name[:17] + "..."
                            else:
                                display_name = file_name
                            item = QTableWidgetItem(f"📄 {display_name}")
                        else:
                            item = QTableWidgetItem("📄 ឯកសារ")
                        item.setData(Qt.UserRole, cell_data)  # Store file path
                    else:
                        item = QTableWidgetItem(str(cell_data) if cell_data else "")
                    
                    # Center align for some columns
                    if col_idx in [0, 3, 4, 5, 6]:
                        item.setTextAlignment(Qt.AlignCenter)
                    
                    self.data_table.setItem(row_idx, col_idx, item)
            
            self.statusBar().showMessage(f"បានផ្ទុកទិន្នន័យ {len(data)} កំណត់ត្រា", 3000)
            
        except Exception as e:
            self.statusBar().showMessage(f"កំហុសក្នុងការផ្ទុកទិន្នន័យ: {str(e)}", 5000)
    
    def on_row_selected(self):
        """Handle row selection in table"""
        selected_rows = self.data_table.selectionModel().selectedRows()
        if selected_rows:
            row = selected_rows[0].row()
            self.selected_row = row
            self.view_file_btn.setEnabled(True)
            self.delete_btn.setEnabled(True)
            self.open_file_btn.setEnabled(True)
            
            # Load file info for preview
            self.load_file_preview(row)
        else:
            self.view_file_btn.setEnabled(False)
            self.delete_btn.setEnabled(False)
            self.open_file_btn.setEnabled(False)
            self.clear_preview()
    
    def load_file_preview(self, row):
        """Load file preview for selected row"""
        try:
            file_path_item = self.data_table.item(row, 6)
            if file_path_item:
                file_path = file_path_item.data(Qt.UserRole)
                if file_path and os.path.exists(file_path):
                    # Update file info
                    file_name = os.path.basename(file_path)
                    file_size = os.path.getsize(file_path)
                    file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')
                    
                    self.file_name_label.setText(f"ឈ្មោះឯកសារ: {file_name}")
                    
                    # Format file size
                    if file_size < 1024:
                        size_str = f"{file_size} bytes"
                    elif file_size < 1024*1024:
                        size_str = f"{file_size/1024:.1f} KB"
                    else:
                        size_str = f"{file_size/(1024*1024):.1f} MB"
                    self.file_size_label.setText(f"ទំហំ: {size_str}")
                    
                    self.file_date_label.setText(f"កាលបរិច្ឆេទ: {file_date}")
                    self.file_path_label.setText(f"ទីតាំង: {file_path}")
                    
                    self.file_info_frame.show()
                    
                    # Display image if it's an image file
                    file_extension = os.path.splitext(file_path)[1].lower()
                    if file_extension in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                        self.preview_label.hide()
                        self.preview_image.show()
                        
                        pixmap = QPixmap(file_path)
                        if not pixmap.isNull():
                            # Scale image to fit preview area
                            scaled_pixmap = pixmap.scaled(350, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                            self.preview_image.setPixmap(scaled_pixmap)
                        else:
                            self.preview_image.clear()
                            self.preview_label.setText("មិនអាចបង្ហាញរូបភាព")
                            self.preview_label.show()
                    else:
                        # For non-image files, show file icon and info
                        self.preview_image.hide()
                        self.preview_label.show()
                        self.preview_label.setText(f"ប្រភេទឯកសារ: {file_extension.upper() if file_extension else 'មិនស្គាល់'}\n\nចុចប៊ូតុង 'បើកឯកសារ' ដើម្បីមើល")
                        
                else:
                    self.clear_preview()
        except Exception as e:
            print(f"Error loading preview: {e}")
            self.clear_preview()
    
    def clear_preview(self):
        """Clear preview area"""
        self.preview_image.clear()
        self.preview_label.setText("ជ្រើសរើសឯកសារដើម្បីបង្ហាញ")
        self.preview_label.show()
        self.file_info_frame.hide()
        self.open_file_btn.setEnabled(False)
    
    def view_selected_file(self):
        """View selected file"""
        if hasattr(self, 'selected_row'):
            file_path_item = self.data_table.item(self.selected_row, 6)
            if file_path_item:
                file_path = file_path_item.data(Qt.UserRole)
                if file_path and os.path.exists(file_path):
                    self.open_file(file_path)
                else:
                    QMessageBox.warning(self, "ការព្រមាន", "ឯកសារមិនមាន!")
    
    def open_selected_file(self):
        """Open selected file from preview"""
        if hasattr(self, 'selected_row'):
            file_path_item = self.data_table.item(self.selected_row, 6)
            if file_path_item:
                file_path = file_path_item.data(Qt.UserRole)
                if file_path and os.path.exists(file_path):
                    self.open_file(file_path)
    
    def open_file(self, file_path):
        """Open file using system default application"""
        try:
            if os.path.exists(file_path):
                # Check file extension
                file_extension = os.path.splitext(file_path)[1].lower()
                
                if file_extension in ['.txt', '.pdf', '.jpg', '.jpeg', '.png', '.bmp']:
                    # For text and image files, open with default application
                    os.startfile(file_path)
                else:
                    # For other files, offer to open folder
                    reply = QMessageBox.question(
                        self, 'បើកឯកសារ',
                        f'ឯកសារ: {os.path.basename(file_path)}\n\nតើអ្នកចង់បើកថតដែលមានឯកសារនេះទេ?',
                        QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
                    )
                    
                    if reply == QMessageBox.Yes:
                        os.startfile(os.path.dirname(file_path))
            else:
                QMessageBox.warning(self, "ការព្រមាន", "ឯកសារមិនមាន!")
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចបើកឯកសារ:\n{str(e)}")
    
    def perform_search_by_name(self):
        """Perform search based on name"""
        search_text = self.search_input.text().strip()
        if not search_text:
            QMessageBox.information(self, "ព័ត៌មាន", "សូមបំពេញឈ្មោះដើម្បីស្វែងរក")
            return
        
        try:
            self.db_cursor.execute("""
                SELECT id, serial_number, name, gender, document_type, village, document_photo
                FROM tax_payers 
                WHERE name LIKE ?
                ORDER BY id DESC
            """, (f"%{search_text}%",))
            
            data = self.db_cursor.fetchall()
            
            if not data:
                QMessageBox.information(self, "ព័ត៌មាន", "មិនមានលទ្ធផលសម្រាប់ការស្វែងរកនេះ")
                self.data_table.setRowCount(0)
                return
            
            self.data_table.setRowCount(len(data))
            
            for row_idx, row_data in enumerate(data):
                for col_idx, cell_data in enumerate(row_data):
                    if col_idx == 6:  # File column
                        if cell_data and os.path.exists(cell_data):
                            file_name = os.path.basename(cell_data)
                            if len(file_name) > 20:
                                display_name = file_name[:17] + "..."
                            else:
                                display_name = file_name
                            item = QTableWidgetItem(f"📄 {display_name}")
                        else:
                            item = QTableWidgetItem("📄 ឯកសារ")
                        item.setData(Qt.UserRole, cell_data)
                    else:
                        item = QTableWidgetItem(str(cell_data) if cell_data else "")
                    
                    if col_idx in [0, 3, 4, 5, 6]:
                        item.setTextAlignment(Qt.AlignCenter)
                    
                    self.data_table.setItem(row_idx, col_idx, item)
            
            self.statusBar().showMessage(f"បានរកឃើញ {len(data)} លទ្ធផល", 3000)
            
            # Select first row if found
            if len(data) > 0:
                self.data_table.selectRow(0)
            
        except Exception as e:
            self.statusBar().showMessage(f"កំហុសក្នុងការស្វែងរក: {str(e)}", 5000)
    
    def search_file_by_name(self):
        """Search for files by name"""
        try:
            # Get all files from database
            self.db_cursor.execute("""
                SELECT id, serial_number, name, gender, document_type, village, document_photo
                FROM tax_payers 
                WHERE document_photo IS NOT NULL AND document_photo != ''
                ORDER BY id DESC
            """)
            
            data = self.db_cursor.fetchall()
            
            if not data:
                QMessageBox.information(self, "ព័ត៌មាន", "មិនមានឯកសារក្នុងទិន្នន័យ")
                return
            
            # Create dialog to show file list
            dialog = QDialog(self)
            dialog.setWindowTitle("ស្វែងរកឯកសារ")
            dialog.setFixedSize(600, 400)
            
            # Set theme colors
            primary_color = get_theme_color("primary")
            
            layout = QVBoxLayout(dialog)
            
            # Search box
            search_layout = QHBoxLayout()
            search_label = QLabel("ស្វែងរកឯកសារ:")
            search_label.setStyleSheet("font-weight: bold;")
            
            file_search_input = QLineEdit()
            file_search_input.setPlaceholderText("បញ្ចូលឈ្មោះឯកសារ...")
            
            search_btn = QPushButton("🔍 ស្វែងរក")
            search_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {primary_color};
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 5px 15px;
                    font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                    min-height: 45px;
                }}
            """)
            
            search_layout.addWidget(search_label)
            search_layout.addWidget(file_search_input, 1)
            search_layout.addWidget(search_btn)
            
            layout.addLayout(search_layout)
            
            # File list
            file_list = QListWidget()
            file_list.setStyleSheet(f"""
                QListWidget {{
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                }}
                QListWidget::item {{
                    padding: 10px;
                    border-bottom: 1px solid #f0f0f0;
                }}
                QListWidget::item:selected {{
                    background-color: {get_theme_color("light")};
                    color: {primary_color};
                    border-left: 3px solid {primary_color};
                }}
            """)
            
            # Add files to list
            for row in data:
                file_path = row[6]
                if file_path and os.path.exists(file_path):
                    file_name = os.path.basename(file_path)
                    item_text = f"{file_name} - {row[2]}"
                    list_item = QListWidgetItem(f"📄 {item_text}")
                    list_item.setData(Qt.UserRole, row[0])  # Store record ID
                    file_list.addItem(list_item)
            
            layout.addWidget(file_list)
            
            # Buttons with dark blue theme
            button_layout = QHBoxLayout()
            view_btn = QPushButton("មើលឯកសារ")
            view_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {primary_color};
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 8px 20px;
                    font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                    min-height: 45px;
                }}
                QPushButton:hover {{
                    background-color: {get_theme_color("secondary")};
                }}
            """)
            
            close_btn = QPushButton("បិទ")
            close_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #6c757d;
                    color: white;
                    border: none;
                    border-radius: 3px;
                    padding: 8px 20px;
                    font-size: 20px;  /* ទំហំពុម្ពអក្សរ 20px */
                    min-height: 45px;
                }}
                QPushButton:hover {{
                    background-color: #5a6268;
                }}
            """)
            
            button_layout.addStretch()
            button_layout.addWidget(view_btn)
            button_layout.addWidget(close_btn)
            
            layout.addLayout(button_layout)
            
            # Connect signals
            def search_files():
                search_text = file_search_input.text().strip().lower()
                for i in range(file_list.count()):
                    item = file_list.item(i)
                    item.setHidden(search_text not in item.text().lower())
            
            def view_selected_file():
                selected_items = file_list.selectedItems()
                if selected_items:
                    record_id = selected_items[0].data(Qt.UserRole)
                    # Find and select the row in table
                    for row in range(self.data_table.rowCount()):
                        id_item = self.data_table.item(row, 0)
                        if id_item and int(id_item.text()) == record_id:
                            self.data_table.selectRow(row)
                            self.data_table.scrollToItem(id_item)
                            dialog.accept()
                            break
            
            search_btn.clicked.connect(search_files)
            file_search_input.textChanged.connect(search_files)
            view_btn.clicked.connect(view_selected_file)
            close_btn.clicked.connect(dialog.reject)
            file_list.itemDoubleClicked.connect(view_selected_file)
            
            dialog.exec_()
            
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"កំហុសក្នុងការស្វែងរកឯកសារ: {str(e)}")
    
    def show_all_data(self):
        """Show all data"""
        self.load_table_data()
        self.statusBar().showMessage("បានបង្ហាញទិន្នន័យទាំងអស់", 3000)
    
    def delete_selected_row(self):
        """Delete selected row from database"""
        if not hasattr(self, 'selected_row'):
            return
        
        reply = QMessageBox.question(
            self, 'លុបទិន្នន័យ',
            'តើអ្នកពិតជាចង់លុបទិន្នន័យនេះមែនទេ?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Get ID of selected row
                id_item = self.data_table.item(self.selected_row, 0)
                if id_item:
                    record_id = int(id_item.text())
                    
                    # Get file path before deleting
                    file_item = self.data_table.item(self.selected_row, 6)
                    file_path = file_item.data(Qt.UserRole) if file_item else None
                    
                    # Delete from database
                    self.db_cursor.execute("DELETE FROM tax_payers WHERE id = ?", (record_id,))
                    self.conn.commit()
                    
                    # Try to delete file (optional)
                    if file_path and os.path.exists(file_path) and file_path.startswith(self.images_dir):
                        try:
                            os.remove(file_path)
                        except:
                            pass  # Don't worry if file delete fails
                    
                    # Refresh data
                    self.load_table_data()
                    self.clear_preview()
                    
                    self.statusBar().showMessage("ទិន្នន័យត្រូវបានលុបដោយជោគជ័យ", 3000)
                    
            except Exception as e:
                QMessageBox.critical(self, "កំហុស", f"មិនអាចលុបទិន្នន័យ:\n{str(e)}")
    
    def export_data(self):
        """Export data to CSV"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "រក្សាទុកឯកសារទិន្នន័យ",
                f"ទិន្នន័យ_អត្រានុកូលដ្ឋាន_{datetime.now().strftime('%Y%m%d')}.csv",
                "ឯកសារ CSV (*.csv)"
            )
            
            if file_path:
                import csv
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    
                    # Write headers
                    writer.writerow([
                        "លេខរៀង", "ឈ្មោះ", "ភេទ", "ប្រភេទឯកសារ", 
                        "ភូមិ", "ឯកសារ", "កាលបរិច្ឆេទចុះឈ្មោះ"
                    ])
                    
                    # Write data
                    self.db_cursor.execute("""
                        SELECT serial_number, name, gender, document_type, village, 
                               document_photo, registration_date
                        FROM tax_payers 
                        ORDER BY id
                    """)
                    
                    for row in self.db_cursor.fetchall():
                        # Extract filename from path
                        file_path = row[5]
                        file_name = os.path.basename(file_path) if file_path else "មិនមាន"
                        writer.writerow([row[0], row[1], row[2], row[3], row[4], file_name, row[6]])
                
                QMessageBox.information(self, "ជោគជ័យ", 
                    f"ទិន្នន័យត្រូវបានបញ្ចេញដោយជោគជ័យ\n\nទីតាំង: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចបញ្ចេញទិន្នន័យ:\n{str(e)}")
    
    def export_report(self):
        """Export report to CSV"""
        try:
            file_path, _ = QFileDialog.getSaveFileName(
                self, "រក្សាទុករបាយការណ៍",
                f"របាយការណ៍_អត្រានុកូលដ្ឋាន_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "ឯកសារ CSV (*.csv)"
            )
            
            if file_path:
                import csv
                with open(file_path, 'w', newline='', encoding='utf-8-sig') as file:
                    writer = csv.writer(file)
                    
                    # Write report header
                    writer.writerow(["របាយការណ៍អត្រានុកូលដ្ឋាន"])
                    writer.writerow([f"កាលបរិច្ឆេទ: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"])
                    writer.writerow([f"អ្នកបង្កើត: អ្នកគ្រប់គ្រងប្រព័ន្ធ"])
                    writer.writerow([])
                    
                    # Write statistics
                    stats = self.get_statistics()
                    writer.writerow(["ស្ថិតិទិន្នន័យ"])
                    writer.writerow(["សរុបអ្នកបង់ប្រាក់:", f"{stats['total']} នាក់"])
                    writer.writerow(["ប្រុស:", f"{stats['male']} នាក់"])
                    writer.writerow(["ស្រី:", f"{stats['female']} នាក់"])
                    writer.writerow(["ភូមិសកម្ម:", f"{stats['villages']} ភូមិ"])
                    writer.writerow(["បានបញ្ជូលថ្ងៃនេះ:", f"{stats['today']} នាក់"])
                    writer.writerow([])
                    
                    # Write village distribution
                    writer.writerow(["ការបែងចែកតាមភូមិ"])
                    self.db_cursor.execute("""
                        SELECT village, COUNT(*) as count 
                        FROM tax_payers 
                        GROUP BY village 
                        ORDER BY count DESC
                    """)
                    
                    writer.writerow(["ភូមិ", "ចំនួន", "ភាគរយ"])
                    
                    total = stats['total']
                    for village, count in self.db_cursor.fetchall():
                        percentage = (count / total * 100) if total > 0 else 0
                        writer.writerow([village, f"{count} នាក់", f"{percentage:.1f}%"])
                    
                    writer.writerow([])
                    
                    # Write gender distribution
                    writer.writerow(["ការបែងចែកតាមភេទ"])
                    male_percent = (stats['male'] / total * 100) if total > 0 else 0
                    female_percent = (stats['female'] / total * 100) if total > 0 else 0
                    
                    writer.writerow(["ប្រុស:", f"{stats['male']} នាក់", f"{male_percent:.1f}%"])
                    writer.writerow(["ស្រី:", f"{stats['female']} នាក់", f"{female_percent:.1f}%"])
                
                QMessageBox.information(self, "ជោគជ័យ", 
                    f"របាយការណ៍ត្រូវបានបញ្ចេញដោយជោគជ័យ\n\nទីតាំង: {file_path}")
                
        except Exception as e:
            QMessageBox.critical(self, "កំហុស", f"មិនអាចបញ្ចេញរបាយការណ៍:\n{str(e)}")
    
    def get_statistics(self):
        """Get statistics from database"""
        stats = {
            'total': 0, 'male': 0, 'female': 0, 
            'villages': 0, 'doc_types': 0, 'today': 0
        }
        
        try:
            # Total count
            self.db_cursor.execute("SELECT COUNT(*) FROM tax_payers")
            stats['total'] = self.db_cursor.fetchone()[0]
            
            # Male count
            self.db_cursor.execute("SELECT COUNT(*) FROM tax_payers WHERE gender = 'ប្រុស'")
            stats['male'] = self.db_cursor.fetchone()[0]
            
            # Female count
            self.db_cursor.execute("SELECT COUNT(*) FROM tax_payers WHERE gender = 'ស្រី'")
            stats['female'] = self.db_cursor.fetchone()[0]
            
            # Active villages count
            self.db_cursor.execute("SELECT COUNT(DISTINCT village) FROM tax_payers")
            stats['villages'] = self.db_cursor.fetchone()[0]
            
            # Document types count
            self.db_cursor.execute("SELECT COUNT(DISTINCT document_type) FROM tax_payers")
            stats['doc_types'] = self.db_cursor.fetchone()[0]
            
            # Today's registrations
            self.db_cursor.execute("""
                SELECT COUNT(*) FROM tax_payers 
                WHERE DATE(registration_date) = DATE('now')
            """)
            stats['today'] = self.db_cursor.fetchone()[0]
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            
        return stats
    
    # ================ Navigation Methods ================
    
    def show_input_tab(self):
        """Show input tab"""
        self.tab_widget.setCurrentIndex(1)
    
    def show_view_tab(self):
        """Show view tab"""
        self.load_table_data()
        self.tab_widget.setCurrentIndex(2)
    
    def show_report_tab(self):
        """Show report tab"""
        self.tab_widget.setCurrentIndex(3)
    
    def show_settings(self):
        """Show settings dialog"""
        settings_dialog = SettingsDialog(self)
        settings_dialog.exec_()
    
    def show_user_profile(self):
        """Show user profile dialog"""
        # Get current user data
        user_data = {
            'username': 'admin',
            'fullname': 'អ្នកគ្រប់គ្រង',
            'email': 'admin@example.com',
            'phone': '012 345 678',
            'role': 'អ្នកគ្រប់គ្រង',
            'join_date': '2024-01-01',
            'data_entered': self.get_statistics()['total'],
            'last_active': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        profile_dialog = UserProfileDialog(user_data, self)
        profile_dialog.exec_()
    
    def show_help(self):
        """Show help dialog"""
        QMessageBox.information(self, "ជំនួយ", 
            "កម្មវិធីគ្រប់គ្រងអត្រានុកូលដ្ឋាន\n\n"
            "មុខងារសំខាន់ៗ:\n"
            "1. 📝 បញ្ជូលទិន្នន័យថ្មី\n"
            "2. 👁️ មើល និងកែសម្រួលទិន្នន័យ\n"
            "3. 📈 របាយការណ៍ស្ថិតិ\n"
            "4. ⚙️ ការកំណត់ប្រព័ន្ធ\n\n"
            "សម្រាប់ជំនួយបន្ថែម សូមទាក់ទង:\n"
            "ទូរស័ព្ទ: 012 345 678\n"
            "អ៊ីមែល: support@example.com")
    
    def closeEvent(self, event):
        """Clean up on close"""
        try:
            if hasattr(self, 'conn'):
                self.conn.close()
        except:
            pass
        event.accept()

def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create and show main window
    window = AdministrativeManagementApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()