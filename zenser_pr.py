import sqlite3
import datetime

# Database setup
def create_database():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    # Create Complaint table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            department TEXT,
            status TEXT DEFAULT 'Pending'
        )
    ''')

    # Create Complaint History table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaint_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER,
            timestamp TEXT,
            action TEXT,
            FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id)
        )
    ''')

    conn.commit()
    conn.close()

# Add complaint
def add_complaint(description):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    # Insert new complaint into the database
    cursor.execute('''
        INSERT INTO complaints (description) VALUES (?)
    ''', (description,))
    conn.commit()

    # Get the new complaint's ID
    complaint_id = cursor.lastrowid

    # Add a history entry for the new complaint
    timestamp = str(datetime.datetime.now())
    cursor.execute('''
        INSERT INTO complaint_history (complaint_id, timestamp, action)
        VALUES (?, ?, ?)
    ''', (complaint_id, timestamp, 'Complaint Registered'))

    conn.commit()
    conn.close()

    print(f"Complaint added successfully with ID {complaint_id}")

# View all complaints
def view_complaints():
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM complaints')
    complaints = cursor.fetchall()

    if not complaints:
        print("No complaints found.")
    else:
        for complaint in complaints:
            print(f"ID: {complaint[0]}, Description: {complaint[1]}, Status: {complaint[3]}, Department: {complaint[2]}")

    conn.close()

# View a specific complaint
def view_complaint(complaint_id):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM complaints WHERE complaint_id = ?', (complaint_id,))
    complaint = cursor.fetchone()

    if complaint:
        print(f"ID: {complaint[0]}")
        print(f"Description: {complaint[1]}")
        print(f"Status: {complaint[3]}")
        print(f"Department: {complaint[2]}")
        
        # Get the history of the complaint
        cursor.execute('SELECT * FROM complaint_history WHERE complaint_id = ?', (complaint_id,))
        history = cursor.fetchall()
        
        print("\nHistory:")
        for record in history:
            print(f"Timestamp: {record[2]}, Action: {record[3]}")
    else:
        print(f"Complaint with ID {complaint_id} not found.")

    conn.close()

# Update a complaint
def update_complaint(complaint_id, status=None, department=None):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    # Check if the complaint exists
    cursor.execute('SELECT * FROM complaints WHERE complaint_id = ?', (complaint_id,))
    complaint = cursor.fetchone()

    if not complaint:
        print(f"Complaint with ID {complaint_id} not found.")
        conn.close()
        return

    # Update status and/or department if provided
    if status:
        cursor.execute('UPDATE complaints SET status = ? WHERE complaint_id = ?', (status, complaint_id))
        action = f"Status updated to {status}"
    if department:
        cursor.execute('UPDATE complaints SET department = ? WHERE complaint_id = ?', (department, complaint_id))
        action = f"Department updated to {department}"

    # Insert history record for the update
    timestamp = str(datetime.datetime.now())
    cursor.execute('''
        INSERT INTO complaint_history (complaint_id, timestamp, action)
        VALUES (?, ?, ?)
    ''', (complaint_id, timestamp, action))

    conn.commit()
    print(f"Complaint with ID {complaint_id} updated successfully.")
    conn.close()

# Delete a complaint
def delete_complaint(complaint_id):
    conn = sqlite3.connect('complaints.db')
    cursor = conn.cursor()

    # Check if the complaint exists
    cursor.execute('SELECT * FROM complaints WHERE complaint_id = ?', (complaint_id,))
    complaint = cursor.fetchone()

    if not complaint:
        print(f"Complaint with ID {complaint_id} not found.")
        conn.close()
        return

    # Delete the complaint and its history
    cursor.execute('DELETE FROM complaint_history WHERE complaint_id = ?', (complaint_id,))
    cursor.execute('DELETE FROM complaints WHERE complaint_id = ?', (complaint_id,))

    conn.commit()
    print(f"Complaint with ID {complaint_id} deleted successfully.")
    conn.close()

# Main function to drive the CLI
def main():
    create_database()

    while True:
        print("\nComplaint Management System")
        print("1. Add Complaint")
        print("2. View All Complaints")
        print("3. View Specific Complaint")
        print("4. Update Complaint")
        print("5. Delete Complaint")
        print("6. Exit")
        
        choice = input("Enter choice: ")

        if choice == '1':
            description = input("Enter complaint description: ")
            add_complaint(description)
        elif choice == '2':
            view_complaints()
        elif choice == '3':
            complaint_id = int(input("Enter complaint ID: "))
            view_complaint(complaint_id)
        elif choice == '4':
            complaint_id = int(input("Enter complaint ID: "))
            status = input("Enter new status (leave blank to skip): ")
            department = input("Enter new department (leave blank to skip): ")
            update_complaint(complaint_id, status, department)
        elif choice == '5':
            complaint_id = int(input("Enter complaint ID: "))
            delete_complaint(complaint_id)
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
