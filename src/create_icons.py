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
    'calculus': create_calculus_icon
}

for name, create_func in icons.items():
    icon = create_func()
    save_icon(icon, name)

print("Icons created successfully!") 