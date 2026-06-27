import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 400
TRIANGLE_HEIGHT = 300
TRIANGLE_COLOR = (0, 0, 0, 128)
BORDER_COLOR = (255, 0, 0)
BORDER_WIDTH = 5
RECTANGLE_COLOR = (255, 255, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAVITY_ACCELERATION = 0.001

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dynamics Physics Simulator")

# Font for error messages
font = pygame.font.Font(None, 36)

def get_valid_input(prompt, min_value):
    while True:
        # Clear the screen
        screen.fill((0, 0, 0))
        pygame.display.flip()

        # Render the prompt
        prompt_text = font.render(prompt.replace(':', ''), True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(WIDTH / 2, 40))
        screen.blit(prompt_text, prompt_rect)
        pygame.display.flip()

        # Get user input
        try:
            value = float(input(prompt))
            if value > min_value:
                return value
            else:
                print_error_message("Invalid input!", f"Please enter a value greater than {min_value}.")
        except ValueError:
            print_error_message("Invalid input!", f"Please enter a value greater than {min_value}.")

def print_error_message(line1, line2):
    # Render the error messages
    error_text1 = font.render(line1, True, BORDER_COLOR)
    error_text2 = font.render(line2, True, BORDER_COLOR)

    # Get the dimensions of the error messages
    text1_rect = error_text1.get_rect(center=(WIDTH / 2, 40))
    text2_rect = error_text2.get_rect(center=(WIDTH / 2, 80))

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the error messages on the screen
    screen.blit(error_text1, text1_rect)
    screen.blit(error_text2, text2_rect)

    # Update the display
    pygame.display.flip()

    # Wait for 2 seconds to show the error messages
    pygame.time.wait(2000)

def display_message(message, color):
    # Split the message into two lines if it is too long
    lines = message.split('\n')

    # Clear the screen
    screen.fill((0, 0, 0))

    for i, line in enumerate(lines):
        # Render each line of the message
        message_text = font.render(line.replace('(Y/N)', ''), True, color)
        message_rect = message_text.get_rect(center=(WIDTH / 2, 40 + i * 40))
        screen.blit(message_text, message_rect)

    # Update the display
    pygame.display.flip()

    # Wait for 2 seconds to show the message
    pygame.time.wait(2000)

def main():
    while True:
        # Get user input for angle and coefficient of friction
        angle_degrees = get_valid_input("Enter the angle (in degrees): ", 33)
        angle_radians = math.radians(angle_degrees)
        friction_coefficient = get_valid_input("Enter the coefficient of friction: ", 0)
        rotated_angle = 180 - angle_degrees

        # Calculate triangle base based on user input and constant height
        triangle_base = TRIANGLE_HEIGHT / math.tan(angle_radians)

        # Calculate the center position for the triangle
        triangle_x = (WIDTH - triangle_base) / 2
        triangle_y = (HEIGHT - TRIANGLE_HEIGHT) / 2
        triangle_vertices = [(triangle_x, triangle_y),
                             (triangle_x, triangle_y + TRIANGLE_HEIGHT),
                             (triangle_x + triangle_base, triangle_y + TRIANGLE_HEIGHT)]

        # Initialize variables
        rect_height = 20
        rect_width = 60
        time = 0
        final_velocity = 0

        # Adjust the initial position of the rectangle
        rect_x = triangle_vertices[0][0] - rect_width // 2
        rect_y = triangle_vertices[0][1] - rect_height

        # Calculate the initial velocity inversely proportional to the coefficient of friction
        initial_velocity = (triangle_base * GRAVITY_ACCELERATION * math.sin(angle_radians)) / (1 + friction_coefficient)

        # Initialize physics variables
        hypotenuse_length = math.dist(triangle_vertices[0], triangle_vertices[2])
        hypotenuse_angle = math.atan2(triangle_vertices[2][1] - triangle_vertices[0][1],
                                      triangle_vertices[2][0] - triangle_vertices[0][0])

        # Main game loop
        running = True
        reached_bottom = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not reached_bottom:
                # Calculate forces and update the position of the rectangle
                horizontal_force = initial_velocity * friction_coefficient
                horizontal_component = horizontal_force * math.cos(hypotenuse_angle)
                vertical_component = horizontal_force * math.sin(hypotenuse_angle) + GRAVITY_ACCELERATION

                # Update rectangle position
                rect_x += horizontal_component
                rect_y += vertical_component

                # Apply gravity
                initial_velocity += GRAVITY_ACCELERATION

                # Ensure the rectangle stays within the screen boundaries
                rect_x = max(0, min(rect_x, WIDTH - rect_width))

                # Stop moving vertically when it reaches the bottom vertex of the triangle
                if rect_y + rect_height >= triangle_vertices[2][1]:
                    reached_bottom = True
                    rect_y = triangle_vertices[2][1] - rect_height

                    # Calculate time and final velocity at the bottom
                    acceleration = 9.81 * (math.sin(angle_radians) - friction_coefficient * math.cos(angle_radians))
                    final_velocity = math.sqrt(2 * (-acceleration) * TRIANGLE_HEIGHT)
                    time = final_velocity / (-acceleration)
                    formatted_velocity = "{:.2f}".format(final_velocity)
                    formatted_time = "{:.2f}".format(time)
                    print(f"Time taken to reach the bottom: {formatted_time} seconds")
                    print(f"Final velocity at the bottom: {formatted_velocity} m/s")

            # Clear the screen and redraw the triangle
            screen.fill((0, 0, 0))
            pygame.draw.polygon(screen, TRIANGLE_COLOR, triangle_vertices)
            pygame.draw.lines(screen, BORDER_COLOR, True, triangle_vertices + [triangle_vertices[0]], BORDER_WIDTH)

            # Create a rotated rectangle surface with the specified dimensions and color
            rotated_rect = pygame.Surface((rect_width, rect_height), pygame.SRCALPHA)
            rotated_rect.fill(RECTANGLE_COLOR)

            # Rotate the rectangle surface by the desired angle
            rotated_rect = pygame.transform.rotate(rotated_rect, rotated_angle)

            # Get the new rectangle dimensions after rotation
            rotated_rect_width, rotated_rect_height = rotated_rect.get_size()

            # Calculate the position to blit the rotated rectangle
            rotated_rect_x = rect_x + rect_width // 2 - rotated_rect_width // 2
            rotated_rect_y = rect_y + rect_height // 2 - rotated_rect_height // 2

            # Blit the rotated rectangle onto the screen
            screen.blit(rotated_rect, (rotated_rect_x, rotated_rect_y))

            pygame.display.flip()

            # Check if the rectangle has reached the bottom and prompt for another calculation
            if reached_bottom:
                pygame.time.wait(2000)
                display_message("Would you like to perform\nanother calculation? (Y/N)", WHITE)
                user_response = input("Would you like to perform another calculation? (Y/N): ").strip().upper()

                if user_response == 'Y' or user_response == 'y':
                    # Clear screen and restart the program
                    screen.fill(BLACK)
                    pygame.display.flip()
                    break  # Exit the inner loop to restart the program
                elif user_response == 'N' or user_response == 'n':
                    # Display goodbye message and quit
                    display_message("Goodbye!", GREEN)
                    pygame.quit()
                    sys.exit()
                else:
                    display_message("Invalid input!", RED)

# Start the main function
main()