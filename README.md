# Educational Simulations

A comprehensive collection of interactive physics and mathematics simulations implemented in Python, featuring a modern, user-friendly interface built with CustomTkinter. This project brings complex scientific concepts to life through visual, interactive demonstrations that make learning engaging and intuitive.

![Physics Simulations Menu](docs/menu_screenshot.png)

## Overview

This educational platform provides seven distinct interactive simulations covering topics from classical physics to quantum mechanics, chaos theory, and mathematical visualization. Each simulation is designed to help students, educators, and enthusiasts explore fundamental scientific principles through hands-on experimentation.

## Simulations

### 1. Boids Simulation
**Experience emergent flocking behavior through nature-inspired algorithms**

Based on Craig Reynolds' seminal 1986 model, this simulation demonstrates how complex, lifelike group behavior emerges from simple individual rules. Each "boid" (bird-like object) follows three fundamental principles:

- **Separation**: Maintain personal space by avoiding crowding with nearby boids
- **Alignment**: Steer toward the average heading of neighboring boids
- **Cohesion**: Move toward the average position of nearby boids

**Key Features:**
- Real-time visualization of emergent flocking patterns
- Adjustable parameters to experiment with different behaviors
- Demonstrates self-organization in complex systems
- Applications in robotics, crowd simulation, and artificial life

**Educational Value:** Illustrates emergence, swarm intelligence, and how simple rules create complex behaviors found in nature (bird flocks, fish schools, insect swarms).

---

### 2. Double-Slit Experiment
**Explore the foundations of quantum mechanics**

This interactive simulation recreates one of the most famous experiments in physics, demonstrating wave-particle duality - a cornerstone of quantum mechanics. Watch as individual particles build up an interference pattern over time, revealing the wave nature of matter.

**Key Features:**
- Real-time particle detection visualization
- Adjustable slit separation (d) and wavelength (λ)
- Theoretical pattern overlay with experimental results
- Progressive pattern buildup showing quantum behavior

**Educational Value:** Demonstrates wave-particle duality, quantum superposition, and the measurement problem in quantum mechanics. Essential for understanding the fundamental nature of reality at the quantum scale.

---

### 3. Double Pendulum
**Witness chaos theory in action**

A classic demonstration of deterministic chaos, the double pendulum system shows how even simple mechanical systems can exhibit unpredictable behavior. This simulation illustrates the famous "butterfly effect" - where tiny changes in initial conditions lead to dramatically different outcomes.

**Key Features:**
- Real-time motion visualization
- Path tracing showing complex trajectories
- Sensitive dependence on initial conditions
- Energy conservation demonstration
- Beautiful, unpredictable motion patterns

**Educational Value:** Perfect introduction to chaos theory, nonlinear dynamics, and the limitations of predictability in deterministic systems. Shows how complex behavior arises from simple physical laws.

---

### 4. Lorenz Attractor
**Discover the butterfly effect through Edward Lorenz's groundbreaking visualization**

This simulation brings to life the famous strange attractor discovered by meteorologist Edward Lorenz in 1963 while studying atmospheric convection. The system traces its distinctive butterfly-shaped pattern in three-dimensional space, never repeating but always staying within bounds.

**Key Features:**
- 3D visualization of the attractor's trajectory
- Interactive rotation and viewing angles
- Parameter adjustment (σ, ρ, β)
- Multiple trajectory plotting
- Real-time system evolution

**Educational Value:** Demonstrates strange attractors, sensitivity to initial conditions, and the mathematical foundations of chaos theory. Essential for understanding weather prediction limitations and complex dynamical systems.

---

### 5. Wave Form Simulator
**Visualize wave physics and interference phenomena**

An interactive tool for studying wave propagation, superposition, and interference patterns. Create multiple wave sources and observe how waves interact, demonstrating fundamental principles of wave mechanics.

**Key Features:**
- Multiple wave source creation
- Real-time interference pattern visualization
- Adjustable frequency, amplitude, and wavelength
- Constructive and destructive interference demonstration
- Standing wave formation
- Wave superposition principle

