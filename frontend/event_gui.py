import tkinter as tk
from tkinter import ttk, messagebox
import requests
from utils import BASE_URL
from tkcalendar import DateEntry

from utils import export_to_excel, print_excel
import os
import pandas as pd
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



class EventManagement:
    def __init__(self, root, token):
        self.root = tk.Toplevel(root)
        self.root.title("Event Management")
        self.root.state("zoomed")
        self.root.configure(bg="#f0f0f0")
        
        self.username = "current_user"
        self.token = token

        # Set window size and position at the center
        window_width = 1375
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Header Section
        self.header_frame = tk.Frame(self.root, bg="#2C3E50", height=50)
        self.header_frame.pack(fill=tk.X)
        
        self.title_label = tk.Label(self.header_frame, text="Event Management",
                                    font=("Helvetica", 16, "bold"), fg="white", bg="#2C3E50")
        self.title_label.pack(pady=10)

        # Sidebar Section
        self.left_frame = tk.Frame(self.root, bg="#2C3E50", width=220)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)

        # Right Section with a border and shadow effect
        self.right_frame = tk.Frame(self.root, bg="#ECF0F1", width=700, relief="ridge", borderwidth=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Subheading Label
        self.subheading_label = tk.Label(self.right_frame, text="Select an option",
                                         font=("Helvetica", 14, "bold"), fg="#2C3E50", bg="#ECF0F1")
        self.subheading_label.pack(pady=10)

        # Event Action Buttons
        self.buttons = []
        event_buttons = [
            ("Create Event", self.create_event),
            ("List Events", self.list_events),
            ("Search by Event ID", self.search_event_by_id),
            ("Update Event", self.update_event),
            ("Cancel Event", self.cancel_event),
        ]

        for text, command in event_buttons:
            btn = tk.Button(self.left_frame, text=text,
                            command=lambda t=text, c=command: self.update_subheading(t, c),
                            width=18, font=("Helvetica", 10, "bold"), anchor="w", padx=10,
                            bg="#34495E", fg="white", relief="flat", bd=0)
            
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3E5770"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495E"))
            btn.pack(pady=8, padx=15, anchor="w", fill="x")
            self.buttons.append(btn)

        # Separation Line
        separator = tk.Frame(self.left_frame, height=4, bg="#ECF0F1")
        separator.pack(fill="x", padx=5, pady=10)

        # Event Payment Buttons
        payment_buttons = [
            ("Create Event Payment", self.create_event_payment),
            ("List Event Payments", self.list_events_payment),
            ("List Payment By Status", self.list_payment_by_status),
            ("Search by Payment ID", self.search_payment_by_id),
            ("Void Payment", self.void_payment),
        ]

        for text, command in payment_buttons:
            btn = tk.Button(self.left_frame, text=text,
                            command=lambda t=text, c=command: self.update_subheading(t, c),
                            width=18, font=("Helvetica", 10, "bold"), anchor="w", padx=10,
                            bg="#34495E", fg="white", relief="flat", bd=0)
            
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#3E5770"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495E"))
            btn.pack(pady=8, padx=15, anchor="w", fill="x")
            self.buttons.append(btn)

        # Dashboard Link with Circular Border
        self.dashboard_label = tk.Label(
            self.left_frame, text="⬅ Dashboard", cursor="hand2",
            font=("Helvetica", 10, "bold"), fg="white", bg="#2C3E50",
            padx=10, pady=5, relief="solid", borderwidth=2, highlightthickness=2,
            highlightbackground="white", highlightcolor="white"
        )
        self.dashboard_label.pack(pady=15, padx=15, anchor="w", fill="x")
        self.dashboard_label.bind("<Enter>", lambda e: self.dashboard_label.config(bg="#3E5770"))
        self.dashboard_label.bind("<Leave>", lambda e: self.dashboard_label.config(bg="#2C3E50"))
        self.dashboard_label.bind("<Button-1>", lambda e: self.open_dashboard_window())

    def open_dashboard_window(self):
        from dashboard import Dashboard  # Import here to avoid circular import issues
        Dashboard(self.root, self.username, self.token)
        self.root.destroy()




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
        

    def update_subheading(self, text, command):
        self.subheading_label.config(text=text)
        command()
     
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
        file_path = os.path.join(download_dir, "event_report.xlsx")

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

     
    
    def create_event(self):
        """Opens a professional pop-up window for creating a new event."""
        create_window = tk.Toplevel(self.root)
        create_window.title("Create Event")
        create_window.configure(bg="#dddddd")  # Light grey background

        # Set window size (smaller)
        window_width = 450
        window_height = 500

        # Get screen width and height
        screen_width = create_window.winfo_screenwidth()
        screen_height = create_window.winfo_screenheight()

        # Calculate x and y coordinates for centering
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set window geometry
        create_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Make the window modal
        create_window.transient(self.root)
        create_window.grab_set()

        # === Dark Header ===
        header_frame = tk.Frame(create_window, bg="#2c3e50", height=40)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Create Event", font=("Arial", 13, "bold"), fg="white", bg="#2c3e50", pady=5)
        header_label.pack()

        # === Main Content Frame ===
        frame = tk.Frame(create_window, bg="#ffffff", padx=15, pady=10, relief="ridge", borderwidth=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === Form Frame Inside Main Frame ===
        form_frame = tk.Frame(frame, bg="#ffffff", padx=5, pady=5)
        form_frame.grid(row=0, columnspan=2, pady=5, padx=5, sticky="ew")

        # Event Fields
        fields = [
            ("Organizer", tk.Entry),
            ("Title", tk.Entry),
            ("Description", tk.Text),
            ("Start Date", DateEntry),
            ("End Date", DateEntry),
            ("Event Amount", tk.Entry),
            ("Caution Fee", tk.Entry),
            ("Location", tk.Entry),
            ("Phone Number", tk.Entry),
            ("Address", tk.Entry),
        ]

        self.entries = {}

        for i, (label_text, field_type) in enumerate(fields):
            label = tk.Label(form_frame, text=label_text, font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#2c3e50")
            label.grid(row=i, column=0, sticky="w", pady=3, padx=5)

            if field_type == tk.Text:
                entry = field_type(form_frame, font=("Helvetica", 11), width=28, height=2)  # Reduced height
            elif field_type == DateEntry:
                entry = field_type(form_frame, font=("Helvetica", 11), width=10, background='darkblue', foreground='white', borderwidth=2)
            else:
                entry = field_type(form_frame, font=("Helvetica", 11), width=25)

            entry.grid(row=i, column=1, pady=3, padx=5, sticky="ew")
            self.entries[label_text] = entry  # ✅ Store entries using label text as dictionary key

        # === Buttons Frame (Compact) ===
        btn_frame = tk.Frame(create_window, bg="#ffffff")
        btn_frame.pack(pady=10)

        # Submit Button
        submit_btn = ttk.Button(btn_frame, text="Submit", command=lambda: self.submit_event(create_window))
        submit_btn.grid(row=0, column=0, padx=5)

        # Cancel Button
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=create_window.destroy)
        cancel_btn.grid(row=0, column=1, padx=5)




    def submit_event(self, create_window):
        """Handles event creation and closes the popup on success."""
        try:
            created_by = self.username  

            event_data = {
                "organizer": self.entries["Organizer"].get(),
                "title": self.entries["Title"].get(),
                "description": self.entries["Description"].get("1.0", "end-1c"),
                "start_datetime": self.entries["Start Date"].get_date().strftime("%Y-%m-%d"),
                "end_datetime": self.entries["End Date"].get_date().strftime("%Y-%m-%d"),
                "event_amount": self.entries["Event Amount"].get(),
                "caution_fee": self.entries["Caution Fee"].get(),
                "location": self.entries["Location"].get(),
                "phone_number": self.entries["Phone Number"].get(),
                "address": self.entries["Address"].get(),
                "payment_status": "active",
                "created_by": created_by,
            }

            if not all(event_data.values()):  
                messagebox.showerror("Error", "Please fill in all fields")
                return

            api_url = "http://127.0.0.1:8000/events/"  
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

            response = requests.post(api_url, json=event_data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                event_id = response_data.get("id")  

                if event_id:
                    messagebox.showinfo("Success", f"Event created successfully!\nEvent ID: {event_id}")
                    create_window.destroy()  
                else:
                    messagebox.showerror("Error", "Event ID missing in response.")

            else:
                messagebox.showerror("Error", response.json().get("detail", "Event creation failed."))

        except KeyError as e:
            messagebox.showerror("Error", f"Missing entry field: {e}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

        
    
    
    def list_events(self):
        """List events with filtering by date."""
        self.clear_right_frame()

        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="📅 List Events", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        # ---------------- Filter Section ---------------- #
        filter_frame = tk.Frame(frame, bg="#ffffff")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Start Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.start_date = DateEntry(filter_frame, font=("Arial", 11))
        self.start_date.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="End Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=2, padx=5, pady=5)
        self.end_date = DateEntry(filter_frame, font=("Arial", 11))
        self.end_date.grid(row=0, column=3, padx=5, pady=5)

        fetch_btn = ttk.Button(filter_frame, text="🔍 Fetch Events", command=lambda: self.fetch_events(self.start_date, self.end_date))
        fetch_btn.grid(row=0, column=4, padx=10, pady=5)

        # ---------------- Event Table ---------------- #
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Organizer", "Title", "Event_Amount", "Caution_Fee", "Start Date", "End Date", "Location", "Phone", "Status", "created_by")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=y_scroll.set)

        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        x_scroll.pack(fill=tk.X)
        self.tree.configure(xscroll=x_scroll.set)

        # Total Amount Label
        self.total_label = tk.Label(frame, text="Total Event Amount: 0.00", font=("Arial", 12, "bold"), bg="#ffffff", fg="blue")
        self.total_label.pack(pady=10)

    def fetch_events(self, start_date_entry, end_date_entry):
        """Fetch events from API and populate the table."""
        api_url = "http://127.0.0.1:8000/events"
        params = {
            "start_date": start_date_entry.get_date().strftime("%Y-%m-%d"),
            "end_date": end_date_entry.get_date().strftime("%Y-%m-%d"),
        }
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.status_code == 200:
                events = response.json()
                self.tree.delete(*self.tree.get_children())  # Clear table
                total_amount = 0

                for event in events:
                    event_amount = float(event.get("event_amount", 0))
                    total_amount += event_amount
                    self.tree.insert("", "end", values=(
                        event.get("id", ""),
                        event.get("organizer", ""),
                        event.get("title", ""),
                        f"{event_amount:,.2f}",
                        f"{float(event.get('caution_fee', 0)) :,.2f}",
                        event.get("start_datetime", ""),
                        event.get("end_datetime", ""),
                        event.get("location", ""),
                        event.get("phone_number", ""),
                        event.get("payment_status", ""),
                        event.get("created_by", ""),
                    ))

                self.total_label.config(text=f"Total Event Amount: {total_amount:,.2f}")

                if not events:
                    messagebox.showinfo("No Results", "No events found for the selected filters.")
                    self.total_label.config(text="Total Event Amount: 0.00")

            else:
                messagebox.showerror("Error", response.json().get("detail", "Failed to retrieve events."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    def clear_right_frame(self):
        """Clears the right frame before rendering new content."""
        for widget in self.right_frame.winfo_children():
            widget.pack_forget()




    
    
    def search_event_by_id(self):
        self.clear_right_frame()
        
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Search Event by ID", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
        
        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)
        
        tk.Label(search_frame, text="Event ID:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.event_id_entry = tk.Entry(search_frame, font=("Arial", 11))
        self.event_id_entry.grid(row=0, column=1, padx=5, pady=5)
        
        search_btn = ttk.Button(
            search_frame, text="Search", command=self.fetch_event_by_id
        )
        search_btn.grid(row=0, column=2, padx=10, pady=5)
        
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Organizer", "Title", "Event_Amount", "Caution_Fee", "Start Date", "End Date", 
                "Location", "Phone Number", "Payment Status", "Created_by")

        self.search_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=140, anchor="center")
        
        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.search_tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_tree.configure(yscroll=y_scroll.set)
        
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.search_tree.xview)
        x_scroll.pack(fill=tk.X)
        self.search_tree.configure(xscroll=x_scroll.set)

    def fetch_event_by_id(self):
        event_id = self.event_id_entry.get().strip()

        if not event_id.isdigit():  # Ensure input is numeric
            messagebox.showerror("Error", "Please enter a valid numeric event ID.")
            return
        
        try:
            api_url = f"http://127.0.0.1:8000/events/{event_id}"
            headers = {"Authorization": f"Bearer {self.token}"}
        
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                event = response.json()
                
                # Ensure the event details exist
                if event:
                    self.search_tree.delete(*self.search_tree.get_children())
                    self.search_tree.insert("", "end", values=(
                        event.get("id", ""),
                        event.get("organizer", ""),
                        event.get("title", ""),
                        #f"₦{float(booking.get('booking_cost', 0)) :,.2f}",
                        f"{float(event.get('event_amount', 0)) :,.2f}",
                        f"{float(event.get('caution_fee', 0)) :,.2f}",
                        event.get("start_datetime", ""),
                        event.get("end_datetime", ""),
                        event.get("location", ""),
                        event.get("phone_number", ""),
                        event.get("payment_status", ""),
                        event.get("created_by", ""),
                    ))
                else:
                    messagebox.showinfo("No Results", "No event found with the provided ID.")
            else:
                messagebox.showerror("Error", response.json().get("detail", "No event found."))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")
  
        
        
    def update_event(self):
        """Opens a professional pop-up window for updating an event."""
        self.update_window = tk.Toplevel(self.root)
        self.update_window.title("Update Event")
        self.update_window.configure(bg="#dddddd")  # Light grey background

        # Set window size (smaller)
        window_width = 450
        window_height = 550

        # Get screen width and height
        screen_width = self.update_window.winfo_screenwidth()
        screen_height = self.update_window.winfo_screenheight()

        # Calculate x and y coordinates for centering
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        # Set window geometry
        self.update_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Make the window modal
        self.update_window.transient(self.root)
        self.update_window.grab_set()

        # === Header (Dark Background) ===
        header_frame = tk.Frame(self.update_window, bg="#2c3e50", height=40)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Update Event", font=("Arial", 13, "bold"), fg="white", bg="#2c3e50", pady=5)
        header_label.pack()

        # === Main Content Frame ===
        frame = tk.Frame(self.update_window, bg="#ffffff", padx=15, pady=10, relief="ridge", borderwidth=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === Form Frame Inside Main Frame ===
        form_frame = tk.Frame(frame, bg="#ffffff", padx=5, pady=5)
        form_frame.grid(row=0, columnspan=2, pady=5, padx=5, sticky="ew")

        # Event Fields
        fields = [
            ("Event ID", tk.Entry),
            ("Organizer", tk.Entry),
            ("Title", tk.Entry),
            ("Description", tk.Text),
            ("Start Date", DateEntry),
            ("End Date", DateEntry),
            ("Event Amount", tk.Entry),
            ("Caution Fee", tk.Entry),
            ("Location", tk.Entry),
            ("Phone Number", tk.Entry),
            ("Address", tk.Entry),
            ("Payment Status", ttk.Combobox),
        ]

        self.entries = {}

        for i, (label_text, field_type) in enumerate(fields):
            label = tk.Label(form_frame, text=label_text, font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#2c3e50")
            label.grid(row=i, column=0, sticky="w", pady=3, padx=5)

            if field_type == tk.Text:
                entry = field_type(form_frame, font=("Helvetica", 11), width=28, height=2)  # Reduced height
            elif field_type == DateEntry:
                entry = field_type(form_frame, font=("Helvetica", 11), width=10, background='darkblue', foreground='white', borderwidth=2)
            elif field_type == ttk.Combobox:
                entry = field_type(form_frame, values=["pending", "complete", "incomplete", "cancelled"], state="readonly", width=20)
                entry.current(0)
            else:
                entry = field_type(form_frame, font=("Helvetica", 11), width=25)

            entry.grid(row=i, column=1, pady=3, padx=5, sticky="ew")
            self.entries[label_text] = entry  # Store entries using label text as dictionary key

        # === Buttons Frame (Compact) ===
        btn_frame = tk.Frame(self.update_window, bg="#ffffff")
        btn_frame.pack(pady=10)

        # Update Button
        update_btn = ttk.Button(btn_frame, text="Update", command=self.submit_update_event)
        update_btn.grid(row=0, column=0, padx=5)

        # Cancel Button
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.update_window.destroy)
        cancel_btn.grid(row=0, column=1, padx=5)
    

    def submit_update_event(self):
        """Collects form data and sends a request to update an event."""
        try:
            event_id = self.entries["Event ID"].get().strip()
            if not event_id.isdigit():
                messagebox.showerror("Error", "Event ID must be a valid number.")
                return
            
            # Collect form data
            event_data = {
                "organizer": self.entries["Organizer"].get().strip(),
                "title": self.entries["Title"].get().strip(),
                "description": self.entries["Description"].get("1.0", "end").strip(),
                "location": self.entries["Location"].get().strip(),
                "phone_number": self.entries["Phone Number"].get().strip(),
                "address": self.entries["Address"].get().strip(),
                "start_datetime": self.entries["Start Date"].get_date().strftime("%Y-%m-%d"),
                "end_datetime": self.entries["End Date"].get_date().strftime("%Y-%m-%d"),
                "event_amount": float(self.entries["Event Amount"].get().strip() or 0),
                "caution_fee": float(self.entries["Caution Fee"].get().strip() or 0),
                "payment_status": self.entries["Payment Status"].get().strip(),
            }

            # Validate that required fields are not empty
            if not all(event_data.values()):
                messagebox.showerror("Error", "All fields must be filled.")
                return

            api_url = f"http://127.0.0.1:8000/events/{event_id}"
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

            response = requests.put(api_url, json=event_data, headers=headers)

            if response.status_code == 200:
                messagebox.showinfo("Success", "Event updated successfully!")
                self.update_window.destroy()  # ✅ Close popup on success
            else:
                messagebox.showerror("Error", response.json().get("detail", "Update failed."))

        except ValueError:
            messagebox.showerror("Error", "Invalid numeric input for Event Amount or Caution Fee.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")
            
      
    def cancel_event(self):
        """Opens a professional pop-up window to cancel an event."""
        cancel_window = tk.Toplevel(self.root)
        cancel_window.title("Cancel Event")
        cancel_window.configure(bg="#dddddd")  # Light grey background

        # Set window size
        window_width = 450
        window_height = 270

        # Get screen width and height
        screen_width = cancel_window.winfo_screenwidth()
        screen_height = cancel_window.winfo_screenheight()

        # Center the window
        x_coordinate = (screen_width - window_width) // 2
        y_coordinate = (screen_height - window_height) // 2

        cancel_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Make the window modal
        cancel_window.transient(self.root)
        cancel_window.grab_set()

        # === Dark Header ===
        header_frame = tk.Frame(cancel_window, bg="#2c3e50", height=40)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Cancel Event", font=("Arial", 13, "bold"), fg="white", bg="#2c3e50", pady=5)
        header_label.pack()

        # === Main Content Frame ===
        frame = tk.Frame(cancel_window, bg="#ffffff", padx=15, pady=10, relief="ridge", borderwidth=2)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # === Form Fields ===
        fields = [
            ("Event ID", tk.Entry),
            ("Cancellation Reason", tk.Entry),
        ]

        self.entries = {}

        for i, (label_text, field_type) in enumerate(fields):
            label = tk.Label(frame, text=label_text, font=("Helvetica", 11, "bold"), bg="#ffffff", fg="#2c3e50")
            label.grid(row=i, column=0, sticky="w", pady=5, padx=5)

            entry = field_type(frame, font=("Helvetica", 11), width=25)
            entry.grid(row=i, column=1, pady=5, padx=5, sticky="ew")
            self.entries[label_text] = entry

        # === Buttons Frame (Compact) ===
        btn_frame = tk.Frame(cancel_window, bg="#ffffff")
        btn_frame.pack(pady=10)

        # Submit Button
        submit_btn = ttk.Button(btn_frame, text="Submit", command=lambda: self.submit_cancel_event(cancel_window))
        submit_btn.grid(row=0, column=0, padx=5)

        # Cancel Button
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=cancel_window.destroy)
        cancel_btn.grid(row=0, column=1, padx=5)

        
    def submit_cancel_event(self, cancel_window):
        """Sends a request to cancel an event by event ID, including the cancellation reason."""
        try:
            event_id = self.entries["Event ID"].get().strip()  # Ensure input is stripped
            cancellation_reason = self.entries["Cancellation Reason"].get().strip()  # Ensure proper retrieval

            if not event_id:
                messagebox.showerror("Error", "Please enter an Event ID.")
                return

            if not cancellation_reason:
                messagebox.showerror("Error", "Cancellation reason is required.")
                return

            # Construct the API URL with cancellation reason as a query parameter
            api_url = f"http://127.0.0.1:8000/events/{event_id}/cancel?cancellation_reason={requests.utils.quote(cancellation_reason)}"

            headers = {"Authorization": f"Bearer {self.token}"}

            # Send PUT request without JSON body since params are in the URL
            response = requests.put(api_url, headers=headers)

            if response.status_code == 200:
                messagebox.showinfo("Success", f"Event ID {event_id} has been successfully canceled!\n"
                                            f"Cancellation Reason: {cancellation_reason}")
                cancel_window.destroy()  # Close the pop-up
            else:
                messagebox.showerror("Error", response.json().get("detail", "Cancellation failed."))

        except KeyError as e:
            messagebox.showerror("Error", f"Missing entry field: {e}")  # Handle missing key errors
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

                
    

    def create_event_payment(self):
        """Opens a centered, professional-looking popup window to create an event payment."""
        self.payment_window = tk.Toplevel(self.root)
        self.payment_window.title("Create Event Payment")
        self.payment_window.configure(bg="#dddddd")  # Light gray background

        # Set window size
        window_width = 450
        window_height = 400

        # Get screen width and height
        screen_width = self.payment_window.winfo_screenwidth()
        screen_height = self.payment_window.winfo_screenheight()

        # Calculate x and y coordinates for centering
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        # Set window geometry
        self.payment_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Make the window modal (disable interactions with main window)
        self.payment_window.transient(self.root)
        self.payment_window.grab_set()

        # Top Dark Header
        header_frame = tk.Frame(self.payment_window, bg="#2c3e50", height=50)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Create Event Payment", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50", pady=10)
        header_label.pack()

        # Main Content Frame with Border
        frame = tk.Frame(self.payment_window, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=3)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Form Frame Inside Main Frame
        form_frame = tk.Frame(frame, bg="#ffffff", padx=10, pady=10)
        form_frame.grid(row=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # Define fields
        labels = ["Event ID:", "Organiser:", "Amount Paid:", "Discount Allowed:", "Payment Method:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text, font=("Helvetica", 12), bg="#ffffff")
            label.grid(row=i, column=0, sticky="w", pady=5, padx=5)

            if label_text == "Payment Method:":
                # ✅ Use Combobox for payment selection
                entry = ttk.Combobox(form_frame, values=["Cash", "POS Card", "Bank Transfer"], state="readonly")
                entry.current(0)  # Set default selection
            else:
                entry = tk.Entry(form_frame)

            entry.grid(row=i, column=1, pady=5, padx=5, sticky="ew")
            self.entries[label_text] = entry  # ✅ Store entries properly

        # Submit Button with Modern Styling
        submit_btn = ttk.Button(frame, text="Submit Payment", command=self.submit_event_payment)
        submit_btn.grid(row=len(labels), column=0, columnspan=2, pady=15)

    def submit_event_payment(self):
        """Handles submission of event payment to backend."""
        try:
            # Validate and fetch Event ID
            event_id_str = self.entries["Event ID:"].get().strip()
            if not event_id_str.isdigit():
                messagebox.showerror("Error", "Event ID must be a valid integer.")
                return
            event_id = int(event_id_str)

            # Validate Organiser Name
            organiser = self.entries["Organiser:"].get().strip()
            if not organiser:
                messagebox.showerror("Error", "Organiser name is required.")
                return

            # Validate Amount Paid
            amount_paid_str = self.entries["Amount Paid:"].get().strip()
            if not amount_paid_str.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Amount Paid must be a valid number.")
                return
            amount_paid = float(amount_paid_str)

            # Validate Discount Allowed (default to 0 if empty)
            discount_allowed_str = self.entries["Discount Allowed:"].get().strip()
            discount_allowed = float(discount_allowed_str) if discount_allowed_str.replace(".", "", 1).isdigit() else 0.0

            # ✅ Fetch Payment Method correctly
            payment_method = self.entries["Payment Method:"].get().strip()
            if not payment_method:
                messagebox.showerror("Error", "Please select a payment method.")
                return

            # Prepare API payload
            payload = {
                "event_id": event_id,
                "organiser": organiser,
                "amount_paid": amount_paid,
                "discount_allowed": discount_allowed,
                "payment_method": payment_method,
                "created_by": self.username  # Ensure `self.username` holds the correct username
            }

            # API URL for creating event payment
            url = "http://127.0.0.1:8000/eventpayment/"
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

            # Send request to API
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()

            if response.status_code == 200:
                messagebox.showinfo("Success", f"Event Payment successful!\nEvent ID: {event_id}\nOrganiser: {organiser}")
                self.payment_window.destroy()     
            else:
                messagebox.showerror("Error", data.get("detail", "Payment failed."))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")   

    
    def list_events_payment(self):
        self.clear_right_frame()
        
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="List Event Payments", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

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
            text="Fetch Payments",
            command=lambda: self.fetch_event_payments(self.start_date, self.end_date)
        )
        fetch_btn.grid(row=0, column=4, padx=10, pady=5)

        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Payment ID", "Event ID", "Organiser", "Event Amount", "Amount Paid", "Discount Allowed", 
                   "Balance Due", "Payment Method", "Payment Status", "Payment Date", "Created By")

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=y_scroll.set)

        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        x_scroll.pack(fill=tk.X)
        self.tree.configure(xscroll=x_scroll.set)

        self.total_payment_label = tk.Label(frame, text="", font=("Arial", 12, "bold"), bg="#ffffff", fg="blue")
        self.total_payment_label.pack(pady=10)

    

    def fetch_event_payments(self, start_date_entry, end_date_entry):
        api_url = "http://127.0.0.1:8000/eventpayment/"  
        params = {
            "start_date": start_date_entry.get_date().strftime("%Y-%m-%d"),
            "end_date": end_date_entry.get_date().strftime("%Y-%m-%d"),
        }
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(api_url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                if not isinstance(data, list):
                    messagebox.showerror("Error", "Unexpected API response format")
                    return
                
                if not data:
                    self.total_payment_label.config(text="Total Payments: 0.00")
                    messagebox.showinfo("No Results", "No payments found for the selected filters.")
                    return
                
                self.tree.delete(*self.tree.get_children())
                total_amount_paid = 0
                
                for payment in data:
                    payment_status = payment.get("payment_status", "").lower()
                    
                    # Exclude voided payments from total computation but still list them
                    if payment_status != "voided":
                        total_amount_paid += float(payment.get("amount_paid", 0))

                    self.tree.insert("", "end", values=(
                        payment.get("id", ""),
                        payment.get("event_id", ""),
                        payment.get("organiser", ""),
                        f"{float(payment.get('event_amount', 0)) :,.2f}",
                        f"{float(payment.get('amount_paid', 0)) :,.2f}",
                        f"{float(payment.get('discount_allowed', 0)) :,.2f}",
                        f"{float(payment.get('balance_due', 0)) :,.2f}",
                        payment.get("payment_method", ""),
                        payment.get("payment_status", ""),
                        payment.get("payment_date", ""),
                        payment.get("created_by", ""),
                    ))
                
                self.total_payment_label.config(
                    text=f"Total Payments: {total_amount_paid:,.2f}"
                )
            else:
                messagebox.showerror("Error", response.json().get("detail", "Failed to retrieve payments."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")





    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.pack_forget()




    def list_payment_by_status(self):
        """Displays the List Payments by Status UI."""
        self.clear_right_frame()  # Ensure old UI elements are removed

        # Create a new frame for the table with scrollable functionality
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="List Payments by Status", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        # Filter Frame
        filter_frame = tk.Frame(frame, bg="#ffffff")
        filter_frame.pack(pady=5)

        # Status Dropdown
        tk.Label(filter_frame, text="Status:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)

        status_options = ["pending", "complete", "incomplete", "voided"]
        self.status_var = tk.StringVar(value=status_options[0])  # Default selection

        status_menu = ttk.Combobox(filter_frame, textvariable=self.status_var, values=status_options, state="readonly")
        status_menu.grid(row=0, column=1, padx=5, pady=5)
        #status_menu.bind("<<ComboboxSelected>>", lambda event: self.status_var.set(status_menu.get()))
        
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
        fetch_btn = ttk.Button(filter_frame, text="Fetch Payments", command=self.fetch_payments_by_status)
        fetch_btn.grid(row=0, column=6, padx=10, pady=5)

        

        # Table Frame
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Total Payment Amount Label
        self.total_cost_label = tk.Label(frame, text="Total Payment Amount: 0.00", 
                                 font=("Arial", 12, "bold"), bg="#ffffff", fg="blue")
        self.total_cost_label.pack(pady=5)

        

        columns = ("Payment ID", "Event ID", "Organiser Name", "Event Amount", "Amount Paid", "Discount Allowed", "Balance Due", "Payment Date", "Status", "Payment Method", "Created By")
        
        if hasattr(self, "tree"):
            self.tree.destroy()

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscroll=y_scroll.set)
        
        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.tree.xview)
        x_scroll.pack(fill=tk.X)
        self.tree.configure(xscroll=x_scroll.set)


    def fetch_payments_by_status(self):
        """Fetch payments based on status and date filters."""
        api_url = "http://127.0.0.1:8000/eventpayment/status"

        # Ensure only valid query parameters are sent
        params = {
            "status": self.status_var.get().strip().lower(),
            "start_date": self.start_date.get_date().strftime("%Y-%m-%d"),
            "end_date": self.end_date.get_date().strftime("%Y-%m-%d"),
        }

        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(api_url, params=params, headers=headers)
            data = response.json()

            if response.status_code == 200:
                self.tree.delete(*self.tree.get_children())  # Clear existing table data
                total_amount = 0

                if isinstance(data, list):  # Ensure response is a list
                    for payment in data:
                        # Extract values safely
                        event_amount = float(payment.get("event_amount", 0))
                        amount_paid = float(payment.get("amount_paid", 0))  # <-- Update to amount_paid
                        discount_allowed = float(payment.get("discount_allowed", 0))
                        balance_due = float(payment.get("balance_due", 0))

                        total_amount += amount_paid  # Sum total amount paid

                        # Insert data into table
                        self.tree.insert("", "end", values=(
                            payment.get("id", ""),
                            payment.get("event_id", ""),
                            payment.get("organiser", ""),
                            f"{event_amount:,.2f}",
                            f"{amount_paid:,.2f}",
                            f"{discount_allowed:,.2f}",
                            f"{balance_due:,.2f}",
                            payment.get("payment_date", ""),
                            payment.get("payment_status", ""),
                            payment.get("payment_method", ""),
                            payment.get("created_by", ""),
                        ))

                    # Update Total Payment Label
                    self.total_cost_label.config(text=f"Total Payment Amount: {total_amount:,.2f}")
                else:
                    messagebox.showinfo("No Results", "No payments found for the selected filters.")
            else:
                messagebox.showerror("Error", data.get("detail", "Failed to retrieve payments."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")
            
            
            


    def search_payment_by_id(self):
        """GUI for searching a payment by ID."""
        self.clear_right_frame()

        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Search Payment by ID", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        # Search Input Frame
        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Payment ID:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.payment_id_entry = tk.Entry(search_frame, font=("Arial", 11))
        self.payment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        search_btn = ttk.Button(
            search_frame, text="Search", command=self.fetch_payment_by_id
        )
        search_btn.grid(row=0, column=2, padx=10, pady=5)

        # Table Frame
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            "ID", "Event ID", "Organiser", "Event Amount", "Amount Paid", 
            "Discount Allowed", "Balance Due", "Payment Method", "Status", 
            "Payment Date", "Created By"
        )

        self.search_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.search_tree.heading(col, text=col)
            self.search_tree.column(col, width=120, anchor="center")

        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.search_tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.search_tree.configure(yscroll=y_scroll.set)

        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.search_tree.xview)
        x_scroll.pack(fill=tk.X)
        self.search_tree.configure(xscroll=x_scroll.set)


    def fetch_payment_by_id(self):
        """Fetch and display payment details by ID."""
        payment_id = self.payment_id_entry.get().strip()

        if not payment_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric payment ID.")
            return

        try:
            api_url = f"http://127.0.0.1:8000/eventpayment/{payment_id}"
            headers = {"Authorization": f"Bearer {self.token}"}

            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                payment = response.json()

                if payment:
                    self.search_tree.delete(*self.search_tree.get_children())

                    # Format amounts
                    event_amount = f"{float(payment.get('event_amount', 0)) :,.2f}"
                    amount_paid = f"{float(payment.get('amount_paid', 0)) :,.2f}"
                    discount_allowed = f"{float(payment.get('discount_allowed', 0)) :,.2f}"
                    balance_due = f"{float(payment.get('balance_due', 0)) :,.2f}"

                    self.search_tree.insert("", "end", values=(
                        payment.get("id", ""),
                        payment.get("event_id", ""),
                        payment.get("organiser", ""),
                        event_amount,
                        amount_paid,
                        discount_allowed,
                        balance_due,
                        payment.get("payment_method", ""),
                        payment.get("payment_status", ""),
                        payment.get("payment_date", ""),
                        payment.get("created_by", ""),
                    ))
                else:
                    messagebox.showinfo("No Results", "No payment found with the provided ID.")
            else:
                messagebox.showerror("Error", response.json().get("detail", "No payment found."))
        
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")
            

  

    def void_payment(self):
        self.clear_right_frame()

        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Void Event Payment", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        input_frame = tk.Frame(frame, bg="#ffffff")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Payment ID:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.payment_id_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.payment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        void_btn = ttk.Button(input_frame, text="Void Payment", command=self.process_void_event_payment)
        void_btn.grid(row=0, column=2, padx=10, pady=5)

        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Payment ID", "Organiser", "Amount Paid", "Discount Allowed", "Balance Due", "Payment Status", "Created By")

        self.void_payment_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.void_payment_tree.heading(col, text=col)
            self.void_payment_tree.column(col, width=120, anchor="center")

        self.void_payment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.void_payment_tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.void_payment_tree.configure(yscroll=y_scroll.set)

        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.void_payment_tree.xview)
        x_scroll.pack(fill=tk.X)
        self.void_payment_tree.configure(xscroll=x_scroll.set)

    def process_void_event_payment(self):
        payment_id = self.payment_id_entry.get().strip()

        if not payment_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric payment ID.")
            return

        try:
            check_url = f"http://127.0.0.1:8000/eventpayment/{payment_id}"
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(check_url, headers=headers)

            if response.status_code == 200:
                payment_data = response.json()
                payment_status = payment_data.get("payment_status", "").lower()

                if payment_status == "voided":
                    messagebox.showerror("Error", f"Payment ID {payment_id} has already been voided.")
                    return
                
                void_url = f"http://127.0.0.1:8000/eventpayment/void/{payment_id}/"
                void_response = requests.put(void_url, headers=headers)

                if void_response.status_code == 200:
                    data = void_response.json()
                    messagebox.showinfo("Success", data.get("message", "Payment voided successfully."))
                    self.fetch_voided_event_payment_by_id(payment_id)
                else:
                    messagebox.showerror("Error", void_response.json().get("detail", "Failed to void payment."))
            else:
                messagebox.showerror("Error", response.json().get("detail", "Payment record not found."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    def fetch_voided_event_payment_by_id(self, payment_id=None):
        if payment_id is None:
            payment_id = self.payment_id_entry.get().strip()

        if not payment_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric payment ID.")
            return

        try:
            api_url = f"http://127.0.0.1:8000/eventpayment/{payment_id}"
            headers = {"Authorization": f"Bearer {self.token}"}
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data:
                    if hasattr(self, "void_payment_tree") and self.void_payment_tree is not None:
                        self.void_payment_tree.delete(*self.void_payment_tree.get_children())

                    self.void_payment_tree.insert("", "end", values=(
                        data.get("id", ""),
                        data.get("organiser", ""),
                        f"{float(data.get('amount_paid', 0)) :,.2f}",
                        f"{float(data.get('discount_allowed', 0)) :,.2f}",
                        f"{float(data.get('balance_due', 0)) :,.2f}",
                        data.get("payment_status", ""),
                        data.get("created_by", ""),
                    ))
                else:
                    messagebox.showinfo("No Results", "No payment found with the provided ID.")
            else:
                messagebox.showerror("Error", response.json().get("detail", "No payment found."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

    
    



# Main Execution
if __name__ == "__main__":
    root = tk.Tk()
    app = EventManagement(root)
    root.mainloop()    