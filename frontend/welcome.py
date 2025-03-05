import tkinter as tk
import random

class WelcomeWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Welcome")
        self.attributes('-fullscreen', True)  # Fullscreen mode
        self.configure(bg="black")  # Background color

        # Create canvas for animation
        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Create falling text
        self.text_id = self.canvas.create_text(self.winfo_screenwidth() // 2, 50, 
                                               text="Welcome to Hotel and Event Management System",
                                               font=("Arial", 24, "bold"), fill="white")

        # Create falling stars
        self.stars = []
        self.create_stars()

        # Start animations
        self.animate_text()
        self.animate_stars()

        # Automatically close after **10 seconds**
        self.after(7000, self.destroy)

    def create_stars(self):
        """Create multiple stars at random positions"""
        colors = ["yellow", "white", "gold", "lightblue", "lightgreen"]
        for _ in range(20):  # Number of stars
            x = random.randint(10, self.winfo_screenwidth() - 10)
            y = random.randint(10, self.winfo_screenheight() - 10)
            size = random.randint(3, 7)
            color = random.choice(colors)
            star = self.canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
            self.stars.append((star, random.randint(2, 5)))  # Store star and speed

    def animate_text(self):
        """Move text downwards like falling effect"""
        x, y = self.canvas.coords(self.text_id)
        if y < self.winfo_screenheight() - 100:
            self.canvas.move(self.text_id, 0, 3)
            self.after(50, self.animate_text)

    def animate_stars(self):
        """Move stars downwards like a falling effect"""
        for star, speed in self.stars:
            x1, y1, x2, y2 = self.canvas.coords(star)
            if y2 < self.winfo_screenheight():
                self.canvas.move(star, 0, speed)
            else:
                self.canvas.coords(star, random.randint(10, self.winfo_screenwidth() - 10), 0,
                                   random.randint(10, self.winfo_screenwidth() - 10) + 5, 5)

        self.after(20, self.animate_stars)  # Repeat animation


# Run the welcome window
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    welcome = WelcomeWindow(root)
    welcome.mainloop()
