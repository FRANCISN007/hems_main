import customtkinter as ctk
from tkinter import messagebox
import requests
import os
from dashboard import Dashboard  # Import the Dashboard class

class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.configure(bg="#2c3e50")

        icon_path = os.path.abspath("frontend/icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        self.api_base_url = "http://127.0.0.1:8000"
        
        self.main_frame = ctk.CTkFrame(self.root, fg_color="#2c3e50")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.create_login_ui()

    def create_login_ui(self):
        self.clear_window()
        
        frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        frame.pack(padx=40, pady=20, fill="x", expand=True)

        ctk.CTkLabel(frame, text="Login", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.username_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=200)
        self.username_entry.pack(pady=5, padx=40, fill='x')
        
        self.password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=200)
        self.password_entry.pack(pady=5, padx=40, fill='x')
        
        ctk.CTkButton(frame, text="Login", command=self.login).pack(pady=10)
        ctk.CTkButton(frame, text="Register", command=self.create_register_ui, fg_color="gray").pack(pady=5)

    def create_register_ui(self):
        self.clear_window()
        
        frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        frame.pack(padx=40, pady=20, fill="x", expand=True)

        ctk.CTkLabel(frame, text="Register", font=("Arial", 18, "bold")).pack(pady=10)
        
        self.reg_username_entry = ctk.CTkEntry(frame, placeholder_text="Username", width=200)
        self.reg_username_entry.pack(pady=5, padx=40, fill='x')
        
        self.reg_password_entry = ctk.CTkEntry(frame, placeholder_text="Password", show="*", width=200)
        self.reg_password_entry.pack(pady=5, padx=40, fill='x')
        
        self.role_combobox = ctk.CTkComboBox(frame, values=["user", "admin"], command=self.toggle_admin_password)
        self.role_combobox.pack(pady=5, padx=40, fill='x')
        self.role_combobox.set("user")
        
        self.admin_password_entry = ctk.CTkEntry(frame, placeholder_text="Admin Password", show="*", width=200)
        
        ctk.CTkButton(frame, text="Register", command=self.register).pack(pady=10)
        ctk.CTkButton(frame, text="Back to Login", command=self.create_login_ui, fg_color="gray").pack(pady=5)

    def toggle_admin_password(self, choice):
        if choice == "admin":
            self.admin_password_entry.pack(pady=5, padx=40, fill='x')
        else:
            self.admin_password_entry.pack_forget()

    def clear_window(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        
        try:
            response = requests.post(f"{self.api_base_url}/users/token", data={"username": username, "password": password})
            response.raise_for_status()
            data = response.json()
            token = data.get("access_token")
            
            if token:
                messagebox.showinfo("Success", "Login successful!")
                self.root.destroy()
                dashboard_root = ctk.CTk()
                Dashboard(dashboard_root, username, token)
                dashboard_root.mainloop()
            else:
                messagebox.showerror("Error", "Invalid response from server.")
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Login failed: {e}")

    def register(self):
        username = self.reg_username_entry.get()
        password = self.reg_password_entry.get()
        role = self.role_combobox.get()
        admin_password = self.admin_password_entry.get() if role == "admin" else None
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return
        
        if role == "admin" and not admin_password:
            messagebox.showerror("Error", "Admin password is required for admin registration.")
            return
        
        try:
            data = {"username": username, "password": password, "role": role, "admin_password": admin_password}
            response = requests.post(f"{self.api_base_url}/users/register/", json=data)
            response.raise_for_status()
            messagebox.showinfo("Success", "User registered successfully!")
            self.create_login_ui()
        except requests.RequestException as e:
            messagebox.showerror("Error", f"Registration failed: {e}")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    app = LoginGUI(root)
    root.mainloop()
