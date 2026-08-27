"""Abstract repository interface for Todo storage"""

from abc import ABC, abstractmethod
from typing import List, Optional
from ..domain.models import Task


class TodoRepository(ABC):
    """
    Abstract base class for Todo task storage.
    
    This interface enables swapping storage implementations
    (in-memory, database, file-based) without changing business logic.
    """
    
    @abstractmethod
    def add(self, task: Task) -> Task:
        """
        Add a new task to the repository.
        
        Args:
            task: Task instance to add
        
        Returns:
            The added task
        
        Raises:
            DuplicateTaskError: If task with same ID already exists
        """
        pass
    
    @abstractmethod
    def get_by_id(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            Task instance if found, None otherwise
        """
        pass
    
    @abstractmethod
    def get_all(self) -> List[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            List of all tasks
        """
        pass
    
    @abstractmethod
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
        pass
    
    @abstractmethod
    def delete(self, task_id: str) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            True if deleted, False if not found
        """
        pass
    
    @abstractmethod
    def exists(self, task_id: str) -> bool:
        """
        Check if a task exists.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            True if task exists, False otherwise
        """
        pass
