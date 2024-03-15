import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class SJFApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shortest Job First (SJF)")

        self.tasks = []
        self.arrival_times = []
        self.burst_times = []

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_input_widgets()

        self.gantt_canvas = FigureCanvasTkAgg(self.create_gantt_chart(), master=self.main_frame)
        self.gantt_canvas.get_tk_widget().grid(column=0, row=3, columnspan=2, pady=10)

        self.create_table()

        self.start_button = ttk.Button(self.main_frame, text="Generate Gantt Chart", command=self.generate_gantt_chart)
        self.start_button.grid(column=0, row=4, columnspan=2, pady=10)

    def create_input_widgets(self):
        ttk.Label(self.main_frame, text="Tasks (comma-separated):").grid(column=0, row=0, pady=5, padx=5, sticky=tk.W)
        self.tasks_entry = ttk.Entry(self.main_frame, width=30)
        self.tasks_entry.grid(column=1, row=0, pady=5, padx=5, sticky=tk.W)

        ttk.Label(self.main_frame, text="Arrival Times (comma-separated):").grid(column=0, row=1, pady=5, padx=5, sticky=tk.W)
        self.arrival_times_entry = ttk.Entry(self.main_frame, width=30)
        self.arrival_times_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)

        ttk.Label(self.main_frame, text="Burst Times (comma-separated):").grid(column=0, row=2, pady=5, padx=5, sticky=tk.W)
        self.burst_times_entry = ttk.Entry(self.main_frame, width=30)
        self.burst_times_entry.grid(column=1, row=2, pady=5, padx=5, sticky=tk.W)

    def create_gantt_chart(self):
        fig = Figure(figsize=(8, 4), tight_layout=True)
        ax = fig.add_subplot(111)
        return fig

    def create_table(self):
        self.tree = ttk.Treeview(self.main_frame, columns=('Task', 'Arrival Time', 'Burst Time', 'Start Time', 'Finish Time'), show='headings')
        self.tree.heading('Task', text='Task')
        self.tree.heading('Arrival Time', text='Arrival Time')
        self.tree.heading('Burst Time', text='Burst Time')
        self.tree.heading('Start Time', text='Start Time')
        self.tree.heading('Finish Time', text='Finish Time')
        self.tree.grid(column=0, row=5, columnspan=2, pady=10)

    def generate_gantt_chart(self):
        self.clear_gantt_chart()

        tasks = self.tasks_entry.get().split(',')
        arrival_times_str = self.arrival_times_entry.get().split(',')
        burst_times_str = self.burst_times_entry.get().split(',')

        try:
            self.tasks = tasks
            self.arrival_times = [int(time.strip()) for time in arrival_times_str]
            self.burst_times = [int(time.strip()) for time in burst_times_str]
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers for arrival times and burst times.")
            return

        if not all(self.tasks) or not all(self.arrival_times) or not all(self.burst_times):
            messagebox.showerror("Error", "All input fields must be non-empty.")
            return

        if len(self.tasks) != len(self.arrival_times) or len(self.tasks) != len(self.burst_times):
            messagebox.showerror("Error", "Number of tasks, arrival times, and burst times must be the same.")
            return

        sorted_tasks, sorted_arrival_times, sorted_burst_times = zip(*sorted(zip(self.tasks, self.arrival_times, self.burst_times), key=lambda x: x[2]))

        self.plot_gantt_chart(sorted_tasks, sorted_arrival_times, sorted_burst_times)
        self.update_table()

    def plot_gantt_chart(self, sorted_tasks, sorted_arrival_times, sorted_burst_times):
        current_time = 0
        for task, arrival_time, burst_time in zip(sorted_tasks, sorted_arrival_times, sorted_burst_times):
            if current_time < arrival_time:
                current_time = arrival_time
            self.gantt_canvas.figure.gca().barh(task, width=burst_time, left=current_time, color=self.get_random_color())
            current_time += burst_time

        self.gantt_canvas.figure.gca().set_xlabel('Time')
        self.gantt_canvas.figure.gca().set_title('Gantt Chart')
        self.gantt_canvas.draw()

    def get_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def clear_gantt_chart(self):
        for patch in self.gantt_canvas.figure.gca().patches:
            patch.remove()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        current_time = 0
        for i, task in enumerate(self.tasks):
            start_time = max(current_time, self.arrival_times[i])
            finish_time = start_time + self.burst_times[i]
            self.tree.insert('', 'end', values=(task, self.arrival_times[i], self.burst_times[i], start_time, finish_time))
            current_time = finish_time

if __name__ == "__main__":
    root = tk.Tk()
    app = SJFApp(root)
    root.mainloop()
