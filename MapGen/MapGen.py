import pygame
import random


class MAP:
    BLOCK_SIZE = 80
    SIZE_Y = 30
    SIZE_X = 30
    RIVER_CHANCE = 200
    RIVER_LENGTH = 15
    RIVER_MIN = 5
    TILE_INFO = [ # INFORMATION ON TILES (SPAWN WEIGHT, FILE NAME)
        [20,"temp_grass.jpg"],
        [5,"temp_mountain.jpg"]
    ]
    RIVER_TILE = [ # Information on river tiles (filename)
        ["START.jpg"],  # Start river tile
        ["END.jpg"],  # End river tile
        ["VERTICAL.jpg"],  #
        ["HORIZONTAL.jpg"],
        ["BEND_LEFT.jpg"],
        ["BEND_RIGHT.jpg"],
        ["LEFT_DOWN.jpg"],
        ["RIGHT_DOWN.jpg"],
        ["END_LEFT.jpg"],
        ["END_RIGHT.jpg"]
    ]


class MapClass:
    """Fully extendible mapclass, image size and spawn weights can be edited"""
    Map = [[0 for x in range(0,MAP.SIZE_X)]for y in range(0,MAP.SIZE_X)]  # generates a 2d array for Map size
    img = pygame.Surface((MAP.SIZE_X,MAP.SIZE_Y))

    def __init__(self, seed=0):  # Initilizes Map class with a seed
        if not (seed == 0):
            random.seed(seed)
        total_weight=0
        for i in MAP.TILE_INFO:
            total_weight += i[0]
        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                rand = random.randint(0, total_weight)
                ndone = True
                for i in range(0,len(MAP.TILE_INFO)):  # Turns random number into Map tile
                    rand -= MAP.TILE_INFO[i][0]
                    if rand <= 0 and ndone:
                        ndone = False
                        self.Map[x][y] = i
        self.__render__()

    def __render__(self):
        ret = pygame.Surface((MAP.SIZE_X*MAP.BLOCK_SIZE,MAP.SIZE_Y*MAP.BLOCK_SIZE))
        for y in range(0,MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                temp_img = pygame.image.load(MAP.TILE_INFO[self.Map[x][y]][1]).convert()
                ret.blit(temp_img,(x*MAP.BLOCK_SIZE,y*MAP.BLOCK_SIZE))
        self.img = ret

    def create_river(self):
        surf = self.img
        for y in range(0, MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                number = random.randint(0, MAP.RIVER_CHANCE)
                if number == 42:  # If tile number is 42
                    placeX = x
                    placeY = y
                    end = 0
                    river_length = random.randint(MAP.RIVER_MIN, MAP.RIVER_LENGTH)
                    temp_riv = pygame.image.load(MAP.RIVER_TILE[0][0]).convert()  # Load river start image
                    surf.blit(temp_riv, (x * MAP.BLOCK_SIZE, y * MAP.BLOCK_SIZE))
                    placeY += 1
                    ran_tile = random.randint(4, 5)

                    for i in range(0, river_length):
                        end += 1
                        temp_riv = pygame.image.load(MAP.RIVER_TILE[ran_tile][0]).convert()
                        if ran_tile == 4:  # Blit tile left one block
                            surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                            placeX -= 1
                            ran_tile = random.randint(4, 7)
                            if end == river_length:
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[8][0]).convert()
                                surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                            elif ran_tile is not 6:
                                ran_tile = 6
                                ran_length = random.randint(1, 2)
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[3][0]).convert()
                                for i in range(0, ran_length):
                                    surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                                    placeX -= 1
                        elif ran_tile == 5:  # Blit tile right one block
                            surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                            placeX += 1
                            ran_tile = random.randint(4, 7)
                            if end == river_length:
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[9][0]).convert()
                                surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                            elif ran_tile is not 7:
                                ran_tile = 7
                                ran_length = random.randint(1, 2)
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[3][0]).convert()
                                for i in range(0, ran_length):
                                    surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                                    placeX += 1
                        elif ran_tile == 6:  # Blit tile right one block
                            surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                            placeY += 1
                            ran_tile = random.randint(4, 7)
                            if end == river_length:
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[1][0]).convert()
                                surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                            elif ran_tile is not 4 or 5:
                                ran_tile = random.randint(4, 5)
                                ran_length = random.randint(1, 2)
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[2][0]).convert()
                                for i in range(0, ran_length):
                                    surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                                    placeY += 1
                        elif ran_tile == 7:  # Blit tile down one block
                            surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                            placeY += 1
                            ran_tile = random.randint(4, 7)
                            if end == river_length:
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[1][0]).convert()
                                surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                            elif ran_tile is not 4 or 5:
                                ran_tile = random.randint(4, 5)
                                ran_length = random.randint(1, 2)
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[2][0]).convert()
                                for i in range(0, ran_length):
                                    surf.blit(temp_riv, (placeX * MAP.BLOCK_SIZE, placeY * MAP.BLOCK_SIZE))
                                    placeY += 1

        return surf


screen = pygame.display.set_mode((1600,1000))
Map= MapClass()
pygame.init()
Map.img = Map.create_river()
temp_scroll = [0,0]  # TEMP SCROLL MECHANIC


def display():
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done=True

            """TEMPORARY SCROLL MECHANIC"""
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if temp_scroll[0] > 0:
                        temp_scroll[0]-= 50

                if event.key == pygame.K_RIGHT:
                    if temp_scroll[0] < (MAP.SIZE_X*MAP.BLOCK_SIZE-1600):
                        temp_scroll[0] += 50

                if event.key == pygame.K_UP:
                    if temp_scroll[1] > 0:
                        temp_scroll[1]-= 50

                if event.key == pygame.K_DOWN:
                    if temp_scroll[1] < (MAP.SIZE_Y*MAP.BLOCK_SIZE-1000):
                        temp_scroll[1] += 50
            """END TEMP SCROLL MECHANIC"""
            
        screen.blit(Map.img,(-temp_scroll[0],-temp_scroll[1]))
        pygame.display.flip()
display()