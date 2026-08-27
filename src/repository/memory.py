"""In-memory implementation of TodoRepository"""

from typing import Dict, List, Optional
from ..domain.models import Task
from ..domain.exceptions import TaskNotFoundError, DuplicateTaskError
from .interface import TodoRepository


class InMemoryTodoRepository(TodoRepository):
    """
    In-memory storage implementation using a dictionary.
    
    This implementation is suitable for Phase I (console app).
    Will be replaced with database-backed repository in Phase II.
    """
    
    def __init__(self):
        """Initialize empty task storage"""
        self._tasks: Dict[str, Task] = {}
    
    def add(self, task: Task) -> Task:
        """
        Add a new task to in-memory storage.
        
        Args:
            task: Task instance to add
        
        Returns:
            The added task
        
        Raises:
            DuplicateTaskError: If task with same ID already exists
        """
        if task.id in self._tasks:
            raise DuplicateTaskError(f"Task with ID {task.id} already exists")
        
        self._tasks[task.id] = task
        return task
    
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            Task instance if found, None otherwise
        """
        return self._tasks.get(task_id)
    
    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            List of all tasks
        """
        return list(self._tasks.values())
    
    def update(self, task: Task) -> Task:
        """
        Update an existing task.
        
        Args:
            task: Task instance with updated data
        
        Returns:
            The updated task
        
        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if task.id not in self._tasks:
            raise TaskNotFoundError(task.id)
        
        self._tasks[task.id] = task
        return task
    
    def delete(self, task_id: str) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            True if deleted, False if not found
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def exists(self, task_id: str) -> bool:
        """
        Check if a task exists.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            True if task exists, False otherwise
        """
        return task_id in self._tasks
