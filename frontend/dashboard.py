import tkinter as tk
from tkinter import messagebox
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
                               bg="#2C3E50", font=("Arial", 15, "bold"))
        title_label.pack(pady=10)

        # Menu Bar (Top Navigation)
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Adding main menu items (No dropdowns)
        self.menu_bar.add_command(label="Users", command=self.manage_users)
        self.menu_bar.add_command(label="Rooms", command=self.manage_rooms)
        self.menu_bar.add_command(label="Bookings", command=self.manage_bookings)
        self.menu_bar.add_command(label="Payments", command=self.manage_payments)
        self.menu_bar.add_command(label="Events", command=self.manage_events)
       # self.menu_bar.add_command(label="E-Payments", command=self.manage_payments)
        self.menu_bar.add_command(label="Logout", command=self.logout)

        # Main Content Frame
        self.main_content = tk.Frame(self.root, bg="#ECF0F1")
        self.main_content.pack(fill=tk.BOTH, expand=True)

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
