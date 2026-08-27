"""Unit tests for repository implementations"""

import unittest
from src.domain.models import Task, Priority
from src.domain.exceptions import TaskNotFoundError, DuplicateTaskError
from src.repository.memory import InMemoryTodoRepository


class TestInMemoryRepository(unittest.TestCase):
    """Test InMemoryTodoRepository"""
    
    def setUp(self):
        """Set up test repository"""
        self.repo = InMemoryTodoRepository()
    
    def test_add_task(self):
        """Test adding a task"""
        task = Task(title="Test Task")
        added = self.repo.add(task)
        
        self.assertEqual(added.id, task.id)
        self.assertTrue(self.repo.exists(task.id))
    
    def test_add_duplicate_raises_error(self):
        """Test adding duplicate task raises error"""
        task = Task(title="Test Task")
        self.repo.add(task)
        
        with self.assertRaises(DuplicateTaskError):
            self.repo.add(task)
    
    def test_get_by_id(self):
        """Test retrieving task by ID"""
        task = Task(title="Test Task")
        self.repo.add(task)
        
        retrieved = self.repo.get_by_id(task.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, task.id)
    
    def test_get_by_id_not_found(self):
        """Test retrieving non-existent task returns None"""
        result = self.repo.get_by_id("non-existent-id")
        self.assertIsNone(result)
    
    def test_get_all(self):
        """Test retrieving all tasks"""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        
        self.repo.add(task1)
        self.repo.add(task2)
        
        all_tasks = self.repo.get_all()
        self.assertEqual(len(all_tasks), 2)
    
    def test_get_all_empty(self):
        """Test retrieving all tasks when empty"""
        all_tasks = self.repo.get_all()
        self.assertEqual(len(all_tasks), 0)
    
    def test_update_task(self):
        """Test updating a task"""
        task = Task(title="Original")
        self.repo.add(task)
        
        task.title = "Updated"
        updated = self.repo.update(task)
        
        self.assertEqual(updated.title, "Updated")
        retrieved = self.repo.get_by_id(task.id)
        self.assertEqual(retrieved.title, "Updated")
    
    def test_update_non_existent_raises_error(self):
        """Test updating non-existent task raises error"""
        task = Task(title="Test")
        
        with self.assertRaises(TaskNotFoundError):
            self.repo.update(task)
    
    def test_delete_task(self):
        """Test deleting a task"""
        task = Task(title="Test Task")
        self.repo.add(task)
        
        result = self.repo.delete(task.id)
        self.assertTrue(result)
        self.assertFalse(self.repo.exists(task.id))
    
    def test_delete_non_existent(self):
        """Test deleting non-existent task returns False"""
        result = self.repo.delete("non-existent-id")
        self.assertFalse(result)
    
    def test_exists(self):
        """Test checking task existence"""
        task = Task(title="Test Task")
        self.repo.add(task)
        
        self.assertTrue(self.repo.exists(task.id))
        self.assertFalse(self.repo.exists("non-existent-id"))


if __name__ == "__main__":
    unittest.main()
