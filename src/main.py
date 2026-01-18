from src.repository import TaskRepository
from src.services.task_service import TaskService
from src.cli.commands import add_task_command, view_tasks_command, update_task_command, delete_task_command, mark_task_complete_command

def main():
    repository = TaskRepository()
    task_service = TaskService(repository)

    try:
        while True:
            print("\n--- Todo App Menu ---")
            print("1. Add Task")
            print("2. View Tasks")
            print("3. Update Task")
            print("4. Delete Task")
            print("5. Mark Task Complete/Incomplete")
            print("6. Exit")
            choice = input("Enter your choice: ")

            if choice == '1':
                add_task_command(task_service)
            elif choice == '2':
                view_tasks_command(task_service)
            elif choice == '3':
                update_task_command(task_service)
            elif choice == '4':
                delete_task_command(task_service)
            elif choice == '5':
                mark_task_complete_command(task_service)
            elif choice == '6':
                print("Exiting Todo App. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Exiting Todo App due to an error.")
if __name__ == "__main__":
    main()
