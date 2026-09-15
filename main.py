#!/usr/bin/env python3
"""
Phase I: In-Memory Python Console Todo Application
Entry point for the application
"""

import sys

# The console UI prints Unicode box-drawing/emoji characters. On a stock
# Windows terminal (cp1252 codepage), that raises UnicodeEncodeError before
# the menu ever prints. Force UTF-8 on stdout/stderr so `python main.py`
# actually works out of the box, not just in UTF-8-default environments.
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

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
