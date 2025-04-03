import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import tkinter as tk

# Set appearance mode and default color theme for customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LorenzAttractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Lorenz Attractor Simulation")
        self.root.geometry("1200x800")
        
        # Create main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Create title frame
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=(5,0))
        
        # Add title
        title_label = ctk.CTkLabel(title_frame, 
                                 text="Interactive Lorenz Attractor Simulation",
                                 font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(padx=5, pady=(5,0))
        
        # Add subtitle
        subtitle_label = ctk.CTkLabel(title_frame, 
                                    text="Exploring Chaos Theory and Atmospheric Convection",
                                    font=ctk.CTkFont(size=16))
        subtitle_label.pack(padx=5, pady=(0,5))
        
        # Create content frame
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create left panel for controls and explanation
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create controls section
        controls_frame = ctk.CTkFrame(left_panel)
        controls_frame.pack(fill="x", padx=5, pady=5)
        
        # Create variables for sliders
        self.sigma_var = tk.DoubleVar(value=10.0)
        self.beta_var = tk.DoubleVar(value=2.666)
        self.rho_var = tk.DoubleVar(value=28.0)
        self.x0_var = tk.DoubleVar(value=1.0)
        self.y0_var = tk.DoubleVar(value=1.0)
        self.z0_var = tk.DoubleVar(value=1.0)
        self.t_max_var = tk.DoubleVar(value=40.0)
        
        # Add sliders
        self.create_slider(controls_frame, "σ (Sigma):", self.sigma_var, 0, 20, 0.1, 0)
        self.create_slider(controls_frame, "β (Beta):", self.beta_var, 0, 10, 0.1, 1)
        self.create_slider(controls_frame, "ρ (Rho):", self.rho_var, 0, 50, 0.1, 2)
        self.create_slider(controls_frame, "X₀:", self.x0_var, -20, 20, 0.1, 3)
        self.create_slider(controls_frame, "Y₀:", self.y0_var, -30, 30, 0.1, 4)
        self.create_slider(controls_frame, "Z₀:", self.z0_var, 0, 50, 0.1, 5)
        self.create_slider(controls_frame, "t_max:", self.t_max_var, 10, 100, 1, 6)
        
        # Add educational text
        edu_text = ctk.CTkTextbox(left_panel, height=200, wrap="word")
        edu_text.pack(fill="both", expand=True, padx=5, pady=5)
        edu_text.insert("1.0", """The Lorenz Attractor is a system of differential equations originally developed to model atmospheric convection. It is one of the most famous examples of how deterministic systems can exhibit chaotic behavior.

Parameters:
• σ (Sigma): Controls the rate of convection
• β (Beta): Related to the physical dimensions of the system
• ρ (Rho): Drives the buoyancy in the system
• X₀, Y₀, Z₀: Initial conditions
• t_max: Duration of simulation

The system demonstrates sensitive dependence on initial conditions—a hallmark of chaos theory. Small changes in parameters or initial conditions can lead to dramatically different trajectories over time.

Try dragging the sliders to see how small changes affect the system's behavior!""")
        edu_text.configure(state="disabled")
        
        # Create plot frame
        self.plot_frame = ctk.CTkFrame(content_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        content_frame.columnconfigure(1, weight=3)
        content_frame.columnconfigure(0, weight=1)
        
        # Initialize the plot
        self.fig = None
        self.canvas = None
        self._update_job = None  # For tracking delayed updates
        self.update_plot()
    
    def create_slider(self, parent, label, variable, min_val, max_val, step, row):
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        
        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w")
        
        slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, variable=variable,
                             width=200, height=16)
        slider.grid(row=0, column=1, sticky="ew", padx=5)
        
        value_label = ctk.CTkLabel(frame, text=f"{variable.get():.3f}",
                                 font=ctk.CTkFont(size=12))
        value_label.grid(row=0, column=2, sticky="e", padx=(0, 5))
        
        frame.columnconfigure(1, weight=1)
        
        def update_label_and_plot(*args):
            value_label.configure(text=f"{variable.get():.3f}")
            # Only cancel if a job is scheduled
            if self._update_job is not None:
                self.root.after_cancel(self._update_job)
            self._update_job = self.root.after(100, self.update_plot)
        
        variable.trace_add("write", update_label_and_plot)
        return slider
    
    def lorenz(self, state, t, sigma, beta, rho):
        """Compute the derivatives for the Lorenz system."""
        x, y, z = state
        dxdt = sigma * (y - x)
        dydt = x * (rho - z) - y
        dzdt = x * y - beta * z
        return [dxdt, dydt, dzdt]
    
    def update_plot(self):
        print("Updating plot... sigma:", self.sigma_var.get(), "beta:", self.beta_var.get(), "rho:", self.rho_var.get(), "x0:", self.x0_var.get(), "y0:", self.y0_var.get(), "z0:", self.z0_var.get(), "t_max:", self.t_max_var.get())
        sigma = self.sigma_var.get()
        beta = self.beta_var.get()
        rho = self.rho_var.get()
        x0 = self.x0_var.get()
        y0 = self.y0_var.get()
        z0 = self.z0_var.get()
        t_max = self.t_max_var.get()
        t = np.linspace(0, t_max, 10000)
        initial_state = [x0, y0, z0]
        states = odeint(self.lorenz, initial_state, t, args=(sigma, beta, rho))
        
        if self.fig is None:
            self.fig = plt.Figure(figsize=(10, 8))
            self.fig.patch.set_facecolor('#242424')
            self.ax = self.fig.add_subplot(111, projection='3d')
            self.ax.set_facecolor('#E5E5E5')
            self.ax.plot(states[:, 0], states[:, 1], states[:, 2], lw=0.5, color='#1f77b4')
            self.ax.set_xlabel('X', color='black')
            self.ax.set_ylabel('Y', color='black')
            self.ax.set_zlabel('Z', color='black')
            self.ax.set_title('Lorenz Attractor', color='black', pad=20)
            self.ax.tick_params(colors='black')
            for spine in self.ax.spines.values():
                spine.set_color('black')
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        else:
            self.ax.clear()
            self.ax.set_facecolor('#E5E5E5')
            self.ax.plot(states[:, 0], states[:, 1], states[:, 2], lw=0.5, color='#1f77b4')
            self.ax.set_xlabel('X', color='black')
            self.ax.set_ylabel('Y', color='black')
            self.ax.set_zlabel('Z', color='black')
            self.ax.set_title('Lorenz Attractor', color='black', pad=20)
            self.ax.tick_params(colors='black')
            for spine in self.ax.spines.values():
                spine.set_color('black')
            self.canvas.draw()

def main():
    root = ctk.CTk()
    app = LorenzAttractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
