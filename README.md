# Autómata Celular - Simulación de Micelio 🍄

Un autómata celular que simula el crecimiento y comportamiento de micelio (hongos) en busca de fuentes de alimento, desarrollado como proyecto universitario para la asignatura de **Grafos y Lenguajes Formales**.

## 🎯 Descripción

Este proyecto implementa un autómata celular que modela el comportamiento inteligente del micelio, el cual:

- **Busca alimento** siguiendo gradientes químicos
- **Crece y se expande** hacia fuentes de nutrientes
- **Mantiene su salud** basada en la proximidad al alimento
- **Evita obstáculos** y se adapta al entorno
- **Forma redes** similares a sistemas neuronales

El micelio real exhibe comportamientos complejos de búsqueda de alimento y optimización de rutas, lo cual este simulador replica usando reglas simples de autómatas celulares.

## 🚀 Características

- **Visualización en tiempo real** con Pygame
- **Sistema de salud** del micelio con efectos visuales
- **Difusión química** que guía el crecimiento
- **Múltiples fuentes de alimento** y obstáculos
- **Comportamiento emergente** similar a redes neuronales
- **Parámetros configurables** para experimentación

## 🛠️ Tecnologías Utilizadas

- **Python 3.13+**
- **Pygame** - Visualización y renderizado
- **NumPy** - Cálculos matriciales eficientes
- **Poetry** - Gestión de dependencias

## 📦 Instalación

### Prerrequisitos

- Python 3.13 o superior
- Poetry (recomendado) o pip

### Opción A: Con Poetry (Recomendado)

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd Automata-celular-mycelium

# Instalar Poetry si no lo tienes
curl -sSL https://install.python-poetry.org | python3 -

# Instalar dependencias
poetry install

# Activar el entorno virtual
poetry shell
```

### Opción B: Con pip

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd Automata-celular-mycelium

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install pygame numpy
```

## 🎮 Uso

### Ejecutar la simulación

**Con Poetry:**

```bash
poetry run python main.py
```

**Con pip/venv:**

```bash
python main.py
```

### Controles

- La simulación se ejecuta automáticamente
- **Cerrar ventana** o **Ctrl+C** para salir
- El micelio crecerá buscando las fuentes de alimento (amarillas)

## ⚙️ Configuración

Puedes modificar los parámetros en `constants.py`:

```python
# Dimensiones de la cuadrícula
GRID_WIDTH = 100        # Ancho de la simulación
GRID_HEIGHT = 80        # Alto de la simulación
CELL_SIZE = 6           # Tamaño de cada celda en píxeles

# Parámetros químicos
DIFFUSION_RATE = 0.3    # Velocidad de difusión química
EVAPORATION_RATE = 0.2  # Velocidad de evaporación
EMISSION_INTENSITY = 5.0 # Intensidad de emisión desde alimento
```

## 🧬 Cómo Funciona

### 1. Inicialización

- Se coloca micelio inicial en el centro
- Se colocan fuentes de alimento en los extremos
- Se crean obstáculos para añadir complejidad
- Se establece un gradiente químico inicial

### 2. Ciclo de Simulación

Cada frame ejecuta:

1. **Emisión química**: Las fuentes de alimento emiten químicos
2. **Difusión química**: Los químicos se propagan por la cuadrícula
3. **Crecimiento del micelio**: El micelio crece hacia mayor concentración química
4. **Actualización de salud**: La salud se actualiza basada en proximidad al alimento
5. **Visualización**: Se renderiza el estado actual

### 3. Reglas del Micelio

- **Crecimiento**: Solo el micelio saludable (salud > 30) puede crecer
- **Dirección**: Crece hacia celdas con mayor concentración química
- **Salud**: Depende de la distancia al alimento y concentración química
- **Muerte**: Muere si la salud cae por debajo de 10
- **Refuerzo**: El micelio saludable refuerza el campo químico

## 🎨 Efectos Visuales

El micelio cambia de color según su salud:

- 🟢 **Verde brillante**: Salud > 70 (muy saludable)
- 🟡 **Verde amarillento**: Salud > 40 (saludable)
- 🟡 **Amarillo**: Salud > 20 (débil)
- 🟠 **Naranja**: Salud ≤ 20 (muriendo)

## 📊 Estructura del Proyecto

```
Automata-celular-mycelium/
├── main.py              # Archivo principal de la simulación
├── constants.py         # Parámetros y constantes configurables
├── pyproject.toml       # Configuración de Poetry
├── poetry.lock          # Lock file de dependencias
├── README.md            # Documentación (este archivo)
└── __pycache__/         # Cache de Python (generado)
```

## 🔬 Conceptos Científicos

Este proyecto implementa conceptos de:

- **Autómatas Celulares**: Sistemas dinámicos discretos
- **Difusión Química**: Modelado de gradientes de concentración
- **Comportamiento Emergente**: Patrones complejos de reglas simples
- **Sistemas Adaptativos**: Respuesta a cambios ambientales
- **Redes Biológicas**: Similitud con redes neuronales y vasculares

