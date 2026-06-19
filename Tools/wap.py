import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *

class WeddingWebsiteApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('គេហទំព័រអាពាហ៍ពិពាហ៍ - Wedding Website')
        self.setGeometry(100, 100, 1200, 700)
        
        # បង្កើត widget កណ្តាល
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # បង្កើត layout ផ្តេក
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        
        # បង្កើត sidebar សម្រាប់ម៉ីនុយ
        self.create_sidebar(main_layout)
        
        # បង្កើត web view
        self.web_view = QWebEngineView()
        main_layout.addWidget(self.web_view, 1)
        
        # បង្កើតគេហទំព័រដំបូង
        self.create_wedding_website()
        
        # បង្ហាញទំព័រដំបូង
        self.load_home_page()
        
    def create_sidebar(self, main_layout):
        # បង្កើត sidebar widget
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #8B4513;
                border-right: 2px solid #654321;
            }
            QPushButton {
                background-color: #D2691E;
                color: white;
                border: none;
                padding: 15px;
                margin: 5px;
                border-radius: 5px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
            QPushButton:pressed {
                background-color: #8B4513;
            }
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                qproperty-alignment: AlignCenter;
            }
        """)
        
        # Layout បញ្ឈរ
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar.setLayout(sidebar_layout)
        
        # ចំណងជើង
        title = QLabel("ម៉ីនុយអាពាហ៍ពិពាហ៍")
        sidebar_layout.addWidget(title)
        
        # បង្កើតប៊ូតុងម៉ីនុយ
        btn_new = QPushButton("បង្កើតថ្មី")
        btn_new.clicked.connect(self.create_new_wedding)
        sidebar_layout.addWidget(btn_new)
        
        btn_register = QPushButton("កត់ចំណងដៃ")
        btn_register.clicked.connect(self.register_marriage)
        sidebar_layout.addWidget(btn_register)
        
        btn_digital = QPushButton("បង្កើតសំបុត្រឌីជីថល")
        btn_digital.clicked.connect(self.create_digital_invitation)
        sidebar_layout.addWidget(btn_digital)
        
        btn_settings = QPushButton("កំណត់")
        btn_settings.clicked.connect(self.open_settings)
        sidebar_layout.addWidget(btn_settings)
        
        btn_home = QPushButton("ទំព័រដើម")
        btn_home.clicked.connect(self.load_home_page)
        sidebar_layout.addWidget(btn_home)
        
        # បន្ថែមទំហំរីក
        sidebar_layout.addStretch()
        
        # បន្ថែម sidebar ទៅ layout សំខាន់
        main_layout.addWidget(sidebar)
        
    def create_wedding_website(self):
        # បង្កើតថតសម្រាប់ផ្ទុកឯកសារ website
        if not os.path.exists("wedding_website"):
            os.makedirs("wedding_website")
        
        # បង្កើតឯកសារ HTML សំខាន់
        html_content = """
        <!DOCTYPE html>
        <html lang="km">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>គេហទំព័រអាពាហ៍ពិពាហ៍</title>
            <style>
                :root {
                    --primary: #8B4513;
                    --secondary: #D2691E;
                    --accent: #FFD700;
                    --light: #FFF8DC;
                }
                
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Battambang', 'Khmer OS', sans-serif;
                }
                
                body {
                    background-color: #FFF8DC;
                    color: #333;
                    line-height: 1.6;
                }
                
                header {
                    background: linear-gradient(to right, #8B4513, #D2691E);
                    color: white;
                    padding: 20px 0;
                    text-align: center;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }
                
                .header-content {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 0 20px;
                }
                
                h1 {
                    font-size: 2.5rem;
                    margin-bottom: 10px;
                }
                
                .subtitle {
                    font-size: 1.2rem;
                    opacity: 0.9;
                }
                
                .main-container {
                    max-width: 1200px;
                    margin: 30px auto;
                    padding: 0 20px;
                }
                
                .section {
                    background: white;
                    border-radius: 10px;
                    padding: 30px;
                    margin-bottom: 30px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
                    border-left: 5px solid var(--secondary);
                }
                
                h2 {
                    color: var(--primary);
                    margin-bottom: 20px;
                    padding-bottom: 10px;
                    border-bottom: 2px dashed var(--accent);
                }
                
                .couple-info {
                    display: flex;
                    justify-content: space-around;
                    flex-wrap: wrap;
                    gap: 30px;
                    margin-top: 30px;
                }
                
                .person {
                    text-align: center;
                    flex: 1;
                    min-width: 250px;
                }
                
                .person-img {
                    width: 200px;
                    height: 200px;
                    border-radius: 50%;
                    object-fit: cover;
                    border: 5px solid var(--secondary);
                    margin-bottom: 15px;
                }
                
                .person-name {
                    font-size: 1.5rem;
                    color: var(--primary);
                    margin-bottom: 5px;
                }
                
                .event-details {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                    gap: 20px;
                    margin-top: 20px;
                }
                
                .event-card {
                    background: var(--light);
                    padding: 20px;
                    border-radius: 8px;
                    text-align: center;
                }
                
                .event-icon {
                    font-size: 2.5rem;
                    color: var(--secondary);
                    margin-bottom: 10px;
                }
                
                .btn {
                    display: inline-block;
                    background: var(--secondary);
                    color: white;
                    padding: 12px 30px;
                    border-radius: 50px;
                    text-decoration: none;
                    font-weight: bold;
                    margin-top: 10px;
                    border: none;
                    cursor: pointer;
                    transition: all 0.3s;
                }
                
                .btn:hover {
                    background: var(--primary);
                    transform: translateY(-3px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }
                
                footer {
                    background: var(--primary);
                    color: white;
                    text-align: center;
                    padding: 20px;
                    margin-top: 50px;
                }
                
                .gallery {
                    display: grid;
                    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                    gap: 15px;
                    margin-top: 20px;
                }
                
                .gallery-img {
                    width: 100%;
                    height: 150px;
                    object-fit: cover;
                    border-radius: 8px;
                    transition: transform 0.3s;
                }
                
                .gallery-img:hover {
                    transform: scale(1.05);
                }
                
                @media (max-width: 768px) {
                    .couple-info {
                        flex-direction: column;
                        align-items: center;
                    }
                    
                    h1 {
                        font-size: 1.8rem;
                    }
                }
            </style>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        </head>
        <body>
            <header>
                <div class="header-content">
                    <h1>អបអរសាទរ អាពាហ៍ពិពាហ៍</h1>
                    <p class="subtitle">សូមទទួលការអញ្ជើញចូលរួមពីយើងខ្ញុំ</p>
                </div>
            </header>
            
            <div class="main-container">
                <section class="section">
                    <h2><i class="fas fa-heart"></i> អំពីគូស្វាមីភរិយា</h2>
                    <div class="couple-info">
                        <div class="person">
                            <img src="https://i.pravatar.cc/200?img=5" alt="ខាងប្រុស" class="person-img">
                            <h3 class="person-name">សុខ សំអាត</h3>
                            <p>កូនច្បងគ្រួសារ លោក សុខ សំណាង និង លោកស្រី មាន សុភមង្គល</p>
                        </div>
                        
                        <div class="person">
                            <div style="font-size: 3rem; color: #D2691E;">&</div>
                        </div>
                        
                        <div class="person">
                            <img src="https://i.pravatar.cc/200?img=8" alt="ខាងស្រី" class="person-img">
                            <h3 class="person-name">ស្រី សិរីមង្គល</h3>
                            <p>កូនច្បងគ្រួសារ លោក ស្រី សុខសាន្ត និង លោកស្រី ពិសិដ្ឋ សុខចិត្ត</p>
                        </div>
                    </div>
                </section>
                
                <section class="section">
                    <h2><i class="fas fa-calendar-alt"></i> ព័ត៌មានអំពីពិធី</h2>
                    <div class="event-details">
                        <div class="event-card">
                            <div class="event-icon"><i class="fas fa-church"></i></div>
                            <h3>ពិធីមង្គលការនៅវត្ត</h3>
                            <p><strong>កាលបរិច្ឆេទ:</strong> ១៥ កក្កដា ២០២៤</p>
                            <p><strong>ម៉ោង:</strong> ៧:០០ព្រឹក</p>
                            <p><strong>ទីតាំង:</strong> វត្តឧណ្ណាលោម</p>
                        </div>
                        
                        <div class="event-card">
                            <div class="event-icon"><i class="fas fa-utensils"></i></div>
                            <h3>ពិធីរាប់ាអាហារពិសេស</h3>
                            <p><strong>កាលបរិច្ឆេទ:</strong> ១៥ កក្កដា ២០២៤</p>
                            <p><strong>ម៉ោង:</strong> ១២:០០ថ្ងៃត្រង់</p>
                            <p><strong>ទីតាំង:</strong> សាលរោងអាពាហ៍ពិពាហ៍ ទួលគោក</p>
                        </div>
                    </div>
                </section>
                
                <section class="section">
                    <h2><i class="fas fa-images"></i> វិចិត្រសាលរូបថត</h2>
                    <div class="gallery">
                        <img src="https://images.unsplash.com/photo-1511285560929-80b456fea0bc?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80" alt="រូបថត ១" class="gallery-img">
                        <img src="https://images.unsplash.com/photo-1465495976277-4387d4b0e4a6?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80" alt="រូបថត ២" class="gallery-img">
                        <img src="https://images.unsplash.com/photo-1511988617509-a57c8a288659?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80" alt="រូបថត ៣" class="gallery-img">
                        <img src="https://images.unsplash.com/photo-1537633552985-df8429e8048b?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=80" alt="រូបថត ៤" class="gallery-img">
                    </div>
                </section>
                
                <section class="section">
                    <h2><i class="fas fa-gift"></i> ការចូលរួមរបស់អ្នក</h2>
                    <p>សូមអញ្ជើញអ្នកទាំងអស់គ្នាចូលរួមពិធីមង្គលការរបស់យើងខ្ញុំ។ ការមកដល់របស់អ្នកគឺជាការគាំទ្រដ៏ធំធេងសម្រាប់យើងខ្ញុំ។</p>
                    <button class="btn" onclick="alert('សូមអរគុណសម្រាប់ការបញ្ជាក់ចូលរួម!')">បញ្ជាក់ចូលរួម</button>
                    <button class="btn" onclick="alert('សូមអរគុណសម្រាប់ការផ្ញើសារអបអរសាទរ!')">ផ្ញើសារអបអរសាទរ</button>
                </section>
            </div>
            
            <footer>
                <p>សូមអរគុណចំពោះការជួយឧបត្ថម្ភ និងការជួយដឹកនាំពីឪពុកម្តាយ សាច់សាលោហិត និងមិត្តភក្តិទាំងអស់គ្នា។</p>
                <p>ទំនាក់ទំនង៖ ០១២ ៣៤៥ ៦៧៨ | អ៊ីមែល៖ wedding@example.com</p>
                <p>© ២០២៤ គេហទំព័រអាពាហ៍ពិពាហ៍។ រក្សាសិទ្ធិគ្រប់យ៉ាង។</p>
            </footer>
            
            <script>
                // JavaScript សម្រាប់គេហទំព័រ
                document.addEventListener('DOMContentLoaded', function() {
                    // បន្ថែមឥទ្ធិពលពេលចុចប៊ូតុង
                    const buttons = document.querySelectorAll('.btn');
                    buttons.forEach(button => {
                        button.addEventListener('click', function() {
                            this.style.transform = 'scale(0.95)';
                            setTimeout(() => {
                                this.style.transform = '';
                            }, 200);
                        });
                    });
                    
                    // បង្ហាញកាលបរិច្ឆេទបច្ចុប្បន្ន
                    const now = new Date();
                    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
                    const dateString = now.toLocaleDateString('km-KH', options);
                    
                    // បង្កើតធាតុសម្រាប់បង្ហាញកាលបរិច្ឆេទ
                    const dateElement = document.createElement('p');
                    dateElement.textContent = `ថ្ងៃនេះ៖ ${dateString}`;
                    dateElement.style.textAlign = 'center';
                    dateElement.style.marginTop = '10px';
                    dateElement.style.color = '#8B4513';
                    dateElement.style.fontWeight = 'bold';
                    
                    document.querySelector('footer').appendChild(dateElement);
                });
            </script>
        </body>
        </html>
        """
        
        # សរសេរឯកសារ HTML
        with open("wedding_website/index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        # បង្កើតទំព័រផ្សេងទៀត
        self.create_other_pages()
        
    def create_other_pages(self):
        # ទំព័រកត់ចំណងដៃ
        register_content = """
        <!DOCTYPE html>
        <html lang="km">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>កត់ចំណងដៃ</title>
            <style>
                body {
                    font-family: 'Battambang', 'Khmer OS', sans-serif;
                    background-color: #FFF8DC;
                    padding: 20px;
                    color: #333;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }
                h1 {
                    color: #8B4513;
                    text-align: center;
                    margin-bottom: 30px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                label {
                    display: block;
                    margin-bottom: 5px;
                    font-weight: bold;
                    color: #555;
                }
                input, select, textarea {
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 16px;
                }
                .row {
                    display: flex;
                    gap: 20px;
                }
                .row .form-group {
                    flex: 1;
                }
                .btn {
                    background: #D2691E;
                    color: white;
                    padding: 12px 30px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    display: block;
                    margin: 30px auto 0;
                }
                .btn:hover {
                    background: #8B4513;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>ទម្រង់កត់ត្រាចំណងដៃ</h1>
                <form id="marriageForm">
                    <div class="row">
                        <div class="form-group">
                            <label for="groomName">ឈ្មោះខាងប្រុស</label>
                            <input type="text" id="groomName" required>
                        </div>
                        <div class="form-group">
                            <label for="brideName">ឈ្មោះខាងស្រី</label>
                            <input type="text" id="brideName" required>
                        </div>
                    </div>
                    
                    <div class="row">
                        <div class="form-group">
                            <label for="weddingDate">កាលបរិច្ឆេទរៀបអាពាហ៍ពិពាហ៍</label>
                            <input type="date" id="weddingDate" required>
                        </div>
                        <div class="form-group">
                            <label for="location">ទីតាំង</label>
                            <input type="text" id="location" required>
                        </div>
                    </div>
                    
                    <div class="form-group">
                        <label for="witnesses">ឈ្មោះសាក្សី (ដាច់ពីគ្នាដោយក្បៀស)</label>
                        <textarea id="witnesses" rows="3"></textarea>
                    </div>
                    
                    <div class="form-group">
                        <label for="notes">កំណត់ចំណាំបន្ថែម</label>
                        <textarea id="notes" rows="4"></textarea>
                    </div>
                    
                    <button type="submit" class="btn">រក្សាទុកការកត់ត្រា</button>
                </form>
            </div>
            
            <script>
                document.getElementById('marriageForm').addEventListener('submit', function(e) {
                    e.preventDefault();
                    alert('ការកត់ត្រាចំណងដៃត្រូវបានរក្សាទុកដោយជោគជ័យ!');
                });
            </script>
        </body>
        </html>
        """
        
        with open("wedding_website/register.html", "w", encoding="utf-8") as f:
            f.write(register_content)
            
        # ទំព័របង្កើតសំបុត្រឌីជីថល
        digital_content = """
        <!DOCTYPE html>
        <html lang="km">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>សំបុត្រអញ្ជើញឌីជីថល</title>
            <style>
                body {
                    font-family: 'Battambang', 'Khmer OS', sans-serif;
                    background-color: #FFF8DC;
                    padding: 20px;
                    color: #333;
                }
                .container {
                    max-width: 1000px;
                    margin: 0 auto;
                }
                h1 {
                    color: #8B4513;
                    text-align: center;
                    margin-bottom: 30px;
                }
                .invitation-card {
                    background: white;
                    border-radius: 10px;
                    padding: 40px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                    border: 2px solid #D2691E;
                    position: relative;
                    margin-bottom: 30px;
                }
                .invitation-header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .invitation-header h2 {
                    color: #8B4513;
                    font-size: 2rem;
                    margin-bottom: 10px;
                }
                .couple-names {
                    font-size: 2.5rem;
                    color: #D2691E;
                    margin: 20px 0;
                    font-weight: bold;
                }
                .details {
                    margin: 30px 0;
                    line-height: 1.8;
                }
                .detail-item {
                    margin-bottom: 15px;
                    font-size: 1.1rem;
                }
                .actions {
                    text-align: center;
                    margin-top: 40px;
                }
                .btn {
                    background: #D2691E;
                    color: white;
                    padding: 12px 30px;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    margin: 0 10px;
                    display: inline-block;
                }
                .btn:hover {
                    background: #8B4513;
                }
                .customize-panel {
                    background: white;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0 5px 15px rgba(0,0,0,0.05);
                    margin-top: 30px;
                }
                .customize-panel h3 {
                    color: #8B4513;
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>បង្កើតសំបុត្រអញ្ជើញឌីជីថល</h1>
                
                <div class="invitation-card" id="invitationCard">
                    <div class="invitation-header">
                        <h2>សំបុត្រអញ្ជើញចូលរួមពិធីអាពាហ៍ពិពាហ៍</h2>
                        <div class="couple-names">សុខ សំអាត & ស្រី សិរីមង្គល</div>
                        <p>សូមអញ្ជើញអ្នកទាំងអស់គ្នាចូលរួមពិធីមង្គលការរបស់យើងខ្ញុំ</p>
                    </div>
                    
                    <div class="details">
                        <div class="detail-item"><strong>កាលបរិច្ឆេទ:</strong> ១៥ កក្កដា ២០២៤</div>
                        <div class="detail-item"><strong>ម៉ោង:</strong> ៧:០០ព្រឹក (ពិធីមង្គលការនៅវត្ត)</div>
                        <div class="detail-item"><strong>ទីតាំងវត្ត:</strong> វត្តឧណ្ណាលោម</div>
                        <div class="detail-item"><strong>ម៉ោងរាប់ាអាហារ:</strong> ១២:០០ថ្ងៃត្រង់</div>
                        <div class="detail-item"><strong>ទីតាំងរាប់ាអាហារ:</strong> សាលរោងអាពាហ៍ពិពាហ៍ ទួលគោក</div>
                    </div>
                    
                    <div class="actions">
                        <p>សូមអរគុណសម្រាប់ការមកដល់របស់អ្នក!</p>
                    </div>
                </div>
                
                <div class="customize-panel">
                    <h3>ការកំណត់ផ្ទាល់ខ្លួន</h3>
                    <div class="form-group">
                        <label>ឈ្មោះគូរៀបអាពាហ៍ពិពាហ៍:</label>
                        <input type="text" id="coupleNames" value="សុខ សំអាត & ស្រី សិរីមង្គល" style="width: 100%; padding: 10px; margin: 10px 0;">
                    </div>
                    <div class="form-group">
                        <label>កាលបរិច្ឆេទ:</label>
                        <input type="text" id="weddingDate" value="១៥ កក្កដា ២០២៤" style="width: 100%; padding: 10px; margin: 10px 0;">
                    </div>
                    <button class="btn" onclick="updateInvitation()">អាប់ដេតសំបុត្រ</button>
                    <button class="btn" onclick="printInvitation()">បោះពុម្ពសំបុត្រ</button>
                    <button class="btn" onclick="shareInvitation()">ចែករំលែកសំបុត្រ</button>
                </div>
            </div>
            
            <script>
                function updateInvitation() {
                    const coupleNames = document.getElementById('coupleNames').value;
                    const weddingDate = document.getElementById('weddingDate').value;
                    
                    document.querySelector('.couple-names').textContent = coupleNames;
                    document.querySelector('.detail-item:nth-child(1)').innerHTML = `<strong>កាលបរិច្ឆេទ:</strong> ${weddingDate}`;
                    
                    alert('សំបុត្រត្រូវបានអាប់ដេតដោយជោគជ័យ!');
                }
                
                function printInvitation() {
                    window.print();
                }
                
                function shareInvitation() {
                    alert('សំបុត្រត្រូវបានចែករំលែកដោយជោគជ័យ! (មុខងារនេះនឹងដំណើរការនៅលើម៉ាស៊ីនជាក់ស្តែង)');
                }
            </script>
        </body>
        </html>
        """
        
        with open("wedding_website/digital.html", "w", encoding="utf-8") as f:
            f.write(digital_content)
    
    # មុខងារប្រតិបត្តិការម៉ីនុយ
    def create_new_wedding(self):
        QMessageBox.information(self, "បង្កើតថ្មី", "ការបង្កើតអាពាហ៍ពិពាហ៍ថ្មីត្រូវបានបើក!")
        self.web_view.setHtml("""
        <html>
        <body style="font-family: 'Khmer OS'; padding: 20px; background-color: #FFF8DC;">
            <h1 style="color: #8B4513;">បង្កើតអាពាហ៍ពិពាហ៍ថ្មី</h1>
            <p>នៅទីនេះអ្នកអាចបង្កើតអាពាហ៍ពិពាហ៍ថ្មី។ សូមបំពេញព័ត៌មានខាងក្រោម៖</p>
            <ul>
                <li>ឈ្មោះខាងប្រុស និងខាងស្រី</li>
                <li>កាលបរិច្ឆេទអាពាហ៍ពិពាហ៍</li>
                <li>ទីតាំង</li>
                <li>ព័ត៌មានលម្អិតផ្សេងៗ</li>
            </ul>
        </body>
        </html>
        """)
    
    def register_marriage(self):
        file_path = os.path.abspath("wedding_website/register.html")
        self.web_view.setUrl(QUrl.fromLocalFile(file_path))
    
    def create_digital_invitation(self):
        file_path = os.path.abspath("wedding_website/digital.html")
        self.web_view.setUrl(QUrl.fromLocalFile(file_path))
    
    def open_settings(self):
        QMessageBox.information(self, "កំណត់", "ផ្នែកកំណត់ត្រូវបានបើក!")
        self.web_view.setHtml("""
        <html>
        <body style="font-family: 'Khmer OS'; padding: 20px; background-color: #FFF8DC;">
            <h1 style="color: #8B4513;">ការកំណត់គេហទំព័រអាពាហ៍ពិពាហ៍</h1>
            <p>នៅទីនេះអ្នកអាចកំណត់រចនាសម្ព័ន្ធនានាសម្រាប់គេហទំព័រ៖</p>
            <ul>
                <li>ការកំណត់រូបរាង</li>
                <li>ការកំណត់ភាសា</li>
                <li>ការកំណត់សិទ្ធិអ្នកប្រើប្រាស់</li>
                <li>ការគ្រប់គ្រងទិន្នន័យ</li>
            </ul>
        </body>
        </html>
        """)
    
    def load_home_page(self):
        file_path = os.path.abspath("wedding_website/index.html")
        self.web_view.setUrl(QUrl.fromLocalFile(file_path))

def main():
    app = QApplication(sys.argv)
    window = WeddingWebsiteApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()