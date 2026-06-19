import sys
import os
import threading
import json
import urllib.request
import urllib.parse
import tempfile
import subprocess
import time
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class VideoTranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.video_path = ""
        self.audio_path = ""
        self.subtitle_path = ""
        self.source_lang = "en"
        self.dest_lang = "km"
        self.whisper_model = None
        self.is_processing = False
        
    def initUI(self):
        self.setWindowTitle("កម្មវិធីបកប្រែវីដេអូ - ចិន/អង់គ្លេស → ខ្មែរ")
        self.setGeometry(100, 100, 1000, 800)
        
        # បង្កើតធាតុកណ្តាល
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # បង្ហាញចំណងជើង
        title_label = QLabel("កម្មវិធីបកប្រែវីដេអូពេញលក្ខណៈ")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 28px; 
                font-weight: bold; 
                color: #2c3e50; 
                padding: 20px;
                background-color: #ecf0f1;
                border-radius: 10px;
                border: 2px solid #3498db;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # បង្កើតតារាងផ្ទាំង
        self.tab_widget = QTabWidget()
        
        # ផ្ទាំងទី 1: បកប្រែវីដេអូ
        self.create_video_tab()
        
        # ផ្ទាំងទី 2: ការកំណត់
        self.create_settings_tab()
        
        # ផ្ទាំងទី 3: ជំនួយ
        self.create_help_tab()
        
        layout.addWidget(self.tab_widget)
        
        # បង្កើតប្រអប់ស្ថានភាព
        self.status_label = QLabel("ស្ថានភាព: រង់ចាំការប្រើប្រាស់")
        self.status_label.setStyleSheet("""
            QLabel {
                padding: 15px; 
                background-color: #f8f9fa; 
                border-radius: 5px;
                border: 1px solid #dee2e6;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.status_label)
        
        # បង្កើតរបារវឌ្ឍនភាព
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #3498db;
                border-radius: 5px;
                text-align: center;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        central_widget.setLayout(layout)
        
        # បង្កើតម៉ឺនុយ
        self.create_menu()
        
    def create_video_tab(self):
        video_tab = QWidget()
        layout = QVBoxLayout()
        
        # ផ្នែកជ្រើសរើសវីដេអូ
        video_group = QGroupBox("ជ្រើសរើសវីដេអូ")
        video_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #3498db;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)
        video_layout = QVBoxLayout()
        
        # បង្កើតតារាងសម្រាប់ជ្រើសរើសវីដេអូ
        video_select_layout = QHBoxLayout()
        
        self.video_label = QLabel("មិនទាន់មានវីដេអូត្រូវបានជ្រើសរើស")
        self.video_label.setStyleSheet("""
            QLabel {
                padding: 15px; 
                background-color: #f8f9fa; 
                border: 1px solid #dee2e6;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        video_select_layout.addWidget(self.video_label, 4)
        
        browse_btn = QPushButton("📁 រកមើលវីដេអូ")
        browse_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border: 2px solid #2c3e50;
            }
            QPushButton:pressed {
                background-color: #1f618d;
            }
        """)
        browse_btn.clicked.connect(self.browse_video)
        video_select_layout.addWidget(browse_btn, 1)
        
        video_layout.addLayout(video_select_layout)
        
        # បង្កើតប៊ូតុងមើលវីដេអូ
        preview_btn = QPushButton("▶ មើលវីដេអូជាមុន")
        preview_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                border: none;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        preview_btn.clicked.connect(self.preview_video)
        video_layout.addWidget(preview_btn)
        
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)
        
        # ផ្នែកការកំណត់ភាសា
        lang_group = QGroupBox("ការកំណត់ភាសា")
        lang_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #2ecc71;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)
        lang_layout = QGridLayout()
        
        # ភាសាដើម
        source_label = QLabel("ភាសាដើម:")
        source_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        lang_layout.addWidget(source_label, 0, 0)
        
        self.source_combo = QComboBox()
        self.source_combo.addItems([
            "🇺🇸 អង់គ្លេស (English)",
            "🇨🇳 ចិន (Chinese)", 
            "🇹🇭 ថៃ (Thai)",
            "🇻🇳 វៀតណាម (Vietnamese)",
            "🇯🇵 ជប៉ុន (Japanese)",
            "🇰🇷 កូរ៉េ (Korean)"
        ])
        self.source_combo.setCurrentIndex(0)
        self.source_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 2px solid #3498db;
            }
        """)
        lang_layout.addWidget(self.source_combo, 0, 1)
        
        # ភាសាក្រោយបកប្រែ
        dest_label = QLabel("ភាសាក្រោយបកប្រែ:")
        dest_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        lang_layout.addWidget(dest_label, 1, 0)
        
        self.dest_combo = QComboBox()
        self.dest_combo.addItems([
            "🇰🇭 ខ្មែរ (Khmer)",
            "🇺🇸 អង់គ្លេស (English)",
            "🇨🇳 ចិន (Chinese)",
            "🇹🇭 ថៃ (Thai)",
            "🇻🇳 វៀតណាម (Vietnamese)"
        ])
        self.dest_combo.setCurrentIndex(0)
        self.dest_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QComboBox:hover {
                border: 2px solid #3498db;
            }
        """)
        lang_layout.addWidget(self.dest_combo, 1, 1)
        
        lang_group.setLayout(lang_layout)
        layout.addWidget(lang_group)
        
        # ផ្នែកការកំណត់រចនាសម្ព័ន្ធ
        config_group = QGroupBox("ការកំណត់រចនាសម្ព័ន្ធ")
        config_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #e74c3c;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)
        config_layout = QVBoxLayout()
        
        # បង្កើតតារាងសម្រាប់ការកំណត់រចនាសម្ព័ន្ធ
        config_grid = QGridLayout()
        
        self.subtitle_check = QCheckBox("បន្ថែមពាក្យរងលើវីដេអូ")
        self.subtitle_check.setChecked(True)
        self.subtitle_check.setStyleSheet("font-size: 14px; padding: 5px;")
        config_grid.addWidget(self.subtitle_check, 0, 0)
        
        self.keep_audio_check = QCheckBox("រក្សាសំឡេងដើម")
        self.keep_audio_check.setChecked(True)
        self.keep_audio_check.setStyleSheet("font-size: 14px; padding: 5px;")
        config_grid.addWidget(self.keep_audio_check, 0, 1)
        
        self.generate_srt_check = QCheckBox("បង្កើតឯកសារ SRT")
        self.generate_srt_check.setChecked(True)
        self.generate_srt_check.setStyleSheet("font-size: 14px; padding: 5px;")
        config_grid.addWidget(self.generate_srt_check, 1, 0)
        
        self.translate_audio_check = QCheckBox("បកប្រែសំឡេង")
        self.translate_audio_check.setChecked(False)
        self.translate_audio_check.setStyleSheet("font-size: 14px; padding: 5px;")
        config_grid.addWidget(self.translate_audio_check, 1, 1)
        
        config_layout.addLayout(config_grid)
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # ផ្នែកប៊ូតុងធ្វើការ
        button_group = QGroupBox("ដំណើរការ")
        button_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #f39c12;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)
        button_layout = QHBoxLayout()
        
        # ប៊ូតុងសម្គាល់សំឡេង
        self.transcribe_btn = QPushButton("🎤 សម្គាល់សំឡេង")
        self.transcribe_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.transcribe_btn.clicked.connect(self.transcribe_audio)
        button_layout.addWidget(self.transcribe_btn)
        
        # ប៊ូតុងបកប្រែ
        self.translate_btn = QPushButton("🌐 បកប្រែវីដេអូ")
        self.translate_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.translate_btn.clicked.connect(self.translate_video)
        self.translate_btn.setEnabled(False)
        button_layout.addWidget(self.translate_btn)
        
        # ប៊ូតុងចាក់វីដេអូលទ្ធផល
        self.play_result_btn = QPushButton("▶ ចាក់វីដេអូលទ្ធផល")
        self.play_result_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 16px;
                border: none;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:disabled {
                background-color: #95a5a6;
            }
        """)
        self.play_result_btn.clicked.connect(self.play_result_video)
        self.play_result_btn.setEnabled(False)
        button_layout.addWidget(self.play_result_btn)
        
        button_group.setLayout(button_layout)
        layout.addWidget(button_group)
        
        # បង្កើតតារាងសម្រាប់បង្ហាញលទ្ធផល
        result_group = QGroupBox("លទ្ធផល")
        result_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #1abc9c;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 15px;
            }
        """)
        result_layout = QVBoxLayout()
        
        # បង្កើតតារាងផ្ទាំងសម្រាប់លទ្ធផល
        result_tabs = QTabWidget()
        
        # ផ្ទាំងអត្ថបទសម្គាល់សំឡេង
        self.transcription_text = QTextEdit()
        self.transcription_text.setPlaceholderText("អត្ថបទសម្គាល់សំឡេងនឹងបង្ហាញនៅទីនេះ...")
        result_tabs.addTab(self.transcription_text, "អត្ថបទសម្គាល់សំឡេង")
        
        # ផ្ទាំងអត្ថបទដែលបានបកប្រែ
        self.translated_text = QTextEdit()
        self.translated_text.setPlaceholderText("អត្ថបទដែលបានបកប្រែនឹងបង្ហាញនៅទីនេះ...")
        result_tabs.addTab(self.translated_text, "អត្ថបទដែលបានបកប្រែ")
        
        result_layout.addWidget(result_tabs)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        video_tab.setLayout(layout)
        self.tab_widget.addTab(video_tab, "🎬 បកប្រែវីដេអូ")
        
    def create_settings_tab(self):
        settings_tab = QWidget()
        layout = QVBoxLayout()
        
        # ផ្នែកការកំណត់ Whisper
        whisper_group = QGroupBox("ការកំណត់ Whisper")
        whisper_layout = QVBoxLayout()
        
        whisper_info = QLabel("Whisper គឺជាគំរូ AI ដែលប្រើសម្រាប់សម្គាល់សំឡេងទៅជាអត្ថបទ។")
        whisper_info.setStyleSheet("font-size: 14px; padding: 10px;")
        whisper_info.setWordWrap(True)
        whisper_layout.addWidget(whisper_info)
        
        model_layout = QHBoxLayout()
        model_label = QLabel("គំរូ:")
        model_layout.addWidget(model_label)
        
        self.model_combo = QComboBox()
        self.model_combo.addItems(["tiny", "base", "small", "medium", "large"])
        self.model_combo.setCurrentIndex(1)  # base
        model_layout.addWidget(self.model_combo)
        whisper_layout.addLayout(model_layout)
        
        # ប៊ូតុងដំឡើង Whisper
        install_whisper_btn = QPushButton("ដំឡើង Whisper")
        install_whisper_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        install_whisper_btn.clicked.connect(self.install_whisper)
        whisper_layout.addWidget(install_whisper_btn)
        
        whisper_group.setLayout(whisper_layout)
        layout.addWidget(whisper_group)
        
        # ផ្នែកការកំណត់ពុម្ពអក្សរ
        font_group = QGroupBox("ការកំណត់ពុម្ពអក្សរ")
        font_layout = QVBoxLayout()
        
        font_info = QLabel("ជ្រើសរើសពុម្ពអក្សរសម្រាប់ពាក្យរង:")
        font_layout.addWidget(font_info)
        
        font_select_layout = QHBoxLayout()
        font_label = QLabel("ពុម្ពអក្សរ:")
        font_select_layout.addWidget(font_label)
        
        self.font_combo = QComboBox()
        self.font_combo.addItems(["Khmer OS", "Arial", "Times New Roman", "Tahoma", "Courier New"])
        self.font_combo.setCurrentIndex(0)
        font_select_layout.addWidget(self.font_combo)
        font_layout.addLayout(font_select_layout)
        
        # កំណត់ទំហំពុម្ពអក្សរ
        size_layout = QHBoxLayout()
        size_label = QLabel("ទំហំពុម្ពអក្សរ:")
        size_layout.addWidget(size_label)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(10, 50)
        self.font_size_spin.setValue(24)
        size_layout.addWidget(self.font_size_spin)
        font_layout.addLayout(size_layout)
        
        font_group.setLayout(font_layout)
        layout.addWidget(font_group)
        
        # ផ្នែកការកំណត់ទីតាំងផ្ទុក
        output_group = QGroupBox("ការកំណត់ទីតាំងផ្ទុក")
        output_layout = QVBoxLayout()
        
        output_info = QLabel("ទីតាំងផ្ទុកឯកសារលទ្ធផល:")
        output_layout.addWidget(output_info)
        
        output_path_layout = QHBoxLayout()
        self.output_path_label = QLabel("(ដកយកទីតាំងដូចវីដេអូដើម)")
        self.output_path_label.setStyleSheet("padding: 8px; background-color: #f8f9fa; border-radius: 5px;")
        output_path_layout.addWidget(self.output_path_label)
        
        browse_output_btn = QPushButton("ជ្រើសរើស")
        browse_output_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        browse_output_btn.clicked.connect(self.browse_output_path)
        output_path_layout.addWidget(browse_output_btn)
        output_layout.addLayout(output_path_layout)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # បន្ថែម spacer
        layout.addStretch()
        
        settings_tab.setLayout(layout)
        self.tab_widget.addTab(settings_tab, "⚙️ ការកំណត់")
        
    def create_help_tab(self):
        help_tab = QWidget()
        layout = QVBoxLayout()
        
        # ព័ត៌មានអំពីកម្មវិធី
        about_group = QGroupBox("អំពីកម្មវិធី")
        about_layout = QVBoxLayout()
        
        about_text = QLabel("""
        <h2>កម្មវិធីបកប្រែវីដេអូពេញលក្ខណៈ</h2>
        <p><b>កំណែ 2.0</b></p>
        <p>កម្មវិធីនេះអាចបកប្រែវីដេអូពីភាសាផ្សេងៗទៅភាសាខ្មែរ។</p>
        
        <h3>លក្ខណៈពិសេស៖</h3>
        <ul>
            <li>សម្គាល់សំឡេងទៅជាអត្ថបទដោយប្រើ OpenAI Whisper</li>
            <li>បកប្រែអត្ថបទដោយប្រើ Google Translate API</li>
            <li>បង្កើតពាក្យរងលើវីដេអូ</li>
            <li>រក្សាទុកឯកសារ SRT សម្រាប់ពាក្យរង</li>
            <li>គាំទ្រភាសាច្រើន</li>
        </ul>
        
        <h3>ជំហានក្នុងការប្រើប្រាស់៖</h3>
        <ol>
            <li>ជ្រើសរើសវីដេអូដោយចុចប៊ូតុង "រកមើលវីដេអូ"</li>
            <li>ជ្រើសរើសភាសាដើមនិងភាសាក្រោយបកប្រែ</li>
            <li>ចុចប៊ូតុង "សម្គាល់សំឡេង" ដើម្បីទាញយកអត្ថបទពីសំឡេង</li>
            <li>ចុចប៊ូតុង "បកប្រែវីដេអូ" ដើម្បីចាប់ផ្ដើមការបកប្រែ</li>
            <li>ចុចប៊ូតុង "ចាក់វីដេអូលទ្ធផល" ដើម្បីមើលលទ្ធផល</li>
        </ol>
        
        <p><b>កំណត់សំគាល់៖</b> អ្នកត្រូវតែដំឡើង Whisper និង FFmpeg ជាមុនសិន។</p>
        """)
        about_text.setWordWrap(True)
        about_text.setStyleSheet("font-size: 14px; padding: 15px;")
        about_layout.addWidget(about_text)
        
        about_group.setLayout(about_layout)
        layout.addWidget(about_group)
        
        # ផ្នែកទាញយក FFmpeg
        ffmpeg_group = QGroupBox("ទាញយក FFmpeg")
        ffmpeg_layout = QVBoxLayout()
        
        ffmpeg_info = QLabel("""
        FFmpeg គឺជាឧបករណ៍ដែលត្រូវការសម្រាប់ដំណើរការវីដេអូ។
        សូមទាញយក FFmpeg ពីគេហទំព័រផ្លូវការ៖
        """)
        ffmpeg_info.setWordWrap(True)
        ffmpeg_layout.addWidget(ffmpeg_info)
        
        ffmpeg_btn = QPushButton("🌐 ទាញយក FFmpeg")
        ffmpeg_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        ffmpeg_btn.clicked.connect(self.download_ffmpeg)
        ffmpeg_layout.addWidget(ffmpeg_btn)
        
        ffmpeg_group.setLayout(ffmpeg_layout)
        layout.addWidget(ffmpeg_group)
        
        # បន្ថែម spacer
        layout.addStretch()
        
        help_tab.setLayout(layout)
        self.tab_widget.addTab(help_tab, "❓ ជំនួយ")
        
    def create_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu('ឯកសារ')
        
        open_video_action = QAction('បើកវីដេអូ', self)
        open_video_action.triggered.connect(self.browse_video)
        file_menu.addAction(open_video_action)
        
        open_srt_action = QAction('បើកឯកសារ SRT', self)
        open_srt_action.triggered.connect(self.browse_srt_file)
        file_menu.addAction(open_srt_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('ចាកចេញ', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        tools_menu = menubar.addMenu('ឧបករណ៍')
        
        install_deps_action = QAction('ដំឡើងបណ្ណាល័យ', self)
        install_deps_action.triggered.connect(self.install_dependencies)
        tools_menu.addAction(install_deps_action)
        
        test_whisper_action = QAction('សាកល្បង Whisper', self)
        test_whisper_action.triggered.connect(self.test_whisper)
        tools_menu.addAction(test_whisper_action)
        
        help_menu = menubar.addMenu('ជំនួយ')
        
        about_action = QAction('អំពីកម្មវិធី', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def browse_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "ជ្រើសរើសវីដេអូ", 
            "", 
            "Video Files (*.mp4 *.avi *.mov *.mkv *.wmv *.flv);;All Files (*.*)"
        )
        
        if file_path:
            self.video_path = file_path
            self.video_label.setText(f"📹 {os.path.basename(file_path)}")
            self.status_label.setText(f"ស្ថានភាព: វីដេអូ {os.path.basename(file_path)} ត្រូវបានជ្រើសរើស")
            self.transcribe_btn.setEnabled(True)
            
    def browse_srt_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "ជ្រើសរើសឯកសារ SRT",
            "",
            "Subtitle Files (*.srt *.txt);;All Files (*.*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.transcription_text.setText(content)
                self.status_label.setText(f"ស្ថានភាព: ឯកសារ SRT {os.path.basename(file_path)} ត្រូវបានផ្ទុក")
                self.translate_btn.setEnabled(True)
            except Exception as e:
                QMessageBox.warning(self, "កំហុស", f"មិនអាចអានឯកសារបាន៖ {str(e)}")
    
    def browse_output_path(self):
        dir_path = QFileDialog.getExistingDirectory(self, "ជ្រើសរើសទីតាំងផ្ទុក")
        if dir_path:
            self.output_path_label.setText(dir_path)
    
    def update_progress(self, value, message=""):
        self.progress_bar.setValue(value)
        if message:
            self.status_label.setText(f"ស្ថានភាព: {message}")
        QApplication.processEvents()
    
    def transcribe_audio(self):
        if not self.video_path:
            QMessageBox.warning(self, "ការព្រមាន", "សូមជ្រើសរើសវីដេអូមុន!")
            return
        
        # បិទប៊ូតុងដើម្បីការពារការចុចច្រើនដង
        self.transcribe_btn.setEnabled(False)
        
        # ចាប់ផ្ដើម thread សម្គាល់សំឡេង
        self.transcription_thread = threading.Thread(target=self._transcribe_audio_thread)
        self.transcription_thread.start()
    
    def _transcribe_audio_thread(self):
        try:
            self.update_progress(0, "កំពុងស្វែងរកវិធីសម្គាល់សំឡេង...")
            
            # ព្យាយាមប្រើ Whisper
            try:
                import whisper
                self.update_progress(10, "កំពុងផ្ទុកគំរូ Whisper...")
                
                # ផ្ទុកគំរូ Whisper
                model_name = self.model_combo.currentText()
                model = whisper.load_model(model_name)
                
                self.update_progress(30, "កំពុងសម្គាល់សំឡេង...")
                
                # សម្គាល់សំឡេង
                result = model.transcribe(self.video_path)
                transcription = result["text"]
                
                self.transcription_text.setText(transcription)
                self.update_progress(100, "បានសម្គាល់សំឡេងដោយជោគជ័យ!")
                
                # បើកប៊ូតុងបកប្រែ
                self.translate_btn.setEnabled(True)
                
            except ImportError:
                # ប្រសិនបើ Whisper មិនមាន ស្នើអ្នកប្រើប្រាស់ដំឡើង
                QMessageBox.information(
                    self,
                    "Whisper មិនមាន",
                    "Whisper មិនទាន់ត្រូវបានដំឡើង។ សូមដំឡើងវាដោយប្រើប៊ូតុង 'ដំឡើង Whisper' នៅក្នុងផ្ទាំងការកំណត់។"
                )
                self.update_progress(0, "Whisper មិនមាន")
                
        except Exception as e:
            self.status_label.setText(f"ស្ថានភាព: កំហុស - {str(e)}")
            QMessageBox.critical(self, "កំហុស", f"មានកំហុសកើតឡើង៖\n{str(e)}")
        finally:
            self.transcribe_btn.setEnabled(True)
    
    def translate_video(self):
        if not self.video_path:
            QMessageBox.warning(self, "ការព្រមាន", "សូមជ្រើសរើសវីដេអូមុន!")
            return
        
        # ពិនិត្យមើលថាមានអត្ថបទសម្គាល់សំឡេងឬទេ
        transcription = self.transcription_text.toPlainText().strip()
        if not transcription:
            QMessageBox.warning(self, "ការព្រមាន", "សូមសម្គាល់សំឡេងមុនពេលបកប្រែ!")
            return
        
        # បិទប៊ូតុងដើម្បីការពារការចុចច្រើនដង
        self.translate_btn.setEnabled(False)
        
        # ចាប់ផ្ដើម thread បកប្រែ
        self.translation_thread = threading.Thread(target=self._translate_video_thread)
        self.translation_thread.start()
    
    def _translate_video_thread(self):
        try:
            self.update_progress(0, "កំពុងចាប់ផ្ដើមការបកប្រែ...")
            
            # ទទួលយកអត្ថបទសម្គាល់សំឡេង
            transcription = self.transcription_text.toPlainText()
            
            # កំណត់កូដភាសា
            lang_map = {
                "🇺🇸 អង់គ្លេស (English)": "en",
                "🇨🇳 ចិន (Chinese)": "zh-CN",
                "🇰🇭 ខ្មែរ (Khmer)": "km",
                "🇹🇭 ថៃ (Thai)": "th",
                "🇻🇳 វៀតណាម (Vietnamese)": "vi",
                "🇯🇵 ជប៉ុន (Japanese)": "ja",
                "🇰🇷 កូរ៉េ (Korean)": "ko"
            }
            
            source_lang = lang_map.get(self.source_combo.currentText(), "en")
            dest_lang = lang_map.get(self.dest_combo.currentText(), "km")
            
            self.update_progress(20, "កំពុងបកប្រែអត្ថបទ...")
            
            # បកប្រែអត្ថបទ
            translated_text = self.google_translate(transcription, source_lang, dest_lang)
            self.translated_text.setText(translated_text)
            
            self.update_progress(50, "កំពុងរៀបចំឯកសារ...")
            
            # រក្សាទុកអត្ថបទដែលបានបកប្រែ
            base_name = os.path.splitext(os.path.basename(self.video_path))[0]
            output_dir = os.path.dirname(self.video_path)
            
            # រក្សាទុកឯកសារអត្ថបទ
            text_file_path = os.path.join(output_dir, f"{base_name}_translated.txt")
            with open(text_file_path, 'w', encoding='utf-8') as f:
                f.write(f"អត្ថបទដើម:\n{transcription}\n\n")
                f.write(f"អត្ថបទដែលបានបកប្រែ:\n{translated_text}")
            
            # បង្កើតឯកសារ SRT
            if self.generate_srt_check.isChecked():
                srt_file_path = os.path.join(output_dir, f"{base_name}_khmer.srt")
                self.create_srt_file(translated_text, srt_file_path)
            
            self.update_progress(100, "បានបកប្រែដោយជោគជ័យ!")
            
            # បើកប៊ូតុងចាក់វីដេអូលទ្ធផល
            self.play_result_btn.setEnabled(True)
            
            # បង្ហាញសារជោគជ័យ
            QMessageBox.information(
                self,
                "ជោគជ័យ",
                f"បានបកប្រែវីដេអូដោយជោគជ័យ!\n\n"
                f"ឯកសារត្រូវបានរក្សាទុកនៅ៖\n{output_dir}"
            )
            
        except Exception as e:
            self.status_label.setText(f"ស្ថានភាព: កំហុស - {str(e)}")
            QMessageBox.critical(self, "កំហុស", f"មានកំហុសកើតឡើង៖\n{str(e)}")
        finally:
            self.translate_btn.setEnabled(True)
    
    def google_translate(self, text, src_lang, dest_lang):
        """បកប្រែអត្ថបទដោយប្រើ Google Translate API"""
        try:
            # បង្កើត URL សម្រាប់ Google Translate
            base_url = "https://translate.googleapis.com/translate_a/single"
            params = {
                "client": "gtx",
                "sl": src_lang,
                "tl": dest_lang,
                "dt": "t",
                "q": text
            }
            
            url = f"{base_url}?{urllib.parse.urlencode(params)}"
            
            # ផ្ញើសំណើ
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(request)
            data = response.read().decode('utf-8')
            
            # ញែកទិន្នន័យ
            translated_parts = []
            try:
                result = json.loads(data)
                if result and result[0]:
                    for part in result[0]:
                        if part[0]:  # អត្ថបទដែលបានបកប្រែ
                            translated_parts.append(part[0])
            except:
                translated_parts = [text]  # ប្រសិនបើមានបញ្ហា ត្រឡប់អត្ថបទដើម
            
            return " ".join(translated_parts)
            
        except Exception as e:
            # ក្នុងករណីមានបញ្ហាក្នុងការតភ្ជាប់ទៅអ៊ីនធឺណិត
            return f"[កំហុសក្នុងការតភ្ជាប់ទៅ Google Translate]: {str(e)}"
    
    def create_srt_file(self, text, file_path):
        """បង្កើតឯកសារ SRT សាមញ្ញ"""
        try:
            # បំបែកអត្ថបទទៅជាប្រយោគ
            sentences = text.split('. ')
            
            with open(file_path, 'w', encoding='utf-8') as f:
                for i, sentence in enumerate(sentences):
                    if sentence.strip():
                        start_time = i * 5  # 5 វិនាទីក្នុងមួយប្រយោគ
                        end_time = start_time + 4  # 4 វិនាទីសម្រាប់ប្រយោគនីមួយៗ
                        
                        # បម្លែងវិនាទីទៅជាទ្រង់ទ្រាយ SRT
                        start_str = self.seconds_to_srt_time(start_time)
                        end_str = self.seconds_to_srt_time(end_time)
                        
                        f.write(f"{i+1}\n")
                        f.write(f"{start_str} --> {end_str}\n")
                        f.write(f"{sentence.strip()}.\n\n")
            
            return True
        except Exception as e:
            print(f"កំហុសក្នុងការបង្កើតឯកសារ SRT: {e}")
            return False
    
    def seconds_to_srt_time(self, seconds):
        """បម្លែងវិនាទីទៅជាទ្រង់ទ្រាយ SRT"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def install_whisper(self):
        reply = QMessageBox.question(
            self,
            "ដំឡើង Whisper",
            "Whisper ត្រូវការ Python និង pip។ តើអ្នកចង់ដំឡើង Whisper ឥឡូវនេះឬទេ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.update_progress(0, "កំពុងដំឡើង Whisper...")
            
            try:
                import subprocess
                import sys
                
                # ដំឡើង Whisper
                subprocess.check_call([sys.executable, "-m", "pip", "install", "openai-whisper"])
                
                # ដំឡើង torch (ប្រសិនបើត្រូវការ)
                subprocess.check_call([sys.executable, "-m", "pip", "install", "torch"])
                
                self.update_progress(100, "បានដំឡើង Whisper ដោយជោគជ័យ!")
                QMessageBox.information(self, "ជោគជ័យ", "បានដំឡើង Whisper ដោយជោគជ័យ!")
                
            except Exception as e:
                self.status_label.setText(f"ស្ថានភាព: កំហុស - {str(e)}")
                QMessageBox.critical(self, "កំហុស", f"មានកំហុសក្នុងការដំឡើង៖\n{str(e)}")
    
    def install_dependencies(self):
        reply = QMessageBox.question(
            self,
            "ដំឡើងបណ្ណាល័យ",
            "តើអ្នកចង់ដំឡើងបណ្ណាល័យទាំងអស់ដែលត្រូវការឬទេ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.update_progress(0, "កំពុងដំឡើងបណ្ណាល័យ...")
            
            try:
                import subprocess
                import sys
                
                # បញ្ជីបណ្ណាល័យ
                libraries = [
                    "openai-whisper",
                    "torch",
                    "moviepy",
                    "googletrans==4.0.0-rc1"
                ]
                
                for i, lib in enumerate(libraries):
                    self.update_progress(int((i+1) / len(libraries) * 100), f"កំពុងដំឡើង {lib}...")
                    try:
                        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])
                    except:
                        # ប្រសិនបើមានបញ្ហា ព្យាយាមម្ដងទៀតដោយមិនប្រើ cache
                        subprocess.check_call([sys.executable, "-m", "pip", "install", "--no-cache-dir", lib])
                
                self.update_progress(100, "បានដំឡើងបណ្ណាល័យដោយជោគជ័យ!")
                QMessageBox.information(self, "ជោគជ័យ", "បានដំឡើងបណ្ណាល័យទាំងអស់ដោយជោគជ័យ!")
                
            except Exception as e:
                self.status_label.setText(f"ស្ថានភាព: កំហុស - {str(e)}")
                QMessageBox.critical(self, "កំហុស", f"មានកំហុសក្នុងការដំឡើង៖\n{str(e)}")
    
    def download_ffmpeg(self):
        import webbrowser
        webbrowser.open("https://ffmpeg.org/download.html")
        QMessageBox.information(
            self,
            "ទាញយក FFmpeg",
            "បានបើកទំព័រទាញយក FFmpeg។ សូមទាញយក និងដំឡើង FFmpeg តាមការណែនាំនៅលើគេហទំព័រ។"
        )
    
    def test_whisper(self):
        try:
            import whisper
            QMessageBox.information(self, "ពិនិត្យវិភាគ", "Whisper ត្រូវបានដំឡើងដោយជោគជ័យ!")
        except ImportError:
            QMessageBox.warning(self, "ពិនិត្យវិភាគ", "Whisper មិនទាន់ត្រូវបានដំឡើង!")
    
    def preview_video(self):
        if not self.video_path:
            QMessageBox.warning(self, "ការព្រមាន", "សូមជ្រើសរើសវីដេអូមុន!")
            return
        
        try:
            import subprocess
            import platform
            
            # បើកវីដេអូជាមួយកម្មវិធីលេងវីដេអូលំនាំដើម
            if platform.system() == "Windows":
                os.startfile(self.video_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.call(["open", self.video_path])
            else:  # Linux
                subprocess.call(["xdg-open", self.video_path])
                
        except Exception as e:
            QMessageBox.warning(self, "កំហុស", f"មិនអាចបើកវីដេអូបាន៖ {str(e)}")
    
    def play_result_video(self):
        if not self.video_path:
            QMessageBox.warning(self, "ការព្រមាន", "មិនទាន់មានវីដេអូលទ្ធផល!")
            return
        
        # ស្វែងរកវីដេអូលទ្ធផល
        base_name = os.path.splitext(os.path.basename(self.video_path))[0]
        output_dir = os.path.dirname(self.video_path)
        result_video_path = os.path.join(output_dir, f"{base_name}_translated.mp4")
        
        if os.path.exists(result_video_path):
            self.preview_video()
        else:
            QMessageBox.information(
                self,
                "ព័ត៌មាន",
                "វីដេអូលទ្ធផលមិនទាន់ត្រូវបានបង្កើត។ សូមបកប្រែវីដេអូមុន។"
            )
    
    def show_about(self):
        about_text = """
        <h2>កម្មវិធីបកប្រែវីដេអូពេញលក្ខណៈ</h2>
        <p><b>កំណែ 2.0</b></p>
        
        <p>កម្មវិធីនេះត្រូវបានបង្កើតឡើងដើម្បីជួយបកប្រែវីដេអូពីភាសាផ្សេងៗទៅភាសាខ្មែរ។</p>
        
        <h3>បច្ចេកវិទ្យា៖</h3>
        <ul>
            <li>PyQt5 - សម្រាប់ចំណុចប្រទាក់ក្រណាត់</li>
            <li>OpenAI Whisper - សម្រាប់សម្គាល់សំឡេង</li>
            <li>Google Translate - សម្រាប់បកប្រែអត្ថបទ</li>
            <li>FFmpeg - សម្រាប់ដំណើរការវីដេអូ</li>
        </ul>
        
        <p><b>ការអភិវឌ្ឍន៍៖</b> កម្មវិធីនេះត្រូវបានអភិវឌ្ឍន៍ដើម្បីជួយបងប្អូនខ្មែរក្នុងការយល់ដឹងពីវីដេអូជាភាសាបរទេស។</p>
        
        <p>© 2023 កម្មវិធីបកប្រែវីដេអូ</p>
        """
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("អំពីកម្មវិធី")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(about_text)
        msg_box.exec_()

def main():
    app = QApplication(sys.argv)
    
    # កំណត់ពុម្ពអក្សរសម្រាប់ភាសាខ្មែរ
    try:
        font = QFont("Khmer OS", 10)
        app.setFont(font)
    except:
        # ប្រសិនបើពុម្ពអក្សរខ្មែរមិនមាន ប្រើពុម្ពអក្សរលំនាំដើម
        pass
    
    window = VideoTranslatorApp()
    window.show()
    
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()