import tkinter as tk
from tkinter import ttk, messagebox
import requests

class UserManagement:
    def __init__(self, parent, token):
        self.token = token
        self.parent = parent
        self.api_base_url = "http://127.0.0.1:8000"

        self.user_management_window = tk.Toplevel(parent)
        self.user_management_window.title("User Management")

        # Set window size and position
        window_width = 850
        window_height = 580
        screen_width = self.user_management_window.winfo_screenwidth()
        screen_height = self.user_management_window.winfo_screenheight()
        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2)
        self.user_management_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
        
        self.user_management_window.configure(bg="#2C2F33")

        self.setup_ui()
        self.fetch_users()

    def setup_ui(self):
        """Set up UI components including buttons and user table."""
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        
        header_label = tk.Label(
            self.user_management_window, text="User Management", 
            font=("Arial", 18, "bold"), bg="#2C2F33", fg="white"
        )
        header_label.pack(pady=10)

        options_frame = ttk.Frame(self.user_management_window)
        options_frame.pack(fill=tk.X, pady=5, padx=10)

        self.add_button = tk.Button(options_frame, text="➕ Add User", command=self.add_user, bg="#7289DA", fg="white", width=15)
        self.add_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.update_button = tk.Button(options_frame, text="✏️ Update User", command=self.update_user, bg="#F1C40F", fg="black", width=15)
        self.update_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.delete_button = tk.Button(options_frame, text="❌ Delete User", command=self.delete_user, bg="#E74C3C", fg="white", width=15)
        self.delete_button.grid(row=0, column=2, padx=5, pady=5)

        tree_frame = ttk.Frame(self.user_management_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tree_scroll_y = ttk.Scrollbar(tree_frame, orient="vertical")
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.users_treeview = ttk.Treeview(
            tree_frame,
            columns=("ID", "Username", "Role"),
            show="headings",
            height=15
        )
        
        self.users_treeview.heading("ID", text="User ID", anchor="center")
        self.users_treeview.column("ID", width=80, anchor="center")
        self.users_treeview.heading("Username", text="Username", anchor="center")
        self.users_treeview.column("Username", width=250, anchor="center")
        self.users_treeview.heading("Role", text="Role", anchor="center")
        self.users_treeview.column("Role", width=150, anchor="center")
        
        self.users_treeview.pack(fill=tk.BOTH, expand=True)
        self.users_treeview.configure(yscrollcommand=tree_scroll_y.set)
        tree_scroll_y.configure(command=self.users_treeview.yview)

    def fetch_users(self):
        try:
            response = requests.get(
                f"{self.api_base_url}/users",
                headers={"Authorization": f"Bearer {self.token}"}
            )
            response.raise_for_status()
            users = response.json()
            self.populate_treeview(users)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch users: {e}")

    def populate_treeview(self, users):
        for row in self.users_treeview.get_children():
            self.users_treeview.delete(row)
        for user in users:
            self.users_treeview.insert("", tk.END, values=(user["id"], user["username"], user["role"]))
    
     
    
    
    def add_user(self):
        self.open_user_form("Add User", self.submit_new_user)

    def update_user(self):
        selected_item = self.users_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to update.")
            return

        values = self.users_treeview.item(selected_item)["values"]
        self.open_user_form("Update User", self.submit_updated_user, values)

    def delete_user(self):
        selected_item = self.users_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a user to delete.")
            return

        username = self.users_treeview.item(selected_item)["values"][1]

        if messagebox.askyesno("Delete User", f"Are you sure you want to delete '{username}'?"):
            try:
                response = requests.delete(
                    f"{self.api_base_url}/users/{username}",
                    headers={"Authorization": f"Bearer {self.token}"}
                )

                if response.status_code == 200:
                    messagebox.showinfo("Success", "User deleted successfully.")
                    self.fetch_users()
                else:
                    messagebox.showerror("Error", f"Failed to delete user: {response.text}")
            except Exception as e:
                messagebox.showerror("Error", f"Error: {e}")

    
    def open_user_form(self, title, submit_callback, values=None):
        """Opens a professional pop-up form for user management."""
        form_window = tk.Toplevel(self.user_management_window)
        form_window.title(title)
        form_window.configure(bg="#f8f9fa")  # Light background

        # Set window size and center it
        window_width, window_height = 400, 350
        x_coordinate = (form_window.winfo_screenwidth() - window_width) // 2
        y_coordinate = (form_window.winfo_screenheight() - window_height) // 2
        form_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        # Make it modal
        form_window.transient(self.user_management_window)
        form_window.grab_set()

        # 🔹 Header Section
        header = tk.Label(form_window, text=title, font=("Arial", 14, "bold"), fg="white", bg="#2c3e50", pady=8)
        header.pack(fill=tk.X)

        # 🔹 Form Frame
        form_frame = tk.Frame(form_window, bg="white", padx=15, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        labels = ["Username", "Password", "Role"]
        entries = {}

        for label in labels:
            tk.Label(form_frame, text=label, font=("Arial", 11, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
            
            if label == "Role":
                role_combobox = ttk.Combobox(form_frame, values=["user", "admin"], state="readonly", width=28)
                role_combobox.pack(pady=5)
                role_combobox.set(values[2] if values else "user")
                entries["Role"] = role_combobox
            else:
                entry = ttk.Entry(form_frame, width=30, font=("Arial", 11))
                if label == "Password":
                    entry.config(show="*")
                entry.pack(pady=5)
                if values and label == "Username":
                    entry.insert(0, values[1])
                entries[label] = entry

        # Admin Password Field
        admin_password_label = tk.Label(form_frame, text="Admin Password:", font=("Arial", 11, "bold"), bg="white", fg="#2c3e50")
        admin_password_entry = ttk.Entry(form_frame, width=30, show="*", font=("Arial", 11))

        def toggle_admin_password(event):
            if role_combobox.get() == "admin":
                admin_password_label.pack(anchor="w")
                admin_password_entry.pack(pady=5)
            else:
                admin_password_label.pack_forget()
                admin_password_entry.pack_forget()

        role_combobox.bind("<<ComboboxSelected>>", toggle_admin_password)
        entries["Admin Password"] = admin_password_entry

        # 🔹 Submit Button
        submit_btn = ttk.Button(form_window, text="Submit", command=lambda: submit_callback(entries, form_window))
        submit_btn.pack(pady=10)

        form_window.mainloop()



    def submit_new_user(self, entries, form_window):
        data = {key.lower(): entry.get() for key, entry in entries.items()}
        if data["role"] == "admin" and not data["admin password"]:
            messagebox.showerror("Error", "Admin password is required when registering an admin.")
            return
        try:
            
            response = requests.post(
                f"{self.api_base_url}/users/register/",
                json=data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code in [200, 201]:
                messagebox.showinfo("Success", "User added successfully.")
                form_window.destroy()
                self.fetch_users()
            else:
                error_message = response.json().get("detail", response.text)
                messagebox.showerror("Error", f"Failed to add user: {error_message}")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")
        


    def submit_updated_user(self, entries, form_window):
        data = {key.lower(): entry.get() for key, entry in entries.items()}
        selected_item = self.users_treeview.selection()
        if not selected_item:
            messagebox.showerror("Error", "No user selected for update.")
            return
        username = self.users_treeview.item(selected_item)["values"][1]
        try:
            response = requests.put(
                f"{self.api_base_url}/users/{username}",
                json=data,
                headers={"Authorization": f"Bearer {self.token}"}
            )
            if response.status_code == 200:
                messagebox.showinfo("Success", "User updated successfully.")
                form_window.destroy()
                self.fetch_users()
        except Exception as e:
            messagebox.showerror("Error", f"Error: {e}")