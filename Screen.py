from abc import ABC, abstractmethod
import pygame
import sys
import os
import random
from Tile import Tile

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

class GraphicState(ABC):
    def __init__(self):
        self.state_changed = False

    def get_state(self):
        return self.state_changed

    def set_state(self,state):
        self.state_changed = state

    def draw(self):
        pass

    def get_next_state(self):
        pass

    def get_activities(self,event):
        pass
    
class FinalScreen(GraphicState):

    def __init__(self, state):
        pygame.init()

        super().__init__()
        #self.image = pygame.image.load("img/elephant.jpg")
        self.font = pygame.font.Font("Risorse/AlexandriaFLF.ttf", 32)

        if state:
            self.text = self.font.render('Congratulazioni! Hai vinto!', True, green, blue)
        else:
            self.text = self.font.render('Peccato! Andrà meglio la prossima volta!', True, green, blue)

        self.textRect = self.text.get_rect()

        # set the center of the rectangular object.
        self.textRect.center = (800 // 2, 600 // 2)

    def draw(self):
        display = pygame.display.set_mode((800, 600))
        #display.blit(self.image, (0, 0))
        display.blit(self.text, self.textRect)

        pygame.display.set_caption("Puzzle_Game")
        pygame.display.flip()
        pygame.display.update()

    def get_activities(self,event):
        display = pygame.display.set_mode((800, 600))

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
        pygame.init()

        super().__init__()
        self.image = pygame.image.load("Risorse/mondrian.jpg")
        self.font = pygame.font.Font("Risorse/AlexandriaFLF.ttf", 32)
        self.text = self.font.render('Premere invio per iniziare', True, green, blue)

        self.textRect = self.text.get_rect()

        # set the center of the rectangular object.
        self.textRect.center = (800 // 2, 600 // 2)

    def draw(self):
        display = pygame.display.set_mode((800, 600))
        display.blit(self.image, (0, 0))
        display.blit(self.text, self.textRect)

        pygame.display.set_caption("Puzzle_Game")
        pygame.display.flip()
        pygame.display.update()

    def get_next_state(self):
        return Game()

    def get_activities(self, event):

        if event.type == pygame.QUIT:
            print("chiudi")
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("invio")
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

        image = pygame.image.load(self.FOLDER_PATH + "/" + self.IMAGE_FILE)
        self.tiles = []

        for c in range(self.ROWS):
            for r in range(self.COLUMNS):
                sprite = image.subsurface(r * self.TILE_WIDTH, c * self.TILE_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)
                self.tiles.append(Tile(sprite))
                self.tiles[c * self.COLUMNS + r].set_right_pos(r * self.TILE_WIDTH, c * self.TILE_HEIGHT)
                print(c, " ", r, " ", c * self.COLUMNS + r)
                print(self.tiles[c * self.COLUMNS + r].get_pos_x(), " ", self.tiles[c * self.COLUMNS + r].get_pos_y())

        # start game

        # display.blit(tiles[(0,0)], (0,0))
        # pygame.display.flip()

        self.x = 0
        self.y = 0

        random.shuffle(self.tiles)

        self.i = len(self.tiles) - 1

        self.is_the_right_pos = True

    def get_activities(self, event):
        display = pygame.display.set_mode((800, 600))

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            pygame.draw.rect(display, (0, 0, 0), (0, 0, self.IMAGE_SIZE[0], self.IMAGE_SIZE[1]))
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

            print(self.tiles[self.i].get_pos_x(), " ", self.x, " ", self.tiles[self.i].get_pos_y(), " ", self.y)

            if event.key == pygame.K_RETURN:

                if self.tiles[self.i].get_pos_x() != self.x or self.tiles[self.i].get_pos_y() != self.y:
                    self.is_the_right_pos = False
                    self.state_changed = True

                if self.i == 0:
                    self.state_changed = True

                print(self.i)

                self.i = self.i - 1
                self.x = 0
                self.y = 0

    def draw(self):
        display = pygame.display.set_mode((800, 600))

        for k in range(self.i + 1, len(self.tiles)):
            display.blit(self.tiles[k].get_sprite(), (self.tiles[k].get_pos_x(), self.tiles[k].get_pos_y()))

        display.blit(self.tiles[self.i].get_sprite(), (self.x, self.y))

        pygame.display.flip()
        pygame.display.update()

    def get_next_state(self):
        return FinalScreen(self.is_the_right_pos)
