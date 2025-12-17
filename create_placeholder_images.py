#!/usr/bin/env python3
"""
Script to create placeholder images for the textbook content
"""
import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_placeholder_image(width, height, title, subtitle, filename):
    """Create a placeholder image with title and subtitle"""
    # Create a new image with a background color
    image = Image.new('RGB', (width, height), color=(64, 64, 128))  # Dark blue background

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Try to use a default font, fallback to default if not available
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 36)
        subtitle_font = ImageFont.truetype("DejaVuSans.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()

    # Draw title
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, height // 3), title, fill=(255, 255, 255), font=title_font)

    # Draw subtitle
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    draw.text((subtitle_x, height // 2), subtitle, fill=(200, 200, 200), font=subtitle_font)

    # Save the image
    image.save(filename)
    print(f"Created: {filename}")

def create_textbook_images():
    """Create placeholder images for textbook sections"""

    # Create various placeholder images for different sections
    images_to_create = [
        (800, 400, "Physical AI & Humanoid Robotics", "Embodied Intelligence Systems", "frontend/static/img/physical-ai-cover.jpg"),
        (800, 400, "ROS 2 Fundamentals", "Robot Operating System", "frontend/static/img/ros2-fundamentals.jpg"),
        (800, 400, "Simulation Environments", "Gazebo & Unity", "frontend/static/img/simulation.jpg"),
        (800, 400, "NVIDIA Isaac Ecosystem", "Perception & Navigation", "frontend/static/img/nvidia-isaac.jpg"),
        (800, 400, "Vision-Language-Action", "Integrating Perception", "frontend/static/img/vla-models.jpg"),
        (800, 400, "Hardware Platforms", "RTX Workstations & Jetson", "frontend/static/img/hardware-platforms.jpg"),
        (800, 400, "Unitree Robots", "Humanoid Systems", "frontend/static/img/unitree-robots.jpg"),
        (800, 400, "Embodied Intelligence", "AI Meets Physical Systems", "frontend/static/img/embodied-intelligence.jpg"),
    ]

    # Ensure the directory exists
    os.makedirs("frontend/static/img", exist_ok=True)

    for width, height, title, subtitle, filename in images_to_create:
        create_placeholder_image(width, height, title, subtitle, filename)

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw, ImageFont
        create_textbook_images()
        print("\n✅ All placeholder images created successfully!")
        print("Images are saved in: frontend/static/img/")
    except ImportError:
        print("Pillow library not available. Install with: pip install Pillow")
        print("Skipping image creation.")