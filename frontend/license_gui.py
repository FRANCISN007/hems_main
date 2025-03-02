import tkinter as tk
from tkinter import messagebox
import requests
from login_gui import LoginGUI

API_URL = "http://127.0.0.1:8000/license"  # FastAPI server URL


class SplashScreen(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Welcome")
        self.state('zoomed')  # Fullscreen splash
        self.configure(bg="black")

        # Welcome text
        self.label = tk.Label(self, text="Welcome to Hotel and Event Management System", 
                              font=("Arial", 28, "bold"), fg="white", bg="black")
        self.label.place(relx=0.5, rely=0.65, anchor="center")  # Positioned lower

        # Produced by text (italicized)
        self.produced_by_label = tk.Label(self, text="Produced by School of Accounting Package", 
                                          font=("Arial", 13, "italic"), fg="white", bg="black")
        self.produced_by_label.place(relx=0.5, rely=0.72, anchor="center")  # Positioned under main text


class LicenseGUI(tk.Toplevel):
    def __init__(self, master, splash_screen):
        super().__init__(master)
        self.master = master  # Store reference to root window
        self.splash_screen = splash_screen  # Store reference to splash screen
        self.title("License Management")
        self.geometry("500x400")

        # Keep License Window on top of Splash
        self.transient(self.splash_screen)  # Makes License screen modal
        self.grab_set()  # Prevents interacting with splash until license is verified

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Position above the splash text (not centered)
        x_position = (screen_width - 500) // 2
        y_position = (screen_height - 720) // 2  # Slightly higher to avoid covering text

        self.geometry(f"500x400+{x_position}+{y_position}")

        self.generate_frame = tk.LabelFrame(self, text="Generate License Key", padx=10, pady=10)
        self.generate_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.password_label = tk.Label(self.generate_frame, text="Admin License Password:")
        self.password_label.pack(padx=5, pady=5)

        self.password_entry = tk.Entry(self.generate_frame, show="*", width=30)
        self.password_entry.pack(padx=5, pady=5)

        self.key_label = tk.Label(self.generate_frame, text="License Key:")
        self.key_label.pack(padx=5, pady=5)

        self.key_entry = tk.Entry(self.generate_frame, width=30)
        self.key_entry.pack(padx=5, pady=5)

        self.generate_button = tk.Button(self.generate_frame, text="Generate License", command=self.generate_license)
        self.generate_button.pack(pady=10)

        self.verify_frame = tk.LabelFrame(self, text="Verify License Key", padx=10, pady=10)
        self.verify_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.verify_key_label = tk.Label(self.verify_frame, text="Enter License Key to Verify:")
        self.verify_key_label.pack(padx=5, pady=5)

        self.verify_key_entry = tk.Entry(self.verify_frame, width=30)
        self.verify_key_entry.pack(padx=5, pady=5)

        self.verify_button = tk.Button(self.verify_frame, text="Verify License", command=self.verify_license)
        self.verify_button.pack(pady=10)

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

                # Destroy Splash and License screens before opening the dashboard
                if self.splash_screen:
                    self.splash_screen.destroy()
                self.destroy()
                
                # Open the dashboard (Login Window)
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

splash = SplashScreen(root)

# Reduce Splash Delay to 2 seconds before showing License GUI (on top of splash)
root.after(2000, lambda: LicenseGUI(root, splash))  

root.mainloop()
