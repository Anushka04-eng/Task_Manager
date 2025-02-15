import tkinter as tk
from tkinter import messagebox

tasks = []

def add_task():
    task = task_entry.get().strip()
    if task:
        tasks.append({"task": task, "completed": False})
        update_task_list()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Task cannot be empty!")

def delete_task():
    try:
        selected_task = task_listbox.curselection()[0]
        tasks.pop(selected_task)
        update_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def mark_task_completed():
    try:
        selected_task = task_listbox.curselection()[0]
        tasks[selected_task]["completed"] = True
        update_task_list()
    except IndexError:
        messagebox.showwarning("Warning", "No task selected!")

def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✓" if task["completed"] else "✗"
        task_listbox.insert(tk.END, f'{status} {task["task"]}')

# GUI Setup
root = tk.Tk()
root.title("Task Manager")
root.geometry("400x400")
root.configure(bg="#f0f0f0")

# Title Label
title_label = tk.Label(root, text="Task Manager", font=("Arial", 16, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Task Entry
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=5)
task_entry = tk.Entry(frame, width=30, font=("Arial", 12))
task_entry.pack(side=tk.LEFT, padx=5)
task_add_button = tk.Button(frame, text="Add", command=add_task, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
task_add_button.pack(side=tk.RIGHT)

# Task Listbox
task_listbox = tk.Listbox(root, width=50, height=10, font=("Arial", 12))
task_listbox.pack(pady=10)

# Buttons
button_frame = tk.Frame(root, bg="#f0f0f0")
button_frame.pack(pady=10)
delete_button = tk.Button(button_frame, text="Delete", command=delete_task, bg="#FF5722", fg="white", font=("Arial", 10, "bold"))
delete_button.grid(row=0, column=0, padx=5)
complete_button = tk.Button(button_frame, text="Complete", command=mark_task_completed, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
complete_button.grid(row=0, column=1, padx=5)

# Run GUI
root.mainloop()
