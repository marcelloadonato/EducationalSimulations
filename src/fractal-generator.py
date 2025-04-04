import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Set CustomTkinter appearance mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class FractalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Mandelbrot Set Explorer")
        self.root.geometry("1200x800")

        # Main frame setup
        main_frame = ctk.CTkFrame(root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title frame
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.pack(fill="x", padx=5, pady=(5, 0))
        title_label = ctk.CTkLabel(title_frame, text="Interactive Mandelbrot Set Explorer",
                                   font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(padx=5, pady=(5, 0))

        # Explanation text
        explanation_text = ctk.CTkTextbox(main_frame, height=100, wrap="word")
        explanation_text.pack(fill="x", padx=5, pady=5)
        explanation_text.insert("1.0", """The Mandelbrot Set is a famous fractal named after Benoît Mandelbrot. It is defined as the set of complex numbers c for which the function f(z) = z² + c does not diverge when iterated from z=0.

Explore the fractal by zooming in and out, panning, and adjusting the maximum number of iterations. Observe the intricate patterns and self-similarity at different scales.""")
        explanation_text.configure(state="disabled")

        # Content frame
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Control frame
        control_frame = ctk.CTkFrame(content_frame)
        control_frame.pack(side="left", fill="y", padx=5, pady=5)

        # Plot frame
        self.plot_frame = ctk.CTkFrame(content_frame)
        self.plot_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        # Zoom buttons
        zoom_frame = ctk.CTkFrame(control_frame)
        zoom_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(zoom_frame, text="Zoom In", command=self.zoom_in).pack(side="left", padx=5)
        ctk.CTkButton(zoom_frame, text="Zoom Out", command=self.zoom_out).pack(side="left", padx=5)

        # Pan buttons
        pan_frame = ctk.CTkFrame(control_frame)
        pan_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(pan_frame, text="←", command=lambda: self.pan("left")).pack(side="left", padx=5)
        ctk.CTkButton(pan_frame, text="→", command=lambda: self.pan("right")).pack(side="left", padx=5)
        ctk.CTkButton(pan_frame, text="↑", command=lambda: self.pan("up")).pack(side="left", padx=5)
        ctk.CTkButton(pan_frame, text="↓", command=lambda: self.pan("down")).pack(side="left", padx=5)

        # Reset button
        ctk.CTkButton(control_frame, text="Reset", command=self.reset_view).pack(fill="x", padx=5, pady=5)

        # Max iterations slider
        self.max_iter_var = tk.IntVar(value=100)
        self.create_slider(control_frame, "Max Iterations:", self.max_iter_var, 10, 500, 0)

        # Color map selection
        self.cmap_var = tk.StringVar(value="viridis")
        cmap_options = ["viridis", "plasma", "inferno", "magma", "cividis"]
        ctk.CTkLabel(control_frame, text="Color Map:").pack(pady=5)
        ctk.CTkOptionMenu(control_frame, variable=self.cmap_var, values=cmap_options,
                          command=self.update_plot).pack(fill="x", padx=5, pady=5)

        # View label
        self.view_label_var = tk.StringVar()
        ctk.CTkLabel(control_frame, textvariable=self.view_label_var).pack(pady=5)

        # Initialize Matplotlib plot
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.fig.patch.set_facecolor('#242424')
        self.ax.set_facecolor('#1c1c1c')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        # Initial view parameters
        self.center_x = -0.5
        self.center_y = 0
        self.scale = 1.5  # Half the width of the view
        self.zoom_factor = 0.5
        self.pan_factor = 0.1

        # Draw initial plot
        self.update_plot()

    def create_slider(self, parent, label, variable, min_val, max_val, row):
        """Create a slider with label and value display."""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="x", padx=5, pady=3)

        # Container for the slider components
        slider_container = ctk.CTkFrame(frame, fg_color="transparent")
        slider_container.pack(fill="x", expand=True)

        # Label
        label = ctk.CTkLabel(slider_container, text=label, font=ctk.CTkFont(size=12), width=100, anchor="w")
        label.pack(side="left", padx=(5, 0))

        # Value label (pack this first so it appears on the right)
        value_label = ctk.CTkLabel(slider_container, text=f"{variable.get()}", font=ctk.CTkFont(size=12), width=30)
        value_label.pack(side="right", padx=(0, 5))

        # Slider
        slider = ctk.CTkSlider(slider_container, from_=min_val, to=max_val, variable=variable,
                            number_of_steps=(max_val - min_val), width=150, height=16)
        slider.pack(side="left", fill="x", expand=True, padx=5)

        def update_label_and_plot(*args):
            value_label.configure(text=f"{variable.get()}")
            self.update_plot()

        variable.trace_add("write", update_label_and_plot)
        return slider

    def compute_mandelbrot(self, width, height, max_iter):
        """Compute the Mandelbrot Set for the current view."""
        real_min = self.center_x - self.scale
        real_max = self.center_x + self.scale
        imag_min = self.center_y - self.scale * height / width
        imag_max = self.center_y + self.scale * height / width

        real = np.linspace(real_min, real_max, width)
        imag = np.linspace(imag_min, imag_max, height)
        c = real[:, np.newaxis] + 1j * imag[np.newaxis, :]

        z = np.zeros_like(c)
        escape_time = np.zeros(c.shape, dtype=int)

        for i in range(max_iter):
            mask = np.abs(z) < 2
            z[mask] = z[mask]**2 + c[mask]
            escape_time += mask

        # Points that didn't escape get value 0
        escape_time[escape_time == max_iter] = 0
        return escape_time, real_min, real_max, imag_min, imag_max

    def update_plot(self, *args):
        """Update the fractal plot based on current parameters."""
        width, height = 800, 600
        max_iter = self.max_iter_var.get()
        cmap = self.cmap_var.get()

        escape_time, real_min, real_max, imag_min, imag_max = self.compute_mandelbrot(width, height, max_iter)

        # Update view label
        self.view_label_var.set(f"View: Re [{real_min:.2f}, {real_max:.2f}], Im [{imag_min:.2f}, {imag_max:.2f}]")

        # Redraw plot
        self.ax.clear()
        self.ax.imshow(escape_time.T, origin='lower', extent=(real_min, real_max, imag_min, imag_max), cmap=cmap)
        self.ax.set_title('Mandelbrot Set', color='white')
        self.ax.set_xlabel('Re', color='white')
        self.ax.set_ylabel('Im', color='white')
        self.canvas.draw()

    def zoom_in(self):
        """Zoom in by reducing the scale."""
        self.scale *= self.zoom_factor
        self.update_plot()

    def zoom_out(self):
        """Zoom out by increasing the scale."""
        self.scale /= self.zoom_factor
        self.update_plot()

    def pan(self, direction):
        """Pan the view in the specified direction."""
        pan_amount = self.pan_factor * self.scale
        if direction == "left":
            self.center_x -= pan_amount
        elif direction == "right":
            self.center_x += pan_amount
        elif direction == "up":
            self.center_y += pan_amount
        elif direction == "down":
            self.center_y -= pan_amount
        self.update_plot()

    def reset_view(self):
        """Reset to the initial view."""
        self.center_x = -0.5
        self.center_y = 0
        self.scale = 1.5
        self.update_plot()

def main():
    root = ctk.CTk()
    app = FractalGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()