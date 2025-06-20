# --- Parámetros del autómata ---
GRID_WIDTH = 240
GRID_HEIGHT = 120
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

# Parámetros químicos optimizados para supervivencia
DIFFUSION_RATE = 0.15        # Reducido para mantener concentraciones
EVAPORATION_RATE = 0.05     # Extremadamente bajo para supervivencia
EMISSION_INTENSITY = 6.0     # Muy alto para crear gradientes fuertes
