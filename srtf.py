import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random

class GanttChartApp:
    def __init__(self, root):  # Correcting the initialization method name
        self.root = root
        self.root.title("Gantt Chart with Table")

        self.tasks = []
        self.start_times = []
        self.durations = []
        self.finish_times = []

        # Create a frame for the GUI
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create entry widgets for user input
        self.create_input_widgets()

        # Create a canvas to display the Gantt chart
        self.gantt_canvas = FigureCanvasTkAgg(self.create_gantt_chart(), master=self.main_frame)
        self.gantt_canvas.get_tk_widget().grid(column=0, row=4, columnspan=3, pady=10)

        # Create a table to display waiting time and turnaround time
        self.create_table()

        # Create a button to start the animation
        self.start_button = ttk.Button(self.main_frame, text="Generate Gantt Chart", command=self.generate_gantt_chart)
        self.start_button.grid(column=0, row=5, columnspan=3, pady=10)

    def create_input_widgets(self):
        ttk.Label(self.main_frame, text="Tasks (comma-separated):").grid(column=0, row=1, pady=5, padx=5, sticky=tk.W)
        self.tasks_entry = ttk.Entry(self.main_frame, width=30)
        self.tasks_entry.grid(column=1, row=1, pady=5, padx=5, sticky=tk.W)

        ttk.Label(self.main_frame, text="Durations (comma-separated):").grid(column=0, row=2, pady=5, padx=5, sticky=tk.W)
        self.durations_entry = ttk.Entry(self.main_frame, width=30)
        self.durations_entry.grid(column=1, row=2, pady=5, padx=5, sticky=tk.W)

    def create_gantt_chart(self):
        fig = Figure(figsize=(8, 4), tight_layout=True)
        ax = fig.add_subplot(111)
        return fig

    def create_table(self):
        # Create a treeview widget for the table
        self.tree = ttk.Treeview(self.main_frame, columns=('Task', 'Waiting Time', 'Turnaround Time'), show='headings')
        self.tree.heading('Task', text='Task')
        self.tree.heading('Waiting Time', text='Waiting Time')
        self.tree.heading('Turnaround Time', text='Turnaround Time')
        self.tree.grid(column=0, row=6, columnspan=3, pady=10)

    def generate_gantt_chart(self):
        self.clear_gantt_chart()

        # Get user input for tasks and durations
        tasks = self.tasks_entry.get().split(',')
        durations_str = self.durations_entry.get().split(',')

        # Clean and validate input
        durations = [int(duration.strip()) if duration.strip() else 0 for duration in durations_str]

        if not all(tasks) or not all(durations):
            messagebox.showerror("Error", "All input fields must be non-empty.")
            return

        if len(tasks) != len(durations):
            messagebox.showerror("Error", "Number of tasks and durations must be the same.")
            return

        self.tasks = tasks
        self.durations = durations

        self.finish_times = self.calculate_finish_times()

        # Plot Gantt chart bars
        for i, task in enumerate(self.tasks):
            self.gantt_canvas.figure.gca().barh(task, width=self.durations[i], left=self.finish_times[i - 1] if i > 0 else 0,
                                                 color=self.get_random_color())

        # Set labels and title
        self.gantt_canvas.figure.gca().set_xlabel('Time')
        self.gantt_canvas.figure.gca().set_title('Gantt Chart')

        self.update_table()

        self.gantt_canvas.draw()

    def calculate_finish_times(self):
        finish_times = [0]
        for i in range(len(self.durations)):
            finish_times.append(finish_times[-1] + self.durations[i])
        return finish_times[1:]

    def get_random_color(self):
        return "#{:06x}".format(random.randint(0, 0xFFFFFF))

    def clear_gantt_chart(self):
        # Clear previous Gantt chart bars
        for patch in self.gantt_canvas.figure.gca().patches:
            patch.remove()

    def update_table(self):
        # Clear previous table data
        for item in self.tree.get_children():
            self.tree.delete(item)

        waiting_times, turnaround_times = self.calculate_waiting_and_turnaround_times()

        # Update table with new data
        for i, task in enumerate(self.tasks):
            self.tree.insert('', 'end', values=(task, waiting_times[i], turnaround_times[i]))

    def calculate_waiting_and_turnaround_times(self):
        waiting_times = [0]
        turnaround_times = [self.durations[0]]
        for i in range(1, len(self.durations)):
            waiting_times.append(turnaround_times[i - 1])
            turnaround_times.append(waiting_times[i] + self.durations[i])
        return waiting_times, turnaround_times

if __name__ == "__main__":  # Correcting the condition to check if the script is executed directly
    root = tk.Tk()
    app = GanttChartApp(root)
    root.mainloop()