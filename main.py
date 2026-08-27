#!/usr/bin/env python3
"""
Phase I: In-Memory Python Console Todo Application
Entry point for the application
"""

from src.repository.memory import InMemoryTodoRepository
from src.service.todo_service import TodoService
from src.cli.console import TodoConsole


def main():
    """Initialize and run the Todo application"""
    # Dependency injection: Repository -> Service -> Console
    repository = InMemoryTodoRepository()
    service = TodoService(repository)
    console = TodoConsole(service)
    
    # Run the application
    console.run()


if __name__ == "__main__":
    main()
