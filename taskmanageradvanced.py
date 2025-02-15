import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import json
import os

tasks = []
TASKS_FILE = "tasks.json"

def save_tasks():
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, default=str)

def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            try:
                tasks = json.load(f)
                for task in tasks:
                    task["deadline"] = datetime.strptime(task["deadline"].split()[0], "%Y-%m-%d")
            except json.JSONDecodeError:
                tasks = []

def add_task():
    task = task_entry.get().strip()
    deadline = deadline_entry.get().strip()
    priority = priority_var.get()
    
    if task and deadline:
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
            tasks.append({"task": task, "completed": False, "deadline": deadline_date, "priority": priority})
            update_task_list()
            save_tasks()
            task_entry.delete(0, tk.END)
            deadline_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date format! Use YYYY-MM-DD.")
    else:
        messagebox.showwarning("Warning", "Task and Deadline cannot be empty!")

def delete_task():
    try:
        selected_task = task_listbox.curselection()[0]
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            tasks.pop(selected_task)
            update_task_list()
            save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def mark_task_completed():
    try:
        selected_task = task_listbox.curselection()[0]
        tasks[selected_task]["completed"] = True
        update_task_list()
        save_tasks()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def edit_task():
    try:
        selected_task = task_listbox.curselection()[0]
        new_task = task_entry.get().strip()
        new_deadline = deadline_entry.get().strip()
        new_priority = priority_var.get()
        
        if new_task and new_deadline:
            try:
                new_deadline_date = datetime.strptime(new_deadline, "%Y-%m-%d")
                tasks[selected_task].update({"task": new_task, "deadline": new_deadline_date, "priority": new_priority})
                update_task_list()
                save_tasks()
                task_entry.delete(0, tk.END)
                deadline_entry.delete(0, tk.END)
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format! Use YYYY-MM-DD.")
        else:
            messagebox.showwarning("Warning", "Task and Deadline cannot be empty!")
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def update_task_list():
    task_listbox.delete(0, tk.END)
    sorted_tasks = sorted(tasks, key=lambda x: (x["completed"], x["deadline"], -x["priority"]))
    for task in sorted_tasks:
        status = "✓" if task["completed"] else "✗"
        deadline = task["deadline"].strftime("%Y-%m-%d")
        priority = "High" if task["priority"] == 3 else "Medium" if task["priority"] == 2 else "Low"
        color = "red" if not task["completed"] and task["deadline"] < datetime.today() else "white"
        task_listbox.insert(tk.END, f'{status} {task["task"]} | Due: {deadline} | Priority: {priority}')
        task_listbox.itemconfig(tk.END, fg=color)

# GUI Setup
root = tk.Tk()
root.title("Task Manager")
root.geometry("500x550")
root.configure(bg="#121212")

# Title Label
title_label = tk.Label(root, text="Task Manager", font=("Arial", 16, "bold"), bg="#121212", fg="white")
title_label.pack(pady=10)

# Task Entry Frame
frame = tk.Frame(root, bg="#121212")
frame.pack(pady=5)
task_entry = tk.Entry(frame, width=25, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
task_entry.grid(row=0, column=0, padx=5)
deadline_entry = tk.Entry(frame, width=12, font=("Arial", 12), bg="#333333", fg="white", insertbackground="white")
deadline_entry.grid(row=0, column=1, padx=5)
task_add_button = tk.Button(frame, text="Add", command=add_task, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
task_add_button.grid(row=0, column=2, padx=5)

# Priority Selection
priority_var = tk.IntVar(value=2)
priority_frame = tk.Frame(root, bg="#121212")
priority_frame.pack(pady=5)
tk.Label(priority_frame, text="Priority:", bg="#121212", fg="white", font=("Arial", 10)).pack(side=tk.LEFT)
tk.Radiobutton(priority_frame, text="Low", variable=priority_var, value=1, bg="#121212", fg="white", selectcolor="#333333").pack(side=tk.LEFT)
tk.Radiobutton(priority_frame, text="Medium", variable=priority_var, value=2, bg="#121212", fg="white", selectcolor="#333333").pack(side=tk.LEFT)
tk.Radiobutton(priority_frame, text="High", variable=priority_var, value=3, bg="#121212", fg="white", selectcolor="#333333").pack(side=tk.LEFT)

# Task Listbox
task_listbox = tk.Listbox(root, width=60, height=10, font=("Arial", 12), bg="#333333", fg="white", selectbackground="#555555", selectforeground="white")
task_listbox.pack(pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=10)
delete_button = tk.Button(button_frame, text="Delete", command=delete_task, bg="#FF5722", fg="white", font=("Arial", 10, "bold"))
delete_button.grid(row=0, column=0, padx=5)
complete_button = tk.Button(button_frame, text="Complete", command=mark_task_completed, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
complete_button.grid(row=0, column=1, padx=5)
edit_button = tk.Button(button_frame, text="Edit", command=edit_task, bg="#FFC107", fg="black", font=("Arial", 10, "bold"))
edit_button.grid(row=0, column=2, padx=5)

# Load existing tasks
load_tasks()
update_task_list()

# Run GUI
root.mainloop()
# In this snippet, we have added a new feature to edit tasks in the Task Manager application. The edit_task function is responsible for updating the task details based on the selected task in the listbox.