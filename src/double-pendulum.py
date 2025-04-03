#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Interactive Double Pendulum Simulation Notebook
# Built by Grok 3 (xAI) - March 30, 2025

# Import necessary libraries
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.scrolledtext as scrolledtext

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Educational Introduction ---
print("""
<h1>Interactive Double Pendulum Simulation</h1>
<h3>Exploring Chaos Theory and Physics</h3>
<p>The double pendulum is a fascinating physical system where two pendulums are attached end-to-end. Despite its simple setup, it exhibits <b>chaotic behavior</b>, making it a perfect tool to study chaos theory and sensitivity to initial conditions.</p>
<p><b>History:</b> Studied since the 17th century, the double pendulum became a cornerstone of chaos theory in the 20th century.</p>
<p><b>Physics:</b> Its motion is governed by a set of nonlinear differential equations derived from Lagrangian mechanics.</p>
<p><b>Chaos:</b> Small changes in initial conditions can lead to drastically different outcomes—try it yourself!</p>
""")

class DoublePendulumGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Double Pendulum Simulation")
        
        # Configure root window
        self.root.geometry("1200x800")
        
        # Create main frame
        main_frame = ctk.CTkFrame(root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # Create educational content frame
        edu_frame = ctk.CTkFrame(main_frame)
        edu_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        
        # Add title
        title_label = ctk.CTkLabel(edu_frame, text="Interactive Double Pendulum Simulation",
                                 font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(padx=5, pady=(5,0))
        
        # Add subtitle
        subtitle_label = ctk.CTkLabel(edu_frame, text="Exploring Chaos Theory and Physics",
                                   font=ctk.CTkFont(size=16))
        subtitle_label.pack(padx=5, pady=(0,5))
        
        # Add educational text
        edu_text = ctk.CTkTextbox(edu_frame, height=100, wrap="word")
        edu_text.pack(padx=5, pady=5, fill="both", expand=True)
        edu_text.insert("1.0", """The double pendulum is a fascinating physical system where two pendulums are attached end-to-end. Despite its simple setup, it exhibits chaotic behavior, making it a perfect tool to study chaos theory and sensitivity to initial conditions.

History: Studied since the 17th century, the double pendulum became a cornerstone of chaos theory in the 20th century.
Physics: Its motion is governed by a set of nonlinear differential equations derived from Lagrangian mechanics.
Chaos: Small changes in initial conditions can lead to drastically different outcomes—try it yourself!""")
        edu_text.configure(state="disabled")
        
        # Create content frame
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Create controls frame
        controls_frame = ctk.CTkFrame(content_frame)
        controls_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Create sliders
        self.L1_var = tk.DoubleVar(value=1.0)
        self.L2_var = tk.DoubleVar(value=1.0)
        self.m1_var = tk.DoubleVar(value=1.0)
        self.m2_var = tk.DoubleVar(value=1.0)
        self.theta1_var = tk.DoubleVar(value=90)
        self.theta2_var = tk.DoubleVar(value=90)
        self.g_var = tk.DoubleVar(value=9.8)
        
        # Add sliders with modern styling
        self.create_slider(controls_frame, "L₁ (m):", self.L1_var, 0.1, 2.0, 0)
        self.create_slider(controls_frame, "L₂ (m):", self.L2_var, 0.1, 2.0, 1)
        self.create_slider(controls_frame, "m₁ (kg):", self.m1_var, 0.1, 5.0, 2)
        self.create_slider(controls_frame, "m₂ (kg):", self.m2_var, 0.1, 5.0, 3)
        self.create_slider(controls_frame, "θ₁ (°):", self.theta1_var, -180, 180, 4)
        self.create_slider(controls_frame, "θ₂ (°):", self.theta2_var, -180, 180, 5)
        self.create_slider(controls_frame, "g (m/s²):", self.g_var, 1.0, 20.0, 6)
        
        # Add parameter explanations with modern styling
        explanation_text = ctk.CTkTextbox(controls_frame, height=150, wrap="word")
        explanation_text.grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        explanation_text.insert("1.0", """Parameter Explanations:

L₁, L₂: Lengths of the pendulums (0.1–2.0 m)
m₁, m₂: Masses of the bobs (0.1–5.0 kg)
θ₁, θ₂: Initial angles (-180° to 180°)
g: Gravitational acceleration (1.0–20.0 m/s²)""")
        explanation_text.configure(state="disabled")
        
        # Add Start button with modern styling
        self.start_button = ctk.CTkButton(controls_frame, text="Start Simulation",
                                       command=self.start_simulation,
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.start_button.grid(row=7, column=0, columnspan=2, pady=10)
        
        # Create plot frame
        self.plot_frame = ctk.CTkFrame(content_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        content_frame.columnconfigure(1, weight=3)
        
        # Initialize animation variables
        self.anim = None
        self.canvas = None
        
        # Configure matplotlib style for dark mode
        plt.style.use('dark_background')
        
        # Start initial simulation
        self.start_simulation()
    
    def create_slider(self, parent, label, variable, min_val, max_val, row):
        # Create frame for this row
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=2)
        
        # Add label
        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w")
        
        # Add slider
        slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, variable=variable,
                            width=200, height=16)
        slider.grid(row=0, column=1, sticky="ew", padx=5)
        
        # Add value label
        value_label = ctk.CTkLabel(frame, text=f"{variable.get():.1f}",
                                font=ctk.CTkFont(size=12))
        value_label.grid(row=0, column=2, sticky="e", padx=(0, 5))
        
        # Configure grid
        frame.columnconfigure(1, weight=1)
        
        # Create update function for this specific slider
        def update_label(*args):
            value_label.configure(text=f"{variable.get():.1f}")
        
        # Bind the update function to the variable
        variable.trace_add("write", update_label)
        
        return slider
    
    def double_pendulum(self, t, y, L1, L2, m1, m2, g):
        """Compute derivatives for the double pendulum system using standard equations."""
        theta1, z1, theta2, z2 = y
        delta = theta1 - theta2
        dtheta1_dt = z1
        dtheta2_dt = z2
        dz1_dt = (-g*(2*m1 + m2)*np.sin(theta1) - m2*g*np.sin(theta1 - 2*theta2) - \
                  2*np.sin(delta)*m2*(z2**2 * L2 + z1**2 * L1 * np.cos(delta))) / (L1*(2*m1 + m2 - m2*np.cos(2*delta)))
        dz2_dt = (2*np.sin(delta)*(z1**2 * L1 * (m1 + m2) + g*(m1 + m2)*np.cos(theta1) + \
                  z2**2 * L2 * m2 * np.cos(delta))) / (L2*(2*m1 + m2 - m2*np.cos(2*delta)))
        return [dtheta1_dt, dz1_dt, dtheta2_dt, dz2_dt]
    
    def start_simulation(self):
        # Clear previous plot if it exists
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        
        # Get parameters from sliders
        L1 = self.L1_var.get()
        L2 = self.L2_var.get()
        m1 = self.m1_var.get()
        m2 = self.m2_var.get()
        theta1 = np.radians(self.theta1_var.get())
        theta2 = np.radians(self.theta2_var.get())
        g = self.g_var.get()
        
        # Set up simulation parameters
        dt = 0.05
        t_max = 30.0
        t = np.arange(0, t_max, dt)
        
        # Initial conditions
        y0 = [theta1, 0, theta2, 0]
        
        # Solve the differential equations
        sol = solve_ivp(self.double_pendulum, [0, t_max], y0, 
                       args=(L1, L2, m1, m2, g), method='RK45', t_eval=t)
        
        theta1_vals = sol.y[0]
        theta2_vals = sol.y[2]
        
        # Calculate positions
        x1 = L1 * np.sin(theta1_vals)
        y1 = -L1 * np.cos(theta1_vals)
        x2 = x1 + L2 * np.sin(theta2_vals)
        y2 = y1 - L2 * np.cos(theta2_vals)
        
        # Create figure and animation
        fig = plt.Figure(figsize=(12, 12))
        gs = fig.add_gridspec(2, 2)
        
        # Set figure background to match dark theme
        fig.patch.set_facecolor('#242424')
        
        # Main animation plot
        ax_main = fig.add_subplot(gs[:, 0])
        ax_main.set_facecolor('#E5E5E5')  # Light grey background
        ax_main.set_xlim(-2.5, 2.5)
        ax_main.set_ylim(-2.5, 2.5)
        ax_main.set_aspect('equal')
        ax_main.set_title('Double Pendulum Motion', color='white')
        ax_main.grid(True, color='#CCCCCC')
        ax_main.set_xlabel('X Position (m)', color='white')
        ax_main.set_ylabel('Y Position (m)', color='white')
        ax_main.tick_params(colors='white')
        for spine in ax_main.spines.values():
            spine.set_color('white')
        
        line, = ax_main.plot([], [], 'o-', lw=2, color='#1f77b4', label='Pendulum')
        trace, = ax_main.plot([], [], '-', lw=1, alpha=0.5, color='#ff7f0e', label='Path')
        ax_main.legend(facecolor='#242424', labelcolor='white')
        
        # Phase space plot for first pendulum
        ax_phase1 = fig.add_subplot(gs[0, 1])
        ax_phase1.set_facecolor('#E5E5E5')  # Light grey background
        ax_phase1.plot(theta1_vals, sol.y[1], color='#1f77b4', lw=1)
        ax_phase1.set_title('Phase Space: θ₁ vs dθ₁/dt', color='white')
        ax_phase1.set_xlabel('θ₁ (rad)', color='white')
        ax_phase1.set_ylabel('dθ₁/dt (rad/s)', color='white')
        ax_phase1.grid(True, color='#CCCCCC')
        ax_phase1.tick_params(colors='white')
        for spine in ax_phase1.spines.values():
            spine.set_color('white')
        
        # Phase space plot for second pendulum
        ax_phase2 = fig.add_subplot(gs[1, 1])
        ax_phase2.set_facecolor('#E5E5E5')  # Light grey background
        ax_phase2.plot(theta2_vals, sol.y[3], color='#2ca02c', lw=1)
        ax_phase2.set_title('Phase Space: θ₂ vs dθ₂/dt', color='white')
        ax_phase2.set_xlabel('θ₂ (rad)', color='white')
        ax_phase2.set_ylabel('dθ₂/dt (rad/s)', color='white')
        ax_phase2.grid(True, color='#CCCCCC')
        ax_phase2.tick_params(colors='white')
        for spine in ax_phase2.spines.values():
            spine.set_color('white')
        
        # Adjust layout
        fig.tight_layout()
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        # Animation update function
        def animate(frame):
            line.set_data([0, x1[frame], x2[frame]], [0, y1[frame], y2[frame]])
            trace.set_data(x2[:frame], y2[:frame])
            return line, trace
        
        # Create animation
        self.anim = FuncAnimation(fig, animate, frames=len(t), 
                                interval=dt*1000, blit=True)
        
        # Update canvas
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = DoublePendulumGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:




