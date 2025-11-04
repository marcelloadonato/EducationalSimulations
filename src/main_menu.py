import customtkinter as ctk
import os
import sys
from PIL import Image
import math

class CarouselControl(ctk.CTkFrame):
    def __init__(self, master, total_cards, cards_per_page, on_page_change):
        super().__init__(master, fg_color="transparent")
        self.total_cards = total_cards
        self.cards_per_page = cards_per_page
        self.total_pages = math.ceil(total_cards / cards_per_page)
        self.current_page = 0
        self.on_page_change = on_page_change

        # Previous button
        self.prev_button = ctk.CTkButton(
            self, 
            text="←",
            width=40,
            height=40,
            command=self.prev_page,
            fg_color="#1e1e2e",
            text_color="#6c5ce7",
            hover_color="#2d2d3f",
            font=ctk.CTkFont(size=20),
            text_color_disabled="#2d2d3f",
            corner_radius=20
        )
        self.prev_button.grid(row=0, column=0, padx=10)

        # Dots for page indication
        self.dots_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.dots_frame.grid(row=0, column=1, padx=20)
        self.dots = []
        for i in range(self.total_pages):
            dot = ctk.CTkButton(
                self.dots_frame,
                text="",
                width=8,
                height=8,
                corner_radius=4,
                fg_color="#6c5ce7" if i == 0 else "#2d2d3f",
                hover_color="#845ef7",
                command=lambda page=i: self.go_to_page(page)
            )
            dot.grid(row=0, column=i, padx=4)
            self.dots.append(dot)

        # Next button
        self.next_button = ctk.CTkButton(
            self, 
            text="→",
            width=40,
            height=40,
            command=self.next_page,
            fg_color="#1e1e2e",
            text_color="#6c5ce7",
            hover_color="#2d2d3f",
            font=ctk.CTkFont(size=20),
            corner_radius=20
        )
        self.next_button.grid(row=0, column=2, padx=10)

        self.update_buttons()

    def update_buttons(self):
        self.prev_button.configure(
            state="normal" if self.current_page > 0 else "disabled",
            text_color="#6c5ce7" if self.current_page > 0 else "#2d2d3f"
        )
        self.next_button.configure(
            state="normal" if self.current_page < self.total_pages - 1 else "disabled",
            text_color="#6c5ce7" if self.current_page < self.total_pages - 1 else "#2d2d3f"
        )
        for i, dot in enumerate(self.dots):
            dot.configure(fg_color="#6c5ce7" if i == self.current_page else "#2d2d3f")

    def go_to_page(self, page):
        if 0 <= page < self.total_pages:
            self.current_page = page
            self.update_buttons()
            self.on_page_change(self.current_page)

    def next_page(self):
        self.go_to_page(self.current_page + 1)

    def prev_page(self):
        self.go_to_page(self.current_page - 1)

