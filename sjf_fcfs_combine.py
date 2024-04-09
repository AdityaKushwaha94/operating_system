import tkinter as tk
from tkinter import ttk, messagebox
import random
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduler")

        self.tasks = []
        self.burst_times = []

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_input_widgets()
        self.create_output_widgets()

    def create_input_widgets(self):
        ttk.Label(self.main_frame, text="Tasks and Burst Times (e.g., T1:10, T2:8, T3:12):").grid(column=0, row=0, columnspan=2, pady=5, padx=5, sticky=tk.W)
        self.tasks_burst_entry = ttk.Entry(self.main_frame, width=50)
        self.tasks_burst_entry.grid(column=0, row=1, columnspan=2, pady=5, padx=5, sticky=tk.W)

        self.start_button = ttk.Button(self.main_frame, text="Generate Schedule", command=self.generate_schedule)
        self.start_button.grid(column=0, row=2, columnspan=2, pady=10)

    def create_output_widgets(self):
        self.output_frame_left = ttk.Frame(self.main_frame)
        self.output_frame_left.grid(column=0, row=3, padx=10, pady=10, sticky='nsew')

        self.output_frame_right = ttk.Frame(self.main_frame)
        self.output_frame_right.grid(column=1, row=3, padx=10, pady=10, sticky='nsew')

        # FCFS Table and Gantt Chart
        self.tree_fcfs = ttk.Treeview(self.output_frame_left, columns=('Task', 'Burst Time', 'Start Time', 'End Time'), show='headings')
        self.tree_fcfs.heading('Task', text='Task')
        self.tree_fcfs.heading('Burst Time', text='Burst Time')
        self.tree_fcfs.heading('Start Time', text='Start Time')
        self.tree_fcfs.heading('End Time', text='End Time')
        self.tree_fcfs.pack(side='top', expand=True, fill='both')

        self.fig_fcfs = Figure(figsize=(5, 4))
        self.ax_fcfs = self.fig_fcfs.add_subplot(111)
        self.canvas_fcfs = FigureCanvasTkAgg(self.fig_fcfs, master=self.output_frame_left)
        self.canvas_fcfs.get_tk_widget().pack(side='top', expand=True, fill='both')

        # SJF Table and Gantt Chart
        self.tree_sjf = ttk.Treeview(self.output_frame_right, columns=('Task', 'Burst Time', 'Start Time', 'End Time'), show='headings')
        self.tree_sjf.heading('Task', text='Task')
        self.tree_sjf.heading('Burst Time', text='Burst Time')
        self.tree_sjf.heading('Start Time', text='Start Time')
        self.tree_sjf.heading('End Time', text='End Time')
        self.tree_sjf.pack(side='top', expand=True, fill='both')

        self.fig_sjf = Figure(figsize=(5, 4))
        self.ax_sjf = self.fig_sjf.add_subplot(111)
        self.canvas_sjf = FigureCanvasTkAgg(self.fig_sjf, master=self.output_frame_right)
        self.canvas_sjf.get_tk_widget().pack(side='top', expand=True, fill='both')

    def generate_schedule(self):
        # Clear previous data
        self.clear_output()

        # Parse input for tasks and burst times
        input_text = self.tasks_burst_entry.get().strip()
        if not input_text:
            messagebox.showerror("Error", "Please enter tasks and burst times.")
            return

        try:
            task_burst_pairs = [pair.strip() for pair in input_text.split(',')]
            self.tasks = []
            self.burst_times = []

            for pair in task_burst_pairs:
                task, burst_time = pair.split(':')
                self.tasks.append(task.strip())
                self.burst_times.append(int(burst_time.strip()))

        except ValueError:
            messagebox.showerror("Error", "Invalid input format. Use 'Task: Burst Time' format (e.g., T1:10, T2:8).")
            return

        # Generate FCFS and SJF schedules
        fcfs_schedule = self.schedule_fcfs()
        sjf_schedule = self.schedule_sjf()

        # Update FCFS table and chart
        self.populate_table(self.tree_fcfs, fcfs_schedule)
        self.plot_gantt_chart(self.ax_fcfs, fcfs_schedule, "FCFS Gantt Chart")

        # Update SJF table and chart
        self.populate_table(self.tree_sjf, sjf_schedule)
        self.plot_gantt_chart(self.ax_sjf, sjf_schedule, "SJF Gantt Chart")

    def schedule_fcfs(self):
        schedule = []
        current_time = 0

        for task, burst_time in zip(self.tasks, self.burst_times):
            start_time = current_time
            end_time = current_time + burst_time
            schedule.append((task, burst_time, start_time, end_time))
            current_time = end_time

        return schedule

    def schedule_sjf(self):
        tasks_with_burst = sorted(list(zip(self.tasks, self.burst_times)), key=lambda x: x[1])
        schedule = []
        current_time = 0

        for task, burst_time in tasks_with_burst:
            start_time = current_time
            end_time = current_time + burst_time
            schedule.append((task, burst_time, start_time, end_time))
            current_time = end_time

        return schedule

    def populate_table(self, tree, schedule):
        for item in tree.get_children():
            tree.delete(item)

        for data in schedule:
            tree.insert('', 'end', values=data)

    def plot_gantt_chart(self, ax, schedule, title):
        ax.clear()

        task_names = [data[0] for data in schedule]
        start_times = [data[2] for data in schedule]
        durations = [data[1] for data in schedule]

        colors = [self.get_random_color() for _ in task_names]  # Generate random colors for tasks

        ax.barh(task_names, durations, left=start_times, color=colors)
        ax.set_xlabel('Time')
        ax.set_title(title)
        ax.invert_yaxis()

        ax.figure.canvas.draw()

    def get_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def clear_output(self):
        self.tree_fcfs.delete(*self.tree_fcfs.get_children())
        self.ax_fcfs.clear()
        self.canvas_fcfs.draw()

        self.tree_sjf.delete(*self.tree_sjf.get_children())
        self.ax_sjf.clear()
        self.canvas_sjf.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
