"""Custom exceptions for Todo application"""


class TodoError(Exception):
    """Base exception for all Todo application errors"""
    pass


class TaskNotFoundError(TodoError):
    """Raised when a task with the specified ID is not found"""
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class ValidationError(TodoError):
    """Raised when input validation fails"""
    pass


class DuplicateTaskError(TodoError):
    """Raised when attempting to create a duplicate task"""
    pass
