import pygame
import random


class MAP:
    BLOCK_SIZE = 80
    SIZE_Y = 30
    SIZE_X = 30
    RIVER_CHANCE = 10  # Higher number means less chance of a river spawning
    RIVER_LENGTH = 15  # Higher number means longer rivers
    RIVER_MIN = 5  # Minimum length of river
    TILE_INFO = [  # INFORMATION ON TILES (SPAWN WEIGHT, FILE NAME)
        [20, "temp_grass.jpg"],
        [5, "temp_mountain.jpg"]
    ]
    RIVER_TILE = [  # Information on river tiles (filename)
        ["START.jpg"],  # Start river tile
        ["END.jpg"],  # End river tile
        ["VERTICAL.jpg"],
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
    Map = [[0 for x in range(0,MAP.SIZE_X)]for y in range(0,MAP.SIZE_X)]  # Generates a 2d array for Map size
    River = [[False for x in range(0,MAP.SIZE_X+2)]for y in range(0,MAP.SIZE_X+2)]  # Generates a 2d array for rivers
    img = pygame.Surface((MAP.SIZE_X,MAP.SIZE_Y))

    def __init__(self, seed=0):
        """Initilizes Map class with a seed"""
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
        """Turns the map array into images"""
        ret = pygame.Surface((MAP.SIZE_X*MAP.BLOCK_SIZE,MAP.SIZE_Y*MAP.BLOCK_SIZE))
        for y in range(0,MAP.SIZE_Y):
            for x in range(0, MAP.SIZE_X):
                temp_img = pygame.image.load(MAP.TILE_INFO[self.Map[x][y]][1]).convert()
                ret.blit(temp_img,(x*MAP.BLOCK_SIZE,y*MAP.BLOCK_SIZE))
        self.img = ret

    def create_river2(self):
        """Checks each on x,1 and 1,y to see if a river starts, 1 is used as the array has a boarder"""
        for y in range(1,MAP.SIZE_Y+1):  # Spawns river starts on the y axis
            number = random.randint(0, MAP.RIVER_CHANCE)  # Generate random number to see if river spawns
            if number == 0:  # If number is 0 change array position to True and run river_flow_y
                self.River[1][y] = True
                MapClass.river_flow_y(self,y)
        for x in range(1, MAP.SIZE_X+1):  # spawns river starts on the x axis
            number = random.randint(0,MAP.RIVER_CHANCE)
            if number == 0:  # If number is 0 change array position to True and run river_flow_x
                self.River[x][1] = True
                MapClass.river_flow_x(self,x)



    def river_flow_y(self,y):
        """Loops placing True in the array until hitting the edge of array,
        randomly picks the direction starting on y axis"""
        x = 1
        while not x >= MAP.SIZE_X and not x < 1 and not y >= MAP.SIZE_Y and not y < 1:
            # While not past the array boundary's
            which_tile = random.randint(0,3)  # Random int used to pick which direction
            if which_tile == 0:
                y -= 1
                self.River[x][y] = True  # up
            if which_tile == 1:
                y += 1
                self.River[x][y] = True  # down
            if which_tile >= 2:
                x += 1
                self.River[x][y] = True  # right

    def river_flow_x(self,x):
        """Loops placing True in the array until hitting the edge of array,
        randomly picks the direction starting on x axis"""
        y = 1
        while not y >= MAP.SIZE_Y and not y < 1 and not x >= MAP.SIZE_X and not x < 1:
            # While not past the array boundary's
            which_tile = random.randint(0,3)  # Random int used to pick which direction
            if which_tile == 0:
                x -= 1
                self.River[x][y] = True  # left
            if which_tile == 1:
                x += 1
                self.River[x][y] = True  # right
            if which_tile >= 2:
                y += 1
                self.River[x][y] = True  # down


    def create_river(self):

        surf = self.img
        for y in range(0, MAP.SIZE_Y):  # For each tile block
            for x in range(0, MAP.SIZE_X):
                number = random.randint(0, MAP.RIVER_CHANCE)
                if number == 42:  # If random tile number is 42
                    placex = x  # Variable used to move where blitting while keeping place
                    placey = y  # Variable used to move where blitting while keeping place
                    end = 0  # Used to place the end tile
                    river_length = random.randint(MAP.RIVER_MIN, MAP.RIVER_LENGTH)
                    temp_riv = pygame.image.load(MAP.RIVER_TILE[0][0]).convert()  # Load river start image
                    surf.blit(temp_riv, (x * MAP.BLOCK_SIZE, y * MAP.BLOCK_SIZE))
                    placey += 1  # Move down one tile
                    ran_tile = random.randint(4, 5)  # Get random number for either left or right tile

                    for i in range(0, river_length):  # Loops until river length is met
                        end += 1
                        temp_riv = pygame.image.load(MAP.RIVER_TILE[ran_tile][0]).convert()

                        if ran_tile == 4:  # If tile is BEND_LEFT
                            surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))
                            placex -= 1  # Move left one tile
                            ran_tile = random.randint(4, 7) # Gets random bend tile

                            if end == river_length:  # Places end part of river relative to the direction
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[8][0]).convert()
                                surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))

                            elif ran_tile is not 6:  # If not bend down make it LEFT_DOWN
                                ran_tile = 6
                                ran_length = random.randint(1, 2)
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[3][0]).convert()
                                for i in range(0, ran_length):  # Blit horizontal tiles to the amount of ran_length
                                    surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))
                                    placex -= 1  # Move left one tile

                        elif ran_tile == 5:  # If tile is BEND_RIGHT
                            surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))
                            placex += 1  # Move right one tile
                            ran_tile = random.randint(4, 7)  # Get random bend tile

                            if end == river_length:  # Places end part of river relative to the direction
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[9][0]).convert()
                                surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))

                            elif ran_tile is not 7:  # If not bend down make it RIGHT_DOWN
                                ran_tile = 7
                                ran_length = random.randint(1, 2)
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[3][0]).convert()
                                for i in range(0, ran_length):  # Blit horizontal tiles to the amount of ran_length
                                    surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))
                                    placex += 1  # Move right one tile

                        elif ran_tile == 6:  # If tile is LEFT_DOWN
                            surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))
                            placey += 1  # Move down one tile
                            ran_tile = random.randint(4, 7)  # Get random bend tile

                            if end == river_length:  # Places end part of river relative to the direction
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[1][0]).convert()
                                surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))

                            elif ran_tile is not 4 or 5:  # If not BEND_LEFT or BEND_RIGHT
                                ran_tile = random.randint(4, 5)  # ran_tile is either BEND_LEFT or BEND_RIGHT
                                ran_length = random.randint(1, 2)
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[2][0]).convert()
                                for i in range(0, ran_length):  # Blit vertical tiles to the amount of ran_length
                                    surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))
                                    placey += 1  # Move down one tile

                        elif ran_tile == 7:  # If tile is RIGHT_DOWN
                            surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))
                            placey += 1  # Move down one tile
                            ran_tile = random.randint(4, 7)  # Get random bend tile

                            if end == river_length:  # Places end part of river relative to the direction
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[1][0]).convert()
                                surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))

                            elif ran_tile is not 4 or 5:  # If not BEND_LEFT or BEND_RIGHT
                                ran_tile = random.randint(4, 5)
                                ran_length = random.randint(1, 2)
                                temp_riv = pygame.image.load(MAP.RIVER_TILE[2][0]).convert()
                                for i in range(0, ran_length):  # Blit vertical tiles to the amount of ran_length
                                    surf.blit(temp_riv, (placex * MAP.BLOCK_SIZE, placey * MAP.BLOCK_SIZE))
                                    placey += 1  # Move down one tile

        return surf


screen = pygame.display.set_mode((1600,1000))
Map= MapClass()
pygame.init()
Map.img = Map.create_river()
Map.create_river2()
print MapClass.River

def SCREEN():
    done=False
    while not done:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                done=True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done=True
        screen.blit(Map.img,(0,0))
        pygame.display.flip()
SCREEN()