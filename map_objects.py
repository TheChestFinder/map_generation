import pygame
from pnoise import Noise
from typing import Sequence, List, Generator, Tuple
from pickle import load, dumps
import constants
pygame.init()
font = pygame.font.SysFont("Arial", 15)
n = Noise()
n.seed(123)

def save_map(map: List[List['Tile']], filepath: str) -> None:
    file = open(filepath, "wb")
    binary_data = dumps(map)
    file.write(binary_data)
    file.close()

def load_map(filepath: str) -> List[List['Tile']]:
    file = open(filepath, "rb")
    return load(file)


class Tile:
    def __init__(self, biome: int, noise: float) -> None:
        self.biome: int = biome
        self.noise: float = noise

Map_Type = List[List[Tile]]


class Map:
    def __init__(self) -> None:
        self.map_img = pygame.Surface((constants.MAP_HEIGHT, constants.MAP_WIDTH))
        
        #self.map = self.generate_map()
        #save_map(self.map, "./map.bin")
        
        #self.map = load_map("./map.bin")
        
        self.tile_imgs = self.load_tile_images()
        #self.draw_map()
        self.offset_px = pygame.Vector2(0, 0)
        self.offset_tiles = pygame.Vector2(0, 0)
        self.map_pos = pygame.Vector2(0, 0)
        self.is_loaded = False
        
    def load_tile_images(self):
        tile_imgs = []
        for i in range(0, 6):
            filename = "./assets/tile-" + str(i) + ".png"
            img = pygame.image.load(filename)
            tile_imgs.append(img)
        return tile_imgs
        
    def handle_pressed(self, pressed: Sequence[bool]):
        u_d_step = pygame.Vector2(0, 5)
        r_l_step = pygame.Vector2(5, 0)
        #print(self.offset_px, self.offset_tiles)
        
        step = pygame.Vector2(0, 0)
        
        if pressed[pygame.K_w] or pressed[pygame.K_UP]:
            step += +u_d_step       
        if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
            step += -u_d_step
            
        if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
            step += +r_l_step
        if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
            step += -r_l_step
          
        next_offset = self.offset_px + step  
          
            
        if next_offset.x > 0:
            self.offset_px.x = -(self.map_img.get_width() - constants.WINDOW_WIDTH) / 2
            self.offset_tiles.x += int(self.offset_px.x / 32)
            self.draw_map()
            return
        
        if next_offset.y > 0:
            self.offset_px.y = -(self.map_img.get_width() - constants.WINDOW_WIDTH) / 2
            self.offset_tiles.y += int(self.offset_px.y / 32)
            self.draw_map()
            return
        
        if next_offset.x < constants.WINDOW_WIDTH - constants.MAP_WIDTH:
            offset_px_x = self.offset_px.x
            tiles_diff = int(offset_px_x / 64)
            #next_offset_tiles_x = self.offset_tiles.x - tiles_diff 
            #if next_offset_tiles_x > constants.MAP_TILES_WIDTH - constants.MAP_WIDTH // 32:
            #    tiles_diff = constants.MAP_TILES_WIDTH - self.offset_tiles.x - constants.MAP_WIDTH // 32
                
                
            self.offset_tiles.x += round(offset_px_x / 64) * -1
            self.offset_px.x = offset_px_x - int(offset_px_x / 2)
            self.draw_map()
            return      
        
        if next_offset.y < constants.WINDOW_HEIGHT - constants.MAP_HEIGHT:
            offset_px_y = self.offset_px.y
            self.offset_tiles.y += round(offset_px_y / 64) * -1
            self.offset_px.y = offset_px_y - int(offset_px_y / 2)
            self.draw_map()
            return   
               
            
        self.offset_px = next_offset

      
    def choose_biome(self, noise: float) -> int:
        intervals = (0, 0.3, 0.4, 0.5, 0.6, 0.7, 1)
        for i in range(len(intervals) -1):
            if noise >= intervals[i] and noise < intervals[i +1]:
                return i
          
      
    def generate_map(self) -> Generator[Map_Type, None, Tuple[int, int]]:
        result = []
        width, height = constants.MAP_TILES_WIDTH, constants.MAP_TILES_HEIGHT
        tpf = 1500
        tile_counter = 0
        total_tiles = width * height
        for i in range(height):
            row = []
            for j in range(width):
                scale = 0.075
                noise = n.perlin(j * scale, i * scale, 500)
                biome = self.choose_biome(noise)
                tile = Tile(biome, noise)
                row.append(tile)
                tile_counter += 1
                if tile_counter % tpf == 0:
                    yield tile_counter, total_tiles
            result.append(row)
        self.map = result
        
    def draw_map(self):
        tiles_i = int(constants.MAP_HEIGHT / 32 + 1)
        tiles_j = int(constants.MAP_WIDTH / 32 + 1)
        for i in range(tiles_i):
            for j in range(tiles_j):
                di, dj = int(self.offset_tiles.y), int( self.offset_tiles.x)
                tile = self.map[i + di][j + dj]
                tile_img: pygame.Surface = self.tile_imgs[tile.biome]
                noise_img = font.render(str(round(tile.noise, 2)), True, (0, 0, 0))
                self.map_img.blit(tile_img, (j* 32, i * 32))
                #self.map_img.blit(noise_img, (j* 32, i * 32))
                             
        
    def draw_checkerboard(self):
        for i in range(400):
            for j in range(400):
                color = (175, 175, 175) if (i + j) % 2 == 0 else (100, 100, 100)
                rect = pygame.Rect((i * 50, j * 50), (50, 50))
                pygame.draw.rect(self.map_img, color, rect)


    def get_minimap(self) -> pygame.Surface:
        surface = pygame.Surface((150, 150))
        surface.set_alpha(200)
        rect = pygame.Rect((0, 0), (10, 10))
        pygame.draw.rect(surface, (255, 0, 0), rect, 1)
        return surface