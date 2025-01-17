from tkinter import Tk, Label, StringVar, OptionMenu, Button, Toplevel, Entry, Frame, PhotoImage, messagebox
from algorithms import Algorithms
from process import Process
import tkinter as ttk
from random import randint, choice

def create_process_objects():
    """Create a list of Process objects from the GUI input"""
    processes = []
    is_priority = "Priority" in selected_option.get()
    
    for i, row in enumerate(process_rows):
        p_id = f"P{i+1}"
        arrival_time = int(row[2].get())
        burst_time = int(row[1].get())
        
        if is_priority:
            priority = int(row[3].get())
            process = Process(p_id, arrival_time, burst_time, priority)
        else:
            process = Process(p_id, arrival_time, burst_time)
            
        processes.append(process)
    
    return processes

def get_algorithm_details():
    """Get algorithm name and quantum value if applicable"""
    algo_name = selected_option.get()
    if "Round Robin" in algo_name:
        return [algo_name, int(quantum_entry.get())]
    return [algo_name, None]

def create_window():
    if validate_inputs():
        # Create the tuple with algorithm details and process objects
        algo_details = get_algorithm_details()
        processes = create_process_objects()
        
        algo=Algorithms()
        match algo_details[0]:
            case "First Come First Served (FCFS)":
                processes=algo.fcfs(processes)
            case "Non-Preemptive Shortest Job First (SJF)":
                processes=algo.sjf_nonpreemptive(processes)
            case "Preemptive Shortest Job First (SJF)":
                processes=algo.sjf_preemptive(processes)
            case "Round Robin (RR)":
                processes=algo.roundRobin(processes, algo_details[1])
            case "Non-Preemptive Priority Scheduling":
                processes=algo.priority_non_preemptive(processes)
            case "Preemptive Priority Scheduling":
                processes=algo.premptive_priority(processes)     
        
        # Create new window
        new_window = Toplevel(window)
        new_window.geometry("1000x600")
        new_window.title("Process Details")
        
        # Main container
        main_frame = Frame(new_window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Algorithm Details Section
        algo_frame = Frame(main_frame)
        algo_frame.pack(fill='x', pady=(0, 20))
        
        Label(algo_frame, text="Algorithm Details", font=("Verdana", 16, "bold")).pack()
        Label(algo_frame, text=f"Algorithm: {algo_details[0]}", font=("Verdana", 12)).pack()
        if algo_details[1]:
            Label(algo_frame, text=f"Time Quantum: {algo_details[1]}", font=("Verdana", 12)).pack()
        
        # Process Table Section
        table_frame = Frame(main_frame)
        table_frame.pack(fill='x', pady=(0, 20))
        
        Label(table_frame, text="Process Details", font=("Verdana", 16, "bold")).pack(pady=(0, 10))
        
        # Create table headers
        headers = ["Process ID", "Arrival Time", "Burst Time"]
        if "Priority" in algo_details[0]:
            headers.extend(["Priority"])
        headers.extend(["Turnaround Time", "Waiting Time", "Response Time"])
        
        # Table container with grid
        grid_frame = Frame(table_frame)
        grid_frame.pack(fill='x')
        
        # Style for headers and cells
        header_style = ("Verdana", 10, "bold")
        cell_style = ("Verdana", 10)
        
        # Add headers
        for col, header in enumerate(headers):
            Label(grid_frame, text=header, font=header_style, borderwidth=1, relief="solid", 
                  width=15, padx=5, pady=5).grid(row=0, column=col, sticky="nsew")
        
        # Calculate averages while adding process data
        total_turnaround = 0
        total_waiting = 0
        total_response = 0
        
        # Add process data
        for row, process in enumerate(processes, start=1):
            # Basic process info
            Label(grid_frame, text=process.p_id, font=cell_style, borderwidth=1, relief="solid",
                  width=15, padx=5, pady=5).grid(row=row, column=0, sticky="nsew")
            Label(grid_frame, text=str(process.arrival_time), font=cell_style, borderwidth=1, relief="solid",
                  width=15, padx=5, pady=5).grid(row=row, column=1, sticky="nsew")
            Label(grid_frame, text=str(process.burst_time), font=cell_style, borderwidth=1, relief="solid",
                  width=15, padx=5, pady=5).grid(row=row, column=2, sticky="nsew")
            
            current_col = 3
            
            # Priority if applicable
            if "Priority" in algo_details[0]:
                Label(grid_frame, text=str(process.priority), font=cell_style, borderwidth=1, relief="solid",
                      width=15, padx=5, pady=5).grid(row=row, column=current_col, sticky="nsew")
                current_col += 1
            
            # Time metrics
            Label(grid_frame, text=f"{process.turnaround_time:.2f}", font=cell_style, borderwidth=1, relief="solid",
                  width=15, padx=5, pady=5).grid(row=row, column=current_col, sticky="nsew")
            Label(grid_frame, text=f"{process.waiting_time:.2f}", font=cell_style, borderwidth=1, relief="solid",
                  width=15, padx=5, pady=5).grid(row=row, column=current_col + 1, sticky="nsew")
            Label(grid_frame, text=f"{process.response_time:.2f}", font=cell_style, borderwidth=1, relief="solid",
                  width=15, padx=5, pady=5).grid(row=row, column=current_col + 2, sticky="nsew")
            
            # Add to totals
            total_turnaround += process.turnaround_time
            total_waiting += process.waiting_time
            total_response += process.response_time
        
        # Configure grid columns to expand equally
        for i in range(len(headers)):
            grid_frame.grid_columnconfigure(i, weight=1)
        
        # Average Metrics Section
        metrics_frame = Frame(main_frame)
        metrics_frame.pack(fill='x', pady=(20, 0))
        
        Label(metrics_frame, text="Average Metrics", font=("Verdana", 16, "bold")).pack(pady=(0, 10))
        
        # Calculate and display averages
        n = len(processes)
        metrics_style = ("Verdana", 12)
        Label(metrics_frame, 
              text=f"Average Turnaround Time: {total_turnaround/n:.2f}s", 
              font=metrics_style).pack()
        Label(metrics_frame, 
              text=f"Average Waiting Time: {total_waiting/n:.2f}s", 
              font=metrics_style).pack()
        Label(metrics_frame, 
              text=f"Average Response Time: {total_response/n:.2f}s", 
              font=metrics_style).pack()
        
        ############################################################################################################################333
        Sfactor=1
        colors =["#FD3B3B","#BFFD3B","#52FD3B","#3B62FD","#FD3BD2","#3BF9FD"]

        spacing_Frame=Frame(new_window,width=100,height=100)
        main_frame = Frame(new_window, bg="#FF0000",height=40,width=1000)
        secondry_frame= Frame(new_window,bg="red")
        # Create main frame


        main_frame.pack(expand=True, padx=10, pady=10,anchor="n")
        # spacing_Frame.grid(row=0,column=1,sticky="nsew")
        # main_frame.grid(row=1,column=1,sticky="nsew")
        # secondry_frame.grid(row=2,column=1,rowspan=1000,sticky="nsew")
        # Create a canvas
        canvas = ttk.Canvas(main_frame, width=1000000, height=40)

        # Create horizontal scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient='horizontal', command=canvas.xview)
        scrollbar.pack(side='bottom', fill='x')

        # Configure canvas
        canvas.configure(xscrollcommand=scrollbar.set)
        canvas.pack(expand=True, fill='both')

        # Create frame inside canvas to hold labels
        inner_frame = Frame(canvas)
        inner_frame.rowconfigure(0,weight=1)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Add some sample labels
        sample_texts = [f"Label {i}" for i in range(1, 21)]
        labels = []
        kturn =-1
        chooosed="#D19B26"
        for i in range((max(end_time for p in processes for start_time, end_time in p.runs)+1)*Sfactor):
            if(kturn>i):
                continue
            try:
                for p in algo.sort_runtimes(processes):
                    if(i==p[1][0] ):
                        
                        chooosed=choice([m for m in colors if m!=chooosed])
                    # inner_frame.columnconfigure(i  ,weight=(p[1][1]-p[1][0])  *Sfactor )
                        kturn=(p[1][1])
                        label = Label(inner_frame,width= (p[1][1]-p[1][0])  ,
                                    background=chooosed,
                                    height=2, text=p[0])
                        inner_frame.columnconfigure(i ,weight=((p[1][1]-p[1][0]))   )
                        label.grid(column=i   *Sfactor,row=0,sticky="ew")
                        labels.append(label)
                        
                        raise "asdfasdf"
                
                #inner_frame.columnconfigure(i  *Sfactor,weight=1*Sfactor    )
                label = Label(inner_frame,width= (1)   ,
                                    background= "#FFFFFF",
                                    height=2, text="")
                inner_frame.columnconfigure(i    ,weight=1    )
                label.grid(column=i  ,row=0,sticky="ew")
                labels.append(label)
            except Exception:
                continue
            

        # Update scroll region after adding labels
        inner_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'))

        def on_mousewheel(event):
        # Shift + MouseWheel for horizontal scrolling
            if event.state == 1:  # Shift is being held
                canvas.xview_scroll(int(-1 * (event.delta / 220)), 'units')
            else:
                canvas.xview_scroll(int(-1 * (event.delta / 220)), 'units')
        # Bind mouse wheel for horizontal scrolling
        canvas.bind('<MouseWheel>', on_mousewheel)
        canvas.bind('<Shift-MouseWheel>', on_mousewheel)
        
# Main window setup remains the same
window = Tk()
window.geometry("1000x600")
window.title("OS CPU")

# Set window icon
icon = PhotoImage(file="image.png")
window.iconphoto(True, icon)

# Add title label
Label(window, text="CPU Scheduling Algorithms", font=("Verdana", 35)).pack(pady=20)

# Dropdown menu
selected_option = StringVar()
selected_option.set("Select an Algorithm")  # Default value

options = [
    "First Come First Served (FCFS)",
    "Non-Preemptive Shortest Job First (SJF)",
    "Preemptive Shortest Job First (SJF)",
    "Round Robin (RR)",
    "Non-Preemptive Priority Scheduling",
    "Preemptive Priority Scheduling"
]

dropdown = OptionMenu(window, selected_option, *options)
dropdown.pack(pady=20)

# Quantum Frame for Round Robin
quantum_frame = Frame(window)
quantum_label = Label(quantum_frame, text="Time Quantum:", font=("Verdana", 10))
quantum_entry = Entry(quantum_frame, width=10, justify='center')

# Header frame
header_frame = Frame(window)
header_frame.pack()

# Header labels - Centered text with consistent width
Label(header_frame, text="Process", width=10, font=("Verdana", 10), anchor="w").grid(row=0, column=0, padx=5)
Label(header_frame, text="Burst Time", width=15, font=("Verdana", 10), anchor="center").grid(row=0, column=1, padx=5)
Label(header_frame, text="Arrival Time", width=15, font=("Verdana", 10), anchor="w").grid(row=0, column=2, padx=5)
priority_label = Label(header_frame, text="Priority", width=15, font=("Verdana", 10), anchor="w")

# Container for process rows
process_frame = Frame(window)
process_frame.pack(pady=10)

# Track process rows
process_rows = []

def validate_integer_input(value):
    """Validate if the input is a positive integer"""
    if value == "": # Allow empty field for user to type
        return True
    try:
        num = int(value)
        return num >= 0
    except ValueError:
        return False

def create_entry():
    """Create a standardized Entry widget with validation"""
    vcmd = (window.register(validate_integer_input), '%P')
    entry = Entry(process_frame, width=15, justify='center', validate='key', validatecommand=vcmd)
    return entry

def create_hidden_button():
    """Create a truly invisible button that maintains spacing but can't be interacted with"""
    button = Label(process_frame, width=4)  # Using Label instead of Button
    button.grid_remove()  # Initially hidden
    return button

def update_process_labels():
    """Update process labels to ensure they're in numerical order"""
    for i, row in enumerate(process_rows):
        row[0].config(text=f"P{i + 1}")

def update_rows(*args):
    is_priority = "Priority" in selected_option.get()
    is_round_robin = "Round Robin" in selected_option.get()

    # Show or hide the Priority header
    if is_priority:
        priority_label.grid(row=0, column=3, padx=5)
    else:
        priority_label.grid_forget()

    # Show or hide the Quantum input
    if is_round_robin:
        quantum_frame.pack(after=dropdown, pady=10)
        quantum_label.pack(side='left', padx=5)
        quantum_entry.pack(side='left', padx=5)
    else:
        quantum_frame.pack_forget()

    # Update existing rows
    for row_index, row in enumerate(process_rows):
        if is_priority and (len(row) == 5 or len(row) == 4):
            priority_entry = create_entry()
            priority_entry.grid(row=row_index + 1, column=3, padx=5, pady=5)
            
            button_index = -2 if len(row) == 5 else -1
            row.insert(3, priority_entry)
            
            row[button_index].grid(row=row_index + 1, column=4, padx=5, pady=5)
            if len(row) > 5:
                row[-1].grid(row=row_index + 1, column=5, padx=5, pady=5)
                
        elif not is_priority and (len(row) == 7 or len(row) == 6):
            row[3].grid_forget()
            row.pop(3)
            
            button_index = -2 if len(row) == 5 else -1
            row[button_index].grid(row=row_index + 1, column=3, padx=5, pady=5)
            if len(row) > 4:
                row[-1].grid(row=row_index + 1, column=4, padx=5, pady=5)

def remove_process_row(row):
    for widget in row:
        widget.grid_forget()
    process_rows.remove(row)

    # Re-align remaining rows
    is_priority = "Priority" in selected_option.get()
    for row_index, row in enumerate(process_rows):
        for col_index, widget in enumerate(row):
            widget.grid(row=row_index + 1, column=col_index, padx=5, pady=5)
    
    update_process_labels()

def add_process_row():
    process_index = len(process_rows) + 1
    is_priority = "Priority" in selected_option.get()

    # Process label - Centered text
    process_label = Label(process_frame, text=f"P{process_index}", width=15, font=("Verdana", 12), anchor="center")
    process_label.grid(row=process_index, column=0, padx=5, pady=5)

    # Entry fields with centered text
    burst_entry = create_entry()
    burst_entry.grid(row=process_index, column=1, padx=5, pady=5)

    arrival_entry = create_entry()
    arrival_entry.grid(row=process_index, column=2, padx=5, pady=5)

    row = [process_label, burst_entry, arrival_entry]
    
    next_column = 3
    if is_priority:
        priority_entry = create_entry()
        priority_entry.grid(row=process_index, column=next_column, padx=5, pady=5)
        row.append(priority_entry)
        next_column += 1

    # Add and remove buttons with consistent width
    add_button = Button(process_frame, text="+", width=3)
    add_button.configure(command=add_process_row)
    add_button.grid(row=process_index, column=next_column, padx=5, pady=5)
    row.append(add_button)

    if process_index > 1:
        remove_button = Button(process_frame, text="-", width=3)
        remove_button.configure(command=lambda: remove_process_row(row))
        remove_button.grid(row=process_index, column=next_column + 1, padx=5, pady=5)
        row.append(remove_button)
    else:
        # Add hidden button for the first row to maintain spacing
        hidden_button = create_hidden_button()
        hidden_button.grid(row=process_index, column=next_column + 1, padx=5, pady=5)
        row.append(hidden_button)

    process_rows.append(row)

def validate_inputs():
    if selected_option.get() == "Select an Algorithm":
        messagebox.showerror("Error", "Please select an algorithm first!")
        return False
    
    is_priority = "Priority" in selected_option.get()
    is_round_robin = "Round Robin" in selected_option.get()

    # Validate quantum for Round Robin
    if is_round_robin:
        if not quantum_entry.get():
            messagebox.showerror("Error", "Please enter a Time Quantum value!")
            return False
        try:
            quantum = int(quantum_entry.get())
            if quantum <= 0:
                messagebox.showerror("Error", "Time Quantum must be a positive integer!")
                return False
        except ValueError:
            messagebox.showerror("Error", "Time Quantum must be a positive integer!")
            return False

    # Validate process inputs
    for row in process_rows:
        if not row[1].get() or not row[2].get():
            messagebox.showerror("Error", "Please fill all Burst Time and Arrival Time fields!")
            return False
        if is_priority and len(row) >= 4 and not row[3].get():
            messagebox.showerror("Error", "Please fill all Priority fields!")
            return False
        
        try:
            # Validate each field is a positive integer
            burst_time = int(row[1].get())
            arrival_time = int(row[2].get())
            
            if burst_time <= 0:
                messagebox.showerror("Error", "Burst Time must be a positive integer!")
                return False
            if arrival_time < 0:
                messagebox.showerror("Error", "Arrival Time must be a non-negative integer!")
                return False
                
            if is_priority and len(row) >= 4:
                priority = int(row[3].get())
                if priority <= 0:
                    messagebox.showerror("Error", "Priority must be a positive integer!")
                    return False
        except ValueError:
            messagebox.showerror("Error", "All input fields must be positive integers!")
            return False

    return True

# Setup quantum entry validation
quantum_vcmd = (window.register(validate_integer_input), '%P')
quantum_entry.configure(validate='key', validatecommand=quantum_vcmd)

# Add the first process row
add_process_row()

# Bind dropdown changes to update rows
selected_option.trace_add("write", update_rows)

# Add Next button
btn = Button(window, text="Next", command=create_window)
btn.pack(pady=20)

# Run the application
window.mainloop()