class SimulationCard(ctk.CTkFrame):
    def __init__(self, master, title, description, command, image_path=None):
        super().__init__(
            master, 
            corner_radius=15,
            fg_color="#1e1e2e",
            border_width=1,
            border_color="#2d2d3f"
        )
        
        self.grid_columnconfigure(0, weight=1)
        
        # Image
        if image_path:
            # Convert to absolute path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            abs_image_path = os.path.join(script_dir, image_path)
            
            if os.path.exists(abs_image_path):
                img = Image.open(abs_image_path)
                target_width = 320  # Fixed width for all cards
                target_height = 200  # Fixed height for all cards
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                self.image = ctk.CTkImage(light_image=img, dark_image=img, size=(target_width, target_height))
                self.image_label = ctk.CTkLabel(
                    self,
                    image=self.image,
                    text="",
                    fg_color="#13131f"
                )
                self.image_label.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
            else:
                print(f"Warning: Image not found at {abs_image_path}")
        
        # Title
        self.title_label = ctk.CTkLabel(
            self, 
            text=title,
            font=ctk.CTkFont(size=20, weight="bold"),
            anchor="w",
            text_color="#ffffff"
        )
        self.title_label.grid(row=1, column=0, padx=20, pady=(25, 10), sticky="w")
        
        # Description
        self.description_label = ctk.CTkLabel(
            self,
            text=description,
            wraplength=280,
            justify="left",
            anchor="w",
            text_color="#a0a0a0"
        )
        self.description_label.grid(row=2, column=0, padx=20, pady=(0, 25), sticky="w")
        
        # Launch button
        self.button = ctk.CTkButton(
            self,
            text="Launch →",
            command=command,
            width=120,
            height=32,
            corner_radius=16,
            font=ctk.CTkFont(size=14),
            fg_color="#4c3b99",  # Darker purple
            hover_color="#5c4aad",  # Slightly lighter when hovering
            text_color="#ffffff"
        )
        self.button.grid(row=3, column=0, padx=20, pady=(0, 25), sticky="w")

        # Bind hover events
        self.bind("<Enter>", self.on_hover_enter)
        self.bind("<Leave>", self.on_hover_leave)

    def on_hover_enter(self, event):
        self.configure(fg_color="#252538")

    def on_hover_leave(self, event):
        self.configure(fg_color="#1e1e2e")

