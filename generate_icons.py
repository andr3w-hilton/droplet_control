#!/usr/bin/env python3
"""Generate PNG icons from SVG for PWA"""

from PIL import Image, ImageDraw, ImageFont
import io

def create_droplet_icon(size):
    """Create a droplet icon with gradient background"""
    # Create image with gradient background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded rectangle background with gradient effect
    corner_radius = int(size * 0.22)  # 42/192 ≈ 0.22

    # Create gradient by drawing horizontal lines with varying colors
    for y in range(size):
        # Interpolate between start color (102, 126, 234) and end color (118, 75, 162)
        ratio = y / size
        r = int(102 + (118 - 102) * ratio)
        g = int(126 + (75 - 126) * ratio)
        b = int(234 + (162 - 234) * ratio)

        # Draw rounded rectangle for each line
        for x in range(size):
            # Check if pixel is inside rounded rectangle
            in_rect = False

            # Calculate distance from corners
            if x < corner_radius and y < corner_radius:
                # Top-left corner
                dx = corner_radius - x
                dy = corner_radius - y
                if dx*dx + dy*dy <= corner_radius*corner_radius:
                    in_rect = True
            elif x >= size - corner_radius and y < corner_radius:
                # Top-right corner
                dx = x - (size - corner_radius)
                dy = corner_radius - y
                if dx*dx + dy*dy <= corner_radius*corner_radius:
                    in_rect = True
            elif x < corner_radius and y >= size - corner_radius:
                # Bottom-left corner
                dx = corner_radius - x
                dy = y - (size - corner_radius)
                if dx*dx + dy*dy <= corner_radius*corner_radius:
                    in_rect = True
            elif x >= size - corner_radius and y >= size - corner_radius:
                # Bottom-right corner
                dx = x - (size - corner_radius)
                dy = y - (size - corner_radius)
                if dx*dx + dy*dy <= corner_radius*corner_radius:
                    in_rect = True
            elif (x >= corner_radius and x < size - corner_radius) or \
                 (y >= corner_radius and y < size - corner_radius):
                # Not in corners
                in_rect = True

            if in_rect:
                draw.point((x, y), fill=(r, g, b, 255))

    # Draw water droplet
    droplet_scale = size / 192

    # Droplet path: starts at (96, 40), curves to (72, 96), curves to (96, 120), curves to (120, 96), back to start
    # Using ellipse approximation for the droplet
    droplet_center_x = int(96 * droplet_scale)
    droplet_top_y = int(40 * droplet_scale)
    droplet_width = int(48 * droplet_scale)  # (120-72)
    droplet_height = int(80 * droplet_scale)  # (120-40)

    # Create droplet shape using polygon
    droplet_points = []
    import math

    # Top point
    droplet_points.append((droplet_center_x, droplet_top_y))

    # Left curve (going down)
    for i in range(10):
        angle = math.pi * 0.75 + (math.pi * 0.75) * (i / 10)
        x = droplet_center_x + (droplet_width / 2) * math.cos(angle)
        y = droplet_top_y + droplet_height * 0.7 + (droplet_height * 0.3) * math.sin(angle)
        droplet_points.append((x, y))

    # Bottom semicircle
    bottom_center_y = droplet_top_y + droplet_height * 0.7
    for i in range(21):
        angle = math.pi + (math.pi) * (i / 20)
        x = droplet_center_x + (droplet_width / 2) * math.cos(angle)
        y = bottom_center_y + (droplet_height * 0.3) * math.sin(angle)
        droplet_points.append((x, y))

    # Right curve (going up)
    for i in range(10):
        angle = math.pi * 1.5 - (math.pi * 0.75) * (i / 10)
        x = droplet_center_x + (droplet_width / 2) * math.cos(angle)
        y = droplet_top_y + droplet_height * 0.7 + (droplet_height * 0.3) * math.sin(angle)
        droplet_points.append((x, y))

    draw.polygon(droplet_points, fill=(255, 255, 255, 230))

    # Draw power symbol
    power_center_x = int(96 * droplet_scale)
    power_center_y = int(136 * droplet_scale)
    power_radius = int(12 * droplet_scale)
    power_stroke = max(1, int(3 * droplet_scale))

    # Draw circle (outline only)
    draw.ellipse(
        [power_center_x - power_radius, power_center_y - power_radius,
         power_center_x + power_radius, power_center_y + power_radius],
        outline=(255, 255, 255, 230),
        width=power_stroke
    )

    # Draw vertical line
    line_top_y = int(124 * droplet_scale)
    draw.line(
        [(power_center_x, power_center_y), (power_center_x, line_top_y)],
        fill=(255, 255, 255, 230),
        width=power_stroke
    )

    return img

# Generate both icon sizes
print("Generating 192x192 icon...")
icon_192 = create_droplet_icon(192)
icon_192.save('icon-192.png')
print("icon-192.png created")

print("Generating 512x512 icon...")
icon_512 = create_droplet_icon(512)
icon_512.save('icon-512.png')
print("icon-512.png created")

print("\nIcons generated successfully!")
