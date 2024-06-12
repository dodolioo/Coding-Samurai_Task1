import os
import json
import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, task_id, title):
        self.task_id = task_id
        self.title = title
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def mark_uncomplete(self):
        self.completed = False

    def __str__(self):
        status = "Complete" if self.completed else "Incomplete"
        return f"ID: {self.task_id}, Title: {self.title}, Status: {status}"

class ToDoList:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
        self.load_tasks()

    def add_task(self, title):
        task = Task(self.next_id, title)
        self.tasks.append(task)
        self.next_id += 1
        self.save_tasks()

    def list_tasks(self):
        return self.tasks

    def mark_task_complete(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                task.mark_complete()
                self.save_tasks()
                return
        raise ValueError("Task not found.")

    def delete_task(self, task_id):
        self.tasks = [task for task in self.tasks if task.task_id != task_id]
        self.save_tasks()

    def edit_task(self, task_id, new_title):
        for task in self.tasks:
            if task.task_id == task_id:
                task.title = new_title
                task.mark_uncomplete()  
                self.save_tasks()
                return
        raise ValueError("Task not found.")

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file)

    def load_tasks(self):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task(task_data['task_id'], task_data['title'])
                    task.completed = task_data['completed']
                    self.tasks.append(task)
                if self.tasks:
                    self.next_id = max(task.task_id for task in self.tasks) + 1

class ToDoListApp:
    def __init__(self, root):
        self.todo_list = ToDoList()

        self.root = root
        self.root.title("To-Do List Application")


        self.bg_color = "#f0f8ff"  # Alice Blue
        self.button_color = "#6495ed"  # Cornflower Blue
        self.button_text_color = "#ffffff"  # White
        self.frame_bg_color = "#e6e6fa"  # Lavender
        self.entry_bg_color = "#ffffff"  # White
        self.label_color = "#00008b"  # Dark Blue

        self.root.configure(bg=self.bg_color)

        self.frame = tk.Frame(root, bg=self.frame_bg_color)
        self.frame.pack(pady=20)

        self.title_label = tk.Label(self.frame, text="Title:", bg=self.frame_bg_color, fg=self.label_color)
        self.title_label.grid(row=0, column=0, padx=5, pady=5)

        self.title_entry = tk.Entry(self.frame, bg=self.entry_bg_color)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task, bg=self.button_color, fg=self.button_text_color)
        self.add_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.tasks_listbox = tk.Listbox(self.frame, width=50)
        self.tasks_listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.complete_button = tk.Button(self.frame, text="Mark Complete", command=self.mark_task_complete, bg=self.button_color, fg=self.button_text_color)
        self.complete_button.grid(row=3, column=0, padx=5, pady=5)

        self.delete_button = tk.Button(self.frame, text="Delete Task", command=self.delete_task, bg=self.button_color, fg=self.button_text_color)
        self.delete_button.grid(row=3, column=1, padx=5, pady=5)
        
        self.edit_button = tk.Button(self.frame, text="Edit Task", command=self.edit_task, bg=self.button_color, fg=self.button_text_color)
        self.edit_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.refresh_tasks()

    def add_task(self):
        title = self.title_entry.get()

        if title:
            self.todo_list.add_task(title)
            self.title_entry.delete(0, tk.END)
            self.refresh_tasks()
        else:
            messagebox.showwarning("Input Error", "Please enter a title.")

    def mark_task_complete(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            task_id = self.tasks_listbox.get(selected_task).split(",")[0].split(":")[1].strip()
            self.todo_list.mark_task_complete(int(task_id))
            self.refresh_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as complete.")

    def delete_task(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            task_id = self.tasks_listbox.get(selected_task).split(",")[0].split(":")[1].strip()
            self.todo_list.delete_task(int(task_id))
            self.refresh_tasks()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def edit_task(self):
        selected_task = self.tasks_listbox.curselection()
        if selected_task:
            task_str = self.tasks_listbox.get(selected_task)
            task_id = int(task_str.split(",")[0].split(":")[1].strip())
            old_task = next((task for task in self.todo_list.list_tasks() if task.task_id == task_id), None)

            if old_task:
                edit_window = tk.Toplevel(self.root)
                edit_window.title("Edit Task")
                edit_window.configure(bg=self.bg_color)

                title_label = tk.Label(edit_window, text="Title:", bg=self.bg_color, fg=self.label_color)
                title_label.grid(row=0, column=0, padx=5, pady=5)
                title_entry = tk.Entry(edit_window, bg=self.entry_bg_color)
                title_entry.grid(row=0, column=1, padx=5, pady=5)
                title_entry.insert(0, old_task.title)

                def save_edits():
                    new_title = title_entry.get()
                    if new_title:
                        self.todo_list.edit_task(task_id, new_title)
                        self.refresh_tasks()
                        edit_window.destroy()
                    else:
                        messagebox.showwarning("Input Error", "Please enter a title.")

                save_button = tk.Button(edit_window, text="Save", command=save_edits, bg=self.button_color, fg=self.button_text_color)
                save_button.grid(row=1, column=0, columnspan=2, pady=10)
        else:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")

    def refresh_tasks(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.todo_list.list_tasks():
            self.tasks_listbox.insert(tk.END, str(task))

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
