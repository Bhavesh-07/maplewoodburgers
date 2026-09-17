import mysql.connector
import random
import time
from datetime import datetime, timedelta

def seed_data():
    config = {
        'user': 'root',
        'password': '',
        'host': '127.0.0.1',
        'database': 'maplewood_db'
    }

    first_names = ['John', 'Jane', 'Michael', 'Emily', 'Chris', 'Sarah', 'David', 'Laura', 'Robert', 'Jessica', 'Daniel', 'Ashley', 'James', 'Taylor', 'Matthew', 'Madison', 'Andrew', 'Alexis', 'Joshua', 'Victoria']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin']
    locations = ['Sulphur', 'Lake Charles', 'Moss Bluff']
    positions = ['Manager', 'Cook', 'Server', 'Cashier', 'Dishwasher']
    
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        print("Seeding 100 applications...")
        
        for i in range(100):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            contact_number = f"337-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com"
            experience = f"I have {random.randint(1, 15)} years of experience in the food industry. Previously worked as a {random.choice(positions)}."
            location = random.choice(locations)
            position = random.choice(positions)
            
            # Generate a random date within the last 30 days
            days_ago = random.randint(0, 30)
            submitted_at = datetime.now() - timedelta(days=days_ago)
            
            query = """
            INSERT INTO applications (first_name, last_name, contact_number, email, experience, location, position, submitted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, contact_number, email, experience, location, position, submitted_at))
            
        conn.commit()
        print("Successfully seeded 100 application records.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error seeding data: {e}")

if __name__ == "__main__":
    seed_data()
