import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import requests
from utils import BASE_URL
import datetime 

from tkinter import Tk, Button, messagebox
from utils import export_to_excel, print_excel
import requests
import os
import sys
import pandas as pd
from payment_gui import PaymentManagement  # Import the Payment GUI
##


class BookingManagement:
    def __init__(self, root, token):
        self.root = tk.Toplevel(root)
        self.tree = ttk.Treeview(self.root)  # Ensure the treeview is initialized
        self.root.title("Booking Management")
        self.root.state("zoomed")
        self.root.configure(bg="#f0f0f0")
        
        self.username = "current_user"
        self.token = token


        # Set application icon
        icon_path = os.path.abspath("frontend/icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

        # Set window size and position
        window_width = 1375
        window_height = 587
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        
        # Main Container Frame
        self.container = tk.Frame(self.root, bg="#ffffff", padx=10, pady=10)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Header Frame
        self.header_frame = tk.Frame(self.container, bg="#2C3E50", height=60)
        self.header_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.title_label = tk.Label(self.header_frame, text="📅 Booking Management", 
                                    font=("Helvetica", 16, "bold"), fg="gold", bg="#2C3E50")
        self.title_label.pack(pady=0)
        
        # ==== New Action Frame (Right Side of Header) ====
        self.action_frame = tk.Frame(self.header_frame, bg="#2C3E50")
        self.action_frame.pack(side=tk.RIGHT, padx=20)  

        # Export to Excel
        self.export_label = tk.Label(self.action_frame, text="📊 Export to Excel",
                                    font=("Helvetica", 10, "bold"), fg="white", bg="#2C3E50", cursor="hand2")
        self.export_label.pack(side=tk.RIGHT, padx=10)
        self.export_label.bind("<Enter>", lambda e: self.export_label.config(fg="#D3D3D3"))
        self.export_label.bind("<Leave>", lambda e: self.export_label.config(fg="white"))
        self.export_label.bind("<Button-1>", lambda e: self.export_report())

        # Print Report
        self.print_label = tk.Label(self.action_frame, text="🖨 Print Report",
                                    font=("Helvetica", 10, "bold"), fg="white", bg="#2C3E50", cursor="hand2")
        self.print_label.pack(side=tk.RIGHT, padx=10)
        self.print_label.bind("<Enter>", lambda e: self.print_label.config(fg="#D3D3D3"))
        self.print_label.bind("<Leave>", lambda e: self.print_label.config(fg="white"))
        self.print_label.bind("<Button-1>", lambda e: self.print_report())


         # ==== Main Content Frame (Holds Sidebar + Right Section) ====
        self.main_frame = tk.Frame(self.container, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

         # ==== Menu Container (With "Menu" Heading) ====
        self.Menu = tk.Frame(self.main_frame, bg="#2C3E50", width=230)
        self.Menu.pack(side=tk.LEFT, fill=tk.Y)

        # === "Menu" Heading ===
        self.menu_label = tk.Label(self.Menu, text="MENU", font=("Helvetica", 12, "bold"), 
                                   fg="white", bg="#34495E", pady=5)
        self.menu_label.pack(fill=tk.X)

        # Sidebar Section (Inside `Menu` Frame)
        self.left_frame = tk.Frame(self.Menu, bg="#2C3E50", width=220)
        self.left_frame.pack(fill=tk.BOTH, expand=True)

        # Right Section (Main Content)
        self.right_frame = tk.Frame(self.main_frame, bg="#ffffff", relief="ridge", borderwidth=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Subheading Label
        self.subheading_label = tk.Label(self.right_frame, text="Select an option",
                                         font=("Helvetica", 14, "bold"), fg="#2C3E50", bg="#ffffff")
        self.subheading_label.pack(pady=10)

        # ==== Booking Action Buttons in Sidebar ====
        buttons = [
            ("Create Booking", self.create_booking),
            ("List Booking", self.list_bookings),
            ("Sort By Status", self.list_bookings_by_status),
            ("Sort Guest Name", self.search_booking),
            ("Sort by ID", self.search_booking_by_id),
            ("Sort By Room", self.search_booking_by_room),
            ("Update", self.update_booking),
            ("Guest Checkout", self.guest_checkout),
            ("Cancel Booking", self.cancel_booking),
        ]
        
        for text, command in buttons:
            btn = tk.Button(self.left_frame, text=text,
                            command=lambda t=text, c=command: self.update_subheading(t, c),
                            width=10, font=("Arial", 10), anchor="w", padx=10,
                            bg="#34495E", fg="white", relief="flat", bd=0)
            btn.pack(pady=8, padx=10, anchor="w", fill="x")

            # Dashboard Link
            self.dashboard_label = tk.Label(
            self.left_frame,
            text="⬅ Dashboard",
            cursor="hand2",
            font=("Helvetica", 10, "bold"),
            fg="white",
            bg="#1A5276",  # Deep Blue Background
            padx=10,
            pady=5,
            relief="solid",
            borderwidth=2
        )
        self.dashboard_label.pack(pady=15, padx=10, anchor="w", fill="x")

        # Change background color when hovering over
        self.dashboard_label.bind("<Enter>", lambda e: self.dashboard_label.config(bg="#154360"))  # Darker Blue on Hover
        self.dashboard_label.bind("<Leave>", lambda e: self.dashboard_label.config(bg="#1A5276"))  # Reset on Leave

        # Click event to open dashboard
        self.dashboard_label.bind("<Button-1>", lambda e: self.open_dashboard_window())


    def update_subheading(self, text, command):
        """Updates the subheading label and runs the selected command"""
        self.subheading_label.config(text=text)
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        command()
    
    def open_dashboard_window(self):
        """Opens the dashboard window"""
        from dashboard import Dashboard
        Dashboard(self.root, self.username, self.token)
        self.root.destroy()



    def apply_grid_effect(self, tree=None):
        if tree is None:
            tree = self.tree  # Default to main tree if none is provided
        
        for i, item in enumerate(tree.get_children()):
            if i % 2 == 0:
                tree.item(item, tags=("evenrow",))
            else:
                tree.item(item, tags=("oddrow",))

        tree.tag_configure("evenrow", background="#f2f2f2")  # Light gray
        tree.tag_configure("oddrow", background="white")      # White


    def open_dashboard_window(self):
        from dashboard import Dashboard  # Import here to avoid circular import issues
        Dashboard(self.root, self.username, self.token)
        self.root.destroy()

    def update_subheading(self, text, command):
        if self.subheading_label.winfo_exists():
            self.subheading_label.config(text=text)
        for widget in self.right_frame.winfo_children():
            widget.destroy()
        command()
        


            
             
        self.fetch_and_display_bookings()

       # Export and Print Buttons in Header Section
        def on_enter(e):
            e.widget.config(bg="#1ABC9C", fg="white")  # Background changes on hover

        def on_leave(e):
            e.widget.config(bg="#2C3E50", fg="white")  # Restore default background & text color

        self.export_button = tk.Label(self.header_frame, text="Export to Excel", 
                                    fg="white", bg="#2C3E50", font=("Helvetica", 9, "bold"), 
                                    cursor="hand2", padx=10, pady=5)
        self.export_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.export_button.bind("<Enter>", on_enter)
        self.export_button.bind("<Leave>", on_leave)
        self.export_button.bind("<Button-1>", lambda e: self.export_report())  # Click event

        self.print_button = tk.Label(self.header_frame, text="Print Report", 
                                    fg="white", bg="#2C3E50", font=("Helvetica", 9, "bold"), 
                                    cursor="hand2", padx=10, pady=5)
        self.print_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.print_button.bind("<Enter>", on_enter)
        self.print_button.bind("<Leave>", on_leave)
        self.print_button.bind("<Button-1>", lambda e: self.print_report())  # Click event


     



    def reset_booking_form(self):
        """Clears all input fields in the booking form."""
        if hasattr(self, "entries"):
            for key, entry in self.entries.items():
                if isinstance(entry, ttk.Combobox):
                    entry.set("")  # Clear combobox selection
                elif isinstance(entry, DateEntry):
                    entry.set_date(datetime.date.today())  # Reset date to today
                elif isinstance(entry, tk.Entry):
                    entry.delete(0, tk.END)  # Clear text entry
                else:
                    print(f"Unknown entry type for {key}")

    





    def fetch_and_display_bookings(self):
        """Fetch booking data from the API"""
        url = "http://127.0.0.1:8000/bookings/list"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.bookings_data = response.json()
            else:
                self.bookings_data = []
                messagebox.showerror("Error", "Failed to fetch bookings.")

        except Exception as e:
            self.bookings_data = []
            messagebox.showerror("Error", f"API Error: {str(e)}")



    def export_report(self):
        """Export only the visible bookings from the Treeview to Excel"""
        if not hasattr(self, "tree") or not self.tree.get_children():
            messagebox.showwarning("Warning", "No data available to export.")
            return

        # Extract column headers
        columns = [self.tree.heading(col)["text"] for col in self.tree["columns"]]

        # Extract row data from Treeview
        rows = []
        for item in self.tree.get_children():
            row_data = [self.tree.item(item)["values"][i] for i in range(len(columns))]
            rows.append(row_data)

        # Convert to DataFrame for better formatting
        df = pd.DataFrame(rows, columns=columns)

        # Save in user's Downloads folder
        download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        file_path = os.path.join(download_dir, "bookings_report.xlsx")

        try:
            df.to_excel(file_path, index=False)  # Export properly formatted Excel
            self.last_exported_file = file_path
            messagebox.showinfo("Success", f"Report exported successfully!\nSaved at: {file_path}")
        except PermissionError:
            messagebox.showerror("Error", "Permission denied! Close the file if it's open and try again.")
        except Exception as e:
            messagebox.showerror("Error", f"Error exporting to Excel: {e}")


    def print_report(self):
        """Print the exported Excel report"""
        if hasattr(self, 'last_exported_file') and self.last_exported_file:
            print_excel(self.last_exported_file)
        else:
            messagebox.showwarning("Warning", "Please export the report before printing.")

    def update_subheading(self, text, command):
        """Updates the subheading label and calls the selected function."""
        if hasattr(self, "subheading_label") and self.subheading_label.winfo_exists():
            self.subheading_label.config(text=text)
        else:
            self.subheading_label = tk.Label(self.right_frame, text=text, font=("Arial", 14, "bold"), bg="#f0f0f0")
            self.subheading_label.pack(pady=10)

        # Clear right frame before displaying new content
        for widget in self.right_frame.winfo_children():
            widget.destroy()

        command()

    

    def create_booking(self):
        self.clear_right_frame()
        """Opens a professional pop-up window for creating a new booking."""
        create_window = tk.Toplevel(self.root)
        create_window.title("Create Booking")
        create_window.configure(bg="#dddddd")  # Light grey background

        # Set window size
        window_width = 450
        window_height = 430
        screen_width = create_window.winfo_screenwidth()
        screen_height = create_window.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        create_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Make it modal
        create_window.transient(self.root)
        create_window.grab_set()

        # 🔹 Dark Header
        header_frame = tk.Frame(create_window, bg="#2c3e50", height=50)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Create Booking", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50", pady=10)
        header_label.pack()

        # 🔹 Main Content Frame with Border
        frame = tk.Frame(create_window, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=3)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 🔹 Form Frame Inside Main Frame
        form_frame = tk.Frame(frame, bg="#ffffff", padx=10, pady=10)
        form_frame.grid(row=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # 📌 Booking Fields
        fields = [
            ("Room Number", tk.Entry),
            ("Guest Name", tk.Entry),
            ("Phone Number", tk.Entry),
            ("Booking Type", ttk.Combobox),
            ("Arrival Date", DateEntry),
            ("Departure Date", DateEntry),
        ]

        self.entries = {}

        for i, (label, field_type) in enumerate(fields):
            label = tk.Label(form_frame, text=label, font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#2c3e50")
            label.grid(row=i, column=0, sticky="w", pady=5, padx=5)

            if field_type == ttk.Combobox:
                entry = field_type(form_frame, values=["checked-in", "reservation", "complimentary"], state="readonly", font=("Helvetica", 12), width=20)
            elif field_type == DateEntry:
                entry = field_type(form_frame, font=("Helvetica", 12), width=12, background='darkblue', foreground='white', borderwidth=2)
            else:
                entry = field_type(form_frame, font=("Helvetica", 12), width=25)

            entry.grid(row=i, column=1, pady=5, padx=5, sticky="ew")
            self.entries[label.cget("text")] = entry  # ✅ Store entry reference with correct label text

        # 🔹 Submit Button
        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.grid(row=len(fields), columnspan=2, pady=15)

        submit_btn = ttk.Button(btn_frame, text="Submit Booking", command=lambda: self.submit_booking(create_window), style="Bold.TButton")
        submit_btn.pack()





    def submit_booking(self, create_window):
        """Collects form data and sends a request to create a booking, then closes the pop-up."""
        try:
            created_by = self.username  

            booking_data = {
                "room_number": self.entries["Room Number"].get(),
                "guest_name": self.entries["Guest Name"].get(),
                "phone_number": self.entries["Phone Number"].get(),
                "arrival_date": self.entries["Arrival Date"].get_date().strftime("%Y-%m-%d"),
                "departure_date": self.entries["Departure Date"].get_date().strftime("%Y-%m-%d"),
                "booking_type": self.entries["Booking Type"].get(),
                "created_by": created_by,
            }

            if not all(booking_data.values()):  
                messagebox.showerror("Error", "Please fill in all fields")
                return

            api_url = "http://127.0.0.1:8000/bookings/create/"  
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

            response = requests.post(api_url, json=booking_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                booking_id = response_data.get("booking_details", {}).get("id")  

                if booking_id:
                    messagebox.showinfo("Success", f"Booking created successfully!\nBooking ID: {booking_id}")
                    
                    # Ensure this method exists before calling
                    if hasattr(self, "reset_booking_form"):
                        self.reset_booking_form()
                    else:
                        print("reset_booking_form method is missing")

                    create_window.destroy()  # Close the pop-up window

                else:
                    messagebox.showerror("Error", "Booking ID missing in response.")

            else:
                messagebox.showerror("Error", response.json().get("detail", "Booking failed."))

        except KeyError as e:
            messagebox.showerror("Error", f"Missing entry field: {e}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    

    def list_bookings(self):
        self.clear_right_frame()
        
        
        # Create a new frame for the table
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="List Bookings Report", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        filter_frame = tk.Frame(frame, bg="#ffffff")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Start Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.start_date = DateEntry(filter_frame, font=("Arial", 11))
        self.start_date.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="End Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=2, padx=5, pady=5)
        self.end_date = DateEntry(filter_frame, font=("Arial", 11))
        self.end_date.grid(row=0, column=3, padx=5, pady=5)

        fetch_btn = ttk.Button(
            filter_frame,
            text="Fetch Bookings",
            command=lambda: self.fetch_bookings(self.start_date, self.end_date)
        )
        fetch_btn.grid(row=0, column=4, padx=10, pady=5)

        # Create a frame to hold the treeview and scrollbars
        table_frame = tk.Frame(frame, bg="#ffffff", bd=1, relief="solid")  # Solid border for grid effect
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # Define Treeview columns
        columns = ("ID", "Room", "Guest", "Booking Cost", "Arrival", "Departure", "Status", "Number of Days", 
                "Booking Type", "Phone Number", "Booking Date", "Payment Status", "Created_by")

        # Create a Treeview widget
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, background="white", fieldbackground="white", borderwidth=1)
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#2c3e50", foreground="white")
        style.map("Treeview", background=[("selected", "#b3d1ff")])

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)  # Set height for visibility

        # Define headings and set column widths
        for col in columns:
            self.tree.heading(col, text=col, anchor="center")
            self.tree.column(col, width=90, anchor="center")  # Adjust column width

        # Pack the Treeview inside a scrollable frame
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Add vertical scrollbar
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=y_scroll.set)

        # Add horizontal scrollbar
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        x_scroll.pack(fill=tk.X)
        self.tree.configure(xscroll=x_scroll.set)

        # Label to display total booking cost
        self.total_booking_cost_label = tk.Label(frame, text="", font=("Arial", 12, "bold"), bg="#ffffff", fg="blue")
        self.total_booking_cost_label.pack(pady=10)

        

    def fetch_bookings(self, start_date_entry, end_date_entry):
        """Fetch bookings from the API and populate the table, while calculating total booking cost."""
        api_url ="http://127.0.0.1:8000/bookings/list"  # Ensure correct endpoint
        params = {
            "start_date": start_date_entry.get_date().strftime("%Y-%m-%d"),
            "end_date": end_date_entry.get_date().strftime("%Y-%m-%d"),
        }
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # print("API Response:", data)  # Debugging output

                if isinstance(data, dict) and "bookings" in data:
                    bookings = data["bookings"]
                    total_booking_cost = data.get("total_booking_cost", 0)  # Get total cost from API
                else:
                    messagebox.showerror("Error", "Unexpected API response format")
                    return

                # Check if bookings list is empty
                if not bookings:
                    self.total_booking_cost_label.config(text="Total Booking Cost: 0.00")  # Reset label
                    messagebox.showinfo("No Results", "No bookings found for the selected filters.")
                    return

                self.tree.delete(*self.tree.get_children())  # Clear table

                for booking in bookings:
                    self.tree.insert("", "end", values=(
                        booking.get("id", ""),
                        booking.get("room_number", ""),
                        booking.get("guest_name", ""),
                        f"{float(booking.get('booking_cost', 0)) :,.2f}",
                        booking.get("arrival_date", ""),
                        booking.get("departure_date", ""),
                        booking.get("status", ""),
                        booking.get("number_of_days", ""),
                        booking.get("booking_type", ""),
                        booking.get("phone_number", ""),
                        booking.get("booking_date", ""),
                        booking.get("payment_status", ""),                    
                        booking.get("created_by", ""),
                    ))

                # Apply grid effect after inserting data
                self.apply_grid_effect()

                # Display total booking cost
                self.total_booking_cost_label.config(
                    text=f"Total Booking Cost: {total_booking_cost:,.2f}"
                )
            
            else:
                messagebox.showerror("Error", response.json().get("detail", "Failed to retrieve bookings."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")


    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.pack_forget()

    
    
    
    
    def list_bookings_by_status(self):
        """Displays the List Bookings by Status UI."""
        self.clear_right_frame()  # Ensure old UI elements are removed

        # Create a new frame for the table with scrollable functionality
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="List Bookings by Status", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        # Filter Frame
        filter_frame = tk.Frame(frame, bg="#ffffff")
        filter_frame.pack(pady=5)

        # Status Dropdown
       # Status Dropdown
        tk.Label(filter_frame, text="Status:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)

        status_options = ["checked-in", "reserved", "checked-out", "cancelled", "complimentary"]
        self.status_var = tk.StringVar(value=status_options[0])  # Default selection

        status_menu = ttk.Combobox(filter_frame, textvariable=self.status_var, values=status_options, state="readonly")
        status_menu.grid(row=0, column=1, padx=5, pady=5)

        # Bind the selection event to a function that updates self.status_var
        def on_status_change(event):
            #print("Selected Status:", self.status_var.get())  # Debugging: Check what is selected
            self.status_var.set(status_menu.get())  # Ensure value updates

        status_menu.bind("<<ComboboxSelected>>", on_status_change)  # Event binding


        # Start Date
        tk.Label(filter_frame, text="Start Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=2, padx=5, pady=5)
        self.start_date = DateEntry(filter_frame, font=("Arial", 11))
        self.start_date.grid(row=0, column=3, padx=5, pady=5)

        # End Date
        tk.Label(filter_frame, text="End Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=4, padx=5, pady=5)
        self.end_date = DateEntry(filter_frame, font=("Arial", 11))
        self.end_date.grid(row=0, column=5, padx=5, pady=5)

        # Fetch Button
        fetch_btn = ttk.Button(filter_frame, text="Fetch Bookings", command=self.fetch_bookings_by_status)
        fetch_btn.grid(row=0, column=6, padx=10, pady=5)

        # Table Frame
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Room", "Guest", "Booking Cost", "Arrival", "Departure", "Status", "Number of Days",
               "Booking Type", "Phone Number", "Booking Date", "Payment Status", "Created_by")


        # ✅ Prevent recreation of table on every call
        if hasattr(self, "tree"):
            self.tree.destroy()

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="center")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=y_scroll.set)
        
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        x_scroll.pack(fill=tk.X)
        self.tree.configure(xscroll=x_scroll.set)

        # ✅ Add Label for Total Booking Cost at the Bottom
        self.total_cost_label = tk.Label(frame, text="Total Booking Cost: 0.00", font=("Arial", 12, "bold"), bg="#ffffff", fg="blue")
        self.total_cost_label.pack(pady=10)  # Placed at the bottom


    def fetch_bookings_by_status(self):
        """Fetch bookings based on status and date filters."""
        api_url = "http://127.0.0.1:8000/bookings/status"

        selected_status = self.status_var.get().strip().lower()  # Ensure correct status retrieval

        # ✅ Debugging: Print the selected status before sending
        #print(f"Selected Status from Dropdown: '{selected_status}'")

        params = {
            "status": selected_status,  # Ensure correct status is passed
            "start_date": self.start_date.get_date().strftime("%Y-%m-%d"),
            "end_date": self.end_date.get_date().strftime("%Y-%m-%d"),
        }

        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(api_url, params=params, headers=headers)
            data = response.json()

            # ✅ Debugging: Print the API response
            #print("API Response:", data)

            if response.status_code == 200:
                if "bookings" in data and isinstance(data["bookings"], list):
                    bookings = data["bookings"]

                    self.tree.delete(*self.tree.get_children())  # Clear previous data

                    total_cost = 0  # Initialize total booking cost

                    if bookings:
                        for booking in bookings:
                            is_canceled = booking.get("status", "").lower() == "cancelled"
                            tag = "cancelled" if is_canceled else "normal"

                            booking_cost = float(booking.get("booking_cost", 0))
                            total_cost += booking_cost

                            self.tree.insert("", "end", values=(
                                booking.get("id", ""),
                                booking.get("room_number", ""),
                                booking.get("guest_name", ""),
                                f"{booking_cost:,.2f}",
                                booking.get("arrival_date", ""),
                                booking.get("departure_date", ""),
                                booking.get("status", ""),
                                booking.get("number_of_days", ""),
                                booking.get("booking_type", ""),
                                booking.get("phone_number", ""),
                                booking.get("booking_date", ""),
                                booking.get("payment_status", ""),                               
                                booking.get("created_by", ""),
                            ), tags=(tag,))

                        # Apply grid effect after inserting data
                        self.apply_grid_effect()


                        self.tree.tag_configure("cancelled", foreground="red")
                        self.tree.tag_configure("normal", foreground="black")
                        self.total_cost_label.config(text=f"Total Booking Cost: {total_cost:,.2f}")
                    else:
                        self.tree.delete(*self.tree.get_children())
                        self.total_cost_label.config(text="Total Booking Cost: ₦0.00")
                        messagebox.showinfo("No Results", "No bookings found for the selected filters.")

                elif "message" in data:
                    messagebox.showinfo("Info", data["message"])
                    self.tree.delete(*self.tree.get_children())
                    self.total_cost_label.config(text="Total Booking Cost: ₦0.00")

            else:
                messagebox.showerror("Error", response.json().get("detail", "Failed to retrieve bookings."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

            
    
    def search_booking(self):
        self.clear_right_frame()
        
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Search Booking by Guest Name", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
        
        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)
        
        tk.Label(search_frame, text="Guest Name:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11))
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        
        search_btn = ttk.Button(
            search_frame, text="Search", command=self.fetch_booking_by_guest_name
        )
        search_btn.grid(row=0, column=2, padx=10, pady=5)
        
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Room", "Guest", "Booking Cost", "Arrival", "Departure", "Status", "Number of Days", 
                "Booking Type", "Phone Number", "Booking Date", "Payment Status")
        
        self.search_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=80, anchor="center")
        
        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.search_tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_tree.configure(yscroll=y_scroll.set)
        
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.search_tree.xview)
        x_scroll.pack(fill=tk.X)
        self.search_tree.configure(xscroll=x_scroll.set)
    
    def fetch_booking_by_guest_name(self):
        guest_name = self.search_entry.get().strip()
        if not guest_name:
            messagebox.showerror("Error", "Please enter a guest name to search.")
            return

        
         
        api_url ="http://127.0.0.1:8000/bookings/search"
        params = {"guest_name": guest_name}
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                bookings = data.get("bookings", [])
                
                self.search_tree.delete(*self.search_tree.get_children())
                
                for booking in bookings:
                    self.search_tree.insert("", "end", values=(
                        booking.get("id", ""),
                        booking.get("room_number", ""),
                        booking.get("guest_name", ""),
                         f"{float(booking.get('booking_cost', 0)) :,.2f}",  # Format booking_cost
                        booking.get("arrival_date", ""),
                        booking.get("departure_date", ""),
                        booking.get("status", ""),
                        booking.get("number_of_days", ""),
                        booking.get("booking_type", ""),
                        booking.get("phone_number", ""),
                        booking.get("booking_date", ""),
                        booking.get("payment_status", ""),
                       
                    ))
            
                # Apply grid effect after inserting data
                self.apply_grid_effect(self.search_tree)

    
            else:
                messagebox.showinfo("No result", response.json().get("detail", "No bookings found."))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    
    def search_booking_by_id(self):
        self.clear_right_frame()
        
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Search Booking by ID", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
        
        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)
        
        tk.Label(search_frame, text="Booking ID:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.booking_id_entry = tk.Entry(search_frame, font=("Arial", 11))
        self.booking_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        search_btn = ttk.Button(
            search_frame, text="Search", command=self.fetch_booking_by_id
        )
        search_btn.grid(row=0, column=2, padx=10, pady=5)
        
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Room", "Guest", "Booking Cost", "Arrival", "Departure", "Status", "Number of Days", 
                "Booking Type", "Phone Number", "Booking Date", "Payment Status", "Created_by")
        
        if hasattr(self, "tree"):
            self.tree.destroy()
        
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=80, anchor="center")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=y_scroll.set)
        
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        x_scroll.pack(fill=tk.X)
        self.tree.configure(xscroll=x_scroll.set)

    def fetch_booking_by_id(self):
        booking_id = self.booking_id_entry.get().strip()
    
        if not booking_id.isdigit():  # Ensure input is numeric
            messagebox.showerror("Error", "Please enter a valid numeric booking ID.")
            return
        
        try:
    
            #booking_id = int(booking_id)  # Convert to integer

            
            api_url = f"http://127.0.0.1:8000/bookings/{booking_id}"
            headers = {"Authorization": f"Bearer {self.token}"}
        
        
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                booking = data.get("booking", {})
                
                # Ensure the booking details exist
                if booking:
                    self.tree.delete(*self.tree.get_children())
                    self.tree.insert("", "end", values=(
                        booking.get("id", ""),
                        booking.get("room_number", ""),
                        booking.get("guest_name", ""),
                        f"{float(booking.get('booking_cost', 0)) :,.2f}",  # Format booking_cost
                        booking.get("arrival_date", ""),
                        booking.get("departure_date", ""),
                        booking.get("status", ""),
                        booking.get("number_of_days", ""),
                        booking.get("booking_type", ""),
                        booking.get("phone_number", ""),
                        booking.get("booking_date", ""),
                        booking.get("payment_status", ""),                       
                        booking.get("created_by", ""),
                    ))

                 # Apply grid effect after inserting data
                    self.apply_grid_effect(self.tree)

   
                else:
                    messagebox.showinfo("No Results", "No booking found with the provided ID.")
            else:
                messagebox.showerror("Error", response.json().get("detail", "No booking found."))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")
     

    #def search_by_room(self):
    def search_booking_by_room(self):
        self.clear_right_frame()

        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Search Booking by Room Number", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Room Number:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.room_number_entry = tk.Entry(search_frame, font=("Arial", 11))
        self.room_number_entry.grid(row=0, column=1, padx=5, pady=5)

        # Date input fields
        tk.Label(search_frame, text="Start Date:", font=("Arial", 11), bg="#ffffff").grid(row=1, column=0, padx=5, pady=5)
        self.start_date_entry = DateEntry(search_frame, font=("Arial", 11), width=12, background="darkblue", foreground="white", borderwidth=2)
        self.start_date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(search_frame, text="End Date:", font=("Arial", 11), bg="#ffffff").grid(row=1, column=2, padx=5, pady=5)
        self.end_date_entry = DateEntry(search_frame, font=("Arial", 11), width=12, background="darkblue", foreground="white", borderwidth=2)
        self.end_date_entry.grid(row=1, column=3, padx=5, pady=5)

        search_btn = ttk.Button(
            search_frame, text="Search", command=self.fetch_booking_by_room
        )
        search_btn.grid(row=2, column=0, columnspan=4, padx=10, pady=10)

        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Room", "Guest", "Booking Cost", "Arrival", "Departure", "Status", "Number of Days", 
                "Booking Type", "Phone Number", "Booking Date", "Payment Status")

        self.search_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=80, anchor="center")

        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.search_tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_tree.configure(yscroll=y_scroll.set)

        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.search_tree.xview)
        x_scroll.pack(fill=tk.X)
        self.search_tree.configure(xscroll=x_scroll.set)

    def fetch_booking_by_room(self):
        room_number = self.room_number_entry.get().strip()

        if not room_number:
            messagebox.showerror("Error", "Please enter a room number.")
            return

        try:
            start_date = self.start_date_entry.get_date()
            end_date = self.end_date_entry.get_date()

            if not start_date or not end_date:
                messagebox.showerror("Error", "Please select both start and end dates.")
                return

            # Ensure date format matches backend expectation
            formatted_start_date = start_date.strftime("%Y-%m-%d")
            formatted_end_date = end_date.strftime("%Y-%m-%d")

            # Construct API URL
            api_url = f"http://127.0.0.1:8000/bookings/room/{room_number}"
            params = {"start_date": formatted_start_date, "end_date": formatted_end_date}
            headers = {"Authorization": f"Bearer {self.token}"}

            # Debugging output
            #print(f"Fetching bookings for Room: {room_number}, Start Date: {formatted_start_date}, End Date: {formatted_end_date}")
            #print(f"API URL: {api_url}, Headers: {headers}")

            # Make the request
            response = requests.get(api_url, params=params, headers=headers)
            response_data = response.json()

            # Print full API response for debugging
            #print("API Response:", response_data)

            # Handle response
            if response.status_code == 200:
                if "bookings" in response_data and response_data["bookings"]:
                    self.search_tree.delete(*self.search_tree.get_children())  # Clear table

                    for booking in response_data["bookings"]:
                        self.search_tree.insert("", "end", values=(
                            booking.get("id", ""),
                            booking.get("room_number", ""),
                            booking.get("guest_name", ""),
                            f"{float(booking.get('booking_cost', 0)) :,.2f}",
                            booking.get("arrival_date", ""),
                            booking.get("departure_date", ""),
                            booking.get("status", ""),
                            booking.get("number_of_days", ""),
                            booking.get("booking_type", ""),
                            booking.get("phone_number", ""),
                            booking.get("booking_date", ""),
                            booking.get("payment_status", ""),
                            
                        ))
                    # Apply grid effect after inserting data
                    self.apply_grid_effect(self.search_tree)

    
                else:
                    messagebox.showinfo("No Results", f"No bookings found for Room {room_number} between {formatted_start_date} and {formatted_end_date}.")
            else:
                error_message = response_data.get("detail", "Failed to retrieve bookings.")
                messagebox.showerror("Error", error_message)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")



    
    def update_subheading(self, text, command):
        self.subheading_label.config(text=text)
        command()

    def update_booking(self):
        self.clear_right_frame()
        """Opens a professional pop-up window for updating a booking."""
        update_window = tk.Toplevel(self.root)
        update_window.title("Update Booking")
        update_window.configure(bg="#dddddd")  # Light grey background

        # Set window size and center it
        window_width = 480
        window_height = 450
        screen_width = update_window.winfo_screenwidth()
        screen_height = update_window.winfo_screenheight()
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2
        update_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Make it modal
        update_window.transient(self.root)
        update_window.grab_set()

        # 🔹 Dark Header
        header_frame = tk.Frame(update_window, bg="#2c3e50", height=50)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Update Booking", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50", pady=10)
        header_label.pack()

        # 🔹 Main Content Frame with Border
        frame = tk.Frame(update_window, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=3)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 🔹 Form Frame Inside Main Frame
        form_frame = tk.Frame(frame, bg="#ffffff", padx=10, pady=10)
        form_frame.grid(row=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # 📌 Booking Fields
        fields = [
            ("Booking ID", tk.Entry),  # Unique field for updates
            ("Room Number", tk.Entry),
            ("Guest Name", tk.Entry),
            ("Phone Number", tk.Entry),
            ("Booking Type", ttk.Combobox),
            ("Arrival Date", DateEntry),
            ("Departure Date", DateEntry),
        ]

        self.entries = {}

        for i, (label, field_type) in enumerate(fields):
            tk.Label(form_frame, text=label, font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#2c3e50").grid(row=i, column=0, sticky="w", pady=5, padx=5)

            if field_type == ttk.Combobox:
                entry = field_type(form_frame, values=["checked-in", "reservation", "complimentary"], state="readonly", font=("Helvetica", 12), width=20)
            elif field_type == DateEntry:
                entry = field_type(form_frame, font=("Helvetica", 12), width=12, background='darkblue', foreground='white', borderwidth=2)
            else:
                entry = field_type(form_frame, font=("Helvetica", 12), width=25)

            entry.grid(row=i, column=1, pady=5, padx=5, sticky="ew")
            self.entries[label] = entry  # ✅ Store entry reference with correct label text

        # 🔹 Submit Button
        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.grid(row=len(fields), columnspan=2, pady=15)

        submit_btn = ttk.Button(btn_frame, text="Submit Update", command=lambda: self.submit_update_booking(update_window), style="Bold.TButton")
        submit_btn.pack()

    def submit_update_booking(self, update_window):
        """Collects form data and sends a request to update a booking."""
        try:
            booking_data = {
                "booking_id": self.entries["Booking ID"].get(),
                "room_number": self.entries["Room Number"].get(),
                "guest_name": self.entries["Guest Name"].get(),
                "phone_number": self.entries["Phone Number"].get(),
                "arrival_date": self.entries["Arrival Date"].get_date().strftime("%Y-%m-%d"),
                "departure_date": self.entries["Departure Date"].get_date().strftime("%Y-%m-%d"),
                "booking_type": self.entries["Booking Type"].get(),
            }

            if not all(booking_data.values()):  # Ensure all fields are filled
                messagebox.showerror("Error", "Please fill in all fields")
                return

            api_url = f"http://127.0.0.1:8000/bookings/update/?booking_id={booking_data['booking_id']}"  # Adjust if needed
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

            response = requests.put(api_url, json=booking_data, headers=headers)

            if response.status_code == 200:
                messagebox.showinfo("Success", "Booking updated successfully!")
                update_window.destroy()  # Close the update window on success
            else:
                messagebox.showerror("Error", response.json().get("detail", "Update failed."))

        except KeyError as e:
            messagebox.showerror("Error", f"Missing entry field: {e}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    def guest_checkout(self):
        self.clear_right_frame()
        """Opens a professional pop-up window for guest checkout."""
        checkout_window = tk.Toplevel(self.root)
        checkout_window.title("Guest Checkout")
        checkout_window.configure(bg="#f8f9fa")  # Light background

        # Set window size and center it
        window_width, window_height = 360, 200
        x_coordinate = (checkout_window.winfo_screenwidth() - window_width) // 2
        y_coordinate = (checkout_window.winfo_screenheight() - window_height) // 2
        checkout_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Make it modal
        checkout_window.transient(self.root)
        checkout_window.grab_set()

        # 🔹 Header Section
        header = tk.Label(checkout_window, text="Guest Checkout", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50", pady=8)
        header.pack(fill=tk.X)

        # 🔹 Form Frame
        form_frame = tk.Frame(checkout_window, bg="white", padx=15, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Room Number Field
        tk.Label(form_frame, text="Room Number", font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        self.room_number_entry = tk.Entry(form_frame, font=("Arial", 11), width=22)
        self.room_number_entry.pack(pady=5)

        # 🔹 Submit Button
        submit_btn = ttk.Button(checkout_window, text="Checkout Guest", command=lambda: self.submit_guest_checkout(checkout_window), style="Bold.TButton")
        submit_btn.pack(pady=10)

    def submit_guest_checkout(self, checkout_window):
        """Sends a request to checkout the guest by room number."""
        try:
            room_number = self.room_number_entry.get()

            if not room_number:
                messagebox.showerror("Error", "Please enter a room number.")
                return

            api_url = f"http://127.0.0.1:8000/bookings/{room_number}/"
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

            response = requests.put(api_url, headers=headers)

            if response.status_code == 200:
                messagebox.showinfo("Success", f"Guest checked out successfully for room number {room_number}!")
                checkout_window.destroy()  # Close window on success
            else:
                messagebox.showerror("Error", response.json().get("detail", "Checkout failed."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

        
            
            
            
    def update_subheading(self, text, command):
        self.subheading_label.config(text=text)
        command()

    
    def cancel_booking(self):
        self.clear_right_frame()
        """Opens a professional pop-up window for booking cancellation."""
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Cancel Booking")
        cancel_window.configure(bg="#f8f9fa")  # Light background

        # Set window size and center it
        window_width, window_height = 380, 250
        x_coordinate = (cancel_window.winfo_screenwidth() - window_width) // 2
        y_coordinate = (cancel_window.winfo_screenheight() - window_height) // 2
        cancel_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Make it modal
        cancel_window.transient(self.root)
        cancel_window.grab_set()

        # 🔹 Header Section
        header = tk.Label(cancel_window, text="Cancel Booking", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50", pady=8)
        header.pack(fill=tk.X)

        # 🔹 Form Frame
        form_frame = tk.Frame(cancel_window, bg="white", padx=15, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Booking ID Field
        tk.Label(form_frame, text="Booking ID", font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        self.booking_id_entry = tk.Entry(form_frame, font=("Arial", 11), width=24)
        self.booking_id_entry.pack(pady=5)

        # Cancellation Reason (Optional)
        tk.Label(form_frame, text="Cancellation Reason (Optional)", font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        self.cancellation_reason_entry = tk.Entry(form_frame, font=("Arial", 11), width=24)
        self.cancellation_reason_entry.pack(pady=5)

        # 🔹 Submit Button
        submit_btn = ttk.Button(cancel_window, text="Cancel Booking", command=lambda: self.submit_cancel_booking(cancel_window), style="Bold.TButton")
        submit_btn.pack(pady=10)

    def submit_cancel_booking(self, cancel_window):
        """Sends a request to cancel the booking by booking ID, with an optional cancellation reason."""
        try:
            booking_id = self.booking_id_entry.get().strip()
            cancellation_reason = self.cancellation_reason_entry.get().strip()

            if not booking_id:
                messagebox.showerror("Error", "Please enter a Booking ID.")
                return

            # Construct API URL
            api_url = f"http://127.0.0.1:8000/bookings/cancel/{booking_id}/"
            if cancellation_reason:
                api_url += f"?cancellation_reason={requests.utils.quote(cancellation_reason)}"

            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
            response = requests.post(api_url, headers=headers)

            if response.status_code == 200:
                canceled_booking = response.json().get("canceled_booking", {})
                messagebox.showinfo("Success", f"Booking {canceled_booking.get('id', booking_id)} canceled successfully!\n"
                                               f"Room Status: {canceled_booking.get('room_status', 'N/A')}\n"
                                               f"Booking Status: {canceled_booking.get('status', 'N/A')}\n"
                                               f"Reason: {canceled_booking.get('cancellation_reason', 'None')}")
                cancel_window.destroy()
            else:
                messagebox.showerror("Error", response.json().get("detail", "Cancellation failed."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")
    






class UpdateBooking:
    def __init__(self, root, token):
        self.root = tk.Toplevel(root)
        self.root.title("Update Booking")
        self.root.geometry("900x600")
        self.token = token
        self.root.configure(bg="#f0f0f0")
        
        
        
   



    
    
    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    BookingManagement(root, token="dummy_token")
    root.mainloop()
    
    
