import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import datetime
import tempfile
import shutil
import time
import pkg_resources
import ast
import sys
import platform  # Import platform to check the operating system

def get_imports(file_path):
    imports = set()
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module if node.module else ''
                for alias in node.names:
                    imports.add(f"{module}.{alias.name}")
    return imports

def convert_to_exe(file_path, output_folder, expiry_time, progress_var):
    # Create the command for PyInstaller with the icon
    icon_path = "icon.ico" if os_var.get() == "Windows" else "icon.icns"  # Change icon based on OS
    
    # Create a temporary directory for our wrapper script
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create the wrapper script
        wrapper_script = os.path.join(temp_dir, "wrapper.py")
        with open(wrapper_script, 'w') as f:
            f.write(f"""
import sys
import time
import importlib.util
import os

# Calculate the expiry timestamp
creation_time = {int(time.time())}
expiry_duration = {expiry_time * 60}  # Ensure this is in seconds
expiry_timestamp = creation_time + expiry_duration

# # Debugging statements to check values
# print("Creation Time:", creation_time)
# print("Expiry Duration (seconds):", expiry_duration)
# print("Expiry Timestamp:", expiry_timestamp)

# Check if the current time exceeds the expiry time
current_time = time.time()
print("Current Time:", current_time)  # Debugging statement
if current_time > expiry_timestamp:
    print('This program has expired. Please contact the developer Safeer Abbas at safeerabbas.624@hotmail.com or https://github.com/SafeerAbbas624')
    input("Press Enter to exit...")
    sys.exit(1)  # Exit the program if expired

# If not expired, run the original script
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    application_path = sys._MEIPASS
else:
    # Running as script
    application_path = os.path.dirname(os.path.abspath(__file__))

original_script = os.path.join(application_path, "{os.path.basename(file_path)}")
print("Running original script:", original_script)  # Debugging statement
try:
    spec = importlib.util.spec_from_file_location("__main__", original_script)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
except Exception as e:
    print("Error running the original script:", e)
    input("Press Enter to exit...")  # Keep the window open to see the error
    sys.exit(1)
""")

        # Copy the original script to the temp directory
        temp_script = os.path.join(temp_dir, os.path.basename(file_path))
        shutil.copy2(file_path, temp_script)

        # Get all imported modules
        imported_modules = get_imports(file_path)

        # Create the PyInstaller command
        command = [
            'pyinstaller',
            '--onefile',  # Keep this for a single executable
            f'--icon={icon_path}',
            f'--add-data={temp_script};.' if os_var.get() == "Windows" else f'--add-data={temp_script}:.',
            '--hidden-import=pkg_resources.py2_warn',
        ]

        # Check the selected OS and adjust the command accordingly
        if os_var.get() == "macOS":  # macOS
            command.append('--windowed')  # Optional: run without a terminal window

        # Add hidden imports for all imported modules
        for module in imported_modules:
            command.append(f'--hidden-import={module}')

        # Add all standard library modules
        for module in sys.stdlib_module_names:
            command.append(f'--hidden-import={module}')

        # Add specific imports that might be missed
        additional_imports = [
            'selenium',
            'seleniumbase',
            'selenium.webdriver',
            'selenium.webdriver.common',
            'selenium.webdriver.common.by',
            'selenium.webdriver.common.keys',
            'selenium.webdriver.support',
            'selenium.webdriver.support.ui',
            'selenium.webdriver.support.expected_conditions',
            'selenium.webdriver.support.wait',
            'openpyxl.styles',
            'openpyxl',
            'tkinter',
            'math',
            'csv',
            'docx',

        ]
        for module in additional_imports:
            command.append(f'--hidden-import={module}')

        # Add the wrapper script and output directory
        command.extend([
            wrapper_script,
            f'--distpath={output_folder}',
            f'--name={os.path.splitext(os.path.basename(file_path))[0]}'
        ])

        print(f"Running command: {' '.join(command)}")  # Debugging statement
        result = subprocess.run(command, capture_output=True, text=True)

        # Check if PyInstaller ran successfully
        if result.returncode != 0:
            print("Error: PyInstaller failed to run.")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return

    # Update progress
    progress_var.set(progress_var.get() + 1)

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        selected_folder_label.config(text=f"Selected Folder: {folder_path}")  # Update the label with the selected folder
        global selected_folder
        selected_folder = folder_path

def create_output_folder():
    # Create a new output folder with the current datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = os.path.join(selected_folder, f"ConvertedFiles_{timestamp}")
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

