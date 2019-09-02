from abc import ABC, abstractmethod
import pygame
import sys
import os
import random
from Tile import Tile
from stopwatch import stopwatch

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
red = (255, 0, 0)


class GraphicState(ABC):
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Puzzle_Game")
        self.state_changed = False
        self.error_message = False
        self.time = 0

    def get_state(self):
        return self.state_changed

    def set_state(self, state):
        self.state_changed = state

    def draw(self):
        pass

    def get_next_state(self):
        pass

    def get_activities(self, event):
        pass


class FinalScreen(GraphicState):

    def __init__(self):

        super().__init__()
        # self.image = pygame.image.load("img/elephant.jpg")
        self.font = pygame.font.Font("Risorse/AlexandriaFLF.ttf", 32)

        self.text = self.font.render('Congratulazioni! Hai vinto!', True, green, blue)

        self.textRect = self.text.get_rect()

        # set the center of the rectangular object.
        self.textRect.center = (1000 // 2, 600 // 2)

    def draw(self):
        # display.blit(self.image, (0, 0))
        self.display.blit(self.text, self.textRect)

        pygame.display.flip()
        pygame.display.update()

    def get_activities(self, event):

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state_changed = True

    def get_next_state(self):
        return Menu()


class Menu(GraphicState):

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load("Risorse/mondrian2.jpg")
        font = pygame.font.Font("Risorse/AlexandriaFLF.ttf", 32)
        self.text = font.render('Premere invio per iniziare', True, green, blue)

        self.textRect = self.text.get_rect()

        # set the center of the rectangular object.
        self.textRect.center = (1000 // 2, 600 // 2)

    def draw(self):

        self.display.blit(self.image, (0, 0))
        self.display.blit(self.text, self.textRect)

        pygame.display.flip()
        pygame.display.update()

    def get_next_state(self):
        return Game()

    def get_activities(self, event):

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.set_state(True)


class Game(GraphicState):
    def __init__(self):

        super().__init__()
        self.FOLDER_PATH = "img"
        self.IMAGE_SIZE = (800, 600)
        self.TILE_WIDTH = 200
        self.TILE_HEIGHT = 200
        self.COLUMNS = 4
        self.ROWS = 3

        # randomized selected image
        files = os.listdir(self.FOLDER_PATH)
        index = random.randrange(0, len(files))
        self.IMAGE_FILE = files[index]

        self.image = pygame.image.load(self.FOLDER_PATH + "/" + self.IMAGE_FILE)
        self.sprite = pygame.transform.scale(self.image, (200, 150))

        font = pygame.font.Font("Risorse/AlexandriaFLF.ttf", 32)
        self.text = font.render('Ops! Posizione sbagliata!', True, red, blue)

        self.textRect = self.text.get_rect()

        # set the center of the rectangular object.
        self.textRect.center = (1000 // 2, 600 // 2)

        self.tiles = []

        for c in range(self.ROWS):
            for r in range(self.COLUMNS):
                sprite = self.image.subsurface(r * self.TILE_WIDTH, c * self.TILE_HEIGHT, self.TILE_WIDTH,
                                               self.TILE_HEIGHT)
                self.tiles.append(Tile(sprite))
                self.tiles[c * self.COLUMNS + r].set_right_pos(r * self.TILE_WIDTH, c * self.TILE_HEIGHT)

        self.x = 0
        self.y = 0

        random.shuffle(self.tiles)

        self.i = len(self.tiles) - 1

        self.time = stopwatch.Stopwatch()

    def get_activities(self, event):

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_a:
                if self.x > 0:
                    self.x = self.x - self.TILE_WIDTH

            if event.key == pygame.K_s:
                if self.y + self.TILE_HEIGHT < self.IMAGE_SIZE[1]:
                    self.y = self.y + self.TILE_HEIGHT

            if event.key == pygame.K_d:
                if self.x + self.TILE_WIDTH < self.IMAGE_SIZE[0]:
                    self.x = self.x + self.TILE_WIDTH

            if event.key == pygame.K_w:
                if self.y > 0:
                    self.y = self.y - self.TILE_HEIGHT

            if event.key == pygame.K_RETURN:

                if self.i == 0:
                    self.state_changed = True

                if self.tiles[self.i].get_pos_x() != self.x or self.tiles[self.i].get_pos_y() != self.y:
                    self.time.reset()
                    self.time.start()
                    self.error_message = True
                else:
                    self.i = self.i - 1
                    self.x = 0
                    self.y = 0

    def draw(self):
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, self.IMAGE_SIZE[0], self.IMAGE_SIZE[1]))
        self.display.blit(self.sprite, (800, 225))

        for k in range(self.i + 1, len(self.tiles)):
            self.display.blit(self.tiles[k].get_sprite(), (self.tiles[k].get_pos_x(), self.tiles[k].get_pos_y()))

        pygame.draw.line(self.display, white, (800, 0), (800, 600))
        self.display.blit(self.tiles[self.i].get_sprite(), (self.x, self.y))

        if self.error_message:
            self.display.blit(self.text, self.textRect)

        if self.time.duration > 1.0:
            self.error_message = False

        pygame.display.flip()
        pygame.display.update()

    def get_next_state(self):
        return FinalScreen()
