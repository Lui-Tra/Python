import pygame


def show_kv_diagramm(diagramm, scale=1, block_width=50, border_width=3, side_distance=100):
    width = (side_distance * 2 + border_width + (block_width + border_width) * len(diagramm[0])) * scale
    height = (side_distance * 2 + border_width + (block_width + border_width) * len(diagramm)) * scale

    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill("#ffffff")

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

        clock.tick(60)
        pygame.display.flip()
