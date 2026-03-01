import pygame
import math
import random
import time
from queue import PriorityQueue
import sys

# ==========================================
# 1. GLOBAL SETTINGS & COLOR DEFINITIONS
# ==========================================
pygame.init()
pygame.font.init()

BASE_WIDTH = 800
UI_OFFSET = 180 

FONT = pygame.font.SysFont('Arial', 16)
BOLD_FONT = pygame.font.SysFont('Arial', 16, bold=True)
TITLE_FONT = pygame.font.SysFont('Arial', 18, bold=True)

WHITE = (255, 255, 255)      
BLACK = (0, 0, 0)            
ORANGE = (255, 140, 0)       
TURQUOISE = (64, 224, 208)   
YELLOW = (255, 215, 0)       
RED = (220, 20, 60)          
GREEN = (50, 205, 50)        
GREY = (200, 200, 200)       
DARK_BG = (30, 30, 30)       

# ==========================================
# 2. GRID NODE CLASS
# ==========================================
class Spot:
    def __init__(self, row, col, gap, total_rows):
        self.row = row
        self.col = col
        self.width = gap 
        self.x = col * self.width
        self.y = (row * self.width) + UI_OFFSET 
        self.color = WHITE
        self.neighbors = []
        self.total_rows = total_rows

    def get_pos(self): return self.row, self.col
    def is_barrier(self): return self.color == BLACK
    def is_closed(self): return self.color == RED
    def is_open(self): return self.color == YELLOW

    def reset(self): self.color = WHITE
    def make_start(self): self.color = ORANGE
    def make_end(self): self.color = TURQUOISE
    def make_barrier(self): self.color = BLACK
    def make_open(self): self.color = YELLOW
    def make_closed(self): self.color = RED
    def make_path(self): self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
