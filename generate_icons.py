#!/usr/bin/env python3
"""Generate PNG icons from SVG for PWA"""

from PIL import Image, ImageDraw
import math

def create_droplet_icon(size):
    """Create a droplet icon with gradient background"""
    # Create image with gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded rectangle background with gradient effect
    corner_radius = int(size * 0.22)

    # Create gradient background
    for y in range(size):
        ratio = y / size
        r = int(102 + (118 - 102) * ratio)
        g = int(126 + (75 - 126) * ratio)
        b = int(234 + (162 - 234) * ratio)

        for x in range(size):
            in_rect = False

            if x < corner_radius and y < corner_radius:
                dx = corner_radius - x
                dy = corner_radius - y
                if dx*dx + dy*dy <= corner_radius*corner_radius:
                    in_rect = True
            elif x >= size - corner_radius and y < corner_radius:
                dx = x - (size - corner_radius)
                dy = corner_radius - y
                if dx*dx + dy*dy <= corner_radius*corner_radius:
                    in_rect = True
            elif x < corner_radius and y >= size - corner_radius:
                dx = corner_radius - x
                dy = y - (size - corner_radius)
                if dx*dx + dy*dy <= corner_radius*corner_radius:
                    in_rect = True
            elif x >= size - corner_radius and y >= size - corner_radius:
                dx = x - (size - corner_radius)
                dy = y - (size - corner_radius)
                if dx*dx + dy*dy <= corner_radius*corner_radius:
                    in_rect = True
            elif (x >= corner_radius and x < size - corner_radius) or \
                 (y >= corner_radius and y < size - corner_radius):
                in_rect = True

            if in_rect:
                draw.point((x, y), fill=(r, g, b, 255))

    # Scale factor from 512px design
    scale = size / 512
    center_x = size / 2

    # Water droplet - classic teardrop shape
    # Top point of droplet
    top_y = 106.67 * scale
    # Bottom center of circular part
    circle_center_y = 256 * scale
    circle_radius = 64 * scale

    droplet_points = []

    # Start at the top point
    droplet_points.append((center_x, top_y))

    # Left side of droplet - smooth curve from top to circle
    num_points = 30
    for i in range(1, num_points):
        t = i / num_points
        # Calculate y position with smooth curve
        y = top_y + (circle_center_y - top_y) * t
        # Calculate x offset using a smooth curve
        # At top: narrow, at bottom: reaches circle radius
        x_offset = circle_radius * math.sin(t * math.pi / 2) * 0.8
        droplet_points.append((center_x - x_offset, y))

    # Bottom semicircle (going counterclockwise from left to right)
    for i in range(num_points + 1):
        angle = math.pi - (math.pi * i / num_points)
        x = center_x + circle_radius * math.cos(angle)
        y = circle_center_y + circle_radius * math.sin(angle)
        droplet_points.append((x, y))

    # Right side of droplet - smooth curve from circle back to top
    for i in range(num_points - 1, 0, -1):
        t = i / num_points
        y = top_y + (circle_center_y - top_y) * t
        x_offset = circle_radius * math.sin(t * math.pi / 2) * 0.8
        droplet_points.append((center_x + x_offset, y))

    # Draw the droplet
    draw.polygon(droplet_points, fill=(255, 255, 255, 230))

    # Power symbol
    power_y = 362.67 * scale
    power_radius = 32 * scale
    power_stroke = max(2, int(8 * scale))

    # Draw power circle
    draw.ellipse(
        [center_x - power_radius, power_y - power_radius,
         center_x + power_radius, power_y + power_radius],
        outline=(255, 255, 255, 230),
        width=power_stroke
    )

    # Draw power line
    line_top = 330.67 * scale
    draw.line(
        [(center_x, power_y), (center_x, line_top)],
        fill=(255, 255, 255, 230),
        width=power_stroke
    )

    return img

# Generate icons
print("Generating 192x192 icon...")
icon_192 = create_droplet_icon(192)
icon_192.save('icon-192.png')
print("icon-192.png created")

print("Generating 512x512 icon...")
icon_512 = create_droplet_icon(512)
icon_512.save('icon-512.png')
print("icon-512.png created")

print("\nIcons generated successfully!")
