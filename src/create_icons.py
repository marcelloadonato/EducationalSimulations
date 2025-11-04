from PIL import Image, ImageDraw
import os
import math
import numpy as np
import matplotlib.pyplot as plt

def create_boids_icon(size=(300, 200)):
    image = Image.new('RGB', size, '#1e1e2e')
    draw = ImageDraw.Draw(image)
    
    # Draw multiple triangular "birds" in a formation
    birds = [
        [(150, 80), (140, 95), (160, 95)],  # Center bird
        [(130, 100), (120, 115), (140, 115)],  # Left bird
        [(170, 100), (160, 115), (180, 115)],  # Right bird
        [(110, 120), (100, 135), (120, 135)],  # Far left bird
        [(190, 120), (180, 135), (200, 135)],  # Far right bird
    ]
    
    for bird in birds:
        draw.polygon(bird, fill='#6c5ce7')
    
    return image

def create_pendulum_icon(size=(300, 200)):
    image = Image.new('RGB', size, '#1e1e2e')
    draw = ImageDraw.Draw(image)
    
    # Draw pendulum mount
    draw.line([(100, 50), (200, 50)], fill='#6c5ce7', width=3)
    
    # Draw first pendulum arm and bob
    draw.line([(150, 50), (120, 100)], fill='#6c5ce7', width=2)
    draw.ellipse([(110, 90), (130, 110)], fill='#845ef7')
    
    # Draw second pendulum arm and bob
    draw.line([(120, 100), (140, 150)], fill='#6c5ce7', width=2)
    draw.ellipse([(130, 140), (150, 160)], fill='#845ef7')
    
    return image

def create_lorenz_icon(size=(300, 200)):
    image = Image.new('RGB', size, '#1e1e2e')
    draw = ImageDraw.Draw(image)
    
    # Draw a simplified Lorenz attractor curve
    points = []
    for t in range(100):
        x = 150 + 30 * math.sin(t * 0.1) * math.cos(t * 0.05)
        y = 100 + 20 * math.sin(t * 0.1)
        points.append((x, y))
    
    # Draw the curve
    for i in range(len(points) - 1):
        draw.line([points[i], points[i + 1]], fill='#6c5ce7', width=2)
    
    return image

def create_wave_icon(size=(300, 200)):
    image = Image.new('RGB', size, '#1e1e2e')
    draw = ImageDraw.Draw(image)
    
    # Draw multiple sine waves with interference
    points1 = []
    points2 = []
    for x in range(300):
        y1 = 100 + 30 * math.sin(x * 0.05)
        y2 = 100 + 20 * math.sin(x * 0.05 + math.pi)
        points1.append((x, y1))
        points2.append((x, y2))
    
    # Draw waves
    for i in range(len(points1) - 1):
        draw.line([points1[i], points1[i + 1]], fill='#6c5ce7', width=2)
        draw.line([points2[i], points2[i + 1]], fill='#845ef7', width=2)
    
    return image