**Educational Value:** Essential for understanding wave mechanics, applicable to sound waves, light, water waves, and quantum mechanics. Demonstrates interference, diffraction, and the superposition principle.

---

### 6. Calculus Explorer
**Interactive visualization of derivatives and integrals**

A hands-on tool for exploring fundamental calculus concepts through interactive visualization of quadratic functions, their derivatives (tangent lines), and definite integrals (area under curves).

**Key Features:**
- Real-time function plotting: f(x) = ax² + bx + c
- Tangent line visualization at any point
- Instantaneous rate of change (derivative) demonstration
- Definite integral visualization with adjustable bounds
- Side-by-side derivative and integral displays
- Interactive coefficient adjustment

**Educational Value:** Makes abstract calculus concepts concrete and visual. Perfect for students learning derivatives, integrals, rates of change, and the fundamental theorem of calculus.

**Key Concepts:**
- Derivative as slope of tangent line: f'(x) = 2ax + b
- Integral as area under curve
- Relationship between differentiation and integration
- Visual understanding of calculus notation

---

### 7. Mandelbrot Explorer (Fractal Generator)
**Dive into the infinite complexity of the Mandelbrot Set**

Explore one of mathematics' most beautiful and mysterious objects - the Mandelbrot Set. This interactive fractal explorer allows you to zoom into infinite self-similar patterns, revealing the stunning complexity that emerges from a simple mathematical formula: f(z) = z² + c.

**Key Features:**
- Infinite zoom capability revealing endless detail
- Multiple color schemes (viridis, plasma, inferno, magma, cividis)
- Pan and navigate through the fractal landscape
- Adjustable iteration depth for detail control
- Real-time rendering
- Self-similarity at all scales

**Educational Value:** Demonstrates fractals, complex numbers, iteration, infinity, and the beauty of mathematical structures. Shows how infinite complexity emerges from simple rules.

**Mathematical Foundation:** The Mandelbrot set consists of all complex numbers c for which the iterative function f(z) = z² + c (starting from z=0) remains bounded.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step-by-Step Installation

1. **Clone the repository:**
```bash
git clone https://github.com/marcelloadonato/EducationalSimulations.git
cd EducationalSimulations
```

2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
```

3. **Activate the virtual environment:**
- **Windows:**
```bash
.\venv\Scripts\activate
```
- **Unix/MacOS:**
```bash
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Dependencies
The project requires the following Python packages:
- `numpy>=1.24.0` - Numerical computations
- `matplotlib>=3.7.0` - Plotting and visualization
- `scipy>=1.10.0` - Scientific computing
- `customtkinter>=5.2.0` - Modern UI components
- `pillow>=10.0.0` - Image handling
- `pytest>=7.4.0` - Testing framework
- `black>=23.7.0` - Code formatting
- `flake8>=6.1.0` - Code linting

## Usage

### Launch the Main Menu
Run the main menu to access all simulations through an intuitive interface:
```bash
python src/main_menu.py
```

The menu features a modern carousel interface with cards for each simulation, complete with descriptions and preview images.

### Run Individual Simulations
Each simulation can also be launched independently:

```bash
# Boids Simulation
python src/boids-simulation.py

# Double-Slit Experiment
python src/double-slit.py

# Double Pendulum
python src/double-pendulum.py

# Lorenz Attractor
python src/lorenz-attractor.py

# Wave Form Simulator
python src/wave-form-simulator.py

# Calculus Explorer
python src/calculus.py

# Mandelbrot Explorer
python src/fractal-generator.py
```

## Project Structure

```
EducationalSimulations/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── LICENSE                        # MIT License
├── docs/                          # Documentation and screenshots
│   └── menu_screenshot.png
├── src/                           # Source code
│   ├── __init__.py               # Package initialization
│   ├── main_menu.py              # Main application launcher
│   ├── boids-simulation.py       # Flocking behavior simulation
│   ├── double-slit.py            # Quantum mechanics simulation
│   ├── double-pendulum.py        # Chaos theory demonstration
│   ├── lorenz-attractor.py       # Strange attractor visualization
│   ├── wave-form-simulator.py    # Wave interference simulator
│   ├── calculus.py               # Interactive calculus explorer
│   ├── fractal-generator.py      # Mandelbrot set explorer
│   ├── create_icons.py           # Icon generation utility
│   └── assets/                   # Images and icons
│       └── icons/
└── tests/                         # Test suite
    └── __init__.py
```

