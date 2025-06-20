# slime_automaton.py

import pygame
import numpy as np

from constants import CELL_SIZE, COLORS, DIFFUSION_RATE, EMISSION_INTENSITY, EMPTY, EVAPORATION_RATE, FOOD, GRID_HEIGHT, GRID_WIDTH, MOLD, OBSTACLE

# Inicialización de Pygame
pygame.init()
screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))

pygame.display.set_caption("Autómata Celular - Moho Slime")
clock = pygame.time.Clock()

# --- Inicialización de matrices ---
grid = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.uint8)
chemical = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.float32)

# Colocar alimento y moho inicial
food1_pos = (GRID_HEIGHT // 2, GRID_WIDTH // 4)
food2_pos = (GRID_HEIGHT // 2, 3 * GRID_WIDTH // 4)
mold_pos = (GRID_HEIGHT // 2 - 5, GRID_WIDTH // 2)

grid[food1_pos] = FOOD
grid[food2_pos] = FOOD
grid[mold_pos] = MOLD

# Ejemplo de obstáculo
grid[GRID_HEIGHT // 2, GRID_WIDTH // 2 - 10:GRID_WIDTH // 2 + 10] = OBSTACLE

# Inicializar químicos: crear gradiente inicial desde las fuentes de alimento
def initialize_chemicals():
    """Crear gradiente químico inicial para guiar el crecimiento"""
    # Crear gradiente inicial desde las fuentes de alimento
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == FOOD:
                # Crear gradiente amplio desde cada fuente de alimento
                for dy in range(-20, 21):
                    for dx in range(-20, 21):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                            distance = np.sqrt(dy*dy + dx*dx)
                            if distance <= 20:
                                # Gradiente exponencial más fuerte
                                strength = 8.0 * np.exp(-distance / 10.0)
                                chemical[ny, nx] = max(chemical[ny, nx], strength)
    
    # Dar químicos iniciales MUY ALTOS al moho para supervivencia
    my, mx = mold_pos
    chemical[my, mx] = 20.0
    
    # Crear área de supervivencia alrededor del moho inicial
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            ny, nx = my + dy, mx + dx
            if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                distance = max(abs(dy), abs(dx))
                strength = 15.0 - distance * 2.0
                chemical[ny, nx] = max(chemical[ny, nx], strength)

# IMPORTANTE: Llamar la inicialización
initialize_chemicals()

def grow_mold(grid, chemical):
    """El moho crece hacia celdas vecinas con mayor concentración química"""
    new_grid = grid.copy()
    growth_count = 0
    
    # Manejar moho existente
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            if grid[y, x] == MOLD:
                # Verificar si hay FOOD cerca (radio ampliado)
                near_food = False
                for dy in range(-8, 9):
                    for dx in range(-8, 9):
                        ny, nx = y + dy, x + dx
                        if (0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH and 
                            grid[ny, nx] == FOOD):
                            near_food = True
                            break
                    if near_food:
                        break
                
                if near_food:
                    # Reforzar químico si está cerca del alimento
                    chemical[y, x] = min(chemical[y, x] + 5.0, 25.0)
                else:
                    # Degradación MUY LENTA para supervivencia
                    chemical[y, x] *= 0.98
                    # Solo morir si químico extremadamente bajo
                    if chemical[y, x] < 0.5 and np.random.random() < 0.01:
                        new_grid[y, x] = EMPTY
    
    # Crecimiento dirigido
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            if grid[y, x] == MOLD:
                neighbors = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
                
                best_neighbor = None
                best_score = 0
                
                for ny, nx in neighbors:
                    if grid[ny, nx] == EMPTY:
                        # Score basado principalmente en concentración química
                        chem_score = chemical[ny, nx]
                        
                        # Pequeño bonus hacia alimento
                        food_bonus = 0
                        min_food_dist = float('inf')
                        for fy in range(GRID_HEIGHT):
                            for fx in range(GRID_WIDTH):
                                if grid[fy, fx] == FOOD:
                                    dist = abs(ny - fy) + abs(nx - fx)
                                    min_food_dist = min(min_food_dist, dist)
                        
                        if min_food_dist < 40:
                            food_bonus = 2.0 / (min_food_dist + 1)
                        
                        total_score = chem_score + food_bonus
                        
                        # Umbral más bajo para facilitar crecimiento
                        if (total_score > best_score and 
                            total_score > 1.5 and 
                            np.random.random() < 0.4):
                            best_neighbor = (ny, nx)
                            best_score = total_score
                
                if best_neighbor:
                    new_grid[best_neighbor] = MOLD
                    growth_count += 1
                    # Dar químico inicial al nuevo moho
                    chemical[best_neighbor] = min(chemical[best_neighbor] + 5.0, 15.0)
    
    if growth_count > 0:
        print(f"Moho creció en {growth_count} celdas")
    return new_grid

def emit_chemical(chemical, grid):
    """Las fuentes de alimento emiten químico más intensamente"""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == FOOD:
                # Emitir químico en un área más amplia alrededor del alimento
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                            distance = abs(dy) + abs(dx)
                            emission = EMISSION_INTENSITY * (3 - distance) / 3
                            chemical[ny, nx] = min(chemical[ny, nx] + emission, 15.0)

def diffuse_chemical(chemical, grid):
    """Difusión química mejorada con caminos reforzados"""
    new_chem = chemical.copy()
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            if grid[y, x] == OBSTACLE:
                new_chem[y, x] = 0.0
                continue
            
            current_val = float(chemical[y, x])
            if not np.isfinite(current_val):
                new_chem[y, x] = 0.0
                continue
            
            # Diferentes parámetros según el tipo de celda
            if grid[y, x] == MOLD:
                # El moho mantiene mejor el químico (actúa como camino reforzado)
                diffusion_factor = DIFFUSION_RATE * 0.3
                evaporation_factor = EVAPORATION_RATE * 0.2
            elif grid[y, x] == FOOD:
                # El alimento no difunde ni se evapora
                continue
            else:
                # Celdas vacías: difusión y evaporación normal
                diffusion_factor = DIFFUSION_RATE
                evaporation_factor = EVAPORATION_RATE
            
            # Calcular laplaciano
            laplacian = (
                float(chemical[y-1, x]) + float(chemical[y+1, x]) +
                float(chemical[y, x-1]) + float(chemical[y, x+1]) - 4.0 * current_val
            )
            
            if not np.isfinite(laplacian):
                new_chem[y, x] = current_val * (1 - evaporation_factor)
                continue
            
            # Aplicar difusión y evaporación
            diffusion_term = diffusion_factor * laplacian
            evaporation_term = current_val * (1 - evaporation_factor)
            new_value = evaporation_term + diffusion_term
            
            new_chem[y, x] = np.clip(new_value, 0.0, 15.0)
    
    return new_chem

def draw_grid(screen, grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = COLORS[grid[y, x]]
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, color, rect)

# --- Loop principal ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 1. Emisión química
    emit_chemical(chemical, grid)
    # 2. Difusión química
    chemical = diffuse_chemical(chemical, grid)
    # 3. Crecimiento del moho
    grid = grow_mold(grid, chemical)

    # 4. Visualización
    draw_grid(screen, grid)
    pygame.display.flip()
    clock.tick(15)  # FPS

pygame.quit()
