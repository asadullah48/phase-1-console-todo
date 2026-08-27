"""Domain models for Todo application"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List
from uuid import uuid4


class TaskStatus(Enum):
    """Task completion status"""
    PENDING = "pending"
    COMPLETED = "completed"


class Priority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    
    @property
    def sort_order(self) -> int:
        """Return numeric value for sorting (higher = more urgent)"""
        order = {
            Priority.LOW: 1,
            Priority.MEDIUM: 2,
            Priority.HIGH: 3,
            Priority.URGENT: 4,
        }
        return order[self]
    
    @property
    def display_icon(self) -> str:
        """Return visual indicator for priority"""
        icons = {
            Priority.LOW: "🟢",
            Priority.MEDIUM: "🟡",
            Priority.HIGH: "🟠",
            Priority.URGENT: "🔴",
        }
        return icons[self]


class Recurrence(Enum):
    """Task recurrence patterns"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    """
    Core domain entity representing a Todo task.
    
    Attributes:
        id: Unique identifier (UUID4)
        title: Task title (1-200 characters)
        description: Detailed description (0-1000 characters)
        status: Current completion status
        priority: Task priority level
        tags: List of categorization tags
        due_date: Optional deadline
        created_at: Creation timestamp
        updated_at: Last modification timestamp
        completed_at: Completion timestamp (if completed)
        recurrence: Optional recurrence pattern
    """
    
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    tags: List[str] = field(default_factory=list)
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    recurrence: Optional[Recurrence] = None
    
    def __post_init__(self):
        """Validate task data after initialization"""
        from .exceptions import ValidationError
        
        # Validate title
        if not self.title or not self.title.strip():
            raise ValidationError("Title cannot be empty")
        
        if len(self.title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")
        
        # Validate description
        if len(self.description) > 1000:
            raise ValidationError("Description cannot exceed 1000 characters")
        
        # Normalize tags
        self.tags = [tag.strip().lower() for tag in self.tags if tag.strip()]
    
    def mark_complete(self) -> None:
        """Mark task as completed"""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        self.updated_at = datetime.now()
    
    def mark_pending(self) -> None:
        """Mark task as pending"""
        self.status = TaskStatus.PENDING
        self.completed_at = None
        self.updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.due_date is None or self.status == TaskStatus.COMPLETED:
            return False
        return datetime.now() > self.due_date
    
    def clone_for_recurrence(self) -> "Task":
        """
        Create a new task instance for recurring tasks.
        Preserves title, description, priority, tags, and recurrence.
        Resets status to PENDING and updates due date.
        """
        from datetime import timedelta
        
        new_due_date = None
        if self.due_date and self.recurrence:
            if self.recurrence == Recurrence.DAILY:
                new_due_date = self.due_date + timedelta(days=1)
            elif self.recurrence == Recurrence.WEEKLY:
                new_due_date = self.due_date + timedelta(weeks=1)
            elif self.recurrence == Recurrence.MONTHLY:
                # Approximate monthly recurrence (30 days)
                new_due_date = self.due_date + timedelta(days=30)
        
        return Task(
            title=self.title,
            description=self.description,
            priority=self.priority,
            tags=self.tags.copy(),
            due_date=new_due_date,
            recurrence=self.recurrence,
        )
    
    def update_fields(self, **kwargs) -> None:
        """
        Update task fields dynamically.
        
        Args:
            **kwargs: Field names and values to update
        
        Raises:
            ValidationError: If attempting to update immutable fields
        """
        from .exceptions import ValidationError
        
        # Immutable fields
        immutable = {"id", "created_at"}
        
        for key, value in kwargs.items():
            if key in immutable:
                raise ValidationError(f"Cannot update immutable field: {key}")
            
            if hasattr(self, key):
                setattr(self, key, value)
        
        # Always update timestamp
        self.updated_at = datetime.now()
        
        # Re-validate after updates
        self.__post_init__()
