import sqlite3
from datetime import datetime

class TodoApp:
    def __init__(self, db_name='todo.db'):
        """Initialize the app with database support."""
        self.db_name = db_name
        # Connect to SQLite database
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        # Create tasks table if it doesn't exist
        self.create_table()

    def create_table(self):
        """Create tasks table if it doesn't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                task TEXT NOT NULL,
                                completed INTEGER DEFAULT 0,
                                created_at TEXT
                              )''')
        self.conn.commit()

    def add_task(self, task):
        """Add a new task to the database."""
        created_at = datetime.now().isoformat()
        self.cursor.execute('INSERT INTO tasks (task, created_at) VALUES (?, ?)', (task, created_at))
        self.conn.commit()
        print(f"Task '{task}' added.")

    def complete_task(self, task_id):
        """Mark a task as completed in the database."""
        self.cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
        self.conn.commit()
        print(f"Task ID '{task_id}' marked as completed.")

    def delete_task(self, task_id):
        """Delete a task from the database."""
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()
        print(f"Task ID '{task_id}' deleted.")

    def show_tasks(self):
        """Display all tasks in the database."""
        self.cursor.execute('SELECT id, task, completed FROM tasks')
        tasks = self.cursor.fetchall()
        
        for task in tasks:
            status = "Completed" if task[2] else "Pending"
            print(f"ID: {task[0]}, Task: {task[1]}, Status: {status}")
    
    def get_all_tasks(self):
        """Retrieve all tasks from the database."""
        self.cursor.execute('SELECT id, task, completed FROM tasks')
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def menu(self):
        """Display the main menu and handle user input."""
        while True:
            print("\nMenu:")
            print("1. Show tasks")
            print("2. Add a new task")
            print("3. Complete a task")
            print("4. Delete a task")
            print("5. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.show_tasks()
            elif choice == '2':
                task = input("Enter the task description: ")
                self.add_task(task)
            elif choice == '3':
                try:
                    task_id = int(input("Enter the task ID to mark as completed: "))
                    self.complete_task(task_id)
                except ValueError:
                    print("Please enter a valid task ID.")
            elif choice == '4':
                try:
                    task_id = int(input("Enter the task ID to delete: "))
                    self.delete_task(task_id)
                except ValueError:
                    print("Please enter a valid task ID.")
            elif choice == '5':
                print("Exiting program.")
                self.close()
                break
            else:
                print("Invalid choice. Please try again.")

# Main program
if __name__ == "__main__":
    app = TodoApp()
    app.menu()