#!/usr/bin/env python
# coding: utf-8

# Boids Flocking Simulation
# Based on Craig Reynolds' Boids algorithm (1986)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.spatial.distance import cdist

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class Boid:
    """Represents a single Boid agent."""
    def __init__(self, x, y, width, height, max_speed):
        self.position = np.array([float(x), float(y)])
        angle = np.random.uniform(0, 2 * np.pi)
        self.velocity = np.array([np.cos(angle), np.sin(angle)]) * np.random.uniform(1, max_speed)
        self.width = width
        self.height = height
        self.max_speed = max_speed
        self.max_force = 0.1 # Max steering force

    def update(self, flock_velocity):
        """Update the boid's velocity and position."""
        self.velocity += flock_velocity
        # Limit speed
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed

        self.position += self.velocity
        self.wrap_edges()

    def wrap_edges(self):
        """Wrap boid position around screen edges."""
        if self.position[0] > self.width: self.position[0] = 0
        elif self.position[0] < 0: self.position[0] = self.width
        if self.position[1] > self.height: self.position[1] = 0
        elif self.position[1] < 0: self.position[1] = self.height

    def apply_rules(self, boids, visual_range, separation_dist, factors):
        """Calculate steering forces based on flocking rules."""
        separation_force = np.zeros(2)
        alignment_force = np.zeros(2)
        cohesion_force = np.zeros(2)
        separation_count = 0
        alignment_count = 0
        cohesion_count = 0

        positions = np.array([b.position for b in boids])
        distances = cdist([self.position], positions)[0]

        for i, other in enumerate(boids):
            if other is self:
                continue # Don't compare with self

            d = distances[i]

            # Separation Rule
            if d > 0 and d < separation_dist:
                diff = self.position - other.position
                separation_force += diff / d # Force inversely proportional to distance
                separation_count += 1

            # Alignment and Cohesion Rules (within visual range)
            if d > 0 and d < visual_range:
                alignment_force += other.velocity
                cohesion_force += other.position
                alignment_count += 1
                cohesion_count += 1

        # Calculate average separation force
        if separation_count > 0:
            separation_force /= separation_count
            separation_steer = self._steer(separation_force)
        else:
            separation_steer = np.zeros(2)

        # Calculate average alignment force
        if alignment_count > 0:
            alignment_force /= alignment_count
            alignment_steer = self._steer(alignment_force - self.velocity) # Steer towards average velocity
        else:
            alignment_steer = np.zeros(2)

        # Calculate average cohesion force
        if cohesion_count > 0:
            cohesion_force /= cohesion_count
            cohesion_steer = self._steer(cohesion_force - self.position) # Steer towards center of mass
        else:
            cohesion_steer = np.zeros(2)

        # Apply factors and sum forces
        total_force = (separation_steer * factors['separation'] +
                       alignment_steer * factors['alignment'] +
                       cohesion_steer * factors['cohesion'])

        # Limit total force
        force_mag = np.linalg.norm(total_force)
        if force_mag > self.max_force:
             total_force = (total_force / force_mag) * self.max_force

        return total_force

    def _steer(self, desired):
        """Calculate steering force towards a desired vector."""
        desired_mag = np.linalg.norm(desired)
        if desired_mag > 0:
            desired = (desired / desired_mag) * self.max_speed
            steer = desired - self.velocity
            steer_mag = np.linalg.norm(steer)
            if steer_mag > self.max_force:
                steer = (steer / steer_mag) * self.max_force
            return steer
        else:
            return np.zeros(2)


class BoidsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Boids Flocking Simulation")
        self.root.geometry("1200x800")

        # --- Main Frame ---
        main_frame = ctk.CTkFrame(root)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # --- Title Frame ---
        title_frame = ctk.CTkFrame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        title_label = ctk.CTkLabel(title_frame, text="Boids Flocking Simulation",
                                 font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(padx=5, pady=5)

        # --- Content Frame ---
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        main_frame.columnconfigure(0, weight=1) # Make content frame expand width
        main_frame.rowconfigure(1, weight=1) # Make content frame expand height

        # --- Controls Frame ---
        controls_frame = ctk.CTkFrame(content_frame)
        controls_frame.grid(row=0, column=0, sticky="ns", padx=5, pady=5) # Stick to top-bottom
        content_frame.rowconfigure(0, weight=1) # Make controls frame expand height if needed

        # --- Parameter Sliders ---
        self.num_boids_var = tk.IntVar(value=50)
        self.visual_range_var = tk.DoubleVar(value=50.0)
        self.separation_dist_var = tk.DoubleVar(value=25.0)
        self.separation_factor_var = tk.DoubleVar(value=1.5)
        self.alignment_factor_var = tk.DoubleVar(value=1.0)
        self.cohesion_factor_var = tk.DoubleVar(value=1.0)
        self.max_speed_var = tk.DoubleVar(value=4.0)

        self.create_slider(controls_frame, "Num Boids:", self.num_boids_var, 10, 200, 0, integer=True)
        self.create_slider(controls_frame, "Visual Range:", self.visual_range_var, 10.0, 150.0, 1)
        self.create_slider(controls_frame, "Separation Dist:", self.separation_dist_var, 5.0, 50.0, 2)
        self.create_slider(controls_frame, "Separation Fac:", self.separation_factor_var, 0.1, 3.0, 3)
        self.create_slider(controls_frame, "Alignment Fac:", self.alignment_factor_var, 0.1, 3.0, 4)
        self.create_slider(controls_frame, "Cohesion Fac:", self.cohesion_factor_var, 0.1, 3.0, 5)
        self.create_slider(controls_frame, "Max Speed:", self.max_speed_var, 1.0, 10.0, 6)

        # Add Start/Restart button
        self.start_button = ctk.CTkButton(controls_frame, text="Start / Restart",
                                       command=self.start_simulation,
                                       font=ctk.CTkFont(size=14, weight="bold"))
        self.start_button.grid(row=7, column=0, columnspan=2, pady=20)

        # --- Add Explanatory Text ---
        explanation_text = ctk.CTkTextbox(controls_frame, height=200, wrap="word", font=ctk.CTkFont(size=12))
        explanation_text.grid(row=8, column=0, columnspan=2, sticky="ew", padx=5, pady=(10, 5))
        explanation_text.insert("1.0", """Boids Simulation:
Models flocking behavior using simple rules applied to individual agents ('boids').

Parameter Explanations:

- Num Boids: Total agents in the simulation.
- Visual Range: How far a boid looks for neighbors to align with and cohere towards.
- Separation Dist: The minimum distance boids try to keep from each other.
- Separation Fac: Strength of the urge to steer away from close neighbors.
- Alignment Fac: Strength of the urge to match the average heading of neighbors.
- Cohesion Fac: Strength of the urge to steer towards the average position of neighbors.
- Max Speed: The top speed any boid can reach.""")
        explanation_text.configure(state="disabled")

        # --- Plot Frame ---
        self.plot_frame = ctk.CTkFrame(content_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        content_frame.columnconfigure(1, weight=3) # Give plot frame more horizontal space

        # --- Animation Variables ---
        self.anim = None
        self.canvas = None
        self.fig = None
        self.ax = None
        self.scatter = None
        self.boids = []
        self.plot_width = 800 # Approximate plot dimensions
        self.plot_height = 700

        plt.style.use('dark_background') # Use dark theme for matplotlib

        self.start_simulation() # Initial simulation start

    def create_slider(self, parent, label, variable, min_val, max_val, row, integer=False):
        """Helper to create a CTkSlider with labels."""
        frame = ctk.CTkFrame(parent)
        frame.grid(row=row, column=0, columnspan=2, sticky="ew", padx=5, pady=3)

        ctk.CTkLabel(frame, text=label, font=ctk.CTkFont(size=12), width=100, anchor="w").grid(row=0, column=0, padx=(5,0))

        slider = ctk.CTkSlider(frame, from_=min_val, to=max_val, variable=variable,
                            number_of_steps= (max_val - min_val) if integer else None,
                            width=150, height=16)
        slider.grid(row=0, column=1, sticky="ew", padx=5)

        value_label = ctk.CTkLabel(frame, text=f"{variable.get():.1f}" if not integer else f"{variable.get()}",
                                font=ctk.CTkFont(size=12), width=30)
        value_label.grid(row=0, column=2, sticky="e", padx=(0, 5))

        frame.columnconfigure(1, weight=1) # Allow slider to expand

        def update_label(*args):
            val = variable.get()
            value_label.configure(text=f"{val:.1f}" if not integer else f"{val}")

        variable.trace_add("write", update_label)
        return slider

    def start_simulation(self):
        """Initialize or reset the Boids simulation."""
        # Stop existing animation if running
        if self.anim:
            self.anim.event_source.stop()
            self.anim = None

        # Clear previous plot widgets
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        plt.close(self.fig) # Close the previous figure explicitly

        # Get parameters
        num_boids = self.num_boids_var.get()
        max_speed = self.max_speed_var.get()

        # Create Boids
        self.boids = [Boid(np.random.uniform(0, self.plot_width),
                           np.random.uniform(0, self.plot_height),
                           self.plot_width, self.plot_height, max_speed)
                      for _ in range(num_boids)]

        # --- Setup Matplotlib Figure and Axes ---
        self.fig = plt.Figure(figsize=(8, 7)) # Adjusted size
        self.fig.patch.set_facecolor('#242424') # Match dark theme background
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#1c1c1c') # Slightly different background for plot area
        self.ax.set_xlim(0, self.plot_width)
        self.ax.set_ylim(0, self.plot_height)
        self.ax.set_xticks([]) # Hide axes ticks
        self.ax.set_yticks([])
        self.ax.set_title('Boids Flocking', color='white')
        for spine in self.ax.spines.values():
             spine.set_color('white') # Keep border white

        # Initialize scatter plot (empty for now)
        # Using simple markers for now, quiver (arrows) can be more complex to update
        self.scatter = self.ax.scatter([], [], s=10, c='cyan')

        # --- Embed Matplotlib in Tkinter ---
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # --- Start Animation ---
        self.anim = FuncAnimation(self.fig, self.animate, interval=30, blit=True) # ~33 FPS
        self.canvas.draw()


    def animate(self, frame):
        """Animation update function."""
        if not self.boids: # Check if boids list is empty
            return self.scatter,

        # Get current parameters for rules
        visual_range = self.visual_range_var.get()
        separation_dist = self.separation_dist_var.get()
        factors = {
            'separation': self.separation_factor_var.get(),
            'alignment': self.alignment_factor_var.get(),
            'cohesion': self.cohesion_factor_var.get()
        }

        # Update each boid
        flock_velocities = [b.apply_rules(self.boids, visual_range, separation_dist, factors) for b in self.boids]
        for i, boid in enumerate(self.boids):
            boid.update(flock_velocities[i])

        # Update scatter plot data
        positions = np.array([b.position for b in self.boids])
        self.scatter.set_offsets(positions)

        return self.scatter, # Return tuple of updated artists for blitting


def main():
    root = ctk.CTk() # Use CTk for the main window
    app = BoidsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 