import tkinter as tk
from tkinter import messagebox
from users_gui import UserManagement
from rooms_gui import RoomManagement
from bookings_gui import BookingManagement
from payment_gui import PaymentManagement
from event_gui import EventManagement  
from utils import load_token, get_user_role
import os
from PIL import Image, ImageTk


class Dashboard:
    def __init__(self, root, username, token):
        self.root = root
        self.token = token
        self.username = username
        self.root.title("Hotel & Event Management System")
        self.root.geometry("1200x700")
        self.root.state("zoomed")
        self.user_role = get_user_role(self.token)

        # Set application icon
        icon_path = os.path.abspath("frontend/icon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # HEADER FRAME
        self.header = tk.Frame(self.root, bg="#2C3E50", height=60)
        self.header.pack(fill=tk.X)

        title_label = tk.Label(self.header, text="Dashboard                                                              Welcome to Hotel & Event Management System    ", fg="white", bg="#2C3E50", 
                               font=("Arial", 14, "bold"))
        title_label.pack(side=tk.LEFT, padx=20, pady=10)
        

        # SIDEBAR FRAME
        self.sidebar = tk.Frame(self.root, bg="#34495E", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # MENU BUTTONS IN SIDEBAR
        menu_items = [
            ("Users", self.manage_users),
            ("Rooms", self.manage_rooms),
            ("Bookings", self.manage_bookings),
            ("Payments", self.manage_payments),
            ("Events", self.manage_events),
        ]

        for text, command in menu_items:
            btn = tk.Button(self.sidebar, text=text, command=command, fg="white", bg="#2C3E50",
                            font=("Arial", 12), relief=tk.FLAT, padx=10, pady=5, anchor="w")
            btn.pack(fill=tk.X, pady=5, padx=10)
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#1ABC9C"))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#2C3E50"))

        # LOGOUT BUTTON (Under "Events" in Sidebar)
        logout_btn = tk.Button(self.sidebar, text="Logout", command=self.logout, fg="white", 
                               bg="#2C3E50", font=("Arial", 12), relief=tk.FLAT, padx=10, pady=5, anchor="w")
        logout_btn.pack(fill=tk.X, pady=20, padx=10)  # Added more space before logout
        logout_btn.bind("<Enter>", lambda e: logout_btn.config(bg="#E74C3C"))  # Red on hover
        logout_btn.bind("<Leave>", lambda e: logout_btn.config(bg="#2C3E50"))  # Back to default

        # MAIN CONTENT FRAME
        self.main_content = tk.Frame(self.root, bg="#ECF0F1", bd=5, relief=tk.RIDGE)
        self.main_content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        welcome_label = tk.Label(self.main_content, text="", 
                                 fg="#2C3E50", bg="#ECF0F1", font=("Arial", 14, "bold"))
        welcome_label.pack(pady=20)

    def manage_users(self):
        if self.user_role != "admin":
            messagebox.showerror("Access Denied", "You do not have permission to manage users.")
            return
        UserManagement(self.root, self.token)

    def manage_rooms(self):
        RoomManagement(self.root, self.token)

    def manage_bookings(self):
        BookingManagement(self.root, self.token)

    def manage_payments(self):
        PaymentManagement(self.root, self.username, self.token)

    def manage_events(self):
        """Opens the Event Management window"""
        EventManagement(self.root, self.token)

    def logout(self):
        self.root.destroy()
        root = tk.Tk()
        from login_gui import LoginGUI
        LoginGUI(root)
        root.mainloop()


if __name__ == "__main__":
    token = load_token()
    if token:
        root = tk.Tk()
        Dashboard(root, token)
        root.mainloop()
    else:
        print("No token found. Please log in.")
