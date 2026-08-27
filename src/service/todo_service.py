"""Business logic service for Todo operations"""

from datetime import datetime
from typing import List, Optional
from ..domain.models import Task, TaskStatus, Priority, Recurrence
from ..domain.exceptions import ValidationError, TaskNotFoundError
from ..repository.interface import TodoRepository


class TodoService:
    """
    Service layer orchestrating Todo business operations.
    
    This class will become the foundation for FastAPI endpoints in Phase II
    and AI agent actions in Phase III.
    """
    
    def __init__(self, repository: TodoRepository):
        """
        Initialize service with a repository.
        
        Args:
            repository: Storage implementation (dependency injection)
        """
        self._repo = repository
    
    def add_task(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        tags: Optional[List[str]] = None,
        due_date: Optional[str] = None,
        recurrence: Optional[Recurrence] = None
    ) -> Task:
        """
        Create and add a new task.
        
        Args:
            title: Task title (required)
            description: Task description (optional)
            priority: Priority level (default: MEDIUM)
            tags: List of tags (optional)
            due_date: Due date in YYYY-MM-DD format (optional)
            recurrence: Recurrence pattern (optional)
        
        Returns:
            The created task
        
        Raises:
            ValidationError: If validation fails
        """
        # Parse and validate due date
        parsed_due_date = None
        if due_date:
            parsed_due_date = self._parse_date(due_date)
            self._validate_due_date(parsed_due_date)
        
        # Create task (validation happens in Task.__post_init__)
        task = Task(
            title=title.strip(),
            description=description.strip(),
            priority=priority,
            tags=tags or [],
            due_date=parsed_due_date,
            recurrence=recurrence,
        )
        
        return self._repo.add(task)
    
    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.
        
        Returns:
            List of all tasks
        """
        return self._repo.get_all()
    
    def get_task_by_id(self, task_id: str) -> Task:
        """
        Retrieve a task by ID.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            The task
        
        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        task = self._repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundError(task_id)
        return task
    
    def update_task(self, task_id: str, **updates) -> Task:
        """
        Update a task's fields.
        
        Args:
            task_id: Unique task identifier
            **updates: Field names and values to update
        
        Returns:
            The updated task
        
        Raises:
            TaskNotFoundError: If task doesn't exist
            ValidationError: If validation fails
        """
        task = self.get_task_by_id(task_id)
        
        # Handle special date parsing. The same rule add_task enforces applies
        # here: validating on create but not on update let a past due date in
        # through the back door.
        if "due_date" in updates and isinstance(updates["due_date"], str):
            updates["due_date"] = self._parse_date(updates["due_date"])
            self._validate_due_date(updates["due_date"])
        
        # Update fields (validation happens in task.update_fields)
        task.update_fields(**updates)
        
        return self._repo.update(task)
    
    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            True if deleted
        
        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        if not self._repo.exists(task_id):
            raise TaskNotFoundError(task_id)
        
        return self._repo.delete(task_id)
    
    def toggle_complete(self, task_id: str) -> Task:
        """
        Toggle task completion status.
        
        If task is recurring and being marked complete, creates next instance.
        
        Args:
            task_id: Unique task identifier
        
        Returns:
            The updated task
        
        Raises:
            TaskNotFoundError: If task doesn't exist
        """
        task = self.get_task_by_id(task_id)
        
        if task.status == TaskStatus.PENDING:
            task.mark_complete()
            
            # Handle recurring tasks
            if task.recurrence:
                next_task = task.clone_for_recurrence()
                self._repo.add(next_task)
        else:
            task.mark_pending()
        
        return self._repo.update(task)
    
    def search_tasks(
        self,
        query: Optional[str] = None,
        tag: Optional[str] = None,
        status: Optional[TaskStatus] = None,
        priority: Optional[Priority] = None
    ) -> List[Task]:
        """
        Search and filter tasks.
        
        Multiple filters are combined with AND logic.
        
        Args:
            query: Substring to search in title (case-insensitive)
            tag: Exact tag match (case-insensitive)
            status: Filter by status
            priority: Filter by priority
        
        Returns:
            List of matching tasks
        """
        tasks = self._repo.get_all()
        
        # Apply filters
        if query:
            query_lower = query.lower()
            tasks = [t for t in tasks if query_lower in t.title.lower()]
        
        if tag:
            tag_lower = tag.lower()
            tasks = [t for t in tasks if tag_lower in t.tags]
        
        if status:
            tasks = [t for t in tasks if t.status == status]
        
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        
        return tasks
    
    def sort_tasks(
        self,
        tasks: List[Task],
        sort_by: str = "created"
    ) -> List[Task]:
        """
        Sort tasks by specified criteria.
        
        Args:
            tasks: List of tasks to sort
            sort_by: Sort criteria ("priority", "due_date", "created", "status")
        
        Returns:
            Sorted list of tasks
        
        Raises:
            ValidationError: If sort_by is invalid
        """
        if sort_by == "priority":
            # Sort by priority (URGENT first)
            return sorted(tasks, key=lambda t: t.priority.sort_order, reverse=True)
        
        elif sort_by == "due_date":
            # Sort by due date (earliest first, None at end)
            return sorted(
                tasks,
                key=lambda t: t.due_date if t.due_date else datetime.max
            )
        
        elif sort_by == "created":
            # Sort by creation date (newest first)
            return sorted(tasks, key=lambda t: t.created_at, reverse=True)
        
        elif sort_by == "status":
            # Sort by status (PENDING first)
            return sorted(
                tasks,
                key=lambda t: 0 if t.status == TaskStatus.PENDING else 1
            )
        
        else:
            raise ValidationError(
                f"Invalid sort_by: {sort_by}. "
                "Must be: priority, due_date, created, or status"
            )
    
    def _parse_date(self, date_str: str) -> datetime:
        """
        Parse date string in YYYY-MM-DD format.
        
        Args:
            date_str: Date string
        
        Returns:
            Datetime object
        
        Raises:
            ValidationError: If format is invalid
        """
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            raise ValidationError(
                f"Invalid date format: {date_str}. Must be YYYY-MM-DD"
            )

    def _validate_due_date(self, parsed_due_date: datetime) -> None:
        """
        Reject a due date that has already passed.

        Compared at **date** granularity, not datetime. Input arrives as
        YYYY-MM-DD, so it parses to midnight; comparing that against
        datetime.now() would reject today's date at every moment except the
        first instant of the day, while the error still claimed the present
        was allowed.

        Args:
            parsed_due_date: Parsed due date

        Raises:
            ValidationError: If the date is before today
        """
        if parsed_due_date.date() < datetime.now().date():
            raise ValidationError("Due date must be in the present or future")
