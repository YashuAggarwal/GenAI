"""
Database initialization and management module.
Creates SQLite database with customer and sales tables and populates with sample data.
"""

import sqlite3
from datetime import datetime, timedelta
import os


def get_db_path():
    """Get the path to the SQLite database file."""
    return os.path.join(os.path.dirname(__file__), "sales.db")


def initialize_database():
    """
    Initialize the database with schema and sample data.
    Creates tables if they don't exist and inserts sample data.
    """
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Create customer table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                customer_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                join_date TEXT NOT NULL
            )
        """)
        
        # Create sales table with foreign key
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount REAL NOT NULL,
                sale_date TEXT NOT NULL,
                FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
            )
        """)
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM customer")
        customer_count = cursor.fetchone()[0]
        
        if customer_count == 0:
            # Insert sample customers
            customers = [
                (1, "Alice Johnson", "alice.j@email.com", "2024-01-15"),
                (2, "Bob Smith", "bob.smith@email.com", "2024-02-20"),
                (3, "Carol Williams", "carol.w@email.com", "2024-03-10"),
                (4, "David Brown", "david.b@email.com", "2024-04-05"),
                (5, "Emma Davis", "emma.d@email.com", "2024-05-12"),
                (6, "Frank Miller", "frank.m@email.com", "2024-06-01"),
                (7, "Grace Wilson", "grace.w@email.com", "2024-07-15"),
                (8, "Henry Moore", "henry.m@email.com", "2024-08-20"),
                (9, "Ivy Taylor", "ivy.t@email.com", "2024-09-10"),
                (10, "Jack Anderson", "jack.a@email.com", "2024-10-05")
            ]
            
            cursor.executemany("""
                INSERT INTO customer (customer_id, name, email, join_date)
                VALUES (?, ?, ?, ?)
            """, customers)
            
            # Insert sample sales with recent dates (last 30 days)
            today = datetime.now()
            sales = [
                # Sales from today
                (1, 1, "Laptop", 1200.00, today.strftime("%Y-%m-%d")),
                (2, 3, "Mouse", 25.50, today.strftime("%Y-%m-%d")),
                (3, 5, "Keyboard", 75.00, today.strftime("%Y-%m-%d")),
                
                # Sales from 1 day ago
                (4, 2, "Monitor", 350.00, (today - timedelta(days=1)).strftime("%Y-%m-%d")),
                (5, 4, "Webcam", 89.99, (today - timedelta(days=1)).strftime("%Y-%m-%d")),
                
                # Sales from 2 days ago
                (6, 1, "Mouse", 25.50, (today - timedelta(days=2)).strftime("%Y-%m-%d")),
                (7, 6, "Headphones", 120.00, (today - timedelta(days=2)).strftime("%Y-%m-%d")),
                (8, 7, "USB Cable", 15.00, (today - timedelta(days=2)).strftime("%Y-%m-%d")),
                
                # Sales from 3 days ago
                (9, 3, "Laptop", 1400.00, (today - timedelta(days=3)).strftime("%Y-%m-%d")),
                (10, 8, "Keyboard", 85.00, (today - timedelta(days=3)).strftime("%Y-%m-%d")),
                
                # Sales from last week
                (11, 2, "Monitor", 400.00, (today - timedelta(days=7)).strftime("%Y-%m-%d")),
                (12, 9, "Mouse", 30.00, (today - timedelta(days=7)).strftime("%Y-%m-%d")),
                (13, 10, "Laptop", 1500.00, (today - timedelta(days=8)).strftime("%Y-%m-%d")),
                
                # Sales from 2 weeks ago
                (14, 5, "Monitor", 380.00, (today - timedelta(days=14)).strftime("%Y-%m-%d")),
                (15, 4, "Headphones", 150.00, (today - timedelta(days=15)).strftime("%Y-%m-%d")),
                
                # Sales from last month
                (16, 1, "USB Cable", 12.00, (today - timedelta(days=25)).strftime("%Y-%m-%d")),
                (17, 6, "Webcam", 95.00, (today - timedelta(days=28)).strftime("%Y-%m-%d")),
                (18, 7, "Keyboard", 90.00, (today - timedelta(days=29)).strftime("%Y-%m-%d")),
                (19, 3, "Mouse", 28.00, (today - timedelta(days=30)).strftime("%Y-%m-%d")),
                (20, 9, "Headphones", 140.00, (today - timedelta(days=30)).strftime("%Y-%m-%d"))
            ]
            
            cursor.executemany("""
                INSERT INTO sales (sale_id, customer_id, product, amount, sale_date)
                VALUES (?, ?, ?, ?, ?)
            """, sales)
            
            conn.commit()
            print("✓ Database initialized successfully with sample data")
        else:
            print("✓ Database already initialized")
            
    except sqlite3.Error as e:
        print(f"✗ Database error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


def get_database_schema():
    """
    Get the database schema as a formatted string for the LLM prompt.
    Returns schema information for both tables.
    """
    schema = """
Database Schema:

Table: customer
- customer_id (INTEGER PRIMARY KEY): Unique customer identifier
- name (TEXT): Customer full name
- email (TEXT): Customer email address
- join_date (TEXT): Date when customer joined (format: YYYY-MM-DD)

Table: sales
- sale_id (INTEGER PRIMARY KEY): Unique sale identifier
- customer_id (INTEGER): Foreign key to customer table
- product (TEXT): Product name
- amount (REAL): Sale amount in dollars
- sale_date (TEXT): Date of sale (format: YYYY-MM-DD)

Relationship: sales.customer_id references customer.customer_id
"""
    return schema.strip()


def get_connection():
    """
    Get a connection to the SQLite database.
    Returns a connection object.
    """
    db_path = get_db_path()
    return sqlite3.connect(db_path)


if __name__ == "__main__":
    # Initialize database when run directly
    initialize_database()
    print("\nDatabase schema:")
    print(get_database_schema())
