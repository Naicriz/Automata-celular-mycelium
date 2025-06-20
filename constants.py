# --- Parámetros del autómata ---
GRID_WIDTH = 100
GRID_HEIGHT = 80
CELL_SIZE = 6  # Tamaño de cada celda en píxeles

# Estados de celda
EMPTY = 0
MOLD = 1
FOOD = 2
OBSTACLE = 3

COLORS = {
    EMPTY: (20, 20, 40),      # Fondo oscuro
    MOLD: (0, 255, 0),        # Verde puro, más brillante
    FOOD: (255, 220, 0),      # Amarillo
    OBSTACLE: (120, 0, 0),    # Rojo oscuro
}

# Parámetros químicos optimizados para supervivencia y exploración
DIFFUSION_RATE = 0.3        # Difusión moderada para mantener gradientes
EVAPORATION_RATE = 0.2      # Evaporación muy lenta para mantener campo base
EMISSION_INTENSITY = 5.0     # Emisión constante desde FOOD
