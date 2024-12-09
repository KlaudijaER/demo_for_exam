import unittest
import os
from git_work import TodoApp

class TestTodoApp (unittest.TestCase):
    def setUp(self):
        """Setting test database and initiaize TodoApp"""
        self.test_db_name = 'test_todo.db'
        self.app = TodoApp(db_name=self.test_db_name)
        self.app.create_table()

    def tearDown(self):
        """clear up the test db after each test"""
        self.app.close()
        if os.path.exists(self.test_db_name):
            os.remove(self.test_db_name)
    
    def test_add_task(self):
        """Test adding a task to the database."""
        self.app.add_task("Test Task 1")
        self.app.cursor.execute('SELECT task FROM tasks')
        tasks = self.app.cursor.fetchall()
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0][0], "Test Task 1")

    def test_complete_task(self):
        """Test marking a task as completed."""
        self.app.add_task("Test Task 2")
        task_id = self.app.cursor.execute('SELECT id FROM tasks WHERE task = "Test Task 2"').fetchone()[0]
        self.app.complete_task(task_id)
        self.app.cursor.execute('SELECT completed FROM tasks WHERE id = ?', (task_id,))
        status = self.app.cursor.fetchone()[0]
        self.assertEqual(status, 1)  # Ensure the task is marked as completed
    
    def test_delete_task(self):
        """Test deleting a task."""
        self.app.add_task("Test Task 3")
        task_id = self.app.cursor.execute('SELECT id FROM tasks WHERE task = "Test Task 3"').fetchone()[0]
        self.app.delete_task(task_id)
        self.app.cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        task = self.app.cursor.fetchone()
        self.assertIsNone(task)  # Ensure the task is deleted
    
    def test_show_tasks(self):
        """Test retrieving tasks from the database."""
        self.app.add_task("Test Task 4")
        self.app.add_task("Test Task 5")
        tasks = self.app.get_all_tasks()
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0][1], "Test Task 4")
        self.assertEqual(tasks[1][1], "Test Task 5")
    
if __name__ == "__main__":
    unittest.main()   