from PIL import Image, ImageDraw
import os
import math

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
    'wave': create_wave_icon
}

for name, create_func in icons.items():
    icon = create_func()
    save_icon(icon, name)

print("Icons created successfully!") 