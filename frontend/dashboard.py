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
    def __init__(self, root, token):
        self.root = root
        self.token = token
        self.root.title("Hotel & Event Management System")


        # Debugging: Print icon paths
        icon_ico_path = os.path.abspath("frontend/icon.ico").replace("\\", "/")
        icon_png_path = os.path.abspath("frontend/icon.png").replace("\\", "/")

        # Try using ICO first
        if os.path.exists(icon_ico_path):
            self.root.iconbitmap(icon_ico_path)
        elif os.path.exists(icon_png_path):
            try:
                # Load and resize the PNG icon
                icon_img = Image.open(icon_png_path)
                icon_resized = icon_img.resize((80, 80))  # Adjust size (e.g., 128x128 if needed)
                self.icon_image = ImageTk.PhotoImage(icon_resized)

                # Set the resized icon
                self.root.iconphoto(True, self.icon_image)
            except Exception as e:
                print(f"Error loading PNG icon: {e}")
        else:
            print("Error: Icon file not found!")


        # Set full screen but allow minimize/maximize
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.state("zoomed")

        # Fetch user role
        self.user_role = get_user_role(self.token)

        # Header Frame
        self.header = tk.Frame(self.root, bg="#D3D3D3", height=60)
        self.header.pack(fill=tk.X)


        title_label = tk.Label(self.header, text="Dashboard", fg="black",
                               bg="#D3D3D3", font=("Arial", 12, "bold"))
        title_label.pack(pady=5)

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


        # Outer Border Frame (Creates the Frame around the screen)
        self.border_frame = tk.Frame(self.root, bg="gray", padx=5, pady=5)  # Gray border
        self.border_frame.pack(fill=tk.BOTH, expand=True)

        # Main Content Frame inside the Border Frame
        self.main_content = tk.Frame(self.border_frame, bg="#F2F3F4", bd=5, relief=tk.RIDGE)
        self.main_content.pack(fill=tk.BOTH, expand=True)


        # Main Content Frame
        #self.main_content = tk.Frame(self.root, bg="#F2F3F4")
        #self.main_content.pack(fill=tk.BOTH, expand=True)

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
