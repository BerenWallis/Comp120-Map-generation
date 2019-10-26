import pygame
import random


class MAP:
    BLOCK_SIZE = 80
    SIZE_Y = 30
    SIZE_X = 30
    SEA_CHANCE = 20  # Higher number means less chance of a sea spawning
    TILE_INFO = [  # INFORMATION ON TILES (SPAWN WEIGHT, FILE NAME)
        [20, "temp_grass.jpg"],
        [5, "temp_mountain.jpg"]
    ]
    SEA_TILE = [  # Information on sea tiles (filename)
        ["1.jpg"],  # left connect only
        ["11.jpg"],  # up left connect
    ]


class MapClass:
    """Fully extendible mapclass, image size and spawn weights can be edited"""
    Map = [[0 for x in range(0, MAP.SIZE_X)]for y in range(0, MAP.SIZE_X)]  # Generates a 2d array for Map size
    Sea = [[False for x in range(0, MAP.SIZE_X+2)]for y in range(0, MAP.SIZE_X+2)]  # Generates a 2d array for seas
    img = pygame.Surface((MAP.SIZE_X, MAP.SIZE_Y))

    def __init__(self, seed=0):
        """Initilizes Map class with a seed"""
        if not (seed == 0):
            random.seed(seed)
        total_weight = 0
        for i in MAP.TILE_INFO:
            total_weight += i[0]
        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                rand = random.randint(0, total_weight)
                ndone = True
                for i in range(0, len(MAP.TILE_INFO)):  # Turns random number into Map tile
                    rand -= MAP.TILE_INFO[i][0]
                    if rand <= 0 and ndone:
                        ndone = False
                        self.Map[x][y] = i
        self.__render__()

    def __render__(self):
        """Turns the map array into images"""
        ret = pygame.Surface((MAP.SIZE_X*MAP.BLOCK_SIZE, MAP.SIZE_Y*MAP.BLOCK_SIZE))
        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                temp_img = pygame.image.load(MAP.TILE_INFO[self.Map[x][y]][1]).convert()
                ret.blit(temp_img, (x*MAP.BLOCK_SIZE, y*MAP.BLOCK_SIZE))
        self.img = ret

    def create_sea(self):
        """Checks each on x,1 and 1,y to see if a sea starts, 1 is used as the array has a boarder"""
        for y in range(1, MAP.SIZE_Y+1):  # Spawns sea starts on the y axis
            number = random.randint(0, MAP.SEA_CHANCE)  # Generate random number to see if sea spawns
            if number == 0:  # If number is 0 change array position to True and run sea_flow_y
                self.Sea[1][y] = True
                MapClass.sea_flow_y(self, y)
        for x in range(1, MAP.SIZE_X+1):  # Spawns sea starts on the x axis
            number = random.randint(0, MAP.SEA_CHANCE)
            if number == 0:  # If number is 0 change array position to True and run sea_flow_x
                self.Sea[x][1] = True
                MapClass.sea_flow_x(self, x)

    def sea_flow_y(self, y):
        """Loops placing True in the array until hitting the edge of array,
        randomly picks the direction starting on y axis"""
        x = 1
        while not x >= MAP.SIZE_X and not x < 1 and not y >= MAP.SIZE_Y and not y < 1:
            # While not past the array boundary's
            which_tile = random.randint(0, 3)  # Random int used to pick which direction
            if which_tile == 0:
                y -= 1
                self.Sea[x][y] = True  # up
            if which_tile == 1:
                y += 1
                self.Sea[x][y] = True  # down
            if which_tile >= 2:
                x += 1
                self.Sea[x][y] = True  # right

    def sea_flow_x(self, x):
        """Loops placing True in the array until hitting the edge of array,
        randomly picks the direction starting on x axis"""
        y = 1
        while not y >= MAP.SIZE_Y and not y < 1 and not x >= MAP.SIZE_X and not x < 1:
            # While not past the array boundary's
            which_tile = random.randint(0, 3)  # Random int used to pick which direction
            if which_tile == 0:
                x -= 1
                self.Sea[x][y] = True  # left
            if which_tile == 1:
                x += 1
                self.Sea[x][y] = True  # right
            if which_tile >= 2:
                y += 1
                self.Sea[x][y] = True  # down

    def sea_render(self):
        """Blits sea images depending on what other places adjacent are seas and sand to some of the edges"""
        surf = self.img
        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                adj = MapClass.sea_check(self, x, y)  # runs function to check whats next to current tile
                if adj == 1 or adj == 10 or adj == 100 or adj == 1000:  # If at the edge of the sea
                    temp_riv = pygame.image.load(MAP.SEA_TILE[0][0]).convert()  # Get sand
                    surf.blit(temp_riv, ((x * MAP.BLOCK_SIZE), (y * MAP.BLOCK_SIZE)))
                elif adj != 0 and adj != 1 and adj != 10 and adj != 100 and adj != 1000:  # If multiple sea connections
                    temp_riv = pygame.image.load(MAP.SEA_TILE[1][0]).convert()
                    surf.blit(temp_riv, ((x * MAP.BLOCK_SIZE), (y * MAP.BLOCK_SIZE)))

        return surf  # return edited image

    def sea_check(self, x, y):
        """Checks adjacent tiles for seas"""
        num_adj = 0  # Variable to return
        if self.Sea[x - 1][y]:  # check left
            num_adj += 1
        if self.Sea[x][y + 1]:  # check up
            num_adj += 10
        if self.Sea[x][y - 1]:  # check down
            num_adj += 100
        if self.Sea[x + 1][y]:  # check right
            num_adj += 1000
        return num_adj


screen = pygame.display.set_mode((1600, 1000))
Map = MapClass()
pygame.init()
Map.create_sea()
Map.img = Map.sea_render()


def main():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
        screen.blit(Map.img, (0, 0))
        pygame.display.flip()
main()
