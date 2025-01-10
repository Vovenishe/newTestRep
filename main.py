import pygame
import random
import sys

# Ініціалізація Pygame
pygame.init()

# Константи
WIDTH, HEIGHT = 800, 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# Клас для кнопки
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        text_surface = FONT.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Клас для динозавра
class Dinosaur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.velocity = 0
        self.gravity = 1
        self.jump_strength = -15
        self.is_jumping = False

    def jump(self):
        if not self.is_jumping:
            self.velocity = self.jump_strength
            self.is_jumping = True

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y >= HEIGHT - self.height:
            self.y = HEIGHT - self.height
            self.is_jumping = False

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

# Клас для перешкод
class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

    def is_off_screen(self):
        return self.x + self.width < 0

# Клас для гри
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.start_button = Button("Start", WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50, GREEN, (0, 200, 0))
        self.restart_button = Button("Restart", WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50, GREEN, (0, 200, 0))
        self.dinosaur = Dinosaur(100, HEIGHT - 60)
        self.obstacles = []
        self.timer = 0
        self.lives = 3
        self.is_running = False
        self.is_game_over = False

    def reset_game(self):
        self.dinosaur = Dinosaur(100, HEIGHT - 60)
        self.obstacles = []
        self.timer = 0
        self.lives = 3
        self.is_running = False
        self.is_game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.is_clicked(pygame.mouse.get_pos()):
                    self.is_running = True
                if self.restart_button.is_clicked(pygame.mouse.get_pos()):
                    self.reset_game()
                    self.is_running = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.dinosaur.jump()

    def spawn_obstacle(self):
        if random.randint(1, 100) < 5:  # Шанс 5% для створення перешкоди
            obstacle = Obstacle(WIDTH, HEIGHT - 60, 40, 40)
            self.obstacles.append(obstacle)

    def check_collisions(self):
        for obstacle in self.obstacles:
            if (self.dinosaur.x < obstacle.x + obstacle.width and
                self.dinosaur.x + self.dinosaur.width > obstacle.x and
                self.dinosaur.y < obstacle.y + obstacle.height and
                self.dinosaur.y + self.dinosaur.height > obstacle.y):
                self.lives -= 1
                self.obstacles.remove(obstacle)
                if self.lives == 0:
                    self.is_game_over = True
                    self.is_running = False

    def update(self):
        if self.is_running:
            self.dinosaur.update()
            for obstacle in self.obstacles:
                obstacle.update()
                if obstacle.is_off_screen():
                    self.obstacles.remove(obstacle)
            self.spawn_obstacle()
            self.check_collisions()
            self.timer += 1

    def draw(self):
        self.screen.fill(WHITE)
        if not self.is_running and not self.is_game_over:
            self.start_button.draw(self.screen)
        elif self.is_game_over:
            game_over_text = FONT.render("Game Over! Time: " + str(self.timer // FPS), True, BLACK)
            self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            self.restart_button.draw(self.screen)
        else:
            self.dinosaur.draw(self.screen)
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            lives_text = FONT.render("Lives: " + str(self.lives), True, BLACK)
            self.screen.blit(lives_text, (10, 10))
            timer_text = FONT.render("Time: " + str(self.timer // FPS), True, BLACK)
            self.screen.blit(timer_text, (WIDTH - 150, 10))
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

# Запуск гри
if __name__ == "__main__":
    game = Game()
    game.run()