"""
Script to add sample customer data for testing
Run this after starting the application for the first time
"""
from database import init_db, add_customer
import random

def add_sample_customers():
    """Add sample customers for testing"""
    init_db()
    
    # Sample names
    names = [
        "Rajesh Kumar", "Priya Sharma", "Amit Patel", "Sunita Devi",
        "Vikram Singh", "Anjali Mehta", "Suresh Reddy", "Kavita Nair",
        "Mohan Das", "Deepika Iyer", "Kiran Joshi", "Neha Kapoor",
        "Ravi Shankar", "Sneha Menon", "Arjun Pillai", "Divya Rao",
        "Nikhil Shah", "Meera Krishnan", "Siddharth Nair", "Anita Banerjee"
    ]
    
    # Sample packages
    packages = [
        "50 Mbps", "100 Mbps", "150 Mbps", "200 Mbps", "300 Mbps",
        "50 Mbps Unlimited", "100 Mbps Unlimited", "200 Mbps Unlimited"
    ]
    
    # Sample addresses
    addresses = [
        "123 Main Street, Area 1", "456 Park Avenue, Area 2",
        "789 Market Road, Area 3", "321 Garden Lane, Area 4",
        "654 Oak Street, Area 5", "987 Pine Avenue, Area 6",
        "147 Elm Road, Area 7", "258 Cedar Lane, Area 8"
    ]
    
    # Sample phone numbers
    phone_base = "98765432"
    
    print("Adding sample customers...")
    
    for i, name in enumerate(names):
        phone = f"{phone_base}{i:02d}"
        address = random.choice(addresses)
        package = random.choice(packages)
        payment = random.choice([500, 750, 1000, 1200, 1500, 1800, 2000, 2500])
        
        customer_id = add_customer(name, phone, address, package, payment)
        print(f"Added customer {customer_id}: {name} - {package} - ₹{payment}")
    
    print(f"\nSuccessfully added {len(names)} sample customers!")
    print("You can now start the application and test all features.")

if __name__ == '__main__':
    add_sample_customers()

