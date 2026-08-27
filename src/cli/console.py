"""Console interface for Todo application"""

import sys
from typing import Optional
from ..domain.models import Task, TaskStatus, Priority, Recurrence
from ..domain.exceptions import TodoError, ValidationError, TaskNotFoundError
from ..service.todo_service import TodoService


class TodoConsole:
    """
    Interactive console interface for Todo management.
    
    Provides a menu-driven CLI for all Todo operations.
    """
    
    def __init__(self, service: TodoService):
        """
        Initialize console with a service.
        
        Args:
            service: TodoService instance
        """
        self._service = service
    
    def run(self) -> None:
        """Main application loop"""
        self._print_header()
        
        while True:
            try:
                self._print_menu()
                choice = input("\nEnter choice: ").strip()
                
                if choice == "1":
                    self._add_task()
                elif choice == "2":
                    self._view_all_tasks()
                elif choice == "3":
                    self._update_task()
                elif choice == "4":
                    self._delete_task()
                elif choice == "5":
                    self._toggle_complete()
                elif choice == "6":
                    self._search_and_filter()
                elif choice == "7":
                    print("\n👋 Goodbye!")
                    sys.exit(0)
                else:
                    print("❌ Invalid choice. Please try again.")
                
                input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                sys.exit(0)
            except TodoError as e:
                print(f"\n❌ Error: {e}")
                input("\nPress Enter to continue...")
    
    def _print_header(self) -> None:
        """Print application header"""
        print("\n" + "=" * 50)
        print("     TODO MANAGER - PHASE I")
        print("     Spec-Driven Development")
        print("=" * 50)
    
    def _print_menu(self) -> None:
        """Print main menu"""
        print("\n" + "─" * 50)
        print("MAIN MENU")
        print("─" * 50)
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete/Incomplete")
        print("6. Search & Filter")
        print("7. Exit")
        print("─" * 50)
    
    def _add_task(self) -> None:
        """Add a new task"""
        print("\n" + "─" * 50)
        print("ADD NEW TASK")
        print("─" * 50)
        
        try:
            title = input("Enter title: ").strip()
            if not title:
                raise ValidationError("Title cannot be empty")
            
            description = input("Enter description (optional): ").strip()
            
            # Priority
            priority_input = input(
                "Enter priority (low/medium/high/urgent) [medium]: "
            ).strip().lower() or "medium"
            
            try:
                priority = Priority[priority_input.upper()]
            except KeyError:
                raise ValidationError(
                    "Invalid priority. Must be: low, medium, high, urgent"
                )
            
            # Tags
            tags_input = input("Enter tags (comma-separated, optional): ").strip()
            tags = [t.strip() for t in tags_input.split(",") if t.strip()]
            
            # Due date
            due_date = input("Enter due date (YYYY-MM-DD, optional): ").strip() or None
            
            # Recurrence
            recurrence_input = input(
                "Create recurring? (daily/weekly/monthly/no) [no]: "
            ).strip().lower() or "no"
            
            recurrence = None
            if recurrence_input != "no":
                try:
                    recurrence = Recurrence[recurrence_input.upper()]
                except KeyError:
                    raise ValidationError(
                        "Invalid recurrence. Must be: daily, weekly, monthly, no"
                    )
            
            # Create task
            task = self._service.add_task(
                title=title,
                description=description,
                priority=priority,
                tags=tags,
                due_date=due_date,
                recurrence=recurrence,
            )
            
            print(f"\n✅ Task created successfully!")
            print(f"ID: {task.id}")
        
        except TodoError as e:
            print(f"\n❌ Error: {e}")
    
    def _view_all_tasks(self) -> None:
        """View all tasks"""
        print("\n" + "─" * 50)
        print("ALL TASKS")
        print("─" * 50)
        
        tasks = self._service.get_all_tasks()
        
        if not tasks:
            print("\nNo tasks found.")
            return
        
        # Ask for sorting
        print("\nSort by:")
        print("1. Priority (default)")
        print("2. Due Date")
        print("3. Created Date")
        print("4. Status")
        
        sort_choice = input("\nEnter choice [1]: ").strip() or "1"
        
        sort_map = {
            "1": "priority",
            "2": "due_date",
            "3": "created",
            "4": "status",
        }
        
        sort_by = sort_map.get(sort_choice, "priority")
        tasks = self._service.sort_tasks(tasks, sort_by)
        
        print(f"\n📋 Total: {len(tasks)} task(s)\n")
        
        for idx, task in enumerate(tasks, 1):
            self._print_task(task, idx)
    
    def _print_task(self, task: Task, number: Optional[int] = None) -> None:
        """
        Print a single task in formatted style.
        
        Args:
            task: Task to print
            number: Optional numbering
        """
        prefix = f"[{number}] " if number else ""
        status_icon = "✅" if task.status == TaskStatus.COMPLETED else "⏳"
        
        print(f"{prefix}{task.priority.display_icon} {task.priority.value.upper()} | {status_icon} {task.status.value.upper()}")
        print(f"    {task.title}")
        
        # Due date
        if task.due_date:
            due_str = task.due_date.strftime("%Y-%m-%d")
            if task.is_overdue():
                print(f"    ⚠️  OVERDUE: {due_str}")
            else:
                print(f"    📅 Due: {due_str}")
        
        # Tags
        if task.tags:
            print(f"    🏷️  Tags: {', '.join(task.tags)}")
        
        # Recurrence
        if task.recurrence:
            print(f"    🔄 Recurs: {task.recurrence.value}")
        
        # Description
        if task.description:
            print(f"    📝 {task.description}")
        
        # Metadata
        print(f"    🆔 ID: {task.id}")
        print(f"    🕐 Created: {task.created_at.strftime('%Y-%m-%d %H:%M')}")
        
        if task.completed_at:
            print(f"    ✓ Completed: {task.completed_at.strftime('%Y-%m-%d %H:%M')}")
        
        print()
    
    def _update_task(self) -> None:
        """Update a task"""
        print("\n" + "─" * 50)
        print("UPDATE TASK")
        print("─" * 50)
        
        task_id = input("Enter task ID: ").strip()
        
        try:
            task = self._service.get_task_by_id(task_id)
            print("\nCurrent task:")
            self._print_task(task)
            
            print("Enter new values (press Enter to keep current):\n")
            
            updates = {}
            
            # Title
            new_title = input(f"Title [{task.title}]: ").strip()
            if new_title:
                updates["title"] = new_title
            
            # Description
            new_desc = input(f"Description [{task.description}]: ").strip()
            if new_desc:
                updates["description"] = new_desc
            
            # Priority
            new_priority = input(
                f"Priority [{task.priority.value}] (low/medium/high/urgent): "
            ).strip().lower()
            if new_priority:
                try:
                    updates["priority"] = Priority[new_priority.upper()]
                except KeyError:
                    raise ValidationError("Invalid priority")
            
            # Tags
            new_tags = input(
                f"Tags [{', '.join(task.tags)}] (comma-separated): "
            ).strip()
            if new_tags:
                updates["tags"] = [t.strip() for t in new_tags.split(",") if t.strip()]
            
            # Due date
            current_due = task.due_date.strftime("%Y-%m-%d") if task.due_date else "None"
            new_due = input(f"Due date [{current_due}] (YYYY-MM-DD): ").strip()
            if new_due:
                updates["due_date"] = new_due
            
            if updates:
                updated_task = self._service.update_task(task_id, **updates)
                print("\n✅ Task updated successfully!")
                self._print_task(updated_task)
            else:
                print("\n⚠️  No changes made.")
        
        except TodoError as e:
            print(f"\n❌ Error: {e}")
    
    def _delete_task(self) -> None:
        """Delete a task"""
        print("\n" + "─" * 50)
        print("DELETE TASK")
        print("─" * 50)
        
        task_id = input("Enter task ID: ").strip()
        
        try:
            task = self._service.get_task_by_id(task_id)
            print("\nTask to delete:")
            self._print_task(task)
            
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            
            if confirm == "yes":
                self._service.delete_task(task_id)
                print("\n✅ Task deleted successfully!")
            else:
                print("\n⚠️  Deletion cancelled.")
        
        except TodoError as e:
            print(f"\n❌ Error: {e}")
    
    def _toggle_complete(self) -> None:
        """Toggle task completion status"""
        print("\n" + "─" * 50)
        print("MARK COMPLETE/INCOMPLETE")
        print("─" * 50)
        
        task_id = input("Enter task ID: ").strip()
        
        try:
            task = self._service.toggle_complete(task_id)
            
            if task.status == TaskStatus.COMPLETED:
                print("\n✅ Task marked as COMPLETED!")
                if task.recurrence:
                    print("🔄 Next recurring instance created.")
            else:
                print("\n⏳ Task marked as PENDING!")
            
            self._print_task(task)
        
        except TodoError as e:
            print(f"\n❌ Error: {e}")
    
    def _search_and_filter(self) -> None:
        """Search and filter tasks"""
        print("\n" + "─" * 50)
        print("SEARCH & FILTER")
        print("─" * 50)
        
        print("\nEnter search criteria (press Enter to skip):\n")
        
        query = input("Search in title: ").strip() or None
        tag = input("Filter by tag: ").strip() or None
        
        # Status filter
        status_input = input("Filter by status (pending/completed): ").strip().lower()
        status = None
        if status_input:
            try:
                status = TaskStatus[status_input.upper()]
            except KeyError:
                print("⚠️  Invalid status, ignoring filter.")
        
        # Priority filter
        priority_input = input(
            "Filter by priority (low/medium/high/urgent): "
        ).strip().lower()
        priority = None
        if priority_input:
            try:
                priority = Priority[priority_input.upper()]
            except KeyError:
                print("⚠️  Invalid priority, ignoring filter.")
        
        # Search
        tasks = self._service.search_tasks(
            query=query,
            tag=tag,
            status=status,
            priority=priority,
        )
        
        if not tasks:
            print("\n❌ No tasks found matching criteria.")
            return
        
        # Ask for sorting
        print("\nSort by:")
        print("1. Priority (default)")
        print("2. Due Date")
        print("3. Created Date")
        print("4. Status")
        
        sort_choice = input("\nEnter choice [1]: ").strip() or "1"
        
        sort_map = {
            "1": "priority",
            "2": "due_date",
            "3": "created",
            "4": "status",
        }
        
        sort_by = sort_map.get(sort_choice, "priority")
        tasks = self._service.sort_tasks(tasks, sort_by)
        
        print(f"\n📋 Found: {len(tasks)} task(s)\n")
        
        for idx, task in enumerate(tasks, 1):
            self._print_task(task, idx)
