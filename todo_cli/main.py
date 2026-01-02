from todo_cli.storage import Storage
from todo_cli.cli import add_task_cli, view_tasks_cli, delete_task_cli, update_task_cli, mark_complete_task_cli

def main():
    """
    Main entry point for the Todo List Manager application.
    Initializes storage and runs the main menu loop, handling user choices.
    """
    print("Todo List Manager started.")
    storage = Storage()

    while True:
        print("\n┌──────────────────────────────────────────┐")
        print("│ 📝 Todo List Manager                     │")
        print("├──────────────────────────────────────────┤")
        print("│                                          │")
        print("│ 1. ➕ Add Task                            │")
        print("│ 2. 📄 View All Tasks                       │")
        print("│ 3. 🗑️ Delete Task                          │")
        print("│ 4. ✏️ Update Task                         │")
        print("│ 5. ✅ Mark as Complete/Incomplete          │")
        print("│ 0. 🚪 Exit                                 │")
        print("│                                          │")
        print("└──────────────────────────────────────────┘")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_task_cli(storage)
        elif choice == "2":
            view_tasks_cli(storage)
        elif choice == "3":
            delete_task_cli(storage)
        elif choice == "4":
            update_task_cli(storage)
        elif choice == "5":
            mark_complete_task_cli(storage)
        elif choice == "0":
            print("Exiting Todo List Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
