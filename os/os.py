import psutil
import datetime
import schedule
import tkinter as tk
from tkinter import messagebox
import threading

app = tk.Tk()
app.title("Data Usage Analyzer")
app.geometry("400x250")

def monitor_process_thread():
    pid = int(entry_pid.get())
    try:
        while monitor_enabled:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            p = psutil.Process(pid)
            cpu_percent = p.cpu_percent(interval=1) / psutil.cpu_count()
            memory_mb = p.memory_full_info().rss / (1024 * 1024)
            memory_percent = p.memory_percent()
            output_text.set(
                f"Time: {current_time}\n"
                f"Process ID: {pid}\n"
                f"CPU Percent: {cpu_percent}\n"
                f"Memory (MB): {memory_mb}\n"
                f"Memory Percent: {memory_percent}"
            )
    except psutil.NoSuchProcess:
        messagebox.showerror("Error", f"Process with ID {pid} not found!")


def warning_thread():
    while warning_enabled:
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 50:
            messagebox.showwarning("Warning", f"Cpu usage is above 50%: {cpu_usage}%")

        mem_usage = psutil.virtual_memory().percent
        if mem_usage > 50:
            messagebox.showwarning("Warning", f"Memory utilization is above 50%: {mem_usage}%")


def start_analysis():
    global monitor_enabled, warning_enabled
    monitor_enabled = True
    warning_enabled = True
    process_monitor_thread = threading.Thread(target=monitor_process_thread)
    process_monitor_thread.daemon = True
    process_monitor_thread.start()

    warning_thread = threading.Thread(target=warning_thread)
    warning_thread.daemon = True
    warning_thread.start()


def stop_analysis():
    global monitor_enabled, warning_enabled
    monitor_enabled = False
    warning_enabled = False

label_pid = tk.Label(app, text="Enter Process ID:")
label_pid.pack()

entry_pid = tk.Entry(app)
entry_pid.pack()

start_button = tk.Button(app, text="Start Analysis", command=start_analysis)
start_button.pack()

stop_button = tk.Button(app, text="Stop Analysis", command=stop_analysis)
stop_button.pack()

output_text = tk.StringVar()
output_label = tk.Label(app, textvariable=output_text)
output_label.pack()

monitor_enabled = False
warning_enabled = False

app.mainloop()