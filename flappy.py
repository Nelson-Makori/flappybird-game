import pygame
import sys
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 800

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ground height
GROUND_HEIGHT = 100

# Gap between pipes
PIPE_GAP = 200
# Horizontal distance between consecutive pipes
PIPE_DISTANCE = 200

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Clone')

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Your bird image or rectangle representation here
        # For simplicity, we'll use a rectangle for the bird
        self.rect = pygame.Rect(50, SCREEN_HEIGHT // 2, 30, 30)
        self.velocity = 0
        self.gravity = 0.6
        self.jump_strength = -9

    def update(self):
        # Update bird position, velocity, etc.
        self.velocity += self.gravity
        self.rect.y += self.velocity

    def jump(self):
        # Implement bird jump action
        self.velocity = self.jump_strength

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, height):
        super().__init__()
        # Your pipe image or rectangle representation here
        # For simplicity, we'll use rectangles for pipes
        self.rect_top = pygame.Rect(x, 0, 50, height)
        self.rect_bottom = pygame.Rect(x, height + PIPE_GAP, 50, SCREEN_HEIGHT - height - PIPE_GAP)

    def update(self):
        # Update pipe position
        self.rect_top.x -= 3
        self.rect_bottom.x -= 3

    def is_offscreen(self):
        # Check if the pipe is off the screen
        return self.rect_top.right < 0

def generate_pipes(last_x):
    pipe_height = random.randint(50, 400)
    new_pipe = Pipe(last_x + PIPE_DISTANCE, pipe_height)
    return new_pipe

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)

def reset_game(bird, pipes):
    bird.rect.y = SCREEN_HEIGHT // 2
    bird.velocity = 0
    pipes.empty()

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = pygame.sprite.Group()
    ground = Ground()

    # Game state
    waiting_for_key = True
    game_over = False
    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Check for key press to start/restart the game
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if waiting_for_key or game_over:
                    waiting_for_key = False
                    game_over = False
                    score = 0
                    reset_game(bird, pipes)

        if waiting_for_key:
            # Clear the screen while waiting for the space bar to be pressed
            screen.fill(WHITE)
            pygame.display.flip()
            continue

        if game_over:
            # Display "Game Over" text
            font = pygame.font.SysFont(None, 36)
            text = font.render("Game Over - Press SPACE to restart", True, BLACK)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.fill(WHITE)
            screen.blit(text, text_rect)
            pygame.display.flip()
            continue

        # Handle key events
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird.jump()

        # Add new pipes periodically
        if len(pipes) == 0 or SCREEN_WIDTH - pipes.sprites()[-1].rect_top.x >= PIPE_DISTANCE:
            new_pipe = generate_pipes(pipes.sprites()[-1].rect_top.x if len(pipes) > 0 else 0)
            pipes.add(new_pipe)

        # Update bird and pipes
        bird.update()
        pipes.update()

        # Remove offscreen pipes
        for pipe in pipes.copy():
            if pipe.is_offscreen():
                pipes.remove(pipe)

        # Collision detection
        # Implement collision detection between bird and pipes
        for pipe in pipes:
            if bird.rect.colliderect(pipe.rect_top) or bird.rect.colliderect(pipe.rect_bottom):
                game_over = True

        # Check for collision with the ground
        if bird.rect.colliderect(ground.rect):
            game_over = True

        # Check for passing pipes
        for pipe in pipes:
            if pipe.rect_top.right == bird.rect.left:
                score += 1

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLACK, bird.rect)

        for pipe in pipes:
            pygame.draw.rect(screen, BLACK, pipe.rect_top)
            pygame.draw.rect(screen, BLACK, pipe.rect_bottom)

        pygame.draw.rect(screen, BLACK, ground.rect)

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    main()
