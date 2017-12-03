#!env python

import math, random, sys
from PIL import Image, ImageDraw

# TODO : Split file and clean later on

# Constants : FIXME check if these should really be constants
WHITE = (255, 255, 255)
POPSIZE = 100 #FIXME
DNASIZE = 500 #FIXME
MUTRATE = 10

class Gene:
    def __init__(self, from_pos, to_pos, color):
        # FIXME add asserts on the params?
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.color = color

    def draw(self, surface):
        surface.line([self.from_pos, self.to_pos], fill=self.color, width=1)

class Individual:
    def __init__(self, winsize):
        self.winsize = winsize
        self.dna = []
        self.image = None

    def addGene(self, from_pos, to_pos, color):
        gene = Gene(from_pos, to_pos, color)
        self.dna.append(gene)

    def getImage(self):
        if self.image is not None:
            return
        self.image = Image.new("RGB", self.winsize, WHITE)
        surface = ImageDraw.Draw(self.image)
        for gene in self.dna:
            gene.draw(surface)
        return self.image

    def getScore(self, image):
        if self.image is None:
            self.getImage()

        score = 0
        for x in range(self.winsize[0]):
            for y in range(self.winsize[1]):
                r1, g1, b1 = image.getpixel((x, y))
                r2, g2, b2 = self.image.getpixel((x, y))
                r = 1 - (math.fabs(r1 - r2) / 255)
                g = 1 - (math.fabs(g1 - g2) / 255)
                b = 1 - (math.fabs(b1 - b2) / 255)
                score += (r + g + b) / 3

        score = score / (self.winsize[0] * self.winsize[1])
        score *= 100

        return score

    def mutate(self):
        for i in range(DNASIZE):
            if random.randint(0, 100) < MUTRATE:
                    from_pos = (random.randint(0, self.winsize[0] - 1),
                                random.randint(0, self.winsize[1] - 1))
                    to_pos = (random.randint(0, self.winsize[0] - 1),
                              random.randint(0, self.winsize[1] - 1))
                    color = (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255))
                    self.dna[i] = Gene(from_pos, to_pos, color)

    def cross(self, ind):
        ret = Individual(self.winsize)
        for i in range(DNASIZE):
            gene = self.dna[i] if random.randint(0, 1) == 0 \
                               else ind.dna[i]
            ret.dna.append(gene)
        return ret

    def save(self):
        if self.image is None:
            self.getImage()

        self.image.save("out.png")

class Population:
    def __init__(self, winsize, previous=None):
        self.winsize = winsize
        self.average = 0
        self.pop = []
        if previous is None:
            for i in range(POPSIZE):
                ind = Individual(self.winsize)
                for j in range(DNASIZE):
                    from_pos = (random.randint(0, self.winsize[0] - 1),
                                random.randint(0, self.winsize[1] - 1))
                    to_pos = (random.randint(0, self.winsize[0] - 1),
                              random.randint(0, self.winsize[1] - 1))
                    color = (random.randint(0, 255),
                             random.randint(0, 255),
                             random.randint(0, 255))
                    ind.addGene(from_pos, to_pos, color)
                self.pop.append({"individual": ind})
        else:
            for i in range(POPSIZE / 2):
                for _ in range(2):
                    #FIXME except i itself?
                    self.pop.append({"individual":
                        previous.getPop()[i]["individual"].cross(previous.getPop()[random.randint(0, POPSIZE/2)]["individual"])})

        for i in self.pop:
            i["individual"].mutate()

    def computeScores(self, image):
        self.average = 0
        for i in self.pop:
            ind = i["individual"]
            score = ind.getScore(image)
            i["score"] = score
            self.average += score
        self.average /= POPSIZE

    def sort(self, image=None):
        if image is not None:
            self.computeScores(image)
        self.pop = sorted(self.pop, key=lambda k: k["score"], reverse=True)

    def getPop(self):
        return self.pop

    def getAverage(self):
        return self.average

class World:
    def __init__(self, path):
        random.seed()
        self.running = True
        self.image = Image.open(path)
        self.image = self.image.convert("RGB")
        self.winsize = self.image.size

    def live(self):
        pop = Population(self.winsize)
        while self.running:
            pop.sort(self.image)
            print pop.getAverage()
            pop = Population(self.winsize, previous=pop)
            pop.getPop()[0]["individual"].save()

if __name__ == '__main__':
    assert (len(sys.argv) == 2) #FIXME maybe add a message
    world = World(sys.argv[1])
    world.live()
