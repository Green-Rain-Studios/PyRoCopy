import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import json

# Constants
APP_TITLE="PyRoCopy"
APP_WINSIZE="700x270"
INITIAL_DIR = os.path.join(os.getcwd(), 'jobs')
DEFAULT_THREADS = 1
OPTIONS_DICT = {
	'Normal Copy': '',
	'Mirror Directories': '/MIR',
	'Copy All File Info': '/COPYALL',
	'Move Files': '/MOV',
	'Copy in Restartable Mode': '/Z'
}

def browse_directory(var):
	var.set(filedialog.askdirectory())

def save_job():
	job = {
		"source": source_var.get(),
		"destination": destination_var.get(),
		"threads": threads_var.get(),
		"option": options_var.get()
	}
	job_file_path = filedialog.asksaveasfilename(initialdir=INITIAL_DIR, defaultextension=".json")
	if job_file_path:
		with open(job_file_path, 'w') as job_file:
			json.dump(job, job_file)

def load_job():
	job_file_path = filedialog.askopenfilename(initialdir=INITIAL_DIR, defaultextension=".json")
	if job_file_path:
		with open(job_file_path, 'r') as job_file:
			job = json.load(job_file)
		source_var.set(job["source"])
		destination_var.set(job["destination"])
		threads_var.set(job["threads"])
		options_var.set(job["option"])

def run_robocopy():
	source = source_var.get()
	destination = destination_var.get()
	if not source or not destination or not os.path.exists(source) or not os.path.exists(destination):
		messagebox.showerror("Error", "Please specify valid source and destination directories.")
		return
	option = OPTIONS_DICT[options_var.get()]
	threads = threads_var.get()
	command = f'robocopy "{source}" "{destination}" {option}'
	if int(threads) > 1:
		command += f' /MT:{threads}'

	def read_process_output(process):
		for line in iter(process.stdout.readline, b''):
			append_output(line.decode('utf-8'))
		for line in iter(process.stderr.readline, b''):
			append_output(line.decode('utf-8'))
		append_output("Copy operation completed.\n")

	def append_output(text):
		output_text.config(state='normal')
		output_text.insert(tk.END, text)
		output_text.config(state='disabled')

	output_text.config(state='normal')
	output_text.insert(tk.END, "Starting copy operation...\n")
	output_text.config(state='disabled')

	# Show the output text box
	output_text.grid(row=4, column=0, sticky='nsew')

	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	threading.Thread(target=read_process_output, args=(process,), daemon=True).start()

root = tk.Tk()
root.title(APP_TITLE)
root.geometry(APP_WINSIZE)

source_var = tk.StringVar()
destination_var = tk.StringVar()
threads_var = tk.StringVar(value=DEFAULT_THREADS)
options_var = tk.StringVar(value='Normal Copy')

tk.Entry(root, textvariable=source_var, width=30).grid(row=0, column=0, sticky='w')
tk.Button(root, text="...", command=lambda: browse_directory(source_var)).grid(row=0, column=1, sticky='w')

tk.Entry(root, textvariable=destination_var, width=30).grid(row=1, column=0, sticky='w')
tk.Button(root, text="...", command=lambda: browse_directory(destination_var)).grid(row=1, column=1, sticky='w')

tk.Label(root, text="CPU Threads").grid(row=2, column=1, sticky='w')
ttk.Combobox(root, textvariable=threads_var, values=list(range(1, os.cpu_count())), width=3).grid(row=2, column=2, sticky='w')

ttk.Combobox(root, textvariable=options_var, values=list(OPTIONS_DICT.keys()), width=30).grid(row=2, column=0, sticky='w')

tk.Button(root, text="Run Robocopy", command=lambda: threading.Thread(target=run_robocopy, daemon=True).start()).grid(row=3, column=0, sticky='w')
tk.Button(root, text="Save Job", command=save_job).grid(row=5, column=1, sticky='w')
tk.Button(root, text="Load Job", command=load_job).grid(row=5, column=2, sticky='w')

output_text = tk.Text(root, width=30, height=10, state='disabled')
output_text.grid(row=4, column=0, sticky='nsew')
# Hide the text box initially
output_text.grid_remove()

root.grid_columnconfigure(0, weight=1, minsize=270)
root.grid_rowconfigure(4, weight=1)
root.resizable(True, True)
root.mainloop()
