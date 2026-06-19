# database_manager.py
import sqlite3
import os
import shutil
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name='study_materials.db'):
        """
        ភ្ជាប់ SQLite Database ដោយស្វ័យប្រវត្តិ
        """
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """ភ្ជាប់ទៅកាន់ database"""
        try:
            # ពិនិត្យមើលថាតើឯកសារ database មានឬអត់
            db_exists = os.path.exists(self.db_name)
            
            # ភ្ជាប់ database
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            
            # កំណត់ឲ្យប្រើភាសាខ្មែរបាន
            self.cursor.execute("PRAGMA encoding = 'UTF-8'")
            
            # បើកប្រើ Foreign Key support
            self.cursor.execute("PRAGMA foreign_keys = ON")
            
            print(f"✅ ភ្ជាប់ database {self.db_name} រួចរាល់")
            
            # បង្កើតតារាងចាំបាច់
            self.create_tables()
            
        except sqlite3.Error as e:
            print(f"❌ មិនអាចភ្ជាប់ database បានទេ: {e}")
            raise e
    
    def create_tables(self):
        """បង្កើតតារាងទាំងអស់"""
        try:
            # តារាង products
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    category TEXT,
                    barcode TEXT UNIQUE,
                    cost_price REAL DEFAULT 0,
                    cost_currency TEXT DEFAULT 'USD',
                    selling_price REAL DEFAULT 0,
                    selling_currency TEXT DEFAULT 'USD',
                    stock INTEGER DEFAULT 0,
                    min_stock INTEGER DEFAULT 5,
                    description TEXT,
                    image_path TEXT,
                    taxable INTEGER DEFAULT 1,
                    discountable INTEGER DEFAULT 1,
                    active INTEGER DEFAULT 1,
                    created_at TEXT,
                    updated_at TEXT
                )
            ''')
            
            # តារាង sales
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sales (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT,
                    total_amount REAL,
                    payment_method TEXT,
                    currency TEXT DEFAULT 'USD',
                    received_amount REAL DEFAULT 0,
                    change_amount REAL DEFAULT 0,
                    customer_name TEXT,
                    customer_phone TEXT
                )
            ''')
            
            # តារាង sale_items
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS sale_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sale_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    price REAL,
                    currency TEXT DEFAULT 'USD',
                    subtotal REAL,
                    FOREIGN KEY (sale_id) REFERENCES sales (id) ON DELETE CASCADE,
                    FOREIGN KEY (product_id) REFERENCES products (id) ON DELETE CASCADE
                )
            ''')
            
            self.conn.commit()
            print("✅ បង្កើតតារាងទាំងអស់រួចរាល់")
            
            # បញ្ចូលទិន្នន័យឧទាហរណ៍
            self.insert_sample_data()
            
        except sqlite3.Error as e:
            print(f"❌ មិនអាចបង្កើតតារាង: {e}")
            self.conn.rollback()
    
    def insert_sample_data(self):
        """បញ្ចូលទិន្នន័យឧទាហរណ៍"""
        try:
            # ពិនិត្យមើលថាតើតារាង products ទទេរឺអត់
            self.cursor.execute("SELECT COUNT(*) FROM products")
            count = self.cursor.fetchone()[0]
            
            if count == 0:
                print("📝 កំពុងបញ្ចូលទិន្នន័យឧទាហរណ៍...")
                
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # ទិន្នន័យឧទាហរណ៍
                sample_products = [
                    ('សៀវភៅគណិតវិទ្យាថ្នាក់ទី១០', 'សៀវភៅ', '9781234567890', 
                     5.00, 'USD', 8.00, 'USD', 50, 10, 
                     'សៀវភៅសិក្សាគណិតវិទ្យាថ្នាក់ទី១០', None, 1, 1, 1,
                     current_time, current_time),
                    
                    ('ប៊ិកខ្មៅ', 'ប៊ិក', '8901234567890', 
                     0.20, 'USD', 0.50, 'USD', 200, 50, 
                     'ប៊ិកខ្មៅសម្រាប់សរសេរ', None, 1, 1, 1,
                     current_time, current_time),
                    
                    ('សៀវភៅកត់ត្រា 100ទំព័រ', 'សៀវភៅកត់ត្រា', '7890123456789', 
                     0.80, 'USD', 1.50, 'USD', 150, 30, 
                     'សៀវភៅកត់ត្រា 100ទំព័រ គម្របរឹង', None, 1, 1, 1,
                     current_time, current_time),
                    
                    ('ខ្មៅដៃ HB', 'ខ្មៅដៃ', '6789012345678', 
                     0.10, 'USD', 0.25, 'USD', 300, 100, 
                     'ខ្មៅដៃ HB សម្រាប់សរសេរ', None, 1, 1, 1,
                     current_time, current_time),
                    
                    ('បន្ទាត់ 30cm', 'បន្ទាត់', '5678901234567', 
                     0.30, 'USD', 0.60, 'USD', 80, 20, 
                     'បន្ទាត់ផ្លាស្ទិច 30cm', None, 1, 1, 1,
                     current_time, current_time),
                ]
                
                for product in sample_products:
                    self.cursor.execute('''
                        INSERT INTO products (
                            name, category, barcode, cost_price, cost_currency,
                            selling_price, selling_currency, stock, min_stock,
                            description, image_path, taxable, discountable, active,
                            created_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', product)
                
                self.conn.commit()
                print(f"✅ បានបញ្ចូលទិន្នន័យឧទាហរណ៍ {len(sample_products)} មុខរួចរាល់")
            
        except sqlite3.Error as e:
            print(f"❌ មិនអាចបញ្ចូលទិន្នន័យឧទាហរណ៍: {e}")
    
    def get_all_products(self):
        """ទាញយកទំនិញទាំងអស់"""
        try:
            self.cursor.execute("""
                SELECT * FROM products 
                WHERE active = 1 
                ORDER BY name
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting products: {e}")
            return []
    
    def get_product_by_id(self, product_id):
        """ទាញយកទំនិញតាម ID"""
        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE id = ?", 
                (product_id,)
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting product: {e}")
            return None
    
    def get_product_by_barcode(self, barcode):
        """ទាញយកទំនិញតាម Barcode"""
        try:
            self.cursor.execute(
                "SELECT * FROM products WHERE barcode = ? AND active = 1", 
                (barcode,)
            )
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error getting product by barcode: {e}")
            return None
    
    def search_products(self, keyword):
        """ស្វែងរកទំនិញ"""
        try:
            self.cursor.execute("""
                SELECT * FROM products 
                WHERE (name LIKE ? OR barcode LIKE ?) AND active = 1
                ORDER BY name
            """, (f'%{keyword}%', f'%{keyword}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error searching products: {e}")
            return []
    
    def insert_product(self, product_data):
        """បញ្ចូលទំនិញថ្មី"""
        try:
            query = """
                INSERT INTO products (
                    name, category, barcode, cost_price, cost_currency,
                    selling_price, selling_currency, stock, min_stock,
                    description, image_path, taxable, discountable, active,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, product_data)
            self.conn.commit()
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                raise Exception("កូដទំនិញនេះមានរួចហើយ!")
            else:
                raise Exception(f"មានបញ្ហាក្នុងការបញ្ចូលទិន្នន័យ: {str(e)}")
        except sqlite3.Error as e:
            raise Exception(f"មានបញ្ហាក្នុងការបញ្ចូលទិន្នន័យ: {str(e)}")
    
    def update_product(self, product_id, update_data):
        """កែប្រែទំនិញ"""
        try:
            query = """
                UPDATE products 
                SET name=?, category=?, barcode=?, cost_price=?, cost_currency=?,
                    selling_price=?, selling_currency=?, stock=?, min_stock=?,
                    description=?, image_path=?, taxable=?, discountable=?, active=?,
                    updated_at=?
                WHERE id=?
            """
            self.cursor.execute(query, update_data + [product_id])
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"មានបញ្ហាក្នុងការកែប្រែទិន្នន័យ: {str(e)}")
    
    def delete_product(self, product_id):
        """លុបទំនិញ"""
        try:
            # យក image path មុនលុប
            self.cursor.execute("SELECT image_path FROM products WHERE id = ?", (product_id,))
            result = self.cursor.fetchone()
            if result and result[0] and os.path.exists(result[0]):
                try:
                    os.remove(result[0])
                except:
                    pass
            
            self.cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.conn.rollback()
            raise Exception(f"មានបញ្ហាក្នុងការលុបទិន្នន័យ: {str(e)}")
    
    def get_low_stock_products(self):
        """ទាញយកទំនិញជិតអស់ស្តុក"""
        try:
            self.cursor.execute("""
                SELECT name, stock, min_stock, image_path
                FROM products
                WHERE stock <= min_stock AND active = 1 AND stock > 0
                ORDER BY stock
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting low stock: {e}")
            return []
    
    def get_out_of_stock_products(self):
        """ទាញយកទំនិញអស់ស្តុក"""
        try:
            self.cursor.execute("""
                SELECT name, stock, image_path
                FROM products
                WHERE stock = 0 AND active = 1
                ORDER BY name
            """)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting out of stock: {e}")
            return []
    
    def get_statistics(self):
        """ទាញយកស្ថិតិទូទៅ"""
        try:
            stats = {}
            
            # ចំនួនទំនិញសរុប
            self.cursor.execute("SELECT COUNT(*), SUM(stock) FROM products WHERE active = 1")
            result = self.cursor.fetchone()
            stats['total_products'] = result[0] or 0
            stats['total_stock'] = result[1] or 0
            
            # ចំនួនទំនិញមានរូបភាព
            self.cursor.execute("""
                SELECT COUNT(*) FROM products 
                WHERE image_path IS NOT NULL AND image_path != '' AND active = 1
            """)
            stats['products_with_image'] = self.cursor.fetchone()[0] or 0
            
            # ចំនួនទំនិញជិតអស់
            self.cursor.execute("""
                SELECT COUNT(*) FROM products 
                WHERE stock <= min_stock AND active = 1 AND stock > 0
            """)
            stats['low_stock'] = self.cursor.fetchone()[0] or 0
            
            # ចំនួនទំនិញអស់ស្តុក
            self.cursor.execute("""
                SELECT COUNT(*) FROM products 
                WHERE stock = 0 AND active = 1
            """)
            stats['out_of_stock'] = self.cursor.fetchone()[0] or 0
            
            # ចំនួនលក់ថ្ងៃនេះ
            today = datetime.now().strftime('%Y-%m-%d')
            self.cursor.execute("""
                SELECT COUNT(*), SUM(total_amount) FROM sales 
                WHERE date LIKE ?
            """, (f'{today}%',))
            result = self.cursor.fetchone()
            stats['today_sales'] = result[0] or 0
            stats['today_revenue'] = result[1] or 0
            
            return stats
            
        except sqlite3.Error as e:
            print(f"Error getting statistics: {e}")
            return {}
    
    def get_sales_report(self, start_date, end_date):
        """ទាញយករបាយការណ៍លក់"""
        try:
            self.cursor.execute("""
                SELECT date, COUNT(*), SUM(total_amount), AVG(total_amount)
                FROM sales
                WHERE date BETWEEN ? AND ?
                GROUP BY date
                ORDER BY date DESC
            """, (f'{start_date} 00:00:00', f'{end_date} 23:59:59'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error getting sales report: {e}")
            return []
    
    def backup_database(self, backup_name=None):
        """បម្រុងទុក database"""
        if not backup_name:
            backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        
        try:
            # បិទការភ្ជាប់បច្ចុប្បន្ន
            self.cursor.close()
            self.conn.close()
            
            # ចម្លងឯកសារ
            shutil.copy2(self.db_name, backup_name)
            
            # ភ្ជាប់ឡើងវិញ
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            
            print(f"✅ បានបម្រុងទុក database ទៅ {backup_name}")
            return backup_name
            
        except Exception as e:
            print(f"❌ Error backing up database: {e}")
            return None
    
    def close(self):
        """បិទការភ្ជាប់ database"""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("🔒 បិទការភ្ជាប់ database រួចរាល់")

# សាកល្បងភ្ជាប់ database ពេលរត់ឯកសារនេះដោយផ្ទាល់
if __name__ == "__main__":
    print("=" * 60)
    print("កំពុងសាកល្បងភ្ជាប់ SQLite Database...")
    print("=" * 60)
    
    try:
        db = DatabaseManager('test.db')
        print("\n✅ សាកល្បងជោគជ័យ!")
        db.close()
    except Exception as e:
        print(f"\n❌ សាកល្បងបរាជ័យ: {e}")
    
    print("=" * 60)