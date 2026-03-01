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
# ==========================================
# 3. HEURISTICS & ALGORITHM LOGIC
# ==========================================
def h_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def h_euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def reconstruct_path(came_from, current, draw_func, expanded, current_time):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
        current.make_path() 
        draw_func(expanded, len(path), current_time) 
        pygame.time.delay(10) # FIX: Adds a fast zip-line animation for the final path
    path.reverse() 
    return path

def algorithm(draw_func, grid, start, end, mode, heuristic_type):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    nodes_expanded = 0 
    
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    
    f_score = {spot: float("inf") for row in grid for spot in row}
    h_func = h_manhattan if heuristic_type == "Manhattan" else h_euclidean
    f_score[start] = h_func(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}
    visited = set() 

    compute_time = 0.0 # FIX: Tracks ONLY math time, ignoring the visual drawing delay

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # START TIMER
        logic_start = time.perf_counter()

        current = open_set.get()[2]
        open_set_hash.remove(current)
        visited.add(current)

        if current == end:
            compute_time += (time.perf_counter() - logic_start) # STOP TIMER
            path = reconstruct_path(came_from, end, draw_func, nodes_expanded, compute_time * 1000)
            end.make_end()
            start.make_start()
            draw_func(nodes_expanded, len(path), compute_time * 1000) 
            return path, nodes_expanded, len(path), compute_time * 1000

        for neighbor in current.neighbors:
            h_val = h_func(neighbor.get_pos(), end.get_pos())
            
            if mode == "A*":
                temp_g_score = g_score[current] + 1
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + h_val  
                    
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        neighbor.make_open() 
                        nodes_expanded += 1

            elif mode == "GBFS":
                if neighbor not in visited and neighbor not in open_set_hash:
                    came_from[neighbor] = current
                    f_score[neighbor] = h_val  
                    
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
                    nodes_expanded += 1

        if current != start:
            current.make_closed() 

        # STOP TIMER (So drawing Pygame rectangles doesn't ruin your algorithm metrics)
        compute_time += (time.perf_counter() - logic_start)

        # UPDATE UI LIVE (Creates the real-time execution effect)
        draw_func(nodes_expanded, 0, compute_time * 1000)
        
    # If no path found
    draw_func(nodes_expanded, 0, compute_time * 1000)
    return None, nodes_expanded, 0, compute_time * 1000

# ==========================================
# 4. GUI, DRAWING, AND CONSOLE OUTPUT
# ==========================================
def make_grid(rows, gap):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def draw_grid_lines(win, rows, gap, true_size):
    for i in range(rows + 1):
        pygame.draw.line(win, GREY, (0, i * gap + UI_OFFSET), (true_size, i * gap + UI_OFFSET))
        pygame.draw.line(win, GREY, (i * gap, UI_OFFSET), (i * gap, true_size + UI_OFFSET))

def reset_search_visuals(grid):
    for row in grid:
        for spot in row:
            if spot.is_closed() or spot.is_open() or spot.color == GREEN:
                spot.reset()

def draw_ui(win, mode, heur, dynamic, expanded, cost, time_ms, rows, true_size):
    pygame.draw.rect(win, DARK_BG, (0, 0, true_size, UI_OFFSET))
    
    texts_left = [
        "--- USER TOGGLES & CONTROLS ---",
        f"[A / G] Active Algorithm: {mode}",
        f"[H] Active Heuristic: {heur}",
        f"[D] Dynamic Mode: {'ON' if dynamic else 'OFF'}",
        f"[+ / -] Grid Size: {rows}x{rows}",
        "[R] 30% Random Map | [C] Clear | [SPACE] Start"
    ]
    for i, text in enumerate(texts_left):
        font = TITLE_FONT if i == 0 else FONT
        render = font.render(text, True, WHITE)
        win.blit(render, (15, 10 + (i * 22)))

    texts_right = [
        "--- REAL-TIME METRICS ---",
        f"Nodes Expanded (Visited): {expanded}",
        f"Final Path Cost: {cost} steps",
        f"Live Compute Time: {time_ms:.3f} ms"
    ]
    
    right_x = min(350, true_size - 300) 
    for i, text in enumerate(texts_right):
        font = TITLE_FONT if i == 0 else BOLD_FONT
        render = font.render(text, True, GREEN)
        win.blit(render, (max(20, right_x), 10 + (i * 22)))

    legend = [
        ("Orange: Start", ORANGE), ("Turquoise: Goal", TURQUOISE), 
        ("Black: Wall", BLACK), ("Yellow: Frontier", YELLOW), 
        ("Red: Visited", RED), ("Green: Path", GREEN)
    ]
    
    x_offset = 15
    for text, color in legend:
        pygame.draw.rect(win, color, (x_offset, 150, 15, 15))
        render = FONT.render(text, True, WHITE)
        win.blit(render, (x_offset + 20, 148))
        x_offset += 120

def draw(win, grid, rows, gap, true_size, mode, heur, expanded, cost, time_ms, dynamic):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
            
    draw_grid_lines(win, rows, gap, true_size)
    pygame.draw.rect(win, BLACK, (0, UI_OFFSET, true_size, true_size), 4) 
    draw_ui(win, mode, heur, dynamic, expanded, cost, time_ms, rows, true_size)
    pygame.display.update()

def get_clicked_pos(pos, gap, true_size):
    y, x = pos
    if y < UI_OFFSET or y >= UI_OFFSET + true_size or x < 0 or x >= true_size: 
        return None, None
    row = (y - UI_OFFSET) // gap
    col = x // gap
    return row, col

def print_path_metrics(path, cost, expanded, mode):
    print(f"\n[{mode}] --- PATHFINDING COMPLETE ---")
    if path:
        path_coords = [(spot.row, spot.col) for spot in path]
        print(f"Path List (Row, Col Coordinates):")
        print(path_coords)
        print(f"Total Path Cost: {cost} steps")
        print(f"Total Nodes Expanded: {expanded}")
    else:
        print("NO PATH FOUND. The goal is completely blocked.")
    print("--------------------------------------\n")