class MainMenu(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Physics Simulations")
        self.geometry("1200x800")
        self.configure(fg_color="#171721")
        
        # Store initial position
        self.bind("<Map>", self.save_position)
        self.initial_position = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="Interactive Physics Simulations",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#ffffff"
        )
        self.title_label.grid(row=0, column=0, pady=(40, 30))
        
        # Cards container
        self.cards_container = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_container.grid(row=1, column=0, sticky="nsew", padx=40)
        self.cards_container.grid_columnconfigure((0, 1, 2), weight=1, uniform="column")
        self.cards_container.grid_rowconfigure(0, weight=1)
        
        # Create simulation cards
        self.cards = self.create_cards()
        
        # Create carousel control
        self.carousel = CarouselControl(
            self, 
            len(self.cards),  # Total number of cards
            3,  # Cards per page
            self.show_page
        )
        self.carousel.grid(row=2, column=0, pady=30)
        
        # Show initial page
        self.show_page(0)
        
    def create_cards(self):
        cards = []
        
        # Boids Simulation Card
        cards.append(SimulationCard(
            self.cards_container,
            "Boids Simulation",
            "Experience the fascinating world of emergent behavior through this interactive flocking simulation. "
            "Based on Craig Reynolds' classic model, each 'boid' follows three simple rules: separation, alignment, "
            "and cohesion. Watch as complex, lifelike flocking patterns emerge from these basic principles.",
            self.launch_boids,
            os.path.join("assets", "boids_icon.png")
        ))
        
        # Double-Slit Experiment Card
        cards.append(SimulationCard(
            self.cards_container,
            "Double-Slit Experiment",
            "Explore the fundamental principles of quantum mechanics with this interactive double-slit experiment simulation. "
            "Watch as individual particles build up an interference pattern over time, demonstrating the wave-particle "
            "duality of quantum mechanics. Adjust slit separation and wavelength to see how they affect the pattern.",
            self.launch_double_slit,
            os.path.join("assets", "double_slit_icon.png")
        ))
        
        # Double Pendulum Card
        cards.append(SimulationCard(
            self.cards_container,
            "Double Pendulum",
            "Explore the fascinating world of chaos theory with this classic physics demonstration. "
            "Watch how tiny changes in initial conditions lead to dramatically different outcomes, "
            "illustrating the famous 'butterfly effect'. Visualize the complex patterns traced by the pendulum's motion.",
            self.launch_pendulum,
            os.path.join("assets", "pendulum_icon.png")
        ))
        
        # Lorenz Attractor Card
        cards.append(SimulationCard(
            self.cards_container,
            "Lorenz Attractor",
            "Discover Edward Lorenz's groundbreaking chaos theory visualization. This simulation brings to life "
            "the famous 'butterfly effect' through a set of three coupled differential equations. Watch as the system "
            "traces out its distinctive butterfly-shaped strange attractor in three-dimensional space.",
            self.launch_lorenz,
            os.path.join("assets", "lorenz_icon.png")
        ))

        # Planetary Motion Card
        cards.append(SimulationCard(
            self.cards_container,
            "Planetary Motion",
            "Explore gravitational physics with this N-body simulator. Watch planets orbit stars, observe binary "
            "star systems, and witness the famous figure-8 choreography. Experiment with different celestial "
            "configurations and see how gravity shapes the cosmos. Features preset scenarios from our solar system to chaotic multi-body systems.",
            self.launch_planetary,
            os.path.join("assets", "planetary_icon.png")
        ))

        # Wave Form Simulator Card
        cards.append(SimulationCard(
            self.cards_container,
            "Wave Form Simulator",
            "Visualize the mesmerizing patterns of wave interference and propagation. Experiment with multiple wave "
            "sources, adjust frequencies and amplitudes in real-time, and observe phenomena like constructive and "
            "destructive interference, standing waves, and wave superposition.",
            self.launch_wave,
            os.path.join("assets", "wave_icon.png")
        ))
        
        # Calculus Explorer Card
        cards.append(SimulationCard(
            self.cards_container,
            "Calculus Explorer",
            "Interactively explore a quadratic function, its tangent line, and the definite integral. Adjust coefficients, "
            "the point of tangency, and integration bounds to visualize calculus concepts like derivatives and integrals.",
            self.launch_calculus,
            os.path.join("assets", "calculus_icon.png")
        ))
        
        # Fractal Generator Card
        cards.append(SimulationCard(
            self.cards_container,
            "Mandelbrot Explorer",
            "Dive into the mesmerizing world of fractals with this interactive Mandelbrot Set explorer. "
            "Zoom in to discover infinite complexity and self-similarity, adjust colors and iterations, "
            "and explore one of mathematics' most beautiful and mysterious objects.",
            self.launch_fractal,
            os.path.join("assets", "fractal_icon.png")
        ))
        
        return cards
    
    def show_page(self, page_number):
        # Hide all cards
        for card in self.cards:
            card.grid_forget()
        
        # Show cards for current page
        cards_per_page = 3
        start_idx = page_number * cards_per_page
        end_idx = min(start_idx + cards_per_page, len(self.cards))
        
        for i, card in enumerate(self.cards[start_idx:end_idx]):
            card.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
    
    def save_position(self, event=None):
        if self.initial_position is None:
            self.initial_position = (self.winfo_x(), self.winfo_y())
    
    def launch_simulation(self, command):
        # Save window position
        self.save_position()
        # Hide the main menu
        self.withdraw()
        
        # Get the correct path relative to the current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Run the simulation with the correct path
        command = command.replace('src/', '')  # Remove src/ prefix if present
        command = f"{sys.executable} {os.path.join(script_dir, command)}"
        os.system(command)
        
        # Show the main menu again
        self.deiconify()
        # Restore position
        if self.initial_position:
            self.geometry(f"+{self.initial_position[0]}+{self.initial_position[1]}")
        # Bring window to front
        self.lift()
        self.focus_force()
    
    def launch_boids(self):
        self.launch_simulation('boids-simulation.py')
        
    def launch_pendulum(self):
        self.launch_simulation('double-pendulum.py')
        
    def launch_lorenz(self):
        self.launch_simulation('lorenz-attractor.py')
        
    def launch_wave(self):
        self.launch_simulation('wave-form-simulator.py')

    def launch_calculus(self):
        self.launch_simulation('calculus.py')

    def launch_fractal(self):
        self.launch_simulation('fractal-generator.py')

    def launch_double_slit(self):
        self.launch_simulation('double-slit.py')

    def launch_planetary(self):
        self.launch_simulation('planetary-motion.py')

if __name__ == "__main__":
    # Set theme
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    app = MainMenu()
    app.mainloop() 