def convert_files():
    if not selected_folder:
        messagebox.showwarning("Warning", "Please select a folder containing .py files.")
        return

    output_folder = create_output_folder()
    py_files = [file for file in os.listdir(selected_folder) if file.endswith('.py')]
    if not py_files:
        messagebox.showinfo("Info", "No .py files found in the selected folder.")
        return

    # Update progress bar
    progress_var.set(0)
    progress_bar['maximum'] = len(py_files)

    # Debugging statement to check expiry time
    expiry_time_value = expiry_var.get()
    print("Selected Expiry Time (minutes):", expiry_time_value)  # Debugging statement

    for file in py_files:
        convert_to_exe(os.path.join(selected_folder, file), output_folder, expiry_time_value, progress_var)
        root.update_idletasks()  # Update the GUI

    messagebox.showinfo("Info", f"Conversion completed! Files are saved in: {output_folder}")

# GUI setup
root = tk.Tk()
root.title("Python to EXE Converter")
root.geometry("800x400")  # Set the GUI size to 800x400

# Set the icon for the GUI window
icon_path = "icon.ico"  # Path to your icon file
root.iconbitmap(icon_path)

# Frame for input
frame = tk.Frame(root)
frame.pack(pady=20, padx=20)  # Added padding for better spacing

# Label to show selected folder
selected_folder_label = tk.Label(frame, text="Selected Folder: None")  # Initialize the label
selected_folder_label.grid(row=1, column=0, columnspan=3, padx=10, pady=10)  # Place the label in the grid

# Expiry time selection
expiry_label = tk.Label(frame, text="Select Expiry Time:")
expiry_label.grid(row=0, column=0, padx=10, pady=10)

expiry_var = tk.IntVar(value=1)  # Set initial value to 1 minute
expiry_scale = tk.Scale(frame, from_=0, to=525600, orient=tk.HORIZONTAL, resolution=1, label="Minutes (0-525600)", length=400, command=lambda value: update_expiry_label(value))
expiry_scale.grid(row=0, column=1, padx=10, pady=10)

# Label to show selected expiry time
expiry_time_label = tk.Label(frame, text="Expiry Time: 1 min")  # Update initial text to reflect initial value
expiry_time_label.grid(row=0, column=2, padx=10, pady=10)

# OS selection
os_label = tk.Label(frame, text="Select Target OS:")
os_label.grid(row=2, column=0, padx=10, pady=10)

os_var = tk.StringVar(value="Windows")  # Default value
os_options = ["Windows", "macOS"]  # Options for OS selection
os_menu = tk.OptionMenu(frame, os_var, *os_options)
os_menu.grid(row=2, column=1, padx=10, pady=10)

def update_expiry_label(value):
    expiry_var.set(int(value))  # Update the expiry_var with the current slider value
    if int(value) == 0:
        expiry_time_label.config(text="Expiry Time: Lifetime")
    elif int(value) < 60:
        expiry_time_label.config(text=f"Expiry Time: {value} min")
    elif int(value) < 1440:  # Less than 24 hours
        hours = int(value) // 60
        minutes = int(value) % 60
        expiry_time_label.config(text=f"Expiry Time: {hours} hour{'s' if hours > 1 else ''} {minutes} min")
    elif int(value) < 10080:  # Less than 7 days
        days = int(value) // 1440
        hours = (int(value) % 1440) // 60
        expiry_time_label.config(text=f"Expiry Time: {days} day{'s' if days > 1 else ''} {hours} hour{'s' if hours > 1 else ''}")
    elif int(value) < 525600:  # Less than 1 year
        weeks = int(value) // 10080
        days = (int(value) % 10080) // 1440
        expiry_time_label.config(text=f"Expiry Time: {weeks} week{'s' if weeks > 1 else ''} {days} day{'s' if days > 1 else ''}")
    else:  # 1 year or more
        expiry_time_label.config(text="Expiry Time: Lifetime")

# Update the label when the slider is released
expiry_scale.bind("<ButtonRelease-1>", lambda event: update_expiry_label(expiry_scale.get()))
expiry_scale.bind("<ButtonRelease-3>", lambda event: update_expiry_label(expiry_scale.get()))  # For right-click

# Bind left and right arrow keys to adjust the slider
def adjust_slider(event):
    if event.keysym == 'Right':
        expiry_scale.set(min(expiry_scale.get() + 1, 525600))  # Increase value, max 525600
    elif event.keysym == 'Left':
        expiry_scale.set(max(expiry_scale.get() - 1, 0))  # Decrease value, min 0
    update_expiry_label(expiry_scale.get())  # Update label after adjustment

root.bind("<Key>", adjust_slider)

# Button to select folder
select_button = tk.Button(root, text="Select Folder", command=select_folder)
select_button.pack(pady=10)

# Button to convert files
convert_button = tk.Button(root, text="Convert Files", command=convert_files)
convert_button.pack(pady=10)

# Progress bar
progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=20, fill=tk.X)

# Initialize selected folder variable
selected_folder = None

root.mainloop()
