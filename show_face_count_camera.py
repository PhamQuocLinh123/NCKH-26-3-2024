import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from tkcalendar import Calendar
from tkinter import filedialog
import pandas as pd

def fetch_data():
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Change password if needed
        database="face_recognizer"
    )

    # Create a cursor to execute the query
    mycursor = mydb.cursor()

    # Execute query to fetch data from the 'face_count_camera' table
    mycursor.execute("SELECT * FROM face_count_camera LIMIT 20 OFFSET " + str((page_number - 1) * 20))
    rows = mycursor.fetchall()

    # Clear table before inserting new data
    table.delete(*table.get_children())

    # Insert fetched data into the table
    for row in rows:
        table.insert("", "end", values=row)

def export_to_excel():
    # Ask user to select location to save the file
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx")

    if file_path:
        try:
            # Get data from table
            data = [table.item(item)["values"] for item in table.get_children()]

            # Create DataFrame from data
            df = pd.DataFrame(data, columns=["ID", "Timestamp", "Count", "Image Path"])

            # Export DataFrame to Excel
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Export Successful", "Data has been exported to Excel successfully.")
        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {str(e)}")

# Create Tkinter GUI
root = tk.Tk()
root.title("Data from Database")

# Set background color
root.configure(background="#3366CC")

# Set window size
root.geometry("800x600")

# Create a frame for the table
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20, fill='both', expand=True)

# Create a table to display data
table = ttk.Treeview(frame, columns=("ID", "Timestamp", "Count", "Image Path"), show="headings", selectmode="browse")
# Define column headings
table.heading("ID", text="ID")
table.heading("Timestamp", text="Timestamp")
table.heading("Count", text="Count")
table.heading("Image Path", text="Image Path")

# Fetch and display data from database
page_number = 1
fetch_data()

# Create a button to export data to Excel
export_button = tk.Button(root, text="Export to Excel", command=export_to_excel, bg="#347083", fg="white")
export_button.pack()

# Style the Treeview widget
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#f0f0f0", fieldbackground="#f0f0f0", foreground="black")
style.map("Treeview", background=[("selected", "#347083")])
style.map("Treeview.Heading", background="#d3d3d3")

# Pack the table
table.pack(side="left", fill="both", expand=True)

# Set column width and format
table.column("ID", width=50, anchor="center")
table.column("Timestamp", width=200, anchor="center")
table.column("Count", width=100, anchor="center")
table.column("Image Path", width=550, anchor="w")

# Function to navigate to the next page
def next_page():
    global page_number
    page_number += 1
    fetch_data()

# Function to navigate to the previous page
def prev_page():
    global page_number
    if page_number > 1:
        page_number -= 1
        fetch_data()

# Create navigation buttons
prev_button = tk.Button(root, text="Previous", command=prev_page)
next_button = tk.Button(root, text="Next", command=next_page)
prev_button.pack(side="left", padx=10)
next_button.pack(side="right", padx=10)

# Center the window on the screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

# Run the Tkinter main loop
root.mainloop()
