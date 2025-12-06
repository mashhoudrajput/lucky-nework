import sqlite3
import os
from datetime import datetime

# Support Docker environment variable for database path
DATABASE_PATH = os.getenv('DATABASE_PATH', 'isp_recovery.db')
DATABASE = DATABASE_PATH

def get_db_connection():
    """Get database connection"""
    # Create directory if it doesn't exist (for Docker volume)
    db_path = DATABASE
    db_dir = os.path.dirname(db_path)
    
    # If path has directory, ensure it exists
    if db_dir and db_dir != '' and not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir, exist_ok=True)
        except Exception:
            pass  # If we can't create dir, try anyway
    
    # If directory creation failed or path is just filename, use current directory
    if db_dir and not os.path.exists(db_dir):
        db_path = os.path.basename(DATABASE)
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with required tables"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            package TEXT NOT NULL,
            payment_amount REAL NOT NULL,
            payment_status TEXT NOT NULL DEFAULT 'Unpaid',
            last_payment_date TEXT,
            created_at TEXT NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

def add_customer(name, phone, address, package, payment_amount):
    """Add a new customer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Set default values for optional fields if empty
    phone = phone or 'N/A'
    address = address or 'N/A'
    
    cursor.execute('''
        INSERT INTO customers (name, phone, address, package, payment_amount, payment_status, created_at)
        VALUES (?, ?, ?, ?, ?, 'Unpaid', ?)
    ''', (name, phone, address, package, payment_amount, created_at))
    
    conn.commit()
    customer_id = cursor.lastrowid
    conn.close()
    return customer_id

def get_all_customers():
    """Get all customers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM customers ORDER BY name')
    customers = cursor.fetchall()
    
    conn.close()
    return customers

def get_customer_by_id(customer_id):
    """Get customer by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
    customer = cursor.fetchone()
    
    conn.close()
    return customer

def update_customer(customer_id, name, phone, address, package, payment_amount):
    """Update customer information"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE customers 
        SET name = ?, phone = ?, address = ?, package = ?, payment_amount = ?
        WHERE id = ?
    ''', (name, phone, address, package, payment_amount, customer_id))
    
    conn.commit()
    conn.close()

def delete_customer(customer_id):
    """Delete a customer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
    
    conn.commit()
    conn.close()

def update_payment_status(customer_id, payment_status):
    """Update payment status for a customer"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    last_payment_date = None
    if payment_status == 'Paid':
        last_payment_date = datetime.now().strftime('%Y-%m-%d')
    
    cursor.execute('''
        UPDATE customers 
        SET payment_status = ?, last_payment_date = ?
        WHERE id = ?
    ''', (payment_status, last_payment_date, customer_id))
    
    conn.commit()
    conn.close()

def get_customers_by_status(status):
    """Get customers filtered by payment status"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if status == 'All':
        cursor.execute('SELECT * FROM customers ORDER BY name')
    else:
        cursor.execute('SELECT * FROM customers WHERE payment_status = ? ORDER BY name', (status,))
    
    customers = cursor.fetchall()
    conn.close()
    return customers

def get_statistics():
    """Get payment statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) as total FROM customers')
    total = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as paid FROM customers WHERE payment_status = 'Paid'")
    paid = cursor.fetchone()['paid']
    
    cursor.execute("SELECT COUNT(*) as unpaid FROM customers WHERE payment_status = 'Unpaid'")
    unpaid = cursor.fetchone()['unpaid']
    
    conn.close()
    return {
        'total': total,
        'paid': paid,
        'unpaid': unpaid
    }

def bulk_update_payment_status(customer_ids, payment_status):
    """Update payment status for multiple customers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    last_payment_date = None
    if payment_status == 'Paid':
        last_payment_date = datetime.now().strftime('%Y-%m-%d')
    
    placeholders = ','.join(['?'] * len(customer_ids))
    cursor.execute(f'''
        UPDATE customers 
        SET payment_status = ?, last_payment_date = ?
        WHERE id IN ({placeholders})
    ''', [payment_status, last_payment_date] + customer_ids)
    
    conn.commit()
    conn.close()
    return cursor.rowcount

def bulk_delete_customers(customer_ids):
    """Delete multiple customers"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    placeholders = ','.join(['?'] * len(customer_ids))
    cursor.execute(f'DELETE FROM customers WHERE id IN ({placeholders})', customer_ids)
    
    conn.commit()
    rows_deleted = cursor.rowcount
    conn.close()
    return rows_deleted

def reset_monthly_payments():
    """Reset all payments to Unpaid status at start of new month"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("UPDATE customers SET payment_status = 'Unpaid', last_payment_date = NULL")
    
    conn.commit()
    conn.close()

