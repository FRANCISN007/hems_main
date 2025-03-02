import tkinter as tk
from tkinter import messagebox
import requests
from login_gui import LoginGUI

API_URL = "http://127.0.0.1:8000/license"  # FastAPI server URL

class LicenseSplashScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("License & Welcome")
        self.state('zoomed')  # Fullscreen window
        self.configure(bg="#2C3E50")
        
        # Enlarged License Frame (Moved Down)
        self.license_frame = tk.Frame(self, bg="white", padx=40, pady=30)
        self.license_frame.place(relx=0.5, rely=0.45, anchor="center", width=500, height=380)  # Increased height

        tk.Label(self.license_frame, text="Admin License Password:", font=("Arial", 12, "bold")).pack(padx=5, pady=5)
        self.password_entry = tk.Entry(self.license_frame, show="*", width=35, font=("Arial", 12))
        self.password_entry.pack(padx=5, pady=5)

        tk.Label(self.license_frame, text="License Key:", font=("Arial", 12, "bold")).pack(padx=5, pady=5)
        self.key_entry = tk.Entry(self.license_frame, width=35, font=("Arial", 12))
        self.key_entry.pack(padx=5, pady=5)
        
        tk.Button(self.license_frame, text="Generate License", font=("Arial", 12), command=self.generate_license).pack(pady=10)
        
        tk.Label(self.license_frame, text="Enter License Key to Verify:", font=("Arial", 12, "bold")).pack(padx=5, pady=5)
        self.verify_key_entry = tk.Entry(self.license_frame, width=35, font=("Arial", 12))
        self.verify_key_entry.pack(padx=5, pady=5)
        
        # 🛠️ Fixed Button Display Issue
        tk.Button(self.license_frame, text="Verify License", font=("Arial", 12), command=self.verify_license).pack(pady=15)

        tk.Label(self, text="✦  W E L C O M E  ✦\nHotel & Event Management System", 
         font=("Century Gothic", 24, "bold"), fg="white", bg="#2C3E50",
         padx=10, pady=5).place(relx=0.5, rely=0.08, anchor="n")  # Adjusted position

        tk.Label(self, text="Produced & Licensed by School of Accounting Package", 
                 font=("Arial", 10, "italic"), fg="white", bg="#2C3E50").place(relx=0.8, rely=0.94, anchor="n")  # Added more space below
        
        tk.Label(self, text="© 2025", 
                 font=("Arial", 10, "italic"), fg="white", bg="#2C3E50").place(relx=0.85, rely=0.97, anchor="n")  # Added more space below




    def generate_license(self):
        license_password = self.password_entry.get()
        key = self.key_entry.get()

        if not license_password or not key:
            messagebox.showerror("Input Error", "Please enter both license password and key.")
            return

        try:
            response = requests.post(
                f"{API_URL}/generate?license_password={license_password}&key={key}", 
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            new_license = response.json()
            messagebox.showinfo("License Generated", f"New License Key: {new_license['key']}")
        except requests.exceptions.HTTPError:
            messagebox.showerror("Error", "Wrong password entered.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    def verify_license(self):
        key = self.verify_key_entry.get()

        if not key:
            messagebox.showerror("Input Error", "Please enter a license key.")
            return

        try:
            response = requests.get(f"{API_URL}/verify/{key}")
            response.raise_for_status()
            result = response.json()

            if result["valid"]:
                messagebox.showinfo("License Valid", "The license key is valid!")
                self.destroy()
                login_window = tk.Toplevel(self.master)
                LoginGUI(login_window)
            else:
                messagebox.showwarning("Invalid License", result["message"])
        except requests.exceptions.HTTPError:
            messagebox.showerror("Error", "Invalid license key")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

# Main Execution
root = tk.Tk()
root.withdraw()
license_splash = LicenseSplashScreen(root)
root.mainloop()
