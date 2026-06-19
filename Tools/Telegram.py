import sys
import os
import re
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from gtts import gTTS  # Online Google TTS
import pygame  # For audio playback
from threading import Thread
import tempfile
import time
import json
import random

class TextToSpeechApp(QMainWindow):
    # Define signals for thread communication
    conversion_completed_signal = pyqtSignal(str)
    conversion_failed_signal = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.current_language = "km"  # Default to Khmer
        self.audio_file = None
        self.is_playing = False
        self.voice_settings = self.load_voice_settings()
        
        # Connect signals to slots
        self.conversion_completed_signal.connect(self.conversion_completed)
        self.conversion_failed_signal.connect(self.conversion_failed)
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            self.pygame_available = True
        except:
            self.pygame_available = False
            print("Pygame mixer initialization failed. Audio playback may not work.")
        
    def load_voice_settings(self):
        """Load default voice settings"""
        return {
            "pitch_variation": 0,  # -10 to 10
            "emphasis_level": 3,   # 1 to 5
            "pause_duration": 0.3, # seconds
            "add_emotions": False,
            "voice_style": "neutral"  # neutral, cheerful, serious, storytelling
        }
        
    def initUI(self):
        self.setWindowTitle('កម្មវិធីបំលែងអក្សរទៅជាសម្លេង (កំណែពិសេស)')
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333;
            }
            QTextEdit {
                font-size: 14px;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
            }
            QPushButton {
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
                border: none;
                min-width: 120px;
            }
            QComboBox {
                font-size: 14px;
                padding: 8px;
                border: 2px solid #2196F3;
                border-radius: 5px;
                background-color: white;
            }
            QSlider {
                height: 30px;
            }
            QSlider::groove:horizontal {
                height: 8px;
                background: #ddd;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #4CAF50;
                width: 24px;
                margin: -8px 0;
                border-radius: 12px;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #607D8B;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel('កម្មវិធីបំលែងអក្សរទៅជាសម្លេង - កំណែពិសេស')
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #2E7D32;
            padding: 15px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                stop:0 #4CAF50, stop:1 #2E7D32);
            color: white;
            border-radius: 8px;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label)
        
        # Language selection
        lang_layout = QHBoxLayout()
        lang_label = QLabel('ជ្រើសរើសភាសា:')
        lang_label.setStyleSheet("color: #1565C0;")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems([
            "ខ្មែរ (Khmer)", 
            "អង់គ្លេស (English - US)", 
            "អង់គ្លេស (English - UK)", 
            "ថៃ (Thai)", 
            "វៀតណាម (Vietnamese)",
            "ចិន (Chinese)",
            "ជប៉ុន (Japanese)",
            "ហ៊្វីលីពីន (Filipino)",
            "ឥណ្ឌូនេស៊ី (Indonesian)",
            "ម៉ាឡេស៊ី (Malay)",
            "កូរ៉េ (Korean)",
            "បារាំង (French)",
            "អេស្ប៉ាញ (Spanish)"
        ])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(lang_label)
        lang_layout.addWidget(self.lang_combo)
        lang_layout.addStretch()
        main_layout.addLayout(lang_layout)
        
        # Text input area
        input_group = QGroupBox("បញ្ចូលអក្សរ")
        input_layout = QVBoxLayout()
        
        input_label = QLabel('បញ្ចូលអក្សរដែលអ្នកចង់បំលែង:')
        input_label.setStyleSheet("color: #D84315;")
        input_layout.addWidget(input_label)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText('''សូមបញ្ចូលអក្សរនៅទីនេះ...

ឧទាហរណ៍:
សួស្តី! តើអ្នកសុខសប្បាយជាទេ?
ខ្ញុំជាកម្មវិធីបំលែងអក្សរទៅជាសម្លេង។
ខ្ញុំអាចនិយាយជាភាសាផ្សេងៗជាច្រើន។

គន្លឹះសម្រាប់សម្លេងកាន់តែពិសេស:
• ប្រើសញ្ញាសំគាល់ (!) សម្រាប់ពាក្យសំខាន់
• ប្រើសញ្ញាសួរ (?) សម្រាប់ប្រយោគសួរ
• ប្រើចំណុច (...) សម្រាប់ការបញ្ឈប់ខ្លី
• ប្រើបន្ទាត់ថ្មីសម្រាប់ការសំដែងផ្សេងៗ''')
        self.text_input.setMinimumHeight(150)
        
        # Add text formatting buttons
        format_layout = QHBoxLayout()
        bold_btn = QPushButton("B")
        bold_btn.setToolTip("ពាក្យសំខាន់ (ដាក់អក្សរដិត)")
        bold_btn.clicked.connect(lambda: self.format_text("**", "**"))
        italic_btn = QPushButton("I")
        italic_btn.setToolTip("ពាក្យប្លែក (ដាក់អក្សរផ្តេក)")
        italic_btn.clicked.connect(lambda: self.format_text("*", "*"))
        pause_btn = QPushButton("...")
        pause_btn.setToolTip("បន្ថែមការបញ្ឈប់")
        pause_btn.clicked.connect(lambda: self.insert_text("... "))
        emphasis_btn = QPushButton("!")
        emphasis_btn.setToolTip("បន្ថែមការសង្កត់សង្កិន")
        emphasis_btn.clicked.connect(lambda: self.insert_text("! "))
        
        for btn in [bold_btn, italic_btn, pause_btn, emphasis_btn]:
            btn.setMaximumWidth(40)
            btn.setStyleSheet("background-color: #E0E0E0;")
            format_layout.addWidget(btn)
        
        format_layout.addStretch()
        input_layout.addLayout(format_layout)
        input_layout.addWidget(self.text_input)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Voice settings - Advanced
        settings_group = QGroupBox("ការកំណត់សម្លេងពិសេស")
        settings_layout = QGridLayout()
        
        # Row 1
        # Voice speed
        speed_label = QLabel('ល្បឿនសម្លេង:')
        self.speed_combo = QComboBox()
        self.speed_combo.addItems(["លឿនណាស់", "លឿន", "ធម្មតា", "យឺត", "យឺតណាស់"])
        self.speed_combo.setCurrentIndex(2)
        settings_layout.addWidget(speed_label, 0, 0)
        settings_layout.addWidget(self.speed_combo, 0, 1)
        
        # Voice style
        style_label = QLabel('ស្ទីលសម្លេង:')
        self.style_combo = QComboBox()
        self.style_combo.addItems(["ធម្មតា", "រីករាយ", "សំដីរឿង", "យ៉ាងសំខាន់", "គួរអោយចាប់អារម្មណ៍"])
        settings_layout.addWidget(style_label, 0, 2)
        settings_layout.addWidget(self.style_combo, 0, 3)
        
        # Row 2
        # Pause duration
        pause_label = QLabel('រយៈពេលបញ្ឈប់:')
        self.pause_slider = QSlider(Qt.Horizontal)
        self.pause_slider.setRange(1, 10)  # 0.1 to 1.0 seconds
        self.pause_slider.setValue(3)
        self.pause_label_value = QLabel('0.3s')
        settings_layout.addWidget(pause_label, 1, 0)
        settings_layout.addWidget(self.pause_slider, 1, 1)
        settings_layout.addWidget(self.pause_label_value, 1, 2)
        
        # Emphasis level
        emphasis_label = QLabel('កម្រិតសង្កត់សង្កិន:')
        self.emphasis_slider = QSlider(Qt.Horizontal)
        self.emphasis_slider.setRange(1, 5)
        self.emphasis_slider.setValue(3)
        self.emphasis_label_value = QLabel('កម្រិត 3')
        settings_layout.addWidget(emphasis_label, 1, 3)
        settings_layout.addWidget(self.emphasis_slider, 1, 4)
        settings_layout.addWidget(self.emphasis_label_value, 1, 5)
        
        # Row 3
        # Volume control
        volume_label = QLabel('កម្រិតសម្លេង:')
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(80)
        self.volume_slider.setTickPosition(QSlider.TicksBelow)
        self.volume_slider.setTickInterval(10)
        self.volume_label_value = QLabel('80%')
        settings_layout.addWidget(volume_label, 2, 0)
        settings_layout.addWidget(self.volume_slider, 2, 1, 1, 3)
        settings_layout.addWidget(self.volume_label_value, 2, 4)
        
        # Advanced features
        features_label = QLabel('មុខងារពិសេស:')
        self.emotion_check = QCheckBox('បន្ថែមអារម្មណ៍')
        self.pause_check = QCheckBox('បន្ថែមការបញ្ឈប់ដោយស្វ័យប្រវត្តិ')
        self.pause_check.setChecked(True)
        settings_layout.addWidget(features_label, 3, 0)
        settings_layout.addWidget(self.emotion_check, 3, 1)
        settings_layout.addWidget(self.pause_check, 3, 2)
        
        settings_group.setLayout(settings_layout)
        main_layout.addWidget(settings_group)
        
        # Connect signals
        self.pause_slider.valueChanged.connect(lambda v: self.pause_label_value.setText(f'{v/10:.1f}s'))
        self.emphasis_slider.valueChanged.connect(lambda v: self.emphasis_label_value.setText(f'កម្រិត {v}'))
        self.volume_slider.valueChanged.connect(lambda v: self.volume_label_value.setText(f'{v}%'))
        
        # Information label
        info_label = QLabel('💡 គន្លឹះ: ប្រើសញ្ញាពិសេស (!, ?, ...) ដើម្បីធ្វើឱ្យសម្លេងកាន់តែពិសេស។ កម្មវិធីនេះត្រូវការអ៊ីនធឺណិត។')
        info_label.setStyleSheet("""
            font-size: 12px;
            color: #5D4037;
            padding: 10px;
            background-color: #FFF3E0;
            border-radius: 5px;
            border: 1px solid #FFB74D;
        """)
        info_label.setWordWrap(True)
        main_layout.addWidget(info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.convert_btn = QPushButton('🎤 បំលែងអក្សរទៅសម្លេង')
        self.convert_btn.setStyleSheet("""
            background-color: #4CAF50; 
            color: white;
            font-size: 16px;
            padding: 12px;
            border-radius: 8px;
        """)
        self.convert_btn.clicked.connect(self.convert_text_to_speech)
        
        self.play_btn = QPushButton('▶ ចាក់សម្លេង')
        self.play_btn.setStyleSheet("""
            background-color: #2196F3; 
            color: white;
            padding: 10px;
        """)
        self.play_btn.clicked.connect(self.play_audio)
        self.play_btn.setEnabled(False)
        
        self.pause_btn = QPushButton('⏸ ផ្អាកសម្លេង')
        self.pause_btn.setStyleSheet("""
            background-color: #FF9800; 
            color: white;
            padding: 10px;
        """)
        self.pause_btn.clicked.connect(self.pause_audio)
        self.pause_btn.setEnabled(False)
        
        self.stop_btn = QPushButton('⏹ បញ្ឈប់សម្លេង')
        self.stop_btn.setStyleSheet("""
            background-color: #F44336; 
            color: white;
            padding: 10px;
        """)
        self.stop_btn.clicked.connect(self.stop_audio)
        self.stop_btn.setEnabled(False)
        
        self.save_btn = QPushButton('💾 រក្សាទុកសម្លេង')
        self.save_btn.setStyleSheet("""
            background-color: #9C27B0; 
            color: white;
            padding: 10px;
        """)
        self.save_btn.clicked.connect(self.save_audio)
        self.save_btn.setEnabled(False)
        
        self.clear_btn = QPushButton('🗑 លុបអក្សរ')
        self.clear_btn.setStyleSheet("""
            background-color: #607D8B; 
            color: white;
            padding: 10px;
        """)
        self.clear_btn.clicked.connect(self.clear_text)
        
        button_layout.addWidget(self.convert_btn)
        button_layout.addWidget(self.play_btn)
        button_layout.addWidget(self.pause_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.clear_btn)
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        # Preview area
        preview_group = QGroupBox("ការមើលជាមុន")
        preview_layout = QVBoxLayout()
        
        self.preview_label = QLabel('ស្ថានភាព: ត្រៀមខ្លួនរួចរាល់...')
        self.preview_label.setStyleSheet("""
            font-size: 12px;
            color: #666;
            padding: 5px;
            background-color: #E8F5E9;
            border-radius: 3px;
        """)
        preview_layout.addWidget(self.preview_label)
        
        preview_group.setLayout(preview_layout)
        main_layout.addWidget(preview_group)
        
        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage('ត្រៀមខ្លួនរួចរាល់។ សូមបញ្ចូលអក្សរនិងចុចបំលែង។')
        
    def format_text(self, start_tag, end_tag):
        cursor = self.text_input.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            cursor.insertText(f"{start_tag}{selected_text}{end_tag}")
        else:
            cursor.insertText(f"{start_tag}{end_tag}")
            
    def insert_text(self, text):
        cursor = self.text_input.textCursor()
        cursor.insertText(text)
        
    def clear_text(self):
        self.text_input.clear()
        self.preview_label.setText('ស្ថានភាព: អត្ថបទត្រូវបានលុប...')
        
    def change_language(self, index):
        # Map index to language codes
        lang_map = {
            0: "km",     # Khmer
            1: "en",     # English US
            2: "en",     # English UK
            3: "th",     # Thai
            4: "vi",     # Vietnamese
            5: "zh-CN",  # Chinese
            6: "ja",     # Japanese
            7: "tl",     # Filipino
            8: "id",     # Indonesian
            9: "ms",     # Malay
            10: "ko",    # Korean
            11: "fr",    # French
            12: "es"     # Spanish
        }
        self.current_language = lang_map.get(index, "km")
        
    def enhance_text_for_speech(self, text):
        """Enhance text with speech markers for better pronunciation"""
        enhanced_text = text
        
        # Add emphasis to words with **bold** markers
        enhanced_text = re.sub(r'\*\*(.*?)\*\*', r'**\1**', enhanced_text)
        
        # Add pauses for ...
        if self.pause_check.isChecked():
            pause_duration = self.pause_slider.value() / 10.0
            # We can't add SSML tags to gTTS, so we'll just add spaces for pauses
            enhanced_text = re.sub(r'\.{3,}', ' ... ', enhanced_text)
            
        # Add emotional markers based on punctuation
        if self.emotion_check.isChecked():
            # For gTTS, we can't add emotional markers directly
            # But we can adjust the text slightly
            enhanced_text = enhanced_text.replace('!', '! ')
            enhanced_text = enhanced_text.replace('?', '? ')
            
        return enhanced_text
        
    def convert_text_to_speech(self):
        text = self.text_input.toPlainText().strip()
        
        if not text:
            QMessageBox.warning(self, 'ការព្រមាន', 'សូមបញ្ចូលអក្សរមុននឹងបំលែង!')
            return
            
        self.status_bar.showMessage('កំពុងបំលែងអក្សរទៅជាសម្លេង...')
        self.preview_label.setText('កំពុងរៀបចំសម្លេងពិសេស...')
        self.convert_btn.setEnabled(False)
        QApplication.processEvents()
        
        # Run conversion in a separate thread
        self.conversion_thread = Thread(target=self.convert_thread, args=(text,))
        self.conversion_thread.daemon = True
        self.conversion_thread.start()
        
    def convert_thread(self, text):
        try:
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                temp_path = tmp.name
            
            # Enhance text for better speech
            enhanced_text = self.enhance_text_for_speech(text)
            
            # Determine speed setting
            speed_map = {
                0: 1.5,  # very fast
                1: 1.2,  # fast
                2: 1.0,  # normal
                3: 0.8,  # slow
                4: 0.6   # very slow
            }
            speed_index = self.speed_combo.currentIndex()
            speed_factor = speed_map.get(speed_index, 1.0)
            
            # For gTTS, we use slow parameter
            slow_speed = (speed_index >= 3)  # Slow if index is 3 or 4
            
            # Convert text to speech using gTTS
            tts = gTTS(text=enhanced_text, lang=self.current_language, slow=slow_speed)
            tts.save(temp_path)
            
            # Apply audio enhancements if pygame is available
            if self.pygame_available:
                self.apply_audio_enhancements(temp_path)
            
            # Emit signal to update UI
            self.conversion_completed_signal.emit(temp_path)
            
        except Exception as e:
            # Emit signal for error
            self.conversion_failed_signal.emit(str(e))
    
    def apply_audio_enhancements(self, audio_path):
        """Apply audio enhancements using pygame"""
        try:
            # Load audio
            pygame.mixer.music.load(audio_path)
            
            # Apply volume from slider
            volume = self.volume_slider.value() / 100.0
            pygame.mixer.music.set_volume(volume)
            
            # Note: More advanced audio processing would require additional libraries
            # like pydub or librosa for effects like reverb, echo, etc.
            
        except Exception as e:
            print(f"Audio enhancement error: {e}")
    
    def conversion_completed(self, file_path):
        self.audio_file = file_path
        self.play_btn.setEnabled(True)
        self.stop_btn.setEnabled(True)
        self.save_btn.setEnabled(True)
        self.convert_btn.setEnabled(True)
        self.status_bar.showMessage('បានបំលែងអក្សរទៅសម្លេងពិសេសរួចរាល់។')
        
        # Get file size
        try:
            file_size = os.path.getsize(file_path) / 1024
            self.preview_label.setText(f'ស្ថានភាព: ត្រៀមចាក់សម្លេង ({file_size:.1f} KB)')
        except:
            self.preview_label.setText('ស្ថានភាព: ត្រៀមចាក់សម្លេង')
        
        # Show success message with details
        text_length = len(self.text_input.toPlainText())
        QMessageBox.information(self, 'ជោគជ័យ', 
            f'បានបំលែងអក្សរទៅសម្លេងដោយជោគជ័យ!\n\n'
            f'ព័ត៌មានលម្អិត:\n'
            f'• ចំនួនអក្សរ: {text_length}\n'
            f'• ភាសា: {self.lang_combo.currentText()}\n'
            f'• ស្ទីល: {self.style_combo.currentText()}\n'
            f'• ល្បឿន: {self.speed_combo.currentText()}\n\n'
            f'ឥឡូវអ្នកអាចចាក់សម្លេងឬរក្សាទុកវា។')
        
    def conversion_failed(self, error_msg):
        QMessageBox.critical(self, 'កំហុស', 
            f'មិនអាចបំលែងអក្សរទៅសម្លេង: {error_msg}\n\n'
            f'សូមពិនិត្យ៖\n'
            f'1. ការភ្ជាប់អ៊ីនធឺណិត\n'
            f'2. អក្សរដែលបានបញ្ចូល\n'
            f'3. ភាសាដែលបានជ្រើសរើស')
        self.status_bar.showMessage('ការបំលែងមានកំហុស។')
        self.preview_label.setText('ស្ថានភាព: មានកំហុសក្នុងការបំលែង')
        self.convert_btn.setEnabled(True)
        
    def play_audio(self):
        if not self.pygame_available:
            QMessageBox.warning(self, 'ការព្រមាន', 'មិនអាចចាក់សម្លេងបានទេ។ Pygame mixer មិនអាចដំណើរការបាន។')
            return
            
        if self.audio_file and os.path.exists(self.audio_file):
            try:
                pygame.mixer.music.load(self.audio_file)
                
                # Set volume
                volume = self.volume_slider.value() / 100.0
                pygame.mixer.music.set_volume(volume)
                
                pygame.mixer.music.play()
                self.is_playing = True
                self.play_btn.setEnabled(False)
                self.pause_btn.setEnabled(True)
                self.stop_btn.setEnabled(True)
                self.status_bar.showMessage('កំពុងចាក់សម្លេងពិសេស...')
                self.preview_label.setText('ស្ថានភាព: កំពុងចាក់សម្លេង...')
                
                # Check when playback finishes
                QTimer.singleShot(100, self.check_playback)
                
            except Exception as e:
                QMessageBox.critical(self, 'កំហុស', f'មិនអាចចាក់សម្លេង: {str(e)}')
        else:
            QMessageBox.warning(self, 'ការព្រមាន', 'មិនមានឯកសារសម្លេងដែលអាចចាក់បានទេ!')
                
    def check_playback(self):
        if pygame.mixer.music.get_busy():
            QTimer.singleShot(100, self.check_playback)
        else:
            if self.is_playing:
                self.playback_finished()
                
    def playback_finished(self):
        self.is_playing = False
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.status_bar.showMessage('បញ្ចប់ការចាក់សម្លេង។')
        self.preview_label.setText('ស្ថានភាព: បញ្ចប់ការចាក់')
        
    def pause_audio(self):
        if not self.pygame_available:
            return
            
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False
            self.pause_btn.setText('▶ បន្តសម្លេង')
            self.status_bar.showMessage('បានផ្អាកសម្លេង។')
            self.preview_label.setText('ស្ថានភាព: ផ្អាក')
        else:
            pygame.mixer.music.unpause()
            self.is_playing = True
            self.pause_btn.setText('⏸ ផ្អាកសម្លេង')
            self.status_bar.showMessage('កំពុងចាក់សម្លេង...')
            self.preview_label.setText('ស្ថានភាព: កំពុងចាក់')
            
    def stop_audio(self):
        if not self.pygame_available:
            return
            
        pygame.mixer.music.stop()
        self.is_playing = False
        self.play_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)
        self.pause_btn.setText('⏸ ផ្អាកសម្លេង')
        self.status_bar.showMessage('បានបញ្ឈប់សម្លេង។')
        self.preview_label.setText('ស្ថានភាព: បញ្ឈប់')
        
    def save_audio(self):
        if not self.audio_file or not os.path.exists(self.audio_file):
            QMessageBox.warning(self, 'ការព្រមាន', 'មិនមានឯកសារសម្លេងដែលអាចរក្សាទុកបានទេ!')
            return
            
        # Set default filename with voice settings
        style = self.style_combo.currentText()
        speed = self.speed_combo.currentText()
        default_filename = f"សម្លេងពិសេស_{style}_{speed}_{time.strftime('%Y%m%d_%H%M%S')}.mp3"
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, 
            'រក្សាទុកឯកសារសម្លេងពិសេស',
            default_filename,
            "ឯកសារសម្លេង (*.mp3 *.wav);;ឯកសារទាំងអស់ (*.*)"
        )
        
        if file_path:
            try:
                import shutil
                shutil.copy2(self.audio_file, file_path)
                self.status_bar.showMessage(f'បានរក្សាទុក: {os.path.basename(file_path)}')
                
                # Show saved details
                file_size = os.path.getsize(file_path) / 1024
                QMessageBox.information(self, 'ជោគជ័យ', 
                    f'បានរក្សាទុកឯកសារសម្លេងពិសេសដោយជោគជ័យ!\n\n'
                    f'ព័ត៌មានសម្លេង៖\n'
                    f'• ទីតាំង: {file_path}\n'
                    f'• ទំហំ: {file_size:.1f} KB\n'
                    f'• ស្ទីល: {style}\n'
                    f'• ល្បឿន: {speed}')
                
            except Exception as e:
                QMessageBox.critical(self, 'កំហុស', f'មិនអាចរក្សាទុកឯកសារ: {str(e)}')

