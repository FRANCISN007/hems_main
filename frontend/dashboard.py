import tkinter as tk
from tkinter import ttk, messagebox
from users_gui import UserManagement
from rooms_gui import RoomManagement
from bookings_gui import BookingManagement
from payment_gui import PaymentManagement
from event_gui import EventManagement  
from utils import load_token, get_user_role

class Dashboard:
    def __init__(self, root, token):
        self.root = root
        self.token = token
        self.root.title("Hotel & Event Management System")
        
        # Set full screen but allow minimize/maximize
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.state("zoomed")
        
        # Fetch user role
        self.user_role = get_user_role(self.token)
        
        # Header Frame
        self.header = tk.Frame(self.root, bg="#2C3E50", height=60)
        self.header.pack(fill=tk.X)
        
        title_label = tk.Label(self.header, text="Hotel & Event Management System", fg="white", 
                               bg="#2C3E50", font=("Arial", 18, "bold"))
        title_label.pack(pady=15)
        
        # Sidebar Frame
        self.sidebar = tk.Frame(self.root, bg="#2C3E50", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        
        # Main Content Frame
        self.main_content = tk.Frame(self.root, bg="#ECF0F1")
        self.main_content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Sidebar Buttons
        self.buttons = [
            ("Dashboard", None),
            ("Users", self.manage_users),
            ("Rooms", self.manage_rooms),
            ("Bookings", self.manage_bookings),
            ("Payments", self.manage_payments),
            ("Events", self.manage_events),
            ("Logout", self.logout)
        ]
        
        self.frames = {}
        for btn_text, command in self.buttons:
            btn = tk.Button(
                self.sidebar, text=btn_text, fg="white", bg="#34495E", font=("Arial", 12),
                command=lambda cmd=command: self.show_frame(cmd), height=2, width=20
            )
            btn.pack(pady=5)
        
        self.show_frame(None)
    
    def show_frame(self, command=None):
        for widget in self.main_content.winfo_children():
            widget.destroy()
        if command:
            command()
    
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
        PaymentManagement(self.root, self.token)
    
    def manage_events(self):
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
