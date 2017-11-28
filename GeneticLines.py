#!env python

import pygame, random
from pygame.locals import *

# TODO : Split file and clean later on

# Constants : FIXME check if these should really be constants
WINSIZE = [640, 480]
WHITE = [255, 255, 255]
POPSIZE = 100 #FIXME
DNASIZE = 100 #FIXME

class Gene:
    def __init__(self, from_pos, to_pos, color):
        # FIXME add asserts on the params?
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.color = color

    def draw(self, surface):
        pygame.draw.line(surface, self.color, self.from_pos, self.to_pos)

class DNA:
    def __init__(self):
        self.dna = []

    def addGene(self, from_pos, to_pos, color):
        gene = Gene(from_pos, to_pos, color)
        self.dna.append(gene)

    def draw(self, surface):
        for gene in self.dna:
            gene.draw(surface)

class Population:
    def __init__(self, previous=None):
        self.pop = []
        if previous is None:
            for i in range(POPSIZE):
                dna = DNA()
                for j in range(DNASIZE):
                    from_pos = (random.randint(0, WINSIZE[0] - 1),
                                random.randint(0, WINSIZE[1] - 1))
                    to_pos = (random.randint(0, WINSIZE[0] - 1),
                              random.randint(0, WINSIZE[1] - 1))
                    color = (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255))
                    dna.addGene(from_pos, to_pos, color)
                self.pop.append(dna)

    def getBest(self):
        return self.pop[0] #FIXME obviously not

    def drawBest(self, surface):
        self.getBest().draw(surface)

class World:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('GeneticLines')

        random.seed()

        self.screen = pygame.display.set_mode(WINSIZE)
        self.running = True

    def live(self):
        while self.running:
            self.screen.fill(WHITE)
            pop = Population()
            pop.drawBest(self.screen)
            pygame.display.update()
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.running = False
                    break

if __name__ == '__main__':
    world = World()
    world.live()