def install_required_packages():
    """Install required Python packages"""
    import subprocess
    import importlib
    
    required_packages = [
        ('PyQt5', 'PyQt5'),
        ('gtts', 'gtts'),
        ('pygame', 'pygame')
    ]
    
    print("កំពុងពិនិត្យនិងដំឡើងប៉ាក់កេចដែលត្រូវការ...")
    
    for package_name, import_name in required_packages:
        try:
            importlib.import_module(import_name)
            print(f"✓ {package_name} បានដំឡើងរួចរាល់")
        except ImportError:
            print(f"កំពុងដំឡើង {package_name}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
                print(f"✓ {package_name} បានដំឡើងដោយជោគជ័យ")
            except Exception as e:
                print(f"✗ មិនអាចដំឡើង {package_name}: {e}")
                return False
    return True

def main():
    # Install required packages
    if not install_required_packages():
        print("មានបញ្ហាក្នុងការដំឡើងប៉ាក់កេចដែលត្រូវការ។")
        response = input("តើអ្នកចង់បន្តដំណើរការកម្មវិធីទេ? (y/n): ")
        if response.lower() != 'y':
            return
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set application font
    font = QFont()
    font.setPointSize(10)
    app.setFont(font)
    
    # Create and show the main window
    window = TextToSpeechApp()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()