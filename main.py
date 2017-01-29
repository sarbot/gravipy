# -*- coding: UTF-8 -*-

import pygame
import numpy as np
import random as rn



class Player(object):


    def __init__(self, name, image):
        self.name = name
        self.image = load_image(image)
        self.image_rotated = self.image
        self.bullets = []
        self.shoot_cd_max = 40
        self.shoot_cd = self.shoot_cd_max# 60 = 1 sec

        self.x, self.y = 100, 400 # (position)
        self.dx, self.dy = 1, 0 # have to be 1 in square abs (direction)
        self.vx, self.vy = 0, 0 # unlimited yet (speed)
        self.rot = 0 # current rotation as angle (rotationspeed)

        self.view_angle = 0 # (viewdirection)
        #self.view_x, self.view_y = 1, 0 # calc by angle_x angle_y has to be 1 in square abs (viewdirection)

        self.rot_step = 0.1# rotation steps
        self.boost = 0.1


    def rotate_left(self):
        self.rot += self.rot_step
        if self.rot > 360:
            self.rot -= 360
        elif self.rot < 0:
            self.rot += 360


    def rotate_right(self):
        self.rot -= self.rot_step
        if self.rot > 360:
            self.rot -= 360
        elif self.rot < 0:
            self.rot += 360


    def speed_up(self):
        self.vx += angle_x(self.view_angle) * self.boost
        self.vy += angle_y(self.view_angle) * self.boost


    def speed_down(self):
        self.vx -= angle_x(self.view_angle) * self.boost
        self.vy -= angle_y(self.view_angle) * self.boost

    def rock_force(self, rocks):
        force_x = 0
        force_y = 0
        for rock in rocks:
            dx, dy, force = rock.get_force((self.x, self.y))
            force_x += dx*force
            force_y += dy*force

        self.vx += force_x
        self.vy += force_y

    def move(self):
        self.x += self.vx
        self.y += self.vy
        self.view_angle += self.rot
        # update shoot cooldown
        if self.shoot_cd >= -1:
            self.shoot_cd -= 1

    def update_bullets(self, screen):
        for b in self.bullets:
            b.move()
            b.render(screen)

    def shoot(self):
        if self.shoot_cd <= 0:
            bullet = Bullet(self.x, self.y, self.view_angle)
            self.bullets.append(bullet)
            self.shoot_cd = self.shoot_cd_max


    def render(self, screen):
        center = self.image.get_rect().center
        self.image_rotated = pygame.transform.rotate(self.image, self.view_angle)
        self.image_rotated.get_rect().center = center #fix top left position rotation
        w = self.image_rotated.get_rect().width
        h = self.image_rotated.get_rect().height
        screen.blit(self.image_rotated, (self.x-w/2, self.y-h/2))


class Rock(object):

    def __init__(self, image, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.vx = 2
        self.vy = 2
        self.size = 4
        self.gravity = 2000
        self.image = load_image(image)
        self.r = 50

    def get_force(self, pos):
        pos_self = (self.x, self.y)
        pos_self = np.array(pos_self)
        pos = np.array(pos)
        delta = pos_self - pos
        print(delta)
        norm = np.linalg.norm(delta)
        print(norm)
        dx = delta[0]/norm
        dy = delta[1]/norm
        force = self.gravity / norm**2
        print(force)
        return dx, dy, force


    def move(self):
        self.x += self.vx
        self.y += self.vy

    def render(self, screen):
        w = self.image.get_rect().width
        h = self.image.get_rect().height
        screen.blit(self.image, (self.x-w/2, self.y-h/2))


class Bullet(object):

    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vx = angle_x(angle)
        self.vy = angle_y(angle)
        self.speed = 30
        self.image = load_image('img/bullet.png')

    def move(self):
        self.x += self.vx * self.speed
        self.y += self.vy * self.speed

    def render(self, screen):
        w = self.image.get_rect().width
        h = self.image.get_rect().height
        screen.blit(self.image, (self.x-w/2, self.y-h/2))


def angle_x(angle):
    angle = 2*np.pi * angle / 360
    x = np.cos(angle)
    return x

def angle_y(angle):
    angle = 2 * np.pi * angle / 360
    y = - np.sin(angle) #minus cause y is inverted to mathematical koordinates
    return y

def load_image(filename, colorkey=None):
    # Hilfsfunktion, um ein Bild zu laden:

    image = pygame.image.load(filename)
    # Das Pixelformat der Surface an den Bildschirm (genauer: die screen-Surface) anpassen.
    # Dabei die passende Funktion verwenden, je nach dem, ob wir ein Bild mit Alpha-Kanal haben oder nicht.
    if image.get_alpha() is None:
        image = image.convert()
    else:
        image = image.convert_alpha()
    # Colorkey des Bildes setzen, falls nicht None.
    # Bei -1 den Pixel im Bild an Position (0, 0) als Colorkey verwenden.
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image




def main():
    pygame.init()
    if not pygame.font: print('Fehler pygame.font Modul konnte nicht geladen werden!')
    if not pygame.mixer: print('Fehler pygame.mixer Modul konnte nicht geladen werden!')
    screen = pygame.display.set_mode((1800, 900),pygame.FULLSCREEN)

    bullets = [] #todo delete old bullets from list (destroy)
    rocks = []

    title = 'GraviPy'

    rock_image = 'img/rock.png'
    rock_number = 2
    for i in range(rock_number):
        rock_x = rn.randint(100,1700)
        rock_y = rn.randint(100, 800)
        rock = Rock(rock_image, (rock_x, rock_y))
        rocks.append(rock)
    #create player
    player_image = 'img/ship.png'
    player = Player('Lukas', player_image)
    # Titel des Fensters setzen, Mauszeiger nicht verstecken und Tastendrücke wiederholt senden.

    pygame.display.set_caption(title)
    pygame.mouse.set_visible(1)
    pygame.key.set_repeat(1, 30)

    # Clock-Objekt erstellen, das wir benötigen, um die Framerate zu begrenzen.

    clock = pygame.time.Clock()

    # Die Schleife, und damit unser Spiel, läuft solange running == True.

    running = True

    while running:

        # Framerate auf 60 Frames pro Sekunde beschränken.
        # Pygame wartet, falls das Programm schneller läuft.
        clock.tick(60)
        # screen-Surface mit Schwarz (RGB = 0, 0, 0) füllen.
        screen.fill((0, 0, 0))
        player.rock_force(rocks)
        player.move()
        player.update_bullets(screen)
        player.render(screen)
        for rock in rocks:
            rock.render(screen)


        # Alle aufgelaufenen Events holen und abarbeiten. am anfang oder ende der schleife?
        for event in pygame.event.get():

            # Spiel beenden, wenn wir ein QUIT-Event finden.
            if event.type == pygame.QUIT:
                running = False

            # Wir interessieren uns auch für "Taste gedrückt"-Events.

            if event.type == pygame.KEYDOWN:

                # Wenn Escape gedrückt wird, posten wir ein QUIT-Event in Pygames Event-Warteschlange.

                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    player.speed_up()
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    player.speed_down()
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.rotate_left()
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.rotate_right()
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    player.shoot()


        # Inhalt von screen anzeigen.
        pygame.display.flip()


# Überprüfen, ob dieses Modul als Programm läuft und nicht in einem anderen Modul importiert wird.

if __name__ == '__main__':
    # Unsere Main-Funktion aufrufen.

    main()