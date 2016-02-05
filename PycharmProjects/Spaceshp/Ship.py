import sys
import pygame
from Classes.Vector import Vector

FPS = 30
NORMAL = 0
TURN_LEFT = 1
TURN_RIGHT = 2
SPEED_UP = 3
SPEED_DOWN = 4


class Ship:
    def __init__(self, pos):
        self.pos = Vector(pos)
        self.image = pygame.Surface((65, 40), pygame.SRCALPHA)
        self.speed = Vector((5.8, 7.4))
        self.state = NORMAL
        self.direction = self.speed
        self.draw()
        self.image_time = self.image

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.state = TURN_LEFT
            if event.key == pygame.K_RIGHT:
                self.state = TURN_RIGHT
            if event.key == pygame.K_UP:
                self.state = SPEED_UP
            if event.key == pygame.K_DOWN:
                self.state = SPEED_DOWN
        if event.type == pygame.KEYUP:
            self.state = NORMAL

    def update(self):
        if self.state == TURN_LEFT:
            self.speed.rotate(-5)

        if self.state == TURN_RIGHT:
            self.speed.rotate(5)

        if self.state == SPEED_DOWN:
            self.speed -= self.speed.normalize()
            if self.speed.len < 1 and self.speed.len != 0:
                self.direction = self.speed
                self.speed = Vector((0, 0))

        if self.state == SPEED_UP:
            if self.speed.len < 1:
                self.speed = self.direction
            self.speed += self.speed.normalize()
        self.pos += self.speed

        if self.pos.x > 800:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = 800
        if self.pos.y > 600:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = 600

    def draw(self):
        pygame.draw.polygon(self.image, (220, 220, 220), [(0, 0), (10, 10), (55, 20), (10, 30),
                                                          (0, 40), (0, 30), (7, 20), (0, 10)])

    def render(self, screen):
        image_rotate = pygame.transform.rotate(self.image, self.speed.angle)
        origin_rec = self.image.get_rect()
        rotate_rec = image_rotate.get_rect()
        rotate_rec.center = origin_rec.center
        rotate_rec.move_ip(self.pos.as_point())
        screen.blit(image_rotate, rotate_rec)
        pygame.draw.line(screen, (0, 255, 0), self.pos.as_point(), (self.pos + self.speed*10).as_point())

pygame.init()
pygame.display.set_mode((800, 600))
screen = pygame.display.get_surface()

ship = Ship((100, 110))

clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        ship.events(event)

        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(FPS)

    ship.update()
    screen.fill((0, 0, 0))
    ship.render(screen)
    pygame.display.flip()
