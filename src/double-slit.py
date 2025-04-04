import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class DoubleSlitGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Double-Slit Experiment Simulation")
        self.root.geometry("1200x800")

        # Protocol for window close button
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Title
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        title_label = ctk.CTkLabel(title_frame, text="Double-Slit Experiment Simulation",
                                   font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(padx=5, pady=5)

        # Explanation
        explanation_text = ctk.CTkTextbox(main_frame, height=100, wrap="word")
        explanation_text.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        explanation_text.insert("1.0", """The double-slit experiment demonstrates the wave-particle duality of quantum mechanics. Even when particles are sent one by one, they build up an interference pattern characteristic of waves. Adjust the slit separation (d) and wavelength (λ) to see how the pattern changes.""")
        explanation_text.configure(state="disabled")

        # Content frame
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        main_frame.rowconfigure(2, weight=1)

        # Control frame
        control_frame = ctk.CTkFrame(content_frame)
        control_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5)

        # Back button
        back_button = ctk.CTkButton(
            control_frame,
            text="← Back to Menu",
            command=self.on_closing,
            width=150,
            height=32,
            corner_radius=16,
            font=ctk.CTkFont(size=14),
            fg_color="#4c3b99",
            hover_color="#5c4aad"
        )
        back_button.grid(row=2, column=0, padx=5, pady=20)

        # Sliders
        self.d_var = tk.DoubleVar(value=1.0)
        self.lambda_var = tk.DoubleVar(value=1.0)
        self.create_slider(control_frame, "Slit Separation (d):", self.d_var, 0.1, 5.0, 0)
        self.create_slider(control_frame, "Wavelength (λ):", self.lambda_var, 0.1, 5.0, 1)

        # Plot frame
        self.plot_frame = ctk.CTkFrame(content_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        content_frame.columnconfigure(1, weight=3)

        # Parameters
        self.x_max = 10  # Screen half-width
        self.N = 1000    # Number of points
        self.x = np.linspace(-self.x_max, self.x_max, self.N)
        self.D = 1.0     # Distance to screen
        self.particles = []  # List of particle positions

        # Matplotlib setup
        plt.style.use('dark_background')
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.line, = self.ax.plot(self.x, np.zeros(self.N), label='Theoretical Pattern', color='cyan')
        self.scat = self.ax.scatter([], [], c='red', alpha=0.1, s=1, label='Particle Detections')
        self.ax.set_xlim(-self.x_max, self.x_max)
        self.ax.set_ylim(0, 1.1)
        self.ax.set_xlabel('Position on Screen')
        self.ax.set_ylabel('Intensity')
        self.ax.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Initial update
        self.update_P()

        # Animation - using Tkinter's after method instead of FuncAnimation
        self.is_animating = True
        self.animate_frame()

    def create_slider(self, parent, label, variable, min_val, max_val, row):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, sticky="ew", padx=5, pady=3)
        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=12), width=100, anchor="w").grid(row=0, column=0, padx=(5, 0))
        slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, variable=variable, number_of_steps=100, width=150)
        slider.grid(row=0, column=1, sticky="ew", padx=5)
        value_label = ctk.CTkLabel(frame, text=f"{variable.get():.1f}", font=ctk.CTkFont(size=12), width=30)
        value_label.grid(row=0, column=2, padx=(0, 5))

        def update_label_and_P(*args):
            value_label.configure(text=f"{variable.get():.1f}")
            self.update_P()
        variable.trace_add("write", update_label_and_P)
        frame.columnconfigure(1, weight=1)
        return slider

    def update_P(self):
        d = self.d_var.get()
        lambda_ = self.lambda_var.get()
        # Compute intensity
        I = np.cos(np.pi * d * self.x / (lambda_ * self.D))**2
        # Normalize for probability
        self.P = I / np.sum(I)
        # Update theoretical curve (normalized to max=1)
        self.line.set_ydata(I / np.max(I))
        # Reset particles
        self.particles = []
        self.scat.set_offsets(np.empty((0, 2)))  # Create empty 2D array with shape (0,2)
        self.canvas.draw()

    def animate_frame(self):
        if not hasattr(self, 'is_animating') or not self.is_animating:
            return
            
        if len(self.particles) < 10000:  # Limit total particles
            # Sample 10 particles per frame
            indices = np.random.choice(self.N, size=10, p=self.P)
            new_xs = self.x[indices]
            self.particles.extend(new_xs)
            # Add small random y for visibility
            y_rand = np.random.uniform(-0.05, 0.05, len(self.particles))
            self.scat.set_offsets(np.c_[self.particles, y_rand])
            self.canvas.draw()
        
        # Schedule next frame
        if hasattr(self, 'is_animating') and self.is_animating:
            self.root.after(50, self.animate_frame)

    def on_closing(self):
        # Stop the animation
        self.is_animating = False
        
        # Close matplotlib figure
        plt.close(self.fig)
        
        # Destroy the window
        self.root.destroy()

    def __del__(self):
        self.is_animating = False

# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = DoubleSlitGUI(root)
    root.mainloop()