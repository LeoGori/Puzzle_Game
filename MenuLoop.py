import pygame
import sys
import random
import os
from Screen import Menu

class MenuLoop:

    def __init__(self):
        self.screen = Menu()

    def generate_screen(self):

        pygame.init()

        display = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Puzzle")
        
        while True:
            pygame.draw.rect(display, (0, 0, 0), (0, 0, 800, 600))

            pygame.time.delay(100)            

            event = pygame.event.wait()

            self.screen.get_activities(event)
            
            if self.screen.get_state():
                self.screen = self.screen.get_next_state()

            self.screen.draw()



def main():

    ml = MenuLoop()

    ml.generate_screen()

if __name__ == "__main__":
        main()