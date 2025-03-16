import tkinter as tk
from CTkMessagebox import CTkMessagebox
import requests
from login_gui import LoginGUI
from PIL import Image, ImageTk
import os

API_URL = "http://127.0.0.1:8000/license"  # FastAPI server URL

class LicenseGUI(tk.Toplevel):
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
            self.iconbitmap(icon_ico_path)
        elif os.path.exists(icon_png_path):
            try:
                icon_img = Image.open(icon_png_path)
                icon_resized = icon_img.resize((80, 80))
                self.icon_image = ImageTk.PhotoImage(icon_resized)
                self.iconphoto(True, self.icon_image)
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
            CTkMessagebox(title="Input Error", message="Please enter both license password and key.", icon="cancel")
            return

        try:
            response = requests.post(
                f"{API_URL}/generate?license_password={license_password}&key={key}", 
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            new_license = response.json()
            CTkMessagebox(title="License Generated", message=f"New License Key: {new_license['key']}", icon="check")

        except requests.exceptions.HTTPError as err:
            if response.status_code == 400:
                error_message = response.json().get("detail", "License key already exists.")
                CTkMessagebox(title="Error", message=error_message, icon="cancel")
            elif response.status_code == 403:
                CTkMessagebox(title="Error", message="Invalid license password.", icon="cancel")
            else:
                CTkMessagebox(title="Error", message=f"HTTP Error: {response.status_code} - {response.text}", icon="cancel")

        except requests.exceptions.RequestException as e:
            CTkMessagebox(title="Error", message=f"Request failed: {e}", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An unexpected error occurred: {e}", icon="cancel")

    def verify_license(self):
        key = self.verify_key_entry.get()

        if not key:
            CTkMessagebox(title="Input Error", message="Please enter a license key.", icon="cancel")
            return

        try:
            response = requests.get(f"{API_URL}/verify/{key}")
            response.raise_for_status()
            result = response.json()

            if result["valid"]:
                msg = CTkMessagebox(title="License Valid", 
                                    message="The license key is valid!", 
                                    icon="check", 
                                    option_1="OK")

                if msg.get() == "OK":  # Only proceed if user clicks OK
                    self.destroy()
                    login_window = tk.Toplevel(self.master)
                    LoginGUI(login_window)
            else:
                CTkMessagebox(title="Invalid License", message=result["message"], icon="warning")

        except requests.exceptions.HTTPError:
            CTkMessagebox(title="Error", message="Invalid license key", icon="cancel")
        except Exception as e:
            CTkMessagebox(title="Error", message=f"An unexpected error occurred: {e}", icon="cancel")

# Main Execution
root = tk.Tk()
root.withdraw()
license_splash = LicenseGUI(root)
root.mainloop()