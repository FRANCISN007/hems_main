import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import requests
from utils import BASE_URL
from datetime import datetime
import pytz
from tkinter import ttk, Tk
import tkinter as tk
import os
import pandas as pd

from tkinter import Tk, Button, messagebox
from utils import export_to_excel, print_excel
import requests
#from bookings_gui import BookingManagement  # Import the Payment GUI





class PaymentManagement:
    def __init__(self, root, token):
        self.root = tk.Toplevel(root)
        self.root.title("Payment Management")
        self.username = "current_user"
        self.root.state("zoomed")
        self.root.configure(bg="#f0f0f0")
        
        self.token = token
        self.payments_data = []
        self.last_exported_file = None

        # Set window size and position
        window_width = 1375
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Header Frame
        self.header_frame = tk.Frame(self.root, bg="#2C3E50", height=50)
        self.header_frame.pack(fill=tk.X)

        # Grid Layout Configuration
        self.header_frame.grid_columnconfigure(0, weight=1)  # Left spacing
        self.header_frame.grid_columnconfigure(1, weight=2)  # Center (title)
        self.header_frame.grid_columnconfigure(2, weight=1)  # Right (actions)

        # Title Label (Centered Properly)
        self.title_label = tk.Label(self.header_frame, text="                                                               Payment Management",
                                    font=("Helvetica", 16, "bold"), fg="white", bg="#2C3E50")
        self.title_label.grid(row=0, column=1, pady=10, sticky="ew")  # Full width, ensures centering

        # Action Frame (Right Side)
        self.action_frame = tk.Frame(self.header_frame, bg="#2C3E50")
        self.action_frame.grid(row=0, column=2, padx=20, sticky="e")  # Stays aligned to the right

        # Export to Excel (Plain Text, No Border)
        self.export_label = tk.Label(self.action_frame, text="📊 Export to Excel",
                                    font=("Helvetica", 10, "bold"), fg="white", bg="#2C3E50", cursor="hand2")
        self.export_label.pack(side=tk.RIGHT, padx=10)
        self.export_label.bind("<Enter>", lambda e: self.export_label.config(fg="#D3D3D3"))
        self.export_label.bind("<Leave>", lambda e: self.export_label.config(fg="white"))
        self.export_label.bind("<Button-1>", lambda e: self.export_report())

        # Print Report (Plain Text, No Border)
        self.print_label = tk.Label(self.action_frame, text="🖨 Print Report",
                                    font=("Helvetica", 10, "bold"), fg="white", bg="#2C3E50", cursor="hand2")
        self.print_label.pack(side=tk.RIGHT, padx=10)
        self.print_label.bind("<Enter>", lambda e: self.print_label.config(fg="#D3D3D3"))
        self.print_label.bind("<Leave>", lambda e: self.print_label.config(fg="white"))
        self.print_label.bind("<Button-1>", lambda e: self.print_report())

        # Sidebar Section
        self.left_frame = tk.Frame(self.root, bg="#2C3E50", width=220)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=0, pady=0)

        # Right Section
        self.right_frame = tk.Frame(self.root, bg="#ffffff", width=700, relief="ridge", borderwidth=2)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Subheading Label
        self.subheading_label = tk.Label(self.right_frame, text="Select an option",
                                         font=("Helvetica", 14, "bold"), fg="#2C3E50", bg="#ffffff")
        self.subheading_label.pack(pady=10)

        # Payment Action Buttons
        buttons = [
            ("Create Payment", self.create_payment),
            ("List All", self.list_payments),
            ("Sort By ID", self.search_payment_by_id),
            ("Sort By Status", self.list_payments_by_status),
            ("Daily Payment", self.list_total_daily_payments),
            ("Debtor List", self.debtor_list),
            ("Void Payment", self.void_payment),
        ]

        for text, command in buttons:
            btn = tk.Button(self.left_frame, text=text,
                            command=lambda t=text, c=command: self.update_subheading(t, c),
                            width=9, font=("Helvetica", 10, "bold"), anchor="w", padx=10,
                            bg="#34495E", fg="white", relief="flat", bd=0)

            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1ABC9C"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#34495E"))
            btn.pack(pady=8, padx=15, anchor="w", fill="x")
        
        # Dashboard Shortcut
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

    def update_subheading(self, text, command):
        self.subheading_label.config(text=text)
        command()




    
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
        from dashboard import Dashboard
        Dashboard(self.root, self.token, self.username)

        self.root.destroy()
    



    def update_subheading(self, text, command):
        self.subheading_label.config(text=text)
        command()


    


    def fetch_and_display_paymentss(self):
        """Fetch booking data from the API"""
        url = "http://127.0.0.1:8000/payments/list"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                self.payments_data = response.json()
            else:
                self.payments_data = []
                messagebox.showerror("Error", "Failed to fetch payments.")

        except Exception as e:
            self.payments_data = []
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

        
        

    def create_payment(self):
        """Opens a professional pop-up window for creating a new payment."""
        create_window = tk.Toplevel(self.root)
        create_window.title("Create Payment")
        create_window.configure(bg="#dddddd")  # Light grey background

        # Set window size
        window_width = 500
        window_height = 400
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

        header_label = tk.Label(header_frame, text="Create Payment", font=("Arial", 14, "bold"), fg="white", bg="#2c3e50", pady=10)
        header_label.pack()

        # 🔹 Main Content Frame with Border
        frame = tk.Frame(create_window, bg="#ffffff", padx=20, pady=20, relief="ridge", borderwidth=3)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 🔹 Form Frame Inside Main Frame
        form_frame = tk.Frame(frame, bg="#ffffff", padx=10, pady=10)
        form_frame.grid(row=0, columnspan=2, pady=10, padx=10, sticky="ew")

        # 📌 Payment Fields
        fields = [
            ("Booking ID", tk.Entry),
            ("Amount Paid", tk.Entry),
            ("Discount Allowed", tk.Entry),
            ("Payment Method", ttk.Combobox),
            ("Payment Date", DateEntry),
        ]

        self.entries = {}

        for i, (label, field_type) in enumerate(fields):
            lbl = tk.Label(form_frame, text=label, font=("Helvetica", 12, "bold"), bg="#ffffff", fg="#2c3e50")
            lbl.grid(row=i, column=0, sticky="w", pady=5, padx=5)

            if field_type == ttk.Combobox:
                entry = field_type(form_frame, values=["Cash", "POS Card", "Bank Transfer"], state="readonly", font=("Helvetica", 12), width=20)
            elif field_type == DateEntry:
                entry = field_type(form_frame, font=("Helvetica", 12), width=12, background='darkblue', foreground='white', borderwidth=2)
            else:
                entry = field_type(form_frame, font=("Helvetica", 12), width=25)

            entry.grid(row=i, column=1, pady=5, padx=5, sticky="ew")
            self.entries[label] = entry  # ✅ Store entry reference with correct label text

        # 🔹 Submit Button
        btn_frame = tk.Frame(frame, bg="#ffffff")
        btn_frame.grid(row=len(fields), columnspan=2, pady=15)

        submit_btn = ttk.Button(btn_frame, text="Submit Payment", command=lambda: self.submit_payment(create_window), style="Bold.TButton")
        submit_btn.pack()




    def submit_payment(self, create_window):
        """Handles payment submission to the backend and closes the pop-up window."""
        try:
            booking_id_str = self.entries["Booking ID"].get().strip()
            if not booking_id_str.isdigit():
                messagebox.showerror("Error", "Booking ID must be a valid integer.")
                return
            booking_id = int(booking_id_str)

            amount_paid_str = self.entries["Amount Paid"].get().strip()
            if not amount_paid_str.replace(".", "", 1).isdigit():
                messagebox.showerror("Error", "Amount Paid must be a valid number.")
                return
            amount_paid = float(amount_paid_str)

            discount_allowed_str = self.entries["Discount Allowed"].get().strip()
            discount_allowed = float(discount_allowed_str) if discount_allowed_str.replace(".", "", 1).isdigit() else 0.0

            payment_method = self.entries["Payment Method"].get().strip()
            if not payment_method:
                messagebox.showerror("Error", "Payment Method is required.")
                return

            payment_date = self.entries["Payment Date"].get_date()
            payment_date = datetime(payment_date.year, payment_date.month, payment_date.day, 0, 0, 0, 0)
            payment_date = pytz.utc.localize(payment_date)
            payment_date_iso = payment_date.isoformat()

            payload = {
                "amount_paid": amount_paid,
                "discount_allowed": discount_allowed,
                "payment_method": payment_method,
                "payment_date": payment_date_iso,
            }

            url = f"http://127.0.0.1:8000/payments/{booking_id}"
            headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers)
            data = response.json()

            if response.status_code == 200:
                payment_details = data.get("payment_details")
                if payment_details:
                    payment_id = payment_details.get("payment_id")
                    created_by = payment_details.get("created_by")
                    messagebox.showinfo(
                        "Success", 
                        f"Payment created successfully!\nPayment ID: {payment_id}\nCreated By: {created_by}"
                    )
                    create_window.destroy()  # Close the pop-up window
                else:
                    messagebox.showerror("Error", "Payment ID missing in response.")
            else:
                messagebox.showerror("Error", data.get("detail", "Payment failed."))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")




    def list_payments(self):
        self.clear_right_frame()
        
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="List Payments", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
        
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
            command=self.fetch_payments
        )
        fetch_btn.grid(row=0, column=4, padx=10, pady=5)
        
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))  # Set the font to bold

        columns = (
        "ID", "Guest Name", "Room Number", "Amount Paid", "Discount Allowed",
        "Balance Due", "Payment Method", "Payment Date", "Status", "Booking ID", "Created_by"
        )

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
    
    def fetch_payments(self):
        api_url = "http://127.0.0.1:8000/payments/list"
        params = {
            "start_date": self.start_date.get_date().strftime("%Y-%m-%d"),
            "end_date": self.end_date.get_date().strftime("%Y-%m-%d"),
        }
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            response = requests.get(api_url, params=params, headers=headers)
            
            #print(response.json())  # Debugging: Check the response from the API

            if response.status_code == 200:
                data = response.json()

                if isinstance(data, dict) and "payments" in data:
                    payments = data["payments"]
                elif isinstance(data, list):
                    payments = data
                else:
                    messagebox.showinfo("info", "No payments found for the specified criteria")
                    return

                self.tree.delete(*self.tree.get_children())  # Clear the table

                if not payments:
                    messagebox.showinfo("No Results", "No payments found for the selected date range.")
                    total_amount = 0  # No payments means total is 0
                else:
                    # Calculate the total excluding voided payments
                    total_amount = sum(payment.get("amount_paid", 0) for payment in payments if payment.get("status") != "voided")

                    for payment in payments:
                        self.tree.insert("", "end", values=(
                            payment.get("payment_id", ""),
                            payment.get("guest_name", ""),
                            payment.get("room_number", ""),
                            f"{float(payment.get('amount_paid', 0)) :,.2f}",  # Format amount_paid
                            f"{float(payment.get('discount_allowed', 0)) :,.2f}",  # Format discount_allowed
                            f"{float(payment.get('balance_due', 0)) :,.2f}",  # Format balance_due
                            payment.get("payment_method", ""),
                            payment.get("payment_date", ""),
                            payment.get("status", ""),
                            payment.get("booking_id", ""),
                            payment.get("created_by", "N/A"),  # Ensure there's a fallback if "created_by" is missing
                        ))

                    self.apply_grid_effect()

                # Ensure any previous total label is removed before adding a new one
                for widget in self.right_frame.winfo_children():
                    if isinstance(widget, tk.Label) and "Total Payment" in widget.cget("text"):
                        widget.destroy()

                # Display total payment amount at the top
                self.total_label = tk.Label(self.right_frame, text=f"Total Payment: {total_amount:,.2f}",
                                            font=("Arial", 12, "bold"), bg="#ffffff", fg="blue")
                self.total_label.pack(side=tk.TOP, pady=5)
            else:
                messagebox.showerror("Error", response.json().get("detail", "Failed to retrieve payments."))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

            
 
    def list_payments_by_status(self):
        """Displays the List Payments by Status UI."""
        self.clear_right_frame()

        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="List Payments by Status", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
        
        filter_frame = tk.Frame(frame, bg="#ffffff")
        filter_frame.pack(pady=5)
        
        # Payment Status Dropdown
        tk.Label(filter_frame, text="Status:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)

        payment_status_options = ["payment completed", "payment incomplete", "voided"]
        self.payment_status_var = tk.StringVar(value=payment_status_options[0])  # Default selection

        status_menu = ttk.Combobox(filter_frame, textvariable=self.payment_status_var, values=payment_status_options, state="readonly")
        status_menu.grid(row=0, column=1, padx=5, pady=5)

        # Bind the selection event to update self.payment_status_var
        def on_payment_status_change(event):
            #print("Selected Payment Status:", self.payment_status_var.get())  # Debugging: Check what is selected
            self.payment_status_var.set(status_menu.get())  # Ensure value updates

        status_menu.bind("<<ComboboxSelected>>", on_payment_status_change)  # Event binding

        
        tk.Label(filter_frame, text="Start Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=2, padx=5, pady=5)
        self.payment_start_date = DateEntry(filter_frame, font=("Arial", 11))
        self.payment_start_date.grid(row=0, column=3, padx=5, pady=5)
        
        tk.Label(filter_frame, text="End Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=4, padx=5, pady=5)
        self.payment_end_date = DateEntry(filter_frame, font=("Arial", 11))
        self.payment_end_date.grid(row=0, column=5, padx=5, pady=5)
        
        fetch_btn = ttk.Button(filter_frame, text="Fetch Payments", command=self.fetch_payments_by_status)
        fetch_btn.grid(row=0, column=6, padx=10, pady=5)
        
        
        
        # Table Frame
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        

        
        columns = ("ID", "Guest Name", "Room Number", "Amount Paid", "Discount", "Balance Due", "Payment Method", "Payment Date", "Status", "Booking ID", "Created_by")
        
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

    def fetch_payments_by_status(self):
        """Fetch payments based on status and date filters."""


        api_url = "http://127.0.0.1:8000/payments/by-status"

        selected_status = self.payment_status_var.get().lower()  # Ensure it's lowercase if required by the backend
        start_date = self.payment_start_date.get_date().strftime("%Y-%m-%d")
        end_date = self.payment_end_date.get_date().strftime("%Y-%m-%d")

        params = {
            "status": selected_status,
            "start_date": start_date,
            "end_date": end_date,
        }

        headers = {"Authorization": f"Bearer {self.token}"}

        # Debugging: Print the API request details
        #print("Fetching payments with parameters:", params)

        try:
            response = requests.get(api_url, params=params, headers=headers)
            #print("API Response Status:", response.status_code)  # Debugging

            if response.status_code == 200:
                data = response.json()
                #print("API Response Data:", data)  # Debugging

                if "payments" in data and data["payments"]:
                    self.tree.delete(*self.tree.get_children())  # Clear previous data
                    #self.tree.delete(*self.tree.get_children())
                    
                    total_payment = 0  # Initialize total sum

                    for payment in data["payments"]:
                        is_voided = payment.get("status", "").lower() == "voided"
                        tag = "voided" if is_voided else "normal"

                        amount_paid = float(payment.get("amount_paid", 0))
                        total_payment += amount_paid

                        self.tree.insert("", "end", values=(
                            payment.get("payment_id", ""),
                            payment.get("guest_name", ""),
                            payment.get("room_number", ""),
                            f"{amount_paid:,.2f}",
                            f"{float(payment.get('discount_allowed', 0)):,.2f}",
                            f"{float(payment.get('balance_due', 0)):,.2f}",
                            payment.get("payment_method", ""),
                            payment.get("payment_date", ""),
                            payment.get("status", ""),
                            payment.get("booking_id", ""),
                            payment.get("created_by", ""),
                        ), tags=(tag,))

                    
                    # Apply the effect to the correct treeview (payment_tree)
                    self.apply_grid_effect(self.tree)
                    


                    self.tree.tag_configure("voided", foreground="red")
                    self.tree.tag_configure("normal", foreground="black")

                    # Display total payment sum below the table
                    if hasattr(self, "total_payment_label"):
                        self.total_payment_label.destroy()

                    self.total_payment_label = tk.Label(
                        self.right_frame,
                        text=f"Total Payment: {total_payment:,.2f}",
                        font=("Arial", 12, "bold"),
                        bg="#ffffff", fg="blue"
                    )
                    self.total_payment_label.pack(pady=10)

                    
                    

                else:
                    messagebox.showinfo("No Results", "No payments found for the selected filters.")
            else:
                error_message = response.json().get("detail", "Failed to retrieve payments.")
                messagebox.showerror("Error", f"API Error: {error_message}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")



        
   
   
    def debtor_list(self):
        self.clear_right_frame()

        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Debtor List", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        # Date range filter
        filter_frame = tk.Frame(frame, bg="#ffffff")
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Start Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.start_date = DateEntry(filter_frame, font=("Arial", 11))
        self.start_date.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(filter_frame, text="End Date:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=2, padx=5, pady=5)
        self.end_date = DateEntry(filter_frame, font=("Arial", 11))
        self.end_date.set_date(datetime.today())  # Default to current date
        self.end_date.grid(row=0, column=3, padx=5, pady=5)

        fetch_btn = ttk.Button(filter_frame, text="Fetch Debtor List", command=self.fetch_debtor_list)
        fetch_btn.grid(row=0, column=4, padx=10, pady=5)

        # Update the total label with blue text
        self.total_label = tk.Label(frame, text="Total Debt Amount: 0", font=("Arial", 12, "bold"), bg="#ffffff", fg="blue")
        self.total_label.pack(pady=5)

        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = (
            "Booking ID", "Guest Name", "Room Number", "Room Price", "Number of Days",
            "Total Due", "Total Paid", "Amount Due", "Booking Date", "Last Payment Date"
        )

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

    def fetch_debtor_list(self):
        api_url = "http://127.0.0.1:8000/payments/debtor_list"
        headers = {"Authorization": f"Bearer {self.token}"}

        params = {
            "start_date": self.start_date.get_date().strftime("%Y-%m-%d"),
            "end_date": self.end_date.get_date().strftime("%Y-%m-%d"),
        }

        try:
            response = requests.get(api_url, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json()

                # Update the total debt amount
                self.total_label.config(text=f"Total Debt Amount: {data.get('total_debt_amount', 0):,.2f}")

                debtors = data.get("debtors", [])
                if not debtors:
                    messagebox.showinfo("Info", "No debtors found.")
                    return

                self.tree.delete(*self.tree.get_children())

                for debtor in debtors:
                    self.tree.insert("", "end", values=(
                        debtor.get("booking_id", ""),
                        debtor.get("guest_name", ""),
                        debtor.get("room_number", ""),
                        f"{float(debtor.get('room_price', 0)) :,.2f}",
                        debtor.get("number_of_days", ""),
                        f"{float(debtor.get('total_due', 0)) :,.2f}",
                        f"{float(debtor.get('total_paid', 0)) :,.2f}",
                        f"{float(debtor.get('amount_due', 0)) :,.2f}",
                        debtor.get("booking_date", ""),
                        debtor.get("last_payment_date", "")
                    ))

                self.apply_grid_effect()
            else:
                #messagebox.showinfo("info", response.json().get("detail", "Failed to retrieve debtor list."))
                messagebox.showinfo("No Results", "No data found for the selected filters.")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")


    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.pack_forget()   
            
            
            

    def list_total_daily_payments(self):
        self.clear_right_frame()
        
        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(frame, text="Total Daily Payments", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)
        
        fetch_btn = ttk.Button(
            frame,
            text="Fetch Today's Payments",
            command=self.fetch_total_daily_payments
        )
        fetch_btn.pack(pady=5)
        
        # Apply green color to the total amount label
        self.total_label = tk.Label(frame, text="Total Amount: 0", font=("Arial", 12, "bold"), bg="#ffffff", fg="blue")
        self.total_label.pack(pady=5)
        
        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("ID", "Guest Name", "Room Number", "Amount Paid", "Discount Allowed", "Balance Due", "Payment Method", "Payment Date", "Status", "Booking ID")
        
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

    def fetch_total_daily_payments(self):
        api_url = "http://127.0.0.1:8000/payments/total_daily_payment"
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(api_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                
                total_amount = data.get("total_amount", 0)
                self.total_label.config(text=f"Total Amount: {total_amount:,.2f}")

                if "payments" in data:
                    payments = data["payments"]
                else:
                    payments = []
                
                self.tree.delete(*self.tree.get_children())
                
                for payment in payments:
                    self.tree.insert("", "end", values=(
                        payment.get("payment_id", ""),
                        payment.get("guest_name", ""),
                        payment.get("room_number", ""),
                        f"{float(payment.get('amount_paid', 0)) :,.2f}",
                        f"{float(payment.get('discount allowed', 0)) :,.2f}",
                        f"{float(payment.get('balance_due', 0)) :,.2f}",
                        payment.get("payment_method", ""),
                        payment.get("payment_date", ""),
                        payment.get("status", ""),
                        payment.get("booking_id", ""),
 
                    ))

                self.apply_grid_effect(self.search_tree)    
            else:
                messagebox.showerror("Error", response.json().get("detail", "Failed to retrieve payments."))
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")



    def search_payment_by_id(self):
        self.clear_right_frame()

        frame = tk.Frame(self.right_frame, bg="#ffffff", padx=10, pady=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(frame, text="Search Payment by ID", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        search_frame = tk.Frame(frame, bg="#ffffff")
        search_frame.pack(pady=5)

        tk.Label(search_frame, text="Payment ID:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.payment_id_entry = tk.Entry(search_frame, font=("Arial", 11))
        self.payment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        search_btn = ttk.Button(
            search_frame, text="Search", command=self.fetch_payment_by_id
        )
        search_btn.grid(row=0, column=2, padx=10, pady=5)

        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("ID", "Guest Name", "Room Number", "Amount Paid", "Discount Allowed", "Balance Due", 
                "Payment Method", "Payment Date", "Status", "Booking ID", "Created_by")
        

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

    def fetch_payment_by_id(self):
        payment_id = self.payment_id_entry.get().strip()

        if not payment_id.isdigit():  # Ensure input is numeric
            messagebox.showerror("Error", "Please enter a valid numeric payment ID.")
            return

        try:
            api_url = f"http://127.0.0.1:8000/payments/{payment_id}"
            headers = {"Authorization": f"Bearer {self.token}"}

            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data:  # Ensure data exists
                    # ✅ Check if the TreeView exists before modifying it
                    if hasattr(self, "tree") and self.tree is not None:
                        self.tree.delete(*self.tree.get_children())

                        # ✅ Extract payment details from the response
                        payment_id = data.get("payment_id", "")
                        guest_name = data.get("guest_name", "")
                        room_number = data.get("room_number", "")
                        amount_paid = f"{float(data.get('amount_paid', 0)) :,.2f}"  # Format amount
                        discount_allowed = f"{float(data.get('discount_allowed', 0)) :,.2f}"  # Format discount
                        balance_due = f"{float(data.get('balance_due', 0)) :,.2f}"  # Format balance
                        payment_method = data.get("payment_method", "")
                        payment_date = data.get("payment_date", "")
                        status = data.get("status", "").lower()  # Normalize status
                        booking_id = data.get("booking_id", "")
                        created_by = data.get("created_by", "")

                        

                        # ✅ Define tag for voided payments
                        tag = "voided" if status == "voided" else "normal"

                        # ✅ Insert data into TreeView
                        self.tree.insert("", "end", values=(
                            payment_id, guest_name, room_number, amount_paid, 
                            discount_allowed, balance_due, payment_method, 
                            payment_date, status, booking_id, created_by,
                        ), tags=(tag,))


                        # ✅ Apply color formatting
                        self.tree.tag_configure("voided", foreground="red")
                        self.tree.tag_configure("normal", foreground="black")

                        self.apply_grid_effect(self.tree)

                    else:
                        messagebox.showerror("Error", "Payment list is not initialized.")

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

        tk.Label(frame, text="Void Payment", font=("Arial", 14, "bold"), bg="#ffffff").pack(pady=10)

        input_frame = tk.Frame(frame, bg="#ffffff")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Payment ID:", font=("Arial", 11), bg="#ffffff").grid(row=0, column=0, padx=5, pady=5)
        self.payment_id_entry = tk.Entry(input_frame, font=("Arial", 11))
        self.payment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        void_btn = ttk.Button(
            input_frame, text="Void Payment", command=self.process_void_payment
        )
        void_btn.grid(row=0, column=2, padx=10, pady=5)

        table_frame = tk.Frame(frame, bg="#ffffff")
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("Payment ID", "Guest Name", "Room Number", "Amount Paid", "Discount Allowed",
                "Balance Due", "Payment Method", "Payment Date", "Payment Status", "Booking ID", "Booking Payment Status", "Created_by")

        self.void_payment_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.void_payment_tree.heading(col, text=col)
            self.void_payment_tree.column(col, width=80, anchor="center")

        self.void_payment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        y_scroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.void_payment_tree.yview)
        y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.void_payment_tree.configure(yscroll=y_scroll.set)

        x_scroll = ttk.Scrollbar(frame, orient="horizontal", command=self.void_payment_tree.xview)
        x_scroll.pack(fill=tk.X)
        self.void_payment_tree.configure(xscroll=x_scroll.set)


    def process_void_payment(self):
        payment_id = self.payment_id_entry.get().strip()

        if not payment_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric payment ID.")
            return

        try:
            # Fetch payment details first to check the status
            check_url = f"http://127.0.0.1:8000/payments/{payment_id}"
            headers = {"Authorization": f"Bearer {self.token}"}
            
            response = requests.get(check_url, headers=headers)

            if response.status_code == 200:
                payment_data = response.json()
                payment_status = payment_data.get("status", "").lower()  # Use "status" instead of "payment_status"

                if payment_status == "void":
                    messagebox.showerror("Error", f"This Payment ID {payment_id} has already been voided before.")
                    return  # Stop further execution
                
                # Proceed with voiding the payment if not already voided
                api_url = f"http://127.0.0.1:8000/payments/void/{payment_id}"
                void_response = requests.put(api_url, headers=headers)

                if void_response.status_code == 200:
                    data = void_response.json()
                    messagebox.showinfo("Success", data.get("message", "Payment has been voided."))
                    
                    # Fetch updated payment and booking data
                    self.fetch_voided_payment_by_id(payment_id)
                else:
                    messagebox.showerror("Error", void_response.json().get("detail", "Failed to void payment."))
            else:
                messagebox.showerror("Error", response.json().get("detail", "Payment record not found."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")




    def fetch_voided_payment_by_id(self, payment_id=None):
        if payment_id is None:
            payment_id = self.payment_id_entry.get().strip()

        if not payment_id.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric payment ID.")
            return

        try:
            api_url = f"http://127.0.0.1:8000/payments/{payment_id}"
            headers = {"Authorization": f"Bearer {self.token}"}

            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                if data:
                    if hasattr(self, "void_payment_tree") and self.void_payment_tree is not None:
                        self.void_payment_tree.delete(*self.void_payment_tree.get_children())  

                    # Insert payment details with booking payment_status
                    self.void_payment_tree.insert("", "end", values=(
                        data.get("payment_id", ""),
                        data.get("guest_name", ""),
                        data.get("room_number", ""),
                        f"{float(data.get('amount_paid', 0)) :,.2f}",
                        f"{float(data.get('discount_allowed', 0)) :,.2f}",
                        f"{float(data.get('balance_due', 0)) :,.2f}",
                        data.get("payment_method", ""),
                        data.get("payment_date", ""),
                        data.get("status", ""),  # Payment status (should be "voided")
                        data.get("booking_id", ""),
                        data.get("booking_payment_status", "N/A"),  # Display updated booking payment_status
                        data.get("created_by", ""),
                    ))

                    self.apply_grid_effect(self.search_tree)
                else:
                    messagebox.showinfo("No Results", "No payment found with the provided ID.")
            else:
                messagebox.showerror("Error", response.json().get("detail", "No payment found."))

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")
        
        

    