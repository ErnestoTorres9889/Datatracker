import tkinter as tk
from tkinter import messagebox
import os
import csv
from datetime import datetime
import threading
import time

class DataTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Tracker Application")
        
        self.data = []
        self.tracking = False
        self.track_thread = None

        self.start_button = tk.Button(root, text="Start", command=self.start_tracking)
        self.start_button.pack(pady=10)

        self.save_button = tk.Button(root, text="Save", command=self.save_data)
        self.save_button.pack(pady=10)
        self.save_button.config(state=tk.DISABLED)

        self.end_button = tk.Button(root, text="End", command=self.end_tracking)
        self.end_button.pack(pady=10)
        self.end_button.config(state=tk.DISABLED)

        self.output_text = tk.Text(root, height=10, width=50)
        self.output_text.pack(pady=10)

    def start_tracking(self):
        if not self.tracking:
            self.tracking = True
            self.save_button.config(state=tk.NORMAL)
            self.end_button.config(state=tk.NORMAL)
            self.update_output("Tracking started...")
            if not self.track_thread or not self.track_thread.is_alive():
                self.track_thread = threading.Thread(target=self.track_data)
                self.track_thread.start()
        else:
            self.update_output("Tracking is already running...")

    def track_data(self):
        while self.tracking:
            result = os.popen('netstat -e').read()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data_usage = {
                "Timestamp": timestamp,
                "Data": result
            }
            self.data.append(data_usage)
            self.update_output(f"Data tracked at {timestamp}:\n{result}")
            time.sleep(5)

    def update_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.yview(tk.END)

    def save_data(self):
        with open("data_usage.csv", "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Timestamp", "Data"])
            writer.writeheader()
            writer.writerows(self.data)
        messagebox.showinfo("Save Data", "Data saved to data_usage.csv")

    def end_tracking(self):
        if self.tracking:
            self.tracking = False
            if self.track_thread:
                self.track_thread.join()
            self.update_output("Tracking stopped.")
            self.save_button.config(state=tk.DISABLED)
            self.end_button.config(state=tk.DISABLED)
        else:
            self.update_output("Tracking is not running.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataTrackerApp(root)
    root.mainloop()