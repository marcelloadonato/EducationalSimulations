"""
Planetary Motion & N-Body Simulator
Simulates gravitational interactions between celestial bodies
"""

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle
import numpy as np
from matplotlib.animation import FuncAnimation
import sys

# Configure matplotlib for dark theme
plt.style.use('dark_background')

class CelestialBody:
    """Represents a celestial body with mass, position, velocity"""

    def __init__(self, mass, position, velocity, color, name, radius=5):
        self.mass = mass
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.color = color
        self.name = name
        self.radius = radius
        self.trail = []
        self.max_trail_length = 500

    def add_to_trail(self):
        """Add current position to trail"""
        self.trail.append(self.position.copy())
        if len(self.trail) > self.max_trail_length:
            self.trail.pop(0)

    def clear_trail(self):
        """Clear the trail"""
        self.trail = []


class PlanetaryMotionSimulator(ctk.CTk):
    """Main application window for planetary motion simulation"""

    def __init__(self):
        super().__init__()

        self.title("Planetary Motion & N-Body Simulator")
        self.geometry("1400x900")

        # Physics constants
        self.G = 6.67430e-11  # Gravitational constant (can be scaled for visualization)
        self.dt = 3600 * 24  # Time step (1 day in seconds)
        self.time_scale = 1.0  # Speed multiplier
        self.simulation_time = 0

        # Simulation state
        self.bodies = []
        self.running = False
        self.show_trails = True
        self.show_vectors = False
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0

        # Color scheme
        self.bg_color = "#1a1a2e"
        self.panel_color = "#16213e"
        self.accent_color = "#0f3460"

        # Create UI
        self.create_widgets()

        # Load default preset
        self.load_preset("inner_solar_system")

        # Animation
        self.animation = None
        self.start_animation()

    def create_widgets(self):
        """Create all UI widgets"""

        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Left control panel
        self.control_panel = ctk.CTkFrame(self, width=320, corner_radius=0)
        self.control_panel.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        self.control_panel.grid_propagate(False)

        # Title
        title = ctk.CTkLabel(
            self.control_panel,
            text="🌍 Planetary Motion",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=20, padx=20)

        # Simulation Controls
        controls_frame = ctk.CTkFrame(self.control_panel)
        controls_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(controls_frame, text="Simulation Controls",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        # Play/Pause button
        self.play_button = ctk.CTkButton(
            controls_frame,
            text="⏸ Pause",
            command=self.toggle_simulation,
            width=260
        )
        self.play_button.pack(pady=5)

        # Reset button
        ctk.CTkButton(
            controls_frame,
            text="🔄 Reset",
            command=self.reset_simulation,
            width=260
        ).pack(pady=5)

        # Time scale
        ctk.CTkLabel(controls_frame, text="Time Speed").pack(pady=(10, 0))
        self.time_scale_slider = ctk.CTkSlider(
            controls_frame,
            from_=0.1,
            to=5.0,
            number_of_steps=49,
            command=self.update_time_scale,
            width=260
        )
        self.time_scale_slider.set(1.0)
        self.time_scale_slider.pack(pady=5)

        self.time_scale_label = ctk.CTkLabel(controls_frame, text="1.0x")
        self.time_scale_label.pack()

        # Zoom control
        ctk.CTkLabel(controls_frame, text="Zoom").pack(pady=(10, 0))
        self.zoom_slider = ctk.CTkSlider(
            controls_frame,
            from_=0.1,
            to=3.0,
            number_of_steps=29,
            command=self.update_zoom,
            width=260
        )
        self.zoom_slider.set(1.0)
        self.zoom_slider.pack(pady=5)

        # Display options
        display_frame = ctk.CTkFrame(self.control_panel)
        display_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(display_frame, text="Display Options",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        self.trails_toggle = ctk.CTkSwitch(
            display_frame,
            text="Show Trails",
            command=self.toggle_trails,
            width=260
        )
        self.trails_toggle.select()
        self.trails_toggle.pack(pady=5)

        self.vectors_toggle = ctk.CTkSwitch(
            display_frame,
            text="Show Velocity Vectors",
            command=self.toggle_vectors,
            width=260
        )
        self.vectors_toggle.pack(pady=5)

        # Preset scenarios
        preset_frame = ctk.CTkFrame(self.control_panel)
        preset_frame.pack(pady=10, padx=20, fill="x")

        ctk.CTkLabel(preset_frame, text="Preset Scenarios",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        presets = [
            ("Inner Solar System", "inner_solar_system"),
            ("Earth-Moon System", "earth_moon"),
            ("Binary Star System", "binary_stars"),
            ("Triple Star System", "triple_stars"),
            ("Figure-8 Orbit", "figure_eight"),
            ("Chaotic 4-Body", "chaotic_four"),
            ("Solar System Scale", "solar_system")
        ]

        for name, key in presets:
            ctk.CTkButton(
                preset_frame,
                text=name,
                command=lambda k=key: self.load_preset(k),
                width=260
            ).pack(pady=2)

        # Info panel
        info_frame = ctk.CTkFrame(self.control_panel)
        info_frame.pack(pady=10, padx=20, fill="both", expand=True)

        ctk.CTkLabel(info_frame, text="System Information",
                    font=ctk.CTkFont(size=16, weight="bold")).pack(pady=5)

        self.info_text = ctk.CTkTextbox(info_frame, height=150, width=260)
        self.info_text.pack(pady=5, padx=5)

        # Right visualization panel
        self.viz_panel = ctk.CTkFrame(self, corner_radius=0)
        self.viz_panel.grid(row=0, column=1, sticky="nsew")

        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 8), facecolor='#0a0a0f')
        self.ax.set_facecolor('#0a0a0f')
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.2, linestyle='--')

        # Embed matplotlib in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_panel)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)

    def update_time_scale(self, value):
        """Update time scale"""
        self.time_scale = float(value)
        self.time_scale_label.configure(text=f"{self.time_scale:.1f}x")

    def update_zoom(self, value):
        """Update zoom level"""
        self.zoom_level = float(value)

    def toggle_simulation(self):
        """Toggle simulation running state"""
        self.running = not self.running
        if self.running:
            self.play_button.configure(text="⏸ Pause")
        else:
            self.play_button.configure(text="▶ Play")

    def toggle_trails(self):
        """Toggle trail display"""
        self.show_trails = self.trails_toggle.get()

    def toggle_vectors(self):
        """Toggle velocity vector display"""
        self.show_vectors = self.vectors_toggle.get()

    def reset_simulation(self):
        """Reset simulation to initial state"""
        self.simulation_time = 0
        for body in self.bodies:
            body.clear_trail()

    def load_preset(self, preset_key):
        """Load a preset scenario"""
        self.bodies = []
        self.simulation_time = 0

        # Scaling factors for visualization
        AU = 1.496e11  # Astronomical Unit in meters
        day = 86400    # Seconds in a day

        if preset_key == "inner_solar_system":
            # Sun, Mercury, Venus, Earth, Mars (scaled for visualization)
            self.G = 6.67430e-11 * 1e10  # Scaled G for better visualization
            self.dt = 3600 * 24  # 1 day

            # Sun (at origin)
            self.bodies.append(CelestialBody(
                mass=1.989e30,
                position=[0, 0],
                velocity=[0, 0],
                color='#FDB813',
                name='Sun',
                radius=15
            ))

            # Mercury
            self.bodies.append(CelestialBody(
                mass=3.285e23,
                position=[0.39 * AU, 0],
                velocity=[0, 47870],
                color='#8C7853',
                name='Mercury',
                radius=4
            ))

            # Venus
            self.bodies.append(CelestialBody(
                mass=4.867e24,
                position=[0.72 * AU, 0],
                velocity=[0, 35020],
                color='#FFC649',
                name='Venus',
                radius=6
            ))

            # Earth
            self.bodies.append(CelestialBody(
                mass=5.972e24,
                position=[1.0 * AU, 0],
                velocity=[0, 29780],
                color='#4A90E2',
                name='Earth',
                radius=6
            ))

            # Mars
            self.bodies.append(CelestialBody(
                mass=6.39e23,
                position=[1.52 * AU, 0],
                velocity=[0, 24070],
                color='#E27B58',
                name='Mars',
                radius=5
            ))

        elif preset_key == "earth_moon":
            self.G = 6.67430e-11 * 1e15
            self.dt = 3600  # 1 hour

            # Earth
            self.bodies.append(CelestialBody(
                mass=5.972e24,
                position=[0, 0],
                velocity=[0, 12.3],
                color='#4A90E2',
                name='Earth',
                radius=12
            ))

            # Moon
            self.bodies.append(CelestialBody(
                mass=7.342e22,
                position=[384400e3, 0],
                velocity=[0, 1022 + 12.3],
                color='#CCCCCC',
                name='Moon',
                radius=6
            ))

        elif preset_key == "binary_stars":
            self.G = 6.67430e-11 * 1e15
            self.dt = 3600 * 6

            # Star 1
            self.bodies.append(CelestialBody(
                mass=1.989e30,
                position=[-1e11, 0],
                velocity=[0, 15000],
                color='#FDB813',
                name='Star A',
                radius=14
            ))

            # Star 2
            self.bodies.append(CelestialBody(
                mass=1.989e30,
                position=[1e11, 0],
                velocity=[0, -15000],
                color='#E85D75',
                name='Star B',
                radius=14
            ))

            # Planet orbiting the binary
            self.bodies.append(CelestialBody(
                mass=5.972e24,
                position=[0, 3e11],
                velocity=[20000, 0],
                color='#4A90E2',
                name='Planet',
                radius=6
            ))

        elif preset_key == "triple_stars":
            self.G = 6.67430e-11 * 1e15
            self.dt = 3600 * 6

            # Create three stars in triangular formation
            angle_offset = 2 * np.pi / 3
            distance = 1.5e11
            velocity = 12000

            for i in range(3):
                angle = i * angle_offset
                colors = ['#FDB813', '#E85D75', '#50C878']
                self.bodies.append(CelestialBody(
                    mass=1.5e30,
                    position=[distance * np.cos(angle), distance * np.sin(angle)],
                    velocity=[-velocity * np.sin(angle), velocity * np.cos(angle)],
                    color=colors[i],
                    name=f'Star {i+1}',
                    radius=12
                ))

        elif preset_key == "figure_eight":
            # Famous figure-8 choreography
            self.G = 1.0
            self.dt = 0.01

            # Three equal masses in figure-8 pattern
            self.bodies.append(CelestialBody(
                mass=1.0,
                position=[-0.97000436, 0.24308753],
                velocity=[0.4662036850, 0.4323657300],
                color='#FF6B6B',
                name='Body 1',
                radius=8
            ))

            self.bodies.append(CelestialBody(
                mass=1.0,
                position=[0.97000436, -0.24308753],
                velocity=[0.4662036850, 0.4323657300],
                color='#4ECDC4',
                name='Body 2',
                radius=8
            ))

            self.bodies.append(CelestialBody(
                mass=1.0,
                position=[0, 0],
                velocity=[-2 * 0.4662036850, -2 * 0.4323657300],
                color='#FFE66D',
                name='Body 3',
                radius=8
            ))

        elif preset_key == "chaotic_four":
            self.G = 6.67430e-11 * 1e15
            self.dt = 3600 * 4

            # Four bodies in potentially chaotic configuration
            configs = [
                (1e30, [0, 0], [0, 0], '#FDB813', 'Central', 15),
                (5e29, [2e11, 0], [0, 18000], '#E85D75', 'Body 1', 10),
                (5e29, [0, 2e11], [-18000, 0], '#4ECDC4', 'Body 2', 10),
                (5e29, [-1.5e11, 1.5e11], [12000, 12000], '#FFE66D', 'Body 3', 10),
            ]

            for mass, pos, vel, color, name, radius in configs:
                self.bodies.append(CelestialBody(
                    mass=mass,
                    position=pos,
                    velocity=vel,
                    color=color,
                    name=name,
                    radius=radius
                ))

        elif preset_key == "solar_system":
            # Full solar system (simplified)
            self.G = 6.67430e-11 * 1e10
            self.dt = 3600 * 24

            # Sun
            self.bodies.append(CelestialBody(
                mass=1.989e30,
                position=[0, 0],
                velocity=[0, 0],
                color='#FDB813',
                name='Sun',
                radius=15
            ))

            # Planets with approximate orbital data
            planets = [
                (3.285e23, 0.39 * AU, 47870, '#8C7853', 'Mercury', 3),
                (4.867e24, 0.72 * AU, 35020, '#FFC649', 'Venus', 5),
                (5.972e24, 1.00 * AU, 29780, '#4A90E2', 'Earth', 6),
                (6.39e23, 1.52 * AU, 24070, '#E27B58', 'Mars', 4),
                (1.898e27, 5.20 * AU, 13070, '#D4A574', 'Jupiter', 11),
                (5.683e26, 9.54 * AU, 9690, '#F4D47C', 'Saturn', 10),
                (8.681e25, 19.19 * AU, 6800, '#5DADE2', 'Uranus', 8),
                (1.024e26, 30.07 * AU, 5430, '#5499C7', 'Neptune', 8),
            ]

            for mass, dist, vel, color, name, radius in planets:
                self.bodies.append(CelestialBody(
                    mass=mass,
                    position=[dist, 0],
                    velocity=[0, vel],
                    color=color,
                    name=name,
                    radius=radius
                ))

        # Reset trails
        for body in self.bodies:
            body.clear_trail()

    def compute_forces(self):
        """Compute gravitational forces on all bodies"""
        forces = [np.array([0.0, 0.0]) for _ in self.bodies]

        for i, body1 in enumerate(self.bodies):
            for j, body2 in enumerate(self.bodies):
                if i != j:
                    # Vector from body1 to body2
                    r_vec = body2.position - body1.position
                    r_mag = np.linalg.norm(r_vec)

                    # Avoid division by zero and extremely close encounters
                    if r_mag < 1e6:
                        r_mag = 1e6

                    # Gravitational force magnitude
                    f_mag = self.G * body1.mass * body2.mass / (r_mag ** 2)

                    # Force vector
                    f_vec = f_mag * r_vec / r_mag

                    forces[i] += f_vec

        return forces

    def update_physics(self):
        """Update physics simulation using velocity Verlet integration"""
        if not self.running or len(self.bodies) == 0:
            return

        # Compute forces
        forces = self.compute_forces()

        # Update positions and velocities
        for body, force in zip(self.bodies, forces):
            # Acceleration
            acceleration = force / body.mass

            # Velocity Verlet integration
            body.position += body.velocity * self.dt * self.time_scale + 0.5 * acceleration * (self.dt * self.time_scale) ** 2

            # Compute new forces for velocity update
            new_forces = self.compute_forces()
            new_acceleration = new_forces[self.bodies.index(body)] / body.mass

            # Update velocity
            body.velocity += 0.5 * (acceleration + new_acceleration) * self.dt * self.time_scale

            # Add to trail
            if self.simulation_time % 5 == 0:  # Add trail point every 5 steps
                body.add_to_trail()

        self.simulation_time += 1

    def calculate_system_energy(self):
        """Calculate total kinetic and potential energy"""
        kinetic = 0
        potential = 0

        for body in self.bodies:
            # Kinetic energy
            v_mag = np.linalg.norm(body.velocity)
            kinetic += 0.5 * body.mass * v_mag ** 2

        # Potential energy
        for i, body1 in enumerate(self.bodies):
            for j, body2 in enumerate(self.bodies):
                if i < j:
                    r = np.linalg.norm(body2.position - body1.position)
                    if r > 0:
                        potential -= self.G * body1.mass * body2.mass / r

        return kinetic, potential

    def update_info_panel(self):
        """Update information panel"""
        try:
            kinetic, potential = self.calculate_system_energy()
            total = kinetic + potential

            info = f"Bodies: {len(self.bodies)}\n"
            info += f"Time Steps: {self.simulation_time}\n"
            info += f"Time Scale: {self.time_scale:.1f}x\n\n"
            info += f"System Energy:\n"
            info += f"Kinetic: {kinetic:.2e} J\n"
            info += f"Potential: {potential:.2e} J\n"
            info += f"Total: {total:.2e} J\n\n"
            info += "Bodies:\n"

            for body in self.bodies:
                v_mag = np.linalg.norm(body.velocity)
                info += f"• {body.name}: {v_mag/1000:.1f} km/s\n"

            self.info_text.delete("1.0", "end")
            self.info_text.insert("1.0", info)
        except:
            pass

    def update_plot(self, frame):
        """Update the plot for animation"""
        if self.running:
            self.update_physics()

        # Clear plot
        self.ax.clear()
        self.ax.set_facecolor('#0a0a0f')
        self.ax.grid(True, alpha=0.2, linestyle='--')

        if len(self.bodies) == 0:
            return

        # Calculate view bounds based on body positions
        all_positions = np.array([body.position for body in self.bodies])

        if len(all_positions) > 0:
            center = np.mean(all_positions, axis=0)
            max_dist = np.max([np.linalg.norm(pos - center) for pos in all_positions])

            if max_dist == 0:
                max_dist = 1e11

            # Set view limits with zoom
            view_range = max_dist * 1.5 / self.zoom_level
            self.ax.set_xlim(center[0] - view_range + self.pan_x, center[0] + view_range + self.pan_x)
            self.ax.set_ylim(center[1] - view_range + self.pan_y, center[1] + view_range + self.pan_y)

        # Draw trails
        if self.show_trails:
            for body in self.bodies:
                if len(body.trail) > 1:
                    trail_array = np.array(body.trail)
                    self.ax.plot(trail_array[:, 0], trail_array[:, 1],
                               color=body.color, alpha=0.3, linewidth=1)

        # Draw bodies
        for body in self.bodies:
            # Draw body as circle
            circle = Circle(body.position, body.radius * max_dist * 0.02,
                          color=body.color, zorder=10)
            self.ax.add_patch(circle)

            # Label
            self.ax.text(body.position[0], body.position[1] + body.radius * max_dist * 0.03,
                        body.name, color=body.color, fontsize=8, ha='center',
                        weight='bold')

            # Draw velocity vector
            if self.show_vectors and np.linalg.norm(body.velocity) > 0:
                vel_scale = max_dist * 0.0001
                self.ax.arrow(body.position[0], body.position[1],
                            body.velocity[0] * vel_scale, body.velocity[1] * vel_scale,
                            head_width=max_dist * 0.03, head_length=max_dist * 0.05,
                            fc=body.color, ec=body.color, alpha=0.6, linewidth=2)

        self.ax.set_xlabel('Distance (m)', color='white', fontsize=10)
        self.ax.set_ylabel('Distance (m)', color='white', fontsize=10)
        self.ax.tick_params(colors='white')

        # Update info panel every 10 frames
        if frame % 10 == 0:
            self.update_info_panel()

    def start_animation(self):
        """Start the matplotlib animation"""
        self.animation = FuncAnimation(
            self.fig,
            self.update_plot,
            interval=16,  # ~60 FPS
            blit=False,
            cache_frame_data=False
        )
        self.canvas.draw()


def main():
    """Main entry point"""
    app = PlanetaryMotionSimulator()
    app.mainloop()


if __name__ == "__main__":
    main()
