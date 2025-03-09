import tkinter as tk
from tkinter import messagebox
import requests
from login_gui import LoginGUI
from PIL import Image, ImageTk
import os



API_URL = "http://127.0.0.1:8000/license"  # FastAPI server URL

class LicenseSplashScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("License & Welcome")
        self.state('zoomed')  # Fullscreen window
        self.configure(bg="#2C3E50")

        # Debugging: Print icon paths
        icon_ico_path = os.path.abspath("frontend/icon.ico").replace("\\", "/")
        icon_png_path = os.path.abspath("frontend/icon.png").replace("\\", "/")

        # Try using ICO first
        if os.path.exists(icon_ico_path):
            self.iconbitmap(icon_ico_path)  # ✅ Fixed: Use `self`, not `self.root`
        elif os.path.exists(icon_png_path):
            try:
                # Load and resize the PNG icon
                icon_img = Image.open(icon_png_path)
                icon_resized = icon_img.resize((80, 80))  # Adjust size (e.g., 128x128 if needed)
                self.icon_image = ImageTk.PhotoImage(icon_resized)

                # Set the resized icon
                self.iconphoto(True, self.icon_image)  # ✅ Fixed: Use `self`, not `self.root`
            except Exception as e:
                print(f"Error loading PNG icon: {e}")
        else:
            print("Error: Icon file not found!")

        # Enlarged License Frame (Moved Down)
        self.license_frame = tk.Frame(self, bg="white", padx=40, pady=30)
        self.license_frame.place(relx=0.5, rely=0.45, anchor="center", width=500, height=380)

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

        tk.Button(self.license_frame, text="Verify License", font=("Arial", 12), command=self.verify_license).pack(pady=15)

        tk.Label(self, text="✦  W E L C O M E  ✦\nHotel & Event Management System", 
                 font=("Century Gothic", 24, "bold"), fg="white", bg="#2C3E50",
                 padx=10, pady=5).place(relx=0.5, rely=0.08, anchor="n")

        tk.Label(self, text="Produced & Licensed by School of Accounting Package", 
                 font=("Arial", 10, "italic"), fg="white", bg="#2C3E50").place(relx=0.8, rely=0.94, anchor="n")

        tk.Label(self, text="© 2025", 
                 font=("Arial", 10, "italic"), fg="white", bg="#2C3E50").place(relx=0.85, rely=0.97, anchor="n")

    def generate_license(self):
        license_password = self.password_entry.get()
        key = self.key_entry.get()

        if not license_password or not key:
            messagebox.showerror("Input Error", "Please enter both license password and key.")
            return

        try:
            # Send request with query parameters
            response = requests.post(
                f"{API_URL}/generate?license_password={license_password}&key={key}", 
                headers={"Content-Type": "application/json"}
            )

            response.raise_for_status()  # Raise an exception if HTTP error occurs
            new_license = response.json()  # Parse response JSON

            messagebox.showinfo("License Generated", f"New License Key: {new_license['key']}")

        except requests.exceptions.HTTPError as err:
            if response.status_code == 400:
                # ✅ Handle duplicate license key error
                error_message = response.json().get("detail", "License key already exists.")
                messagebox.showerror("Error", error_message)
            elif response.status_code == 403:
                messagebox.showerror("Error", "Invalid license password.")
            else:
                messagebox.showerror("Error", f"HTTP Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Request failed: {e}")

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
