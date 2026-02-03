import pygame
import random
import math

# =========================================================
#                       GAME CLASS
# =========================================================
class Game:
    """
    Main Game Class
    Handles the game loop, initialization, and core game logic
    """

    def __init__(self, width, height):
        """
        Initialize the game window, spaceship, enemies, and background
        """
        pygame.init()
        self.width = width
        self.height = height

        # Set up display
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Space Invaders")

        # Game clock and state
        self.clock = pygame.time.Clock()
        self.running = True

        # Player spaceship
        self.spaceship = SpaceShip(self, 600, 600)

        # Game score
        self.score = 0

        # Initialize enemies
        self.enemies = []
        for _ in range(12):
            self.enemies.append(Enemy(
                self,
                random.randint(0, 1216),
                random.randint(30, 130)
            ))

        # Load and scale background image
        self.background_img = pygame.image.load("background.png")
        self.background_img = pygame.transform.scale(self.background_img, (self.width, self.height))

    # ------------------------------
    # GAME LOOP
    # ------------------------------
    def run(self):
        """
        Main game loop
        Handles events, updates all objects, checks collisions, and renders everything
        """
        while self.running:
            self.clock.tick(60)  # Limit FPS to 60
            self.screen.blit(self.background_img, (0, 0))

            # Handle all events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Handle key presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(-10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_SPACE:
                        self.spaceship.fire_bullet()

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.spaceship.move(10)
                    if event.key == pygame.K_RIGHT:
                        self.spaceship.move(-10)

            # Update spaceship position and render
            self.spaceship.update()

            # Update bullets
            for bullet in self.spaceship.bullets[:]:
                if bullet.is_fired:
                    bullet.update()
                else:
                    self.spaceship.bullets.remove(bullet)

            # Update enemies and check collisions
            for enemy in self.enemies:
                enemy.update()
                enemy.check_collision()
                # Check for game over
                if enemy.y > 570:
                    for i in self.enemies:
                        i.y = 1000  # Move all enemies off-screen
                    self.print_game_over()
                    break

            # Display score
            self.print_score()
            pygame.display.update()

    # ------------------------------
    # GAME OVER DISPLAY
    # ------------------------------
    def print_game_over(self):
        """
        Display GAME OVER screen for 3 seconds and quit the game
        """
        go_font = pygame.font.Font("freesansbold.ttf", 64)
        go_text = go_font.render("GAME OVER", True, (255, 255, 255))
        self.screen.blit(go_text, (350, 300))
        pygame.display.update()
        pygame.time.wait(3000)
        pygame.quit()

    # ------------------------------
    # SCORE DISPLAY
    # ------------------------------
    def print_score(self):
        """
        Render the current score in the top-left corner
        """
        score_font = pygame.font.Font("freesansbold.ttf", 24)
        score_text = score_font.render("Points: " + str(self.score), True, (255, 255, 255))
        self.screen.blit(score_text, (8, 8))


# =========================================================
#                     SPACESHIP CLASS
# =========================================================
class SpaceShip:
    """
    Player-controlled spaceship
    Handles movement, bullet firing, and rendering
    """

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.change_x = 0
        self.spaceship_img = pygame.image.load("spaceship.png")
        self.bullets = []

    def fire_bullet(self):
        """
        Fire a bullet from the current spaceship position
        """
        bullet = Bullet(self.game, self.x, self.y)
        bullet.fire()
        self.bullets.append(bullet)

    def move(self, speed):
        """
        Adjust the horizontal movement speed
        """
        self.change_x += speed

    def update(self):
        """
        Update spaceship position and draw on screen
        """
        self.x += self.change_x

        # Keep spaceship on screen
        if self.x < 0:
            self.x = 0
        elif self.x > 1216:
            self.x = 1216

        self.game.screen.blit(self.spaceship_img, (self.x, self.y))


# =========================================================
#                        BULLET CLASS
# =========================================================
class Bullet:
    """
    Bullet fired by the player
    Handles movement and rendering
    """

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.is_fired = False
        self.fire_speed = 10
        self.fire_img = pygame.image.load("fire.png")

    def fire(self):
        """
        Activate the bullet
        """
        self.is_fired = True

    def update(self):
        """
        Update bullet position and draw on screen
        """
        self.y -= self.fire_speed
        if self.y <= 0:
            self.is_fired = False
        self.game.screen.blit(self.fire_img, (self.x, self.y))


# =========================================================
#                         ENEMY CLASS
# =========================================================
class Enemy:
    """
    Enemy alien class
    Handles movement, collision detection, and rendering
    """

    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.change_x = 5
        self.change_y = 100
        self.enemy_img = pygame.image.load("enemy.png")

    def check_collision(self):
        """
        Check for collision with bullets
        Reset enemy position and increase score if hit
        """
        for bullet in self.game.spaceship.bullets:
            distance = math.sqrt((self.x - bullet.x) ** 2 + (self.y - bullet.y) ** 2)
            if distance < 35:
                bullet.is_fired = False
                self.game.score += 1
                # Respawn enemy at a random location
                self.x = random.randint(0, 1216)
                self.y = random.randint(50, 150)

    def update(self):
        """
        Update enemy position and handle screen boundaries
        """
        self.x += self.change_x

        # Bounce off the screen edges
        if self.x >= 1216:
            self.y += self.change_y
            self.change_x = -5
        elif self.x <= 0:
            self.y += self.change_y
            self.change_x = 5

        self.game.screen.blit(self.enemy_img, (self.x, self.y))


# =========================================================
#                         MAIN EXECUTION
# =========================================================
if __name__ == "__main__":
    game = Game(1280, 720)
    game.run()
