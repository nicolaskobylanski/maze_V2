import pygame
import random

# Inicio pygame
pygame.init()

# Creo una pantalla de juego
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()

# Propiedades del jugador
square_size = 50
square_color = (0, 0, 0)
square_x, square_y = 0, 0  # Spawn arriba a la izquierda
square_speed = 50

# Propiedades del laberinto
maze_size = screen_width // square_size
maze = [[0] * maze_size for _ in range(maze_size)]
start_pos = (0, 0)
end_pos = (maze_size - 1, maze_size - 1)

# Propiedades de la cuadrícula
grid_size = square_size
grid_color = (100, 100, 100)

# Boolean que comprueba si el jugador se ha movido en el cuadrado en el que se encuentra
square_moved = False

# Depth-First Search Maze Generation -> Un algoritmo sencillo utilizado para crear un modelo de laberinto aleatorio cada vez que se inicia el juego
stack = [start_pos]
visited = set()
visited.add(start_pos)

while stack:
    current = stack[-1]
    x, y = current

    neighbors = [(x + 2, y), (x - 2, y), (x, y + 2), (x, y - 2)]

    unvisited_neighbors = [neighbor for neighbor in neighbors if 0 <= neighbor[0] < maze_size and 0 <= neighbor[1] < maze_size and neighbor not in visited]

    if unvisited_neighbors:
        next_cell = random.choice(unvisited_neighbors)
        nx, ny = next_cell
        wall_x, wall_y = (x + nx) // 2, (y + ny) // 2
        maze[wall_x][wall_y] = 1
        visited.add(next_cell)
        stack.append(next_cell)
    else:
        stack.pop()

# Creo el bucle principal del juego
running = True
keys_history = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not square_moved:
        # Mueve al jugador en la cuadrícula
        if keys[pygame.K_LEFT] and square_x > 0 and not maze[(square_x - 1) // square_size][square_y // square_size]:
            square_x -= square_speed
            square_moved = True
            keys_history.append("Left")
        if keys[pygame.K_RIGHT] and square_x < screen_width - square_size and not maze[(square_x + square_size) // square_size][square_y // square_size]:
            square_x += square_speed
            square_moved = True
            keys_history.append("Right")
        if keys[pygame.K_UP] and square_y > 0 and not maze[square_x // square_size][(square_y - 1) // square_size]:
            square_y -= square_speed
            square_moved = True
            keys_history.append("Up")
        if keys[pygame.K_DOWN] and square_y < screen_height - square_size and not maze[square_x // square_size][(square_y + square_size) // square_size]:
            square_y += square_speed
            square_moved = True
            keys_history.append("Down")

    # Comprueba si el jugador ha alcanzado la posición final del laberinto
    if (square_x, square_y) == (750, 550):
        running = False

    if not any(keys):
        square_moved = False

    # Fondo blanco
    screen.fill((255, 255, 255))

    # Dibujar la cuadrícula
    for x in range(0, screen_width, grid_size):
        pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height))
    for y in range(0, screen_height, grid_size):
        pygame.draw.line(screen, grid_color, (0, y), (screen_width, y))

    # Dibujar el laberinto
    for i in range(maze_size):
        for j in range(maze_size):
            if maze[i][j] == 1:
                pygame.draw.rect(screen, (255, 0, 0), (i * square_size, j * square_size, square_size, square_size))
            elif (i, j) == start_pos:
                pygame.draw.rect(screen, (0, 255, 0), (i * square_size, j * square_size, square_size, square_size))
                font = pygame.font.Font(None, 36)
                text = font.render("S", True, (0, 0, 0))
                screen.blit(text, (i * square_size + square_size // 3, j * square_size + square_size // 3))
            elif (i, j) == end_pos:
                pygame.draw.rect(screen, (0, 0, 255), (750, 550, 50, 50))
                font = pygame.font.Font(None, 36)
                text = font.render("F", True, (0, 0, 0))
                screen.blit(text, (765, 565))

    # Dibujar el personaje
    pygame.draw.rect(screen, square_color, (square_x, square_y, square_size, square_size))

    pygame.display.flip()
    clock.tick(30)

print(keys_history)
pygame.quit()

