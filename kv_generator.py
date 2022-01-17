import math

import pygame
import pygame.freetype


def mirror_kv_h(kv, new_var):
    res = kv
    for i, line in enumerate(kv):
        new_line = []
        for vars in line:
            new_vars = dict(vars)
            new_vars[new_var] = True
            new_line.append(new_vars)
        res[i] += reversed(new_line)
    return res


def mirror_kv_v(kv, new_var):
    res = kv
    for line in reversed(kv):
        new_line = []
        for vars in line:
            new_vars = dict(vars)
            new_vars[new_var] = 1
            new_line.append(vars | {new_var:True})
        res.append(new_line)
    return res


def __generate_kv__(variables, current_variables):
    if len(current_variables) == 0:
        return [[{v: False for v in variables}]]
    else:
        prev_variables = current_variables[:-1]
        new_var = current_variables[-1]

        prev_kv = __generate_kv__(variables, prev_variables)

        if len(prev_variables) % 2 == 0:
            return mirror_kv_h(prev_kv, new_var)
        else:
            return mirror_kv_v(prev_kv, new_var)

def render_kv_diagramm(diagramm, variables, scale=1, block_width=50, border_width=3, side_distance=100):
    pygame.init()

    width = (side_distance * 2 + border_width + (block_width + border_width) * len(diagramm[0])) * scale
    height = (side_distance * 2 + border_width + (block_width + border_width) * len(diagramm)) * scale
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        screen.fill("#ffffff")
        render_cells(diagramm, screen)
        render_names(variables, screen)
        clock.tick(60)
        pygame.display.flip()


def draw_text(screen, pos, text):
    pygame.freetype.SysFont("Segoe UI", 20).render_to(screen, pos, text, (0, 0, 0))


def draw_centered_text(screen, pos, text):
    text, rect = pygame.freetype.SysFont("Segoe UI", 20).render(text, (0, 0, 0))
    screen.blit(text, (pos[0]-rect.width//2, pos[1]))

first_time = True

def render_names(variables, screen, scale=1, block_width=50, border_width=3, side_distance=150):
    global first_time

    num_columns = (2 ** math.ceil(len(variables) / 2))
    num_rows = (2 ** math.floor(len(variables) / 2))

    for n, var in enumerate(variables):
        if n % 2 == 0:
            line_length = (2 ** math.ceil((n + 1) / 2))
            indent = math.ceil(line_length / 2) * (block_width + border_width)
            if (line_length == num_columns):
                line_length //= 2
            num_lines = math.ceil((num_columns // line_length) / 2)

            y = scale * (side_distance - 15*(n+1))
            for i in range(num_lines):

                start_x = scale * (indent + side_distance + (2*line_length*i) * (block_width + border_width))
                end_x = start_x + line_length * (block_width + border_width)

                if n == 0:
                    color = "blue"
                elif n == 2:
                    color = "green"
                elif n == 4:
                    color = "red"
                else:
                    color = "orange"

                pygame.draw.line(screen, color,
                             (start_x, y),
                             (end_x, y)
                            )

                draw_centered_text(screen, (start_x+(end_x-start_x)//2, y-15), var)
        else:
            line_length = (2 ** math.floor((n+1) / 2))
            indent = math.ceil(line_length / 2) * (block_width + border_width)
            if (line_length == num_rows):
                line_length //= 2
            num_lines = (num_rows // line_length) // 2

            x = scale * (side_distance - 15 * (n + 1))
            for i in range(num_lines):

                start_y = scale * (indent + side_distance + (2*line_length*i) * (block_width + border_width))
                end_y = start_y + line_length * (block_width + border_width)

                if n == 1:
                    color = "blue"
                elif n == 3:
                    color = "green"
                elif n == 5:
                    color = "red"
                else:
                    color = "orange"

                pygame.draw.line(screen, color,
                                 (x, start_y),
                                 (x, end_y)
                                 )

                draw_text(screen, (x - 15, start_y + (end_y - start_y) // 2), var)


def render_cells(diagramm, screen, scale=1, block_width=50, border_width=3, side_distance=150):
    for row in range(len(diagramm)):
        for col in range(len(diagramm[0])):
            pygame.draw.rect(screen,
                             "black",
                             [scale * (side_distance + col * (border_width + block_width)),
                              scale * (side_distance + row * (border_width + block_width)),
                              scale * (block_width + 2 * border_width),
                              scale * (block_width + 2 * border_width)]
                             )

            color = "red" if diagramm[row][col] else "white"
            pygame.draw.rect(screen,
                             color,
                             [scale * (side_distance + border_width + col * (border_width + block_width)),
                              scale * (side_distance + border_width + row * (border_width + block_width)),
                              scale * block_width,
                              scale * block_width]
                             )

def generate_kv(variables):
    return __generate_kv__(variables, variables)


def print_matrix(matrix):
    for line in matrix:
        for elem in line:
            print(elem, end=" ")
        print()


if __name__ == '__main__':
    print("res:")
    matrix = generate_kv([1, 2])
    print_matrix(matrix)
    matrix = generate_kv([1, 2, 3])
    print_matrix(matrix)
