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
# Nueva matriz para la "salud" del moho (para efectos visuales)
mold_health = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.float32)

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
                for dy in range(-25, 26):
                    for dx in range(-25, 26):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                            distance = np.sqrt(dy*dy + dx*dx)
                            if distance <= 25:
                                # Gradiente exponencial más fuerte
                                strength = 10.0 * np.exp(-distance / 12.0)
                                chemical[ny, nx] = max(chemical[ny, nx], strength)
    
    # Dar químicos iniciales al moho para supervivencia
    my, mx = mold_pos
    chemical[my, mx] = 15.0
    mold_health[my, mx] = 100.0  # Salud inicial máxima
    
    # Crear área de supervivencia alrededor del moho inicial
    for dy in range(-2, 3):
        for dx in range(-2, 3):
            ny, nx = my + dy, mx + dx
            if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                distance = max(abs(dy), abs(dx))
                strength = max(10.0 - distance * 3.0, 5.0)
                chemical[ny, nx] = max(chemical[ny, nx], strength)

# IMPORTANTE: Llamar la inicialización
initialize_chemicals()

def calculate_food_distance(y, x):
    """Calcular la distancia mínima a cualquier fuente de alimento"""
    min_dist = float('inf')
    for fy in range(GRID_HEIGHT):
        for fx in range(GRID_WIDTH):
            if grid[fy, fx] == FOOD:
                dist = np.sqrt((y - fy)**2 + (x - fx)**2)
                min_dist = min(min_dist, dist)
    return min_dist

def grow_mold(grid, chemical):
    """El moho crece hacia celdas vecinas con mayor concentración química"""
    global mold_health  # Mover al inicio de la función
    
    new_grid = grid.copy()
    new_health = mold_health.copy()
    growth_count = 0
    death_count = 0
    
    # Actualizar salud del moho existente basada en distancia al alimento
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            if grid[y, x] == MOLD:
                food_dist = calculate_food_distance(y, x)
                
                # La salud depende de la distancia al alimento y concentración química
                health_from_food = max(0, 100 - food_dist * 3)  # Decae con distancia
                health_from_chem = chemical[y, x] * 8  # Bonus por químicos
                
                target_health = min(health_from_food + health_from_chem, 100.0)
                
                # Cambio gradual de salud
                if target_health > mold_health[y, x]:
                    new_health[y, x] = min(mold_health[y, x] + 2.0, target_health)
                else:
                    new_health[y, x] = max(mold_health[y, x] - 1.5, target_health)
                
                # El moho muere si la salud es muy baja
                if new_health[y, x] <= 10.0:
                    new_grid[y, x] = EMPTY
                    new_health[y, x] = 0.0
                    death_count += 1
                else:
                    # Reforzar químico en moho saludable (efecto neuronal)
                    if new_health[y, x] > 50:
                        chemical[y, x] = min(chemical[y, x] + 1.0, 12.0)
    
    # Crecimiento dirigido hacia alimento
    for y in range(1, GRID_HEIGHT - 1):
        for x in range(1, GRID_WIDTH - 1):
            if grid[y, x] == MOLD and mold_health[y, x] > 30:  # Solo moho saludable puede crecer
                neighbors = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]
                
                best_neighbor = None
                best_score = 0
                
                for ny, nx in neighbors:
                    if grid[ny, nx] == EMPTY:
                        # Score basado en concentración química y proximidad al alimento
                        chem_score = chemical[ny, nx]
                        food_dist = calculate_food_distance(ny, nx)
                        
                        # Bonus por estar más cerca del alimento
                        proximity_bonus = max(0, 20 - food_dist) / 20 * 5
                        
                        total_score = chem_score + proximity_bonus
                        
                        # Crecer si hay suficiente atractivo
                        if (total_score > best_score and 
                            total_score > 3.0 and 
                            np.random.random() < 0.2):
                            best_neighbor = (ny, nx)
                            best_score = total_score
                
                if best_neighbor:
                    ny, nx = best_neighbor
                    new_grid[ny, nx] = MOLD
                    # Salud inicial basada en proximidad al alimento
                    food_dist = calculate_food_distance(ny, nx)
                    initial_health = max(30, 80 - food_dist * 2)
                    new_health[ny, nx] = initial_health
                    growth_count += 1
    
    # Actualizar matriz global de salud
    mold_health = new_health  # Ya no necesitas 'global' aquí porque está al inicio
    
    if growth_count > 0 or death_count > 0:
        print(f"Moho: +{growth_count} nuevas celdas, -{death_count} muertas")
    
    return new_grid

def emit_chemical(chemical, grid):
    """Las fuentes de alimento emiten químico continuamente"""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == FOOD:
                # Emitir químico en un área amplia alrededor del alimento
                for dy in range(-3, 4):
                    for dx in range(-3, 4):
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < GRID_HEIGHT and 0 <= nx < GRID_WIDTH:
                            distance = max(abs(dy), abs(dx))
                            emission = EMISSION_INTENSITY * (4 - distance) / 4
                            chemical[ny, nx] = min(chemical[ny, nx] + emission, 20.0)

def diffuse_chemical(chemical, grid):
    """Difusión química con refuerzo en caminos de moho"""
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
                # El moho saludable actúa como "cable neuronal"
                health_factor = mold_health[y, x] / 100.0
                diffusion_factor = DIFFUSION_RATE * (0.5 + health_factor * 0.5)
                evaporation_factor = EVAPORATION_RATE * (0.1 + (1 - health_factor) * 0.9)
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
            
            new_chem[y, x] = np.clip(new_value, 0.0, 20.0)
    
    return new_chem

def draw_grid(screen, grid):
    """Dibujar la cuadrícula con efectos visuales para mostrar la salud del moho"""
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if grid[y, x] == MOLD:
                # Color del moho basado en su salud (efecto neuronal)
                health = mold_health[y, x]
                if health > 70:
                    color = (0, 255, 0)      # Verde brillante (saludable)
                elif health > 40:
                    color = (128, 255, 0)    # Verde amarillento (medio)
                elif health > 20:
                    color = (255, 255, 0)    # Amarillo (débil)
                else:
                    color = (255, 128, 0)    # Naranja (muriendo)
            else:
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
