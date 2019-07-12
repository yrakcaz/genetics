#!env python

import math, random, sys
from PIL import Image, ImageDraw

# TODO : Split file and clean later on

# Constants : FIXME check if these should really be constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
MAXSIZE = 50
POPSIZE = 30 #FIXME
DNASIZE = 400 #FIXME
MUTRATE = 1000

class Gene:
    def __init__(self, x, y, xlen, ylen):
        # FIXME add asserts on the params?
        self.x = x
        self.y = y
        self.xlen = xlen
        self.ylen = ylen

    def mutate(self, winsize):
        if random.randint(0, MUTRATE) == 0:
            self.x = random.randint(0, winsize[0] - 1)
        if random.randint(0, MUTRATE) == 0:
            self.y = random.randint(0, winsize[1] - 1)
        if random.randint(0, MUTRATE / 2) == 0:
            self.xlen = random.randint(0, MAXSIZE)
        if random.randint(0, MUTRATE / 2) == 0:
            self.ylen = random.randint(0, MAXSIZE)

    def draw(self, surface):
        from_pos = (self.x, self.y)
        to_pos = (self.x + self.xlen, self.y + self.ylen)
        surface.line([from_pos, to_pos], fill=BLACK, width=1)

class Individual:
    def __init__(self, winsize):
        self.winsize = winsize
        self.dna = []
        self.image = None

    def addGene(self, x, y, xlen, ylen):
        gene = Gene(x, y, xlen, ylen)
        self.dna.append(gene)

    def getImage(self):
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
                r = math.fabs(r1 - r2)
                g = math.fabs(g1 - g2)
                b = math.fabs(b1 - b2)
                score += (r + g + b)
        return score

    def mutate(self):
        # FIXME below isn't good
        for i in range(DNASIZE):
            self.dna[i].mutate(self.winsize)

    def cross(self, ind):
        ret = Individual(self.winsize)
        for i in range(DNASIZE):
            gene = self.dna[i] if random.randint(0, 1) == 0 \
                               else ind.dna[i]
            ret.addGene(gene.x, gene.y, gene.xlen, gene.ylen)
        return ret

    def save(self):
        # FIXME there's probably a problem with that, use pygame instead
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
                    (x, y) = (random.randint(0, self.winsize[0] - 1),
                              random.randint(0, self.winsize[1] - 1))
                    (xlen, ylen) = (random.randint(0, MAXSIZE), #FIXME add a const for the max size?
                                    random.randint(0, MAXSIZE))
                    ind.addGene(x, y, xlen, ylen)
                self.pop.append({"individual": ind})
        else:
            for i in range(POPSIZE):
                    self.pop.append({"individual":
                        self.goodEnoughIndividual(previous).cross(
                            self.goodEnoughIndividual(previous))})

    def mutate(self):
        for i in self.pop:
            i["individual"].mutate()

    def computeScores(self, image):
        self.average = 0
        for i in self.pop:
            ind = i["individual"]
            score = ind.getScore(image)
            i["score"] = score #FIXME score should be within the ind class?
            self.average += score
        self.average /= POPSIZE

    def sort(self, image=None):
        if image is not None:
            self.computeScores(image)
        self.pop = sorted(self.pop, key=lambda k: k["score"], reverse=True)

    def goodEnoughIndividual(self, pop):
        for i in pop.pop:
            if random.randint(0, 1) == 0:
                return i["individual"]
        return pop.pop[0]["individual"]

    def getPop(self):
        return self.pop

    def getAverage(self):
        return self.average

class World:
    def __init__(self, path):
        random.seed()
        self.running = True
        self.image = Image.open(path)
        self.image = self.image.convert('1')
        self.image = self.image.convert("RGB")
        self.winsize = self.image.size

    def live(self):
        pop = Population(self.winsize)
        while self.running:
            pop.sort(self.image)
            print pop.getAverage()
            pop.getPop()[0]["individual"].save()
            pop = Population(self.winsize, previous=pop)
            pop.mutate()

if __name__ == '__main__':
    assert (len(sys.argv) == 2) #FIXME maybe add a message
    world = World(sys.argv[1])
    world.live()
