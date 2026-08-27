"""Unit tests for domain models"""

import unittest
from datetime import datetime, timedelta
from src.domain.models import Task, TaskStatus, Priority, Recurrence
from src.domain.exceptions import ValidationError


class TestTask(unittest.TestCase):
    """Test Task domain model"""
    
    def test_create_task_with_defaults(self):
        """Test creating a task with minimal required fields"""
        task = Task(title="Test Task")
        
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertEqual(task.priority, Priority.MEDIUM)
        self.assertEqual(task.tags, [])
        self.assertIsNone(task.due_date)
        self.assertIsNone(task.completed_at)
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
    
    def test_create_task_with_all_fields(self):
        """Test creating a task with all fields"""
        due_date = datetime.now() + timedelta(days=1)
        task = Task(
            title="Complete Task",
            description="Test description",
            priority=Priority.HIGH,
            tags=["work", "urgent"],
            due_date=due_date,
            recurrence=Recurrence.DAILY,
        )
        
        self.assertEqual(task.title, "Complete Task")
        self.assertEqual(task.description, "Test description")
        self.assertEqual(task.priority, Priority.HIGH)
        self.assertEqual(task.tags, ["work", "urgent"])
        self.assertEqual(task.due_date, due_date)
        self.assertEqual(task.recurrence, Recurrence.DAILY)
    
    def test_empty_title_raises_error(self):
        """Test that empty title raises ValidationError"""
        with self.assertRaises(ValidationError):
            Task(title="")
        
        with self.assertRaises(ValidationError):
            Task(title="   ")
    
    def test_title_too_long_raises_error(self):
        """Test that title exceeding 200 chars raises error"""
        with self.assertRaises(ValidationError):
            Task(title="a" * 201)
    
    def test_description_too_long_raises_error(self):
        """Test that description exceeding 1000 chars raises error"""
        with self.assertRaises(ValidationError):
            Task(title="Test", description="a" * 1001)
    
    def test_tags_normalized(self):
        """Test that tags are normalized (trimmed, lowercase)"""
        task = Task(title="Test", tags=["  Work  ", "URGENT", "home"])
        
        self.assertEqual(task.tags, ["work", "urgent", "home"])
    
    def test_mark_complete(self):
        """Test marking task as complete"""
        task = Task(title="Test")
        task.mark_complete()
        
        self.assertEqual(task.status, TaskStatus.COMPLETED)
        self.assertIsNotNone(task.completed_at)
    
    def test_mark_pending(self):
        """Test marking task as pending"""
        task = Task(title="Test")
        task.mark_complete()
        task.mark_pending()
        
        self.assertEqual(task.status, TaskStatus.PENDING)
        self.assertIsNone(task.completed_at)
    
    def test_is_overdue(self):
        """Test overdue detection"""
        # Past due date, pending
        past_task = Task(
            title="Overdue",
            due_date=datetime.now() - timedelta(days=1)
        )
        self.assertTrue(past_task.is_overdue())
        
        # Future due date
        future_task = Task(
            title="Not Overdue",
            due_date=datetime.now() + timedelta(days=1)
        )
        self.assertFalse(future_task.is_overdue())
        
        # Completed task (not overdue even if past)
        completed_task = Task(
            title="Completed",
            due_date=datetime.now() - timedelta(days=1)
        )
        completed_task.mark_complete()
        self.assertFalse(completed_task.is_overdue())
    
    def test_clone_for_recurrence_daily(self):
        """Test cloning task for daily recurrence"""
        original = Task(
            title="Daily Task",
            description="Test",
            priority=Priority.HIGH,
            tags=["daily"],
            due_date=datetime(2025, 12, 14),
            recurrence=Recurrence.DAILY,
        )
        
        clone = original.clone_for_recurrence()
        
        self.assertEqual(clone.title, original.title)
        self.assertEqual(clone.description, original.description)
        self.assertEqual(clone.priority, original.priority)
        self.assertEqual(clone.tags, original.tags)
        self.assertEqual(clone.recurrence, original.recurrence)
        self.assertEqual(clone.status, TaskStatus.PENDING)
        self.assertNotEqual(clone.id, original.id)
        self.assertEqual(clone.due_date, datetime(2025, 12, 15))
    
    def test_update_fields(self):
        """Test updating task fields"""
        task = Task(title="Original")
        task.update_fields(title="Updated", priority=Priority.URGENT)
        
        self.assertEqual(task.title, "Updated")
        self.assertEqual(task.priority, Priority.URGENT)
    
    def test_update_immutable_field_raises_error(self):
        """Test that updating immutable fields raises error"""
        task = Task(title="Test")
        
        with self.assertRaises(ValidationError):
            task.update_fields(id="new-id")
        
        with self.assertRaises(ValidationError):
            task.update_fields(created_at=datetime.now())


class TestPriority(unittest.TestCase):
    """Test Priority enum"""
    
    def test_sort_order(self):
        """Test priority sort order"""
        self.assertEqual(Priority.LOW.sort_order, 1)
        self.assertEqual(Priority.MEDIUM.sort_order, 2)
        self.assertEqual(Priority.HIGH.sort_order, 3)
        self.assertEqual(Priority.URGENT.sort_order, 4)
    
    def test_display_icon(self):
        """Test priority display icons"""
        self.assertEqual(Priority.LOW.display_icon, "🟢")
        self.assertEqual(Priority.MEDIUM.display_icon, "🟡")
        self.assertEqual(Priority.HIGH.display_icon, "🟠")
        self.assertEqual(Priority.URGENT.display_icon, "🔴")


if __name__ == "__main__":
    unittest.main()