def create_calculus_icon(size=(300, 200)):
    # Create figure with transparent background
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_facecolor('#1e1e2e')
    plt.gcf().set_facecolor('#1e1e2e')

    # Create data for the quadratic function
    x = np.linspace(-2, 2, 200)
    y = 0.8 * x**2 - 0.5  # Quadratic function

    # Plot main function
    plt.plot(x, y, color='#6c5ce7', linewidth=4)

    # Add tangent line at x=0.7
    x0 = 0.7
    y0 = 0.8 * x0**2 - 0.5
    slope = 2 * 0.8 * x0
    b = y0 - slope * x0
    tangent_y = slope * x + b
    plt.plot(x, tangent_y, '--', color='#845ef7', linewidth=3)

    # Add point of tangency
    plt.plot([x0], [y0], 'o', color='#ff6b6b', markersize=12)

    # Shade area under curve from -1 to 1
    x_integral = np.linspace(-1, 1, 100)
    y_integral = 0.8 * x_integral**2 - 0.5
    plt.fill_between(x_integral, y_integral, -2, alpha=0.3, color='#4c3b99')

    # Set plot limits and remove axes
    plt.xlim(-2, 2)
    plt.ylim(-2, 2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Save to a temporary file and convert to PIL Image
    temp_path = 'src/assets/temp_calculus.png'
    plt.savefig(temp_path, 
                bbox_inches='tight',
                transparent=False,
                dpi=100,
                pad_inches=0.1)
    plt.close()

    # Load the temporary file and convert to PIL Image
    image = Image.open(temp_path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    
    # Delete temporary file
    os.remove(temp_path)
    
    return image

def create_fractal_icon(size=(300, 200)):
    # Create figure with transparent background
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_facecolor('#1e1e2e')
    plt.gcf().set_facecolor('#1e1e2e')

    # Create a simplified version of the Mandelbrot set for the icon
    width, height = 300, 200
    x = np.linspace(-2, 0.5, width)
    y = np.linspace(-1, 1, height)
    X, Y = np.meshgrid(x, y)
    Z = X + Y*1j
    c = Z.copy()
    
    # Compute a simple version of the set
    for i in range(20):
        mask = np.abs(Z) < 2
        Z[mask] = Z[mask]**2 + c[mask]
    
    # Create the plot
    plt.imshow(np.abs(Z) < 2, extent=(-2, 0.5, -1, 1), cmap='viridis')
    
    # Remove axes for cleaner look
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Save to a temporary file and convert to PIL Image
    temp_path = 'src/assets/temp_fractal.png'
    plt.savefig(temp_path, 
                bbox_inches='tight',
                transparent=False,
                dpi=100,
                pad_inches=0.1)
    plt.close()

    # Load the temporary file and convert to PIL Image
    image = Image.open(temp_path)
    image = image.resize(size, Image.Resampling.LANCZOS)
    
    # Delete temporary file
    os.remove(temp_path)
    
    return image

def create_double_slit_icon(size=(300, 200)):
    # Create figure with transparent background
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_facecolor('#1e1e2e')
    plt.gcf().set_facecolor('#1e1e2e')

    # Create the screen pattern
    x = np.linspace(-2, 2, 1000)
    k = 5  # wave number
    d = 0.5  # slit separation
    pattern = np.cos(k * d * x)**2  # interference pattern

    # Plot the interference pattern
    plt.plot(x, pattern, color='#6c5ce7', linewidth=2)

    # Draw the slits
    plt.plot([-0.25, -0.25], [0.3, 0.5], color='#845ef7', linewidth=4)
    plt.plot([0.25, 0.25], [0.3, 0.5], color='#845ef7', linewidth=4)

    # Add some "particle" dots
    np.random.seed(42)  # for reproducibility
    x_dots = np.random.uniform(-2, 2, 30)
    y_dots = np.cos(k * d * x_dots)**2 + np.random.normal(0, 0.05, 30)
    plt.scatter(x_dots, y_dots, color='#ff6b6b', alpha=0.6, s=20)

    # Set plot limits and remove axes
    plt.xlim(-2, 2)
    plt.ylim(-0.2, 1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Save to a temporary file and convert to PIL Image
    temp_path = 'src/assets/temp_double_slit.png'
    plt.savefig(temp_path,
                bbox_inches='tight',
                transparent=False,
                dpi=100,
                pad_inches=0.1)
    plt.close()

    # Load the temporary file and convert to PIL Image
    image = Image.open(temp_path)
    image = image.resize(size, Image.Resampling.LANCZOS)

    # Delete temporary file
    os.remove(temp_path)

    return image

def create_planetary_motion_icon(size=(300, 200)):
    # Create figure with transparent background
    plt.figure(figsize=(10, 10))
    ax = plt.gca()
    ax.set_facecolor('#1e1e2e')
    plt.gcf().set_facecolor('#1e1e2e')

    # Draw the Sun at center
    sun = plt.Circle((0, 0), 0.3, color='#FDB813', zorder=10)
    ax.add_patch(sun)

    # Draw orbital paths for planets
    orbits = [0.8, 1.3, 1.8, 2.3]
    for radius in orbits:
        circle = plt.Circle((0, 0), radius, fill=False,
                          color='#6c5ce7', alpha=0.3, linewidth=1.5, linestyle='--')
        ax.add_patch(circle)

    # Draw planets at different positions
    planets = [
        (0.8, 45, '#8C7853', 0.08),   # Mercury-like
        (1.3, 120, '#FFC649', 0.12),  # Venus-like
        (1.8, 200, '#4A90E2', 0.13),  # Earth-like
        (2.3, 310, '#E27B58', 0.10),  # Mars-like
    ]

    for radius, angle, color, planet_size in planets:
        angle_rad = np.radians(angle)
        x = radius * np.cos(angle_rad)
        y = radius * np.sin(angle_rad)

        # Draw planet
        planet = plt.Circle((x, y), planet_size, color=color, zorder=9)
        ax.add_patch(planet)

        # Draw trail arc (partial orbit)
        trail_angles = np.linspace(angle_rad - np.pi/3, angle_rad, 30)
        trail_x = radius * np.cos(trail_angles)
        trail_y = radius * np.sin(trail_angles)
        plt.plot(trail_x, trail_y, color=color, alpha=0.5, linewidth=2)

    # Set equal aspect ratio and limits
    ax.set_aspect('equal')
    plt.xlim(-2.8, 2.8)
    plt.ylim(-2.8, 2.8)

    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    # Save to a temporary file and convert to PIL Image
    temp_path = 'src/assets/temp_planetary.png'
    plt.savefig(temp_path,
                bbox_inches='tight',
                transparent=False,
                dpi=100,
                pad_inches=0.1)
    plt.close()

    # Load the temporary file and convert to PIL Image
    image = Image.open(temp_path)
    image = image.resize(size, Image.Resampling.LANCZOS)

    # Delete temporary file
    os.remove(temp_path)

    return image

def save_icon(image, name):
    if not os.path.exists('src/assets'):
        os.makedirs('src/assets')
    
    # Resize to final icon size while maintaining quality
    image = image.resize((600, 400), Image.Resampling.LANCZOS)
    image.save(f'src/assets/{name}_icon.png', quality=95)

# Create and save icons
icons = {
    'boids': create_boids_icon,
    'pendulum': create_pendulum_icon,
    'lorenz': create_lorenz_icon,
    'wave': create_wave_icon,
    'calculus': create_calculus_icon,
    'fractal': create_fractal_icon,
    'double_slit': create_double_slit_icon,
    'planetary': create_planetary_motion_icon
}

for name, create_func in icons.items():
    icon = create_func()
    save_icon(icon, name)

print("Icons created successfully!") 