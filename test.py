import pygame
import pygame.freetype
import random

pygame.init()
FONT = pygame.freetype.SysFont(None, 32)

class Player(pygame.sprite.Sprite):
    def __init__(self, color, canvas, bindings):
        super().__init__()
        self.image = pygame.Surface((32, 32))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=canvas.get_rect().center)
        self.canvas = canvas
        self.bindings = bindings
        self.pos = pygame.Vector2(self.rect.topleft)

    def update(self):
        pressed = pygame.key.get_pressed()
        direction = pygame.Vector2()
        for key in self.bindings:
            if pressed[key]:
                direction += self.bindings[key]

        if direction.length() > 0: 
            direction.normalize_ip()
            self.pos += direction*4

        self.rect.topleft = self.pos
        self.rect.clamp_ip(self.canvas.get_rect())
        self.pos = self.rect.topleft

class Game(pygame.sprite.Sprite):
    def __init__(self, color, bg_color, bindings, left):
        super().__init__()
        self.bg_color = bg_color
        self.image = pygame.Surface((400, 600))
        self.image.fill(self.bg_color)
        self.rect = self.image.get_rect(left=0 if left else 400)
        self.player = Player(color, self.image, bindings)
        self.target = pygame.Vector2(random.randint(100, 300), random.randint(100, 500))
        self.stuff = pygame.sprite.Group(self.player)
        self.score = 0

    def update(self):
        self.stuff.update()
        self.image.fill(self.bg_color)
        self.stuff.draw(self.image)
        FONT.render_to(self.image, (190, 50), str(self.score), (200, 200, 200))
        pygame.draw.circle(self.image, (210, 210, 210), [int(v) for v in self.target], 5)
        if (self.player.rect.center - self.target).length() <= 20:
            self.score += 1
            self.target = pygame.Vector2(random.randint(100, 300), random.randint(100, 500))

def main():
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    player1_bindings = {
        pygame.K_w: pygame.Vector2(0, -1),
        pygame.K_a: pygame.Vector2(-1, 0),
        pygame.K_s: pygame.Vector2(0, 1),
        pygame.K_d: pygame.Vector2(1, 0)
    }
    player2_bindings = {
        pygame.K_UP: pygame.Vector2(0, -1),
        pygame.K_LEFT: pygame.Vector2(-1, 0),
        pygame.K_DOWN: pygame.Vector2(0, 1),
        pygame.K_RIGHT: pygame.Vector2(1, 0)
    }
    player1 = Game(pygame.Color('dodgerblue'), (30, 30, 30), player1_bindings, True)
    player2 = Game(pygame.Color('orange'), (80, 20, 30), player2_bindings, False)
    games = pygame.sprite.Group(player1, player2)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        games.update()
        screen.fill((30, 30, 30))
        games.draw(screen)
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