## Educational Applications

### For Students
- **Visual Learning**: See abstract concepts come to life
- **Interactive Exploration**: Experiment with parameters and observe results
- **Hands-On Discovery**: Learn through experimentation rather than passive observation
- **Multiple Disciplines**: Covers physics, mathematics, and computer science

### For Educators
- **Classroom Demonstrations**: Perfect for lectures and presentations
- **Lab Activities**: Students can explore concepts independently
- **Assignment Ideas**: Create experiments based on parameter variations
- **Cross-Curricular**: Integrates physics, math, and computational thinking

### Topics Covered
- **Physics**: Classical mechanics, chaos theory, wave mechanics, quantum mechanics
- **Mathematics**: Calculus, complex numbers, fractals, dynamical systems
- **Computer Science**: Algorithms, simulation, numerical methods, emergent behavior
- **General Science**: Scientific method, hypothesis testing, data visualization

## Development

### Code Quality Tools

**Format code:**
```bash
black src/
```

**Lint code:**
```bash
flake8 src/
```

**Run tests:**
```bash
pytest
```

### Contributing
Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
4. **Run tests and linting**
5. **Commit your changes** (`git commit -m 'Add some AmazingFeature'`)
6. **Push to the branch** (`git push origin feature/AmazingFeature`)
7. **Open a Pull Request**

### Ideas for Contributions
- Add new simulations (planetary motion, electromagnetic fields, etc.)
- Improve UI/UX design
- Add more interactive parameters
- Create educational worksheets or guides
- Optimize performance for complex simulations
- Add export functionality (save images, data, animations)
- Implement additional color schemes or visualization options
- Add sound/audio feedback where appropriate
- Create mobile or web versions

## Technical Details

### Architecture
- **Frontend**: CustomTkinter for modern, cross-platform GUI
- **Visualization**: Matplotlib for high-quality scientific plotting
- **Computation**: NumPy and SciPy for efficient numerical calculations
- **Design Pattern**: Object-oriented architecture with modular simulation classes

### Performance Considerations
- Efficient numerical computation using NumPy vectorization
- Real-time rendering optimization
- Configurable detail levels for performance tuning
- Responsive UI with separate computation threads where needed

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Display**: 1200x800 minimum resolution recommended
- **Graphics**: No special GPU requirements

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

You are free to:
- Use the software for any purpose
- Modify the software
- Distribute the software
- Use it in educational and commercial settings

## Acknowledgments

### Inspiration and Theory
- **Craig Reynolds** - Original Boids algorithm (1986)
- **Edward Lorenz** - Lorenz attractor and chaos theory foundations
- **Benoît Mandelbrot** - Fractal geometry and the Mandelbrot set
- **Thomas Young** - Double-slit experiment (1801)
- **Isaac Newton & Gottfried Leibniz** - Calculus foundations

### Technology
- **CustomTkinter** project for modern UI components
- **NumPy** and **SciPy** communities for scientific computing tools
- **Matplotlib** for publication-quality visualizations
- The open-source community for inspiration and support

## Support and Feedback

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: Share ideas and ask questions in GitHub Discussions
- **Education**: If you use this in a classroom, we'd love to hear about it!

## Roadmap

Future enhancements being considered:
- [ ] Additional simulations (N-body problem, cellular automata, etc.)
- [ ] Export animations and data
- [ ] Interactive tutorials and guided experiments
- [ ] Multi-language support
- [ ] Web-based version
- [ ] VR/AR implementations
- [ ] Curriculum-aligned lesson plans
- [ ] Student assessment tools

---

**Made with dedication to science education and the joy of discovery**

*Star this repository if you find it useful for teaching or learning!*
