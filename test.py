import pygame
import math

pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Rotated Rectangles")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def draw_rotated_rectangle(surface, color, center, size, angle):
    # Create a surface for the rotated rectangle
    rotated_rect_surface = pygame.Surface(size, pygame.SRCALPHA)
    # Draw the rectangle on the rotated surface
    pygame.draw.rect(rotated_rect_surface, color, (0, 0, *size))
    # Rotate the surface
    rotated_surface = pygame.transform.rotate(rotated_rect_surface, angle)
    # Get the rectangle of the rotated surface
    rotated_rect = rotated_surface.get_rect(center=center)
    # Draw the rotated surface onto the main surface
    surface.blit(rotated_surface, rotated_rect)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear the screen
    screen.fill(BLACK)
    
    # Draw a rotated rectangle
    rectangle_center = (screen_width // 2, screen_height // 2)
    rectangle_size = (100, 50)  # Width, Height
    angle_degrees = 45
    draw_rotated_rectangle(screen, WHITE, rectangle_center, rectangle_size, angle_degrees)
    
    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
