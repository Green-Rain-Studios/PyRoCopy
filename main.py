import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import json

root = tk.Tk()
root.title("PyRoCopy")
root.geometry('700x270')

# Get the maximum number of threads
max_threads = os.cpu_count()

# Create a list of possible thread counts
thread_counts = list(range(1, max_threads))

threads_var = tk.StringVar()
threads_var.set(1)

def browse_source():
    source_var.set(filedialog.askdirectory())

def browse_destination():
    destination_var.set(filedialog.askdirectory())

def save_job():
    job = {
        "source": source_var.get(),
        "destination": destination_var.get(),
        "threads": threads_var.get(),
        "option": options_var.get()
    }
    job_file_path = filedialog.asksaveasfilename(initialdir=os.path.join(os.getcwd(), 'jobs'), defaultextension=".json")
    if job_file_path:  # Ensure a file name was selected
        with open(job_file_path, 'w') as job_file:
            json.dump(job, job_file)

def load_job():
    job_file_path = filedialog.askopenfilename(initialdir=os.path.join(os.getcwd(), 'jobs'), defaultextension=".json")
    with open(job_file_path, 'r') as job_file:
        job = json.load(job_file)
    source_var.set(job["source"])
    destination_var.set(job["destination"])
    threads_var.set(job["threads"])
    options_var.set(job["option"])

# Create a label for the threads dropdown
threads_label = tk.Label(root, text="CPU Threads")
threads_label.grid(row=2, column=1, sticky='w')

# Create the Combobox
threads_combobox = ttk.Combobox(root, textvariable=threads_var, values=thread_counts, width=3)
threads_combobox.grid(row=2, column=2, sticky='w')

source_var = tk.StringVar()
source_entry = tk.Entry(root, textvariable=source_var, width=30)
source_entry.grid(row=0, column=0, sticky='w')
source_entry.insert(0, "Enter source directory")  # Add placeholder text
source_button = tk.Button(root, text="...", command=browse_source)
source_button.grid(row=0, column=1, sticky='w')

destination_var = tk.StringVar()
destination_entry = tk.Entry(root, textvariable=destination_var, width=30)
destination_entry.grid(row=1, column=0, sticky='w')
destination_entry.insert(0, "Enter destination directory")  # Add placeholder text
destination_button = tk.Button(root, text="...", command=browse_destination)
destination_button.grid(row=1, column=1, sticky='w')

options_dict = {'Normal Copy': '', 'Mirror Directories': '/MIR', 'Copy All File Info': '/COPYALL', 'Move Files': '/MOV', 'Copy in Restartable Mode': '/Z'}

options_var = tk.StringVar()
options_combobox = ttk.Combobox(root, textvariable=options_var, width=30)
options_combobox['values'] = list(options_dict.keys())
options_combobox.grid(row=2, column=0, sticky='w')
options_var.set('Normal Copy')  # Set the default value

run_button = tk.Button(root, text="Run Robocopy", command=lambda: threading.Thread(target=run_robocopy, daemon=True).start())
run_button.grid(row=3, column=0, sticky='w')

save_button = tk.Button(root, text="Save Job", command=save_job)
save_button.grid(row=5, column=1, sticky='w')

load_button = tk.Button(root, text="Load Job", command=load_job)
load_button.grid(row=5, column=2, sticky='w')

output_text = tk.Text(root, width=30, height=10)
output_text.grid(row=4, column=0, sticky='nsew')
output_text.config(state='disabled')

# Update the run_robocopy function
def run_robocopy():
    source = source_var.get()
    destination = destination_var.get()
    if not source or not destination or not os.path.exists(source) or not os.path.exists(destination):
        messagebox.showerror("Error", "Please specify valid source and destination directories.")
        return
    option = options_dict[options_var.get()]
    threads = threads_var.get()
    command = f'robocopy "{source}" "{destination}" {option}'
    if int(threads) > 1:
        command += f' /MT:{threads}'
    output_text.config(state='normal')
    output_text.insert(tk.END, "Starting copy operation...\n")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout:
        output_text.insert(tk.END, line)
    for line in process.stderr:
        output_text.insert(tk.END, line)
    output_text.insert(tk.END, "Copy operation completed.\n")
    output_text.config(state='disabled')

root.grid_columnconfigure(0, weight=1, minsize=270)
root.grid_rowconfigure(4, weight=1)
root.resizable(True, True)
root.mainloop()
