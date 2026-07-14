#!/usr/bin/env python3
"""TaskLite: a tiny command-line to-do list manager.

Tasks are stored as a JSON list in tasks.json, in the current directory.
"""

import json
import sys
from pathlib import Path

TASKS_FILE = Path("tasks.json")


def load_tasks():
    """Return the list of tasks, or an empty list if none exist yet."""
    if not TASKS_FILE.exists():
        return []
    with open(TASKS_FILE) as f:
        return json.load(f)


def save_tasks(tasks):
    """Write the given list of tasks back to tasks.json."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(description, priority="normal"):
    """Add a new, not-yet-done task with the given description."""
    tasks = load_tasks()
    tasks.append(
        {
            "description": description,
            "priority": priority,
            "done": False,
        }
    )
    save_tasks(tasks)
    print(f"Added: {description}")


def sort_by_priority(tasks):
    """Sort tasks so high-priority tasks come first, then normal, then low."""
    priority_order = {"high": 0, "normal": 1, "low": 2}
    return sorted(tasks, key=lambda task: priority_order.get(task["priority"], 1))


def list_tasks(sort=False):
    """Print all tasks with a status checkbox and a display number."""
    tasks = load_tasks()

    if sort:
        tasks = sort_by_priority(tasks)

    if not tasks:
        print('No tasks yet. Add one with: tasklite add "buy milk"')
        return

    for i, task in enumerate(tasks):
        status = "x" if task["done"] else " "
        print(f"[{status}] {i + 1}. {task['description']}")


def mark_done(index):
    """Mark a task as completed."""
    tasks = load_tasks()

    if index < 1 or index > len(tasks):
        print("No such task.")
        return

    tasks[index - 1]["done"] = True
    save_tasks(tasks)
    print(f"Marked task {index} as done.")


def remove_task(index):
    """Remove a task."""
    tasks = load_tasks()

    if index < 1 or index > len(tasks):
        print("No such task.")
        return

    removed = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f"Removed: {removed['description']}")


def clear_tasks():
    """Delete all tasks after user confirmation."""
    tasks = load_tasks()

    if not tasks:
        print("No tasks to clear.")
        return

    confirm = input(
        "Are you sure you want to delete all tasks? Type 'yes' to confirm: "
    )

    if confirm.strip().lower() == "yes":
        save_tasks([])
        print("All tasks have been deleted.")
    else:
        print("Operation cancelled.")


def main():
    if len(sys.argv) < 2:
        print("Usage: tasklite <add|list|done|remove|clear> [args]")
        return

    command = sys.argv[1]

    if command == "add":
        description = " ".join(sys.argv[2:])
        if not description:
            print("Please provide a task description.")
            return
        add_task(description)

    elif command == "list":
        sort = "--sort" in sys.argv
        list_tasks(sort=sort)

    elif command == "done":
        if len(sys.argv) < 3:
            print("Usage: tasklite done <task_number>")
            return
        mark_done(int(sys.argv[2]))

    elif command == "remove":
        if len(sys.argv) < 3:
            print("Usage: tasklite remove <task_number>")
            return
        remove_task(int(sys.argv[2]))

    elif command == "clear":
        clear_tasks()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
