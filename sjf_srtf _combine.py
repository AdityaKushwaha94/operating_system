import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class SchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scheduler")

        self.tasks = []
        self.burst_times = []

        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.create_input_widgets()

        self.gantt_canvas_sjf = FigureCanvasTkAgg(self.create_gantt_chart(), master=self.main_frame)
        self.gantt_canvas_sjf.get_tk_widget().grid(column=0, row=3, pady=10)
        self.gantt_canvas_srtf = FigureCanvasTkAgg(self.create_gantt_chart(), master=self.main_frame)
        self.gantt_canvas_srtf.get_tk_widget().grid(column=1, row=3, pady=10)

        self.create_table()

        self.start_button = ttk.Button(self.main_frame, text="Generate Gantt Charts", command=self.generate_gantt_charts)
        self.start_button.grid(column=0, row=4, columnspan=2, pady=10)

    def create_input_widgets(self):
        ttk.Label(self.main_frame, text="Tasks (comma-separated):").grid(column=0, row=0, pady=5, padx=5, sticky=tk.W)
        self.tasks_entry = ttk.Entry(self.main_frame, width=30)
        self.tasks_entry.grid(column=1, row=0, pady=5, padx=5, sticky=tk.W)

        ttk.Label(self.main_frame, text="Burst Times (comma-separated):").grid(column=0, row=1, pady=5, padx=5, sticky=tk.W)
        self.burst_times_entry = ttk.Entry(self.main_frame, width=30)
        self.burst_times_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)

    def create_gantt_chart(self):
        fig = Figure(figsize=(8, 4), tight_layout=True)
        ax = fig.add_subplot(111)
        return fig

    def create_table(self):
        self.tree_sjf = ttk.Treeview(self.main_frame, columns=('Task', 'Burst Time', 'Turnaround Time', 'Waiting Time'), show='headings')
        self.tree_sjf.heading('Task', text='Task')
        self.tree_sjf.heading('Burst Time', text='Burst Time')
        self.tree_sjf.heading('Turnaround Time', text='Turnaround Time')
        self.tree_sjf.heading('Waiting Time', text='Waiting Time')
        self.tree_sjf.grid(column=0, row=5, pady=10)
        
        self.tree_srtf = ttk.Treeview(self.main_frame, columns=('Task', 'Burst Time', 'Turnaround Time', 'Waiting Time'), show='headings')
        self.tree_srtf.heading('Task', text='Task')
        self.tree_srtf.heading('Burst Time', text='Burst Time')
        self.tree_srtf.heading('Turnaround Time', text='Turnaround Time')
        self.tree_srtf.heading('Waiting Time', text='Waiting Time')
        self.tree_srtf.grid(column=1, row=5, pady=10)

    def generate_gantt_charts(self):
        self.clear_gantt_charts()

        tasks = self.tasks_entry.get().split(',')
        burst_times_str = self.burst_times_entry.get().split(',')

        try:
            self.tasks = tasks
            self.burst_times = [int(time.strip()) for time in burst_times_str]
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter numbers for burst times.")
            return

        if not all(self.tasks) or not all(self.burst_times):
            messagebox.showerror("Error", "All input fields must be non-empty.")
            return

        if len(self.tasks) != len(self.burst_times):
            messagebox.showerror("Error", "Number of tasks and burst times must be the same.")
            return

        self.run_sjf()
        self.run_srtf()

    def run_sjf(self):
        current_time = 0
        remaining_burst_times = self.burst_times.copy()
        tasks_completed = 0
        gantt_chart_data = []

        while tasks_completed < len(self.tasks):
            remaining_tasks = [(i, burst_time) for i, burst_time in enumerate(remaining_burst_times) if burst_time > 0]
            shortest_task_index, shortest_burst_time = min(remaining_tasks, key=lambda x: x[1])
            task = self.tasks[shortest_task_index]
            gantt_chart_data.append((current_time, task))
            current_time += 1
            remaining_burst_times[shortest_task_index] -= 1

            if remaining_burst_times[shortest_task_index] == 0:
                tasks_completed += 1

        self.plot_gantt_chart(gantt_chart_data, self.gantt_canvas_sjf)
        self.update_table(gantt_chart_data, self.tree_sjf)

    def run_srtf(self):
        current_time = 0
        remaining_burst_times = self.burst_times.copy()
        tasks_completed = 0
        gantt_chart_data = []

        while tasks_completed < len(self.tasks):
            remaining_tasks = [(i, burst_time) for i, burst_time in enumerate(remaining_burst_times) if burst_time > 0]
            shortest_task_index, shortest_burst_time = min(remaining_tasks, key=lambda x: x[1])
            task = self.tasks[shortest_task_index]
            gantt_chart_data.append((current_time, task))
            current_time += 1
            remaining_burst_times[shortest_task_index] -= 1

            if remaining_burst_times[shortest_task_index] == 0:
                tasks_completed += 1

        self.plot_gantt_chart(gantt_chart_data, self.gantt_canvas_srtf)
        self.update_table(gantt_chart_data, self.tree_srtf)

    def plot_gantt_chart(self, gantt_chart_data, canvas):
        ax = canvas.figure.add_subplot(111)
        gantt_colors = {task: self.get_random_color() for _, task in gantt_chart_data}
        prev_task = None
        for time, task in gantt_chart_data:
            if task != prev_task:
                ax.barh(task, width=1, left=time, color=gantt_colors[task], label=task)
            else:
                ax.barh(task, width=1, left=time, color=gantt_colors[task])
            prev_task = task

        ax.set_xlabel('Time')
        ax.set_title('Gantt Chart')
        ax.legend(loc='upper right')
        canvas.draw()

    def get_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def clear_gantt_charts(self):
        self.gantt_canvas_sjf.figure.clear()
        self.gantt_canvas_sjf.draw()
        self.gantt_canvas_srtf.figure.clear()
        self.gantt_canvas_srtf.draw()

    def update_table(self, gantt_chart_data, tree):
        for item in tree.get_children():
            tree.delete(item)

        task_completion_times = {}
        for time, task in gantt_chart_data:
            if task not in task_completion_times:
                task_completion_times[task] = time

        for task in self.tasks:
            finish_time = task_completion_times.get(task, 0)
            turnaround_time = finish_time
            waiting_time = turnaround_time - self.burst_times[self.tasks.index(task)]
            tree.insert('', 'end', values=(task, self.burst_times[self.tasks.index(task)], turnaround_time, waiting_time))

if __name__ == "__main__":
    root = tk.Tk()
    app = SchedulerApp(root)
    root.mainloop()