## 🎓 Contexto Académico

**Asignatura**: Grafos y Lenguajes Formales
**Universidad**: Universidad Tecnológica Metropolitana
**Autor**: Naicriz (isalazarjara@gmail.com) y compañeros
**Año**: 2025

## 🤝 Contribuciones

Este es un proyecto académico, pero las sugerencias y mejoras son bienvenidas:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📝 Licencia

MIT

## 🌿 Flujo de Trabajo con Git

### Configuración Inicial

1. **Configura tu información de Git** (solo la primera vez):

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

### Creación de Branches

Usamos la siguiente convención para nombrar branches:

```bash
# Para nuevas funcionalidades
git checkout -b funcionalidad/nombre-de-la-funcionalidad

# Para corrección de errores
git checkout -b correccion/descripcion-del-error

# Para mejoras
git checkout -b mejora/descripcion-de-la-mejora

# Para documentación
git checkout -b docs/descripcion-de-la-documentacion

# Ejemplos:
git checkout -b funcionalidad/login-sistema
git checkout -b correccion/error-formulario-contacto
git checkout -b mejora/optimizar-rendimiento
git checkout -b docs/actualizar-readme
```

### Flujo de Commits

#### 1. Antes de hacer cambios

```bash
# Asegúrate de estar en la rama correcta
git checkout core
git pull origin core

# Crea tu nueva rama
git checkout -b funcionalidad/mi-nueva-funcionalidad
```

#### 2. Realizar cambios y commits

```bash
# Agregar archivos específicos
git add archivo1.tsx archivo2.ts

# O agregar todos los cambios
git add .

# Commit con mensaje descriptivo
git commit -m "tipo: descripción clara de los cambios"
```

#### 3. Convención de Mensajes de Commit

Usamos la siguiente estructura:

```
tipo: descripción breve

[descripción más detallada si es necesaria]
```

**Tipos de commit:**

- `nueva:` Nueva funcionalidad
- `corrige:` Corrección de errores
- `docs:` Cambios en documentación
- `estilo:` Cambios de formato (espacios, comas, etc.)
- `refactor:` Refactorización de código
- `test:` Agregar o modificar tests
- `config:` Cambios en build, dependencias, etc.

**Ejemplos:**

```bash
git commit -m "nueva: agregar formulario de login"
git commit -m "corrige: corregir validación de email en registro"
git commit -m "docs: actualizar README con instrucciones"
git commit -m "estilo: formatear código con prettier"
git commit -m "refactor: reorganizar componentes de usuario"
git commit -m "test: agregar pruebas para formulario"
git commit -m "config: actualizar dependencias de desarrollo"
```

#### 4. Subir cambios al repositorio

```bash
# Primera vez que subes la rama
git push -u origin funcionalidad/mi-nueva-funcionalidad

# Siguientes pushes
git push
```

### Integración de Cambios

#### 1. Antes de hacer Pull Request

```bash
# Actualizar main(core) local
git checkout core
git pull origin core

# Volver a tu rama y rebasear
git checkout funcionalidad/mi-nueva-funcionalidad
git rebase core

# Si hay conflictos, resolverlos y continuar
git add .
git rebase --continue

# Subir cambios actualizados
git push --force-with-lease
```

#### 2. Crear Pull Request

1. Ve al repositorio en GitHub
2. Crea un Pull Request desde tu rama hacia `core`
3. Describe los cambios realizados
4. Solicita revisión del equipo
5. Espera aprobación antes de hacer merge

### Comandos Útiles

```bash
# Ver estado de archivos
git status

# Ver historial de commits
git log --oneline

# Ver diferencias
git diff

# Cambiar de rama
git checkout nombre-de-rama

# Ver todas las ramas
git branch -a

# Eliminar rama local (después del merge)
git branch -d funcionalidad/mi-funcionalidad

# Eliminar rama remota
git push origin --delete funcionalidad/mi-funcionalidad
```

## 👥 Colaboración en Equipo

### Reglas de Colaboración

1. **Nunca hacer push directo a `core`**
2. **Siempre crear Pull Request para revisión**
3. **Escribir commits descriptivos**
4. **Mantener las ramas actualizadas con `core`**
5. **Eliminar ramas después del merge**
6. **Comunicar cambios importantes al equipo**

### Comunicación

- Usa mensajes de commit claros y descriptivos
- Comenta tu código cuando sea necesario
- Documenta funcionalidades nuevas
- Reporta errores o problemas en GitHub Issues

## 🔮 Posibles Mejoras

- [ ] Interfaz gráfica para ajustar parámetros en tiempo real
- [ ] Métricas de análisis del crecimiento
- [ ] Exportación de datos de simulación
- [ ] Diferentes tipos de micelio con comportamientos únicos
- [ ] Modo de replay para analizar simulaciones
- [ ] Integración con análisis de grafos

---

*"El micelio representa la red neuronal de la naturaleza"* - Paul Stamets
