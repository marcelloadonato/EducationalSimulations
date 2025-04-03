import customtkinter as ctk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import math

# Set theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CalculusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Interactive Calculus Explorer")
        self.geometry("1200x800")  # Increased size to accommodate text
        self.configure(fg_color="#171721")

        # Configure grid
        self.grid_columnconfigure(0, weight=1)  # Plot frame
        self.grid_columnconfigure(1, weight=0)  # Controls frame
        self.grid_rowconfigure(0, weight=0)  # Title
        self.grid_rowconfigure(1, weight=1)  # Main content
        
        # Title and Description
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=(20,0))
        
        title = ctk.CTkLabel(
            title_frame,
            text="Interactive Calculus Explorer",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        )
        title.pack()
        
        description = ctk.CTkLabel(
            title_frame,
            text="Explore the fundamental concepts of calculus using an interactive quadratic function.\n"
                 "Adjust the coefficients (a, b, c) to modify the function f(x) = ax² + bx + c and observe how derivatives and integrals change.",
            font=ctk.CTkFont(size=14),
            text_color="#a0a0a0",
            wraplength=800
        )
        description.pack(pady=(5,0))

        # Main content frame
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=20)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=0)

        # Left side (plots and explanations)
        left_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, sticky="nsew")

        # Plot frame
        self.plot_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        self.plot_frame.pack(fill="both", expand=True)

        self.fig, self.axs = plt.subplots(1, 2, figsize=(12, 6), facecolor='#171721')
        plt.style.use('dark_background')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        # Explanatory text frame
        text_frame = ctk.CTkFrame(left_frame, fg_color="#1e1e2e")
        text_frame.pack(fill="x", pady=(20,0))

        # Add explanatory text for both visualizations
        derivative_text = (
            "Left Plot - Derivatives and Tangent Lines:\n"
            "• The purple curve shows the quadratic function f(x)\n"
            "• The dashed line is the tangent line at point x₀\n"
            "• The red dot shows the point of tangency\n"
            "• The slope of the tangent line equals f'(x₀) = 2ax₀ + b\n"
            "• This visualizes the derivative as the instantaneous rate of change"
        )
        
        integral_text = (
            "Right Plot - Definite Integrals:\n"
            "• The shaded region shows the area between f(x) and the x-axis\n"
            "• This area represents the definite integral from x_lower to x_upper\n"
            "• The integral ∫f(x)dx gives the signed area under the curve\n"
            "• Positive when f(x) > 0, negative when f(x) < 0\n"
            "• The antiderivative F(x) = (a/3)x³ + (b/2)x² + cx"
        )

        derivative_label = ctk.CTkLabel(
            text_frame,
            text=derivative_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="w",
            text_color="#ffffff"
        )
        derivative_label.pack(side="left", padx=20, pady=15)

        separator = ctk.CTkFrame(text_frame, width=2, fg_color="#2d2d3f")
        separator.pack(side="left", fill="y", padx=10, pady=10)

        integral_label = ctk.CTkLabel(
            text_frame,
            text=integral_text,
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="w",
            text_color="#ffffff"
        )
        integral_label.pack(side="left", padx=20, pady=15)

        # Controls Frame (right side)
        self.controls_frame = ctk.CTkFrame(content_frame, width=250, fg_color="#1e1e2e")
        self.controls_frame.grid(row=0, column=1, sticky="ns", padx=(20,0))
        self.controls_frame.grid_propagate(False)

        # Function parameters label
        params_label = ctk.CTkLabel(
            self.controls_frame,
            text="Function Parameters",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        params_label.grid(row=0, column=0, padx=15, pady=(15,5), sticky="w")

        # Sliders
        self.sliders = {}
        slider_params = {
            "a": {"min": -5.0, "max": 5.0, "value": 1.0, "description": "Coefficient of x²"},
            "b": {"min": -5.0, "max": 5.0, "value": 0.0, "description": "Coefficient of x"},
            "c": {"min": -10.0, "max": 10.0, "value": 0.0, "description": "Constant term"},
            "x₀": {"min": -10.0, "max": 10.0, "value": 0.0, "description": "Point of tangency"},
            "x_lower": {"min": -10.0, "max": 10.0, "value": -5.0, "description": "Lower bound of integral"},
            "x_upper": {"min": -10.0, "max": 10.0, "value": 5.0, "description": "Upper bound of integral"}
        }

        row_index = 1
        for name, params in slider_params.items():
            # Parameter name and current value
            label = ctk.CTkLabel(
                self.controls_frame,
                text=f"{name}: {params['value']:.2f}",
                anchor="w",
                font=ctk.CTkFont(size=14)
            )
            label.grid(row=row_index, column=0, padx=15, pady=(15,0), sticky="w")
            row_index += 1
            
            # Parameter description
            desc_label = ctk.CTkLabel(
                self.controls_frame,
                text=params['description'],
                anchor="w",
                font=ctk.CTkFont(size=12),
                text_color="#a0a0a0"
            )
            desc_label.grid(row=row_index, column=0, padx=15, pady=(0,5), sticky="w")
            row_index += 1

            slider = ctk.CTkSlider(
                self.controls_frame,
                from_=params["min"],
                to=params["max"],
                number_of_steps=200,
                command=lambda value, n=name: self.update_slider_label(n, value)
            )
            slider.set(params["value"])
            slider.grid(row=row_index, column=0, padx=15, pady=(0,15), sticky="ew")
            self.sliders[name] = {"widget": slider, "label": label, "value": params["value"]}
            row_index += 1

        self.update_plot()

    def update_slider_label(self, name, value):
        self.sliders[name]["value"] = value
        self.sliders[name]["label"].configure(text=f"{name}: {value:.2f}")
        # Ensure lower bound is less than upper bound
        if name == "x_lower" and value >= self.sliders["x_upper"]["value"]:
             self.sliders["x_upper"]["widget"].set(value + 0.1) # Adjust upper slightly
             self.update_slider_label("x_upper", value + 0.1)
             return # Avoid redundant plot update if upper also changed
        elif name == "x_upper" and value <= self.sliders["x_lower"]["value"]:
             self.sliders["x_lower"]["widget"].set(value - 0.1) # Adjust lower slightly
             self.update_slider_label("x_lower", value - 0.1)
             return # Avoid redundant plot update if lower also changed

        self.update_plot()


    # --- Calculus Functions (from notebook) ---
    def function(self, x, a, b, c):
        return a * x**2 + b * x + c

    def derivative(self, x, a, b, c):
        return 2 * a * x + b

    def tangent_line(self, x, a, b, c, x0):
        return self.function(x0, a, b, c) + self.derivative(x0, a, b, c) * (x - x0)

    def integrate_function(self, a, b, c, x_lower, x_upper):
        F = lambda x_val: (a / 3) * x_val**3 + (b / 2) * x_val**2 + c * x_val
        # Handle potential numerical issues if bounds are identical
        if abs(x_upper - x_lower) < 1e-9:
            return 0.0
        return F(x_upper) - F(x_lower)

    # --- Plotting ---
    def update_plot(self):
        a = self.sliders["a"]["value"]
        b = self.sliders["b"]["value"]
        c = self.sliders["c"]["value"]
        x0 = self.sliders["x₀"]["value"]
        x_lower = self.sliders["x_lower"]["value"]
        x_upper = self.sliders["x_upper"]["value"]

        # Clear previous plots
        for ax in self.axs:
            ax.clear()
            # Reset style potentially cleared by clear()
            ax.set_facecolor('#1e1e2e')
            ax.grid(True, color='#2d2d3f', linestyle='--')
            ax.spines['bottom'].set_color('#a0a0a0')
            ax.spines['top'].set_color('#a0a0a0')
            ax.spines['left'].set_color('#a0a0a0')
            ax.spines['right'].set_color('#a0a0a0')
            ax.tick_params(axis='x', colors='#a0a0a0')
            ax.tick_params(axis='y', colors='#a0a0a0')
            ax.xaxis.label.set_color('#a0a0a0')
            ax.yaxis.label.set_color('#a0a0a0')
            ax.title.set_color('#ffffff')


        x = np.linspace(-10, 10, 400)
        y = self.function(x, a, b, c)
        y_tan = self.tangent_line(x, a, b, c, x0)
        f_x0 = self.function(x0, a, b, c)

        # Prepare equations
        func_eq = f"$f(x) = {a:.2f}x^2 {'+' if b>=0 else '-'} {abs(b):.2f}x {'+' if c>=0 else '-'} {abs(c):.2f}$"
        fprime_x0 = self.derivative(x0, a, b, c)
        tangent_eq = f"$T(x) = {f_x0:.2f} {'+' if fprime_x0>=0 else '-'} {abs(fprime_x0):.2f}(x {'-' if x0>=0 else '+'} {abs(x0):.2f})$"

        # Subplot 1: Function and tangent
        self.axs[0].plot(x, y, label='f(x)', lw=2, color='#6c5ce7')
        self.axs[0].plot(x, y_tan, label=f'Tangent at x={x0:.2f}', lw=2, linestyle='--', color='#845ef7')
        self.axs[0].scatter([x0], [f_x0], color='#ff6b6b', zorder=5, s=50) # Enhanced point
        self.axs[0].set_xlabel('x')
        self.axs[0].set_ylabel('f(x)')
        self.axs[0].set_title('Function and Tangent Line')
        self.axs[0].legend(facecolor='#252538', edgecolor='#a0a0a0', labelcolor='#ffffff')
        # Dynamic Y limits based on visible function range + tangent point
        visible_y = np.concatenate((y, [f_x0], y_tan)) # Include tangent line in y-limit calculation
        min_y = np.min(visible_y)
        max_y = np.max(visible_y)
        padding = (max_y - min_y) * 0.1 # Add 10% padding
        self.axs[0].set_ylim(min_y - padding, max_y + padding)
        self.axs[0].set_xlim(-10, 10)

        # Subplot 2: Integral
        self.axs[1].plot(x, y, label='f(x)', lw=2, color='#6c5ce7')
        ix = np.linspace(x_lower, x_upper, 200)
        iy = self.function(ix, a, b, c)
        self.axs[1].fill_between(ix, iy, color='#4c3b99', alpha=0.6) # Adjusted color/alpha
        self.axs[1].set_xlabel('x')
        self.axs[1].set_ylabel('f(x)')
        self.axs[1].set_title('Definite Integral (Area)')
        # Match Y limits with the first plot for consistency
        self.axs[1].set_ylim(self.axs[0].get_ylim())
        self.axs[1].set_xlim(-10, 10)

        # Display integral value
        integral_value = self.integrate_function(a, b, c, x_lower, x_upper)
        integral_text = f"$\int_{{{x_lower:.2f}}}^{{{x_upper:.2f}}} f(x) dx = {integral_value:.3f}$"
        self.axs[1].text(0.5, 0.95, integral_text,
                    transform=self.axs[1].transAxes, fontsize=12, verticalalignment='top', horizontalalignment='center',
                    bbox=dict(boxstyle="round", facecolor="#252538", alpha=0.8), color='#ffffff') # Themed bbox

        # Add overall title with equations
        self.fig.suptitle(f"{func_eq}\n{tangent_eq}", fontsize=14, y=0.98, color='#ffffff')

        # Adjust layout and draw
        self.fig.tight_layout(rect=[0, 0, 1, 0.95]) # Adjust rect to prevent title overlap
        self.canvas.draw()

if __name__ == "__main__":
    app = CalculusApp()
    app.mainloop() 