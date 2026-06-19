# run.py
import sys
import os

def main():
    """រត់កម្មវិធី"""
    print("=" * 60)
    print("ប្រព័ន្ធគ្រប់គ្រងការលក់សម្ភារៈសិក្សា")
    print("=" * 60)
    
    # ពិនិត្យមើលថាតើមាន PyQt5 ឬអត់
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QFont
    except ImportError:
        print("❌ សូមដំឡើង PyQt5 ជាមុនសិន:")
        print("   pip install PyQt5")
        sys.exit(1)
    
    # ពិនិត្យមើល database
    try:
        from database_manager import DatabaseManager
        print("🔄 កំពុងភ្ជាប់ database...")
        db = DatabaseManager('study_materials.db')
        db.close()
        print("✅ ភ្ជាប់ database រួចរាល់")
    except Exception as e:
        print(f"❌ មិនអាចភ្ជាប់ database: {e}")
        sys.exit(1)
    
    # រត់កម្មវិធី
    print("🚀 កំពុងបើកដំណើរការកម្មវិធី...")
    print("=" * 60)
    
    from main import main as run_main
    run_main()

if __name__ == "__main__":
    main()