#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# Set appearance mode and default color theme for customtkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class WaveFormSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Wave Interference Simulator")
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
                                 text="Wave Interference Simulator",
                                 font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(padx=5, pady=(5,0))
        
        # Add subtitle
        subtitle_label = ctk.CTkLabel(title_frame, 
                                    text="Exploring Wave Physics and Interference Patterns",
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
        self.separation_var = tk.DoubleVar(value=2.0)
        self.wavelength_var = tk.DoubleVar(value=1.0)
        self.phase_diff_var = tk.DoubleVar(value=0.0)
        
        # Add sliders
        self.create_slider(controls_frame, "Separation (d):", self.separation_var, 0.5, 5.0, 0.1, 0)
        self.create_slider(controls_frame, "Wavelength (λ):", self.wavelength_var, 0.5, 3.0, 0.1, 1)
        self.create_slider(controls_frame, "Phase Diff (φ):", self.phase_diff_var, 0, 2*np.pi, 0.1, 2)
        
        # Add educational text
        edu_text = ctk.CTkTextbox(left_panel, height=200, wrap="word")
        edu_text.pack(fill="both", expand=True, padx=5, pady=5)
        edu_text.insert("1.0", """Wave Interference: A Fundamental Concept

Waves from two coherent sources overlap and combine:
• Constructive: Amplitudes add
• Destructive: Amplitudes cancel

Real-World Examples:
• Light: Soap bubbles, interferometers
• Sound: Noise-cancelling headphones
• Water, seismic, and quantum waves

Parameters:
• Separation (d): Distance between sources
• Wavelength (λ): Distance between wave peaks
• Phase Difference (φ): Time/position offset between waves

Try adjusting the sliders to see how these parameters affect the interference pattern!""")
        edu_text.configure(state="disabled")
        
        # Create plot frame
        self.plot_frame = ctk.CTkFrame(content_frame)
        self.plot_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        content_frame.columnconfigure(1, weight=3)
        content_frame.columnconfigure(0, weight=1)
        
        # Initialize matplotlib figure and canvas
        self.setup_matplotlib()
        
        # Initial plot update
        self.update_plot()
    
    def setup_matplotlib(self):
        """Initialize the matplotlib figure and canvas once."""
        self.fig = plt.Figure(figsize=(12, 10), constrained_layout=True)
        self.fig.patch.set_facecolor('#242424')
        
        # Create subplots
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(223)
        self.ax3 = self.fig.add_subplot(224)
        
        # Style the axes
        for ax in [self.ax1, self.ax2, self.ax3]:
            ax.set_facecolor('#E5E5E5')
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Initialize plot elements
        self.line_total, = self.ax1.plot([], [], label='Total Wave', color='#1f77b4', lw=2.5)
        self.line_wave1, = self.ax1.plot([], [], '--', label='Wave 1', color='#ff7f0e', lw=1.5, alpha=0.7)
        self.line_wave2, = self.ax1.plot([], [], '--', label='Wave 2', color='#2ca02c', lw=1.5, alpha=0.7)
        self.ax1.legend(loc='upper right')
        
        # Initialize 2D plots
        self.im2 = self.ax2.imshow(np.zeros((100, 100)), extent=(-10, 10, -10, 10),
                                 cmap='magma', origin='lower', interpolation='bilinear')
        self.im3 = self.ax3.imshow(np.zeros((100, 100)), extent=(-10, 10, -10, 10),
                                 cmap='magma', origin='lower', interpolation='bilinear')
        
        # Set titles and labels
        self.ax1.set_title('1D Wave Interference', color='white', pad=10)
        self.ax1.set_xlabel('Position', color='white')
        self.ax1.set_ylabel('Amplitude', color='white')
        
        self.ax2.set_title('Equal Amplitudes', color='white')
        self.ax2.set_xlabel('x', color='white')
        self.ax2.set_ylabel('y', color='white')
        
        self.ax3.set_title('Unequal Amplitudes', color='white')
        self.ax3.set_xlabel('x', color='white')
        self.ax3.set_ylabel('y', color='white')
        
        # Add colorbars
        self.fig.colorbar(self.im2, ax=self.ax2, label='Intensity')
        self.fig.colorbar(self.im3, ax=self.ax3, label='Intensity')
    
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
            if hasattr(self, '_update_job') and self._update_job is not None:
                self.root.after_cancel(self._update_job)
            self._update_job = self.root.after(100, self.update_plot)
        
        variable.trace_add("write", update_label_and_plot)
        return slider
    
    def update_plot(self):
        """Update the plot data without recreating the figure."""
        # Get current values
        separation = self.separation_var.get()
        wavelength = self.wavelength_var.get()
        phase_diff = self.phase_diff_var.get()
        
        # --- Data Calculations ---
        x_1d = np.linspace(0, 10, 1000)
        wave1_1d = np.sin(2 * np.pi * x_1d / wavelength)
        wave2_1d = np.sin(2 * np.pi * (x_1d + separation) / wavelength + phase_diff)
        total_wave_1d = wave1_1d + wave2_1d

        # Update 1D plot
        self.line_total.set_data(x_1d, total_wave_1d)
        self.line_wave1.set_data(x_1d, wave1_1d)
        self.line_wave2.set_data(x_1d, wave2_1d)
        self.ax1.relim()
        self.ax1.autoscale_view()

        # Calculate 2D data
        x_2d = np.linspace(-10, 10, 200)
        y_2d = np.linspace(-10, 10, 200)
        X, Y = np.meshgrid(x_2d, y_2d)
        source1 = (-separation / 2, 0)
        source2 = (separation / 2, 0)
        r1 = np.sqrt((X - source1[0])**2 + (Y - source1[1])**2)
        r2 = np.sqrt((X - source2[0])**2 + (Y - source2[1])**2)
        k = 2 * np.pi / wavelength

        # Equal amplitudes
        wave1_eq = np.sin(k * r1)
        wave2_eq = np.sin(k * r2 + phase_diff)
        intensity_eq = (wave1_eq + wave2_eq)**2

        # Unequal amplitudes
        wave1_uneq = np.sin(k * r1)
        wave2_uneq = 0.5 * np.sin(k * r2 + phase_diff)
        intensity_uneq = (wave1_uneq + wave2_uneq)**2

        # Update 2D plots
        self.im2.set_data(intensity_eq)
        self.im3.set_data(intensity_uneq)
        
        # Update source positions
        for ax in [self.ax2, self.ax3]:
            ax.clear()
            ax.imshow(intensity_eq if ax == self.ax2 else intensity_uneq,
                     extent=(-10, 10, -10, 10), cmap='magma',
                     origin='lower', interpolation='bilinear')
            ax.plot([source1[0], source2[0]], [source1[1], source2[1]], 'wo',
                    markersize=8, label='Sources')
            ax.set_title('Equal Amplitudes' if ax == self.ax2 else 'Unequal Amplitudes',
                        color='white')
            ax.set_xlabel('x', color='white')
            ax.set_ylabel('y', color='white')
            ax.tick_params(colors='white')
        
        # Redraw canvas
        self.canvas.draw_idle()

def main():
    root = ctk.CTk()
    app = WaveFormSimulatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()


# In[ ]:




