import pygame

import parser
from Operator import NotOperator
from Variable import Variable


class Resolvent:
    def __init__(self, clause, parent1, parent2, row):
        self.clause = clause
        self.parent1 = parent1
        self.parent2 = parent2
        self.row = row
        self.rendered_text = None
        self.pos = None
        self.center_pos = None

    def __eq__(self, other):
        if isinstance(other, Resolvent):
            return other.clause == self.clause
        return False

    def set_pos(self, pos):
        self.pos = pos
        self.center_pos = [pos[0] + self.rendered_text[1].w // 2, pos[1] + self.rendered_text[1].h // 2]

    def get_all(self, row):
        if self.parent1 is None:
            if self.row == row or row == -1:
                return [self]
            else:
                return []
        else:
            if self.row == row or row == -1:
                return [self] + self.parent1.get_all(row) + self.parent2.get_all(row)
            else:
                return self.parent1.get_all(row) + self.parent2.get_all(row)

    def render_texts(self, font):
        self.rendered_text = font.render(str(self.clause).replace("[", "{").replace("]", "}"), (0, 0, 0))
        if self.parent1 is not None:
            self.parent1.render_texts(font)
            self.parent2.render_texts(font)

    def calc_pos(self, h_spacer):
        if self.row == 0:
            return self.pos
        p1 = self.parent1.calc_pos(h_spacer)
        p2 = self.parent2.calc_pos(h_spacer)
        self.set_pos([(p1[0] + p2[0]) // 2, (self.row + 1) * h_spacer])
        return self.pos

    def display(self, screen):
        if self.parent1 is not None:
            for it in [self.parent1, self.parent2]:
                pygame.draw.line(screen, (0, 0, 0),
                                 [self.center_pos[0], self.center_pos[1] - self.rendered_text[1].h // 1.5],
                                 [it.center_pos[0], it.center_pos[1] + self.rendered_text[1].h // 1.5],
                                 8)
            self.parent1.display(screen)
            self.parent2.display(screen)
        screen.blit(self.rendered_text[0], self.pos)

    def traverse(self, indent=0):
        print(" " * indent + str(self.clause) + " " + str(self.row))
        if self.parent1 is not None:
            self.parent1.traverse(indent + 2)
            self.parent2.traverse(indent + 2)

    def is_linear(self, clause_list):
        # TODO fix
        path = []
        current = self
        while current is not None:
            path.append(current)
            current = current.parent1

        linear = True
        for it in path:
            if it.parent2 not in path and it.parent2 not in clause_list:
                linear = False

        return linear

    def __repr__(self):
        return str(self.clause)


def get_resolvent_path(clause_list, linear=False):
    contradiction = Resolvent([], None, None, -1)

    resolvents = [Resolvent(it, None, None, 0) for it in clause_list]

    while contradiction not in resolvents:
        new = []
        for parent1 in resolvents:
            for parent2 in resolvents:
                if parent1 != parent2:
                    pairs = [it for it in parent1.clause if it not in parent2.clause] + \
                            [it for it in parent2.clause if it not in parent1.clause]
                    rem = []
                    for it in pairs:
                        inverse = NotOperator(it) if isinstance(it, Variable) else it.children[0]
                        if inverse not in pairs:
                            rem.append(it)
                    for it in rem:
                        pairs.remove(it)

                    if len(pairs) == 2:
                        resolvent = [it for it in parent1.clause]
                        for it in parent2.clause:
                            if it not in resolvent:
                                resolvent.append(it)
                        for it in pairs:
                            resolvent.remove(it)
                        new.append(Resolvent(resolvent, parent1, parent2, max(parent1.row, parent2.row) + 1))
        resolvents.extend(new)

    if linear:
        for it in resolvents:
            if len(it.clause) == 0 and it.is_linear(clause_list):
                return it
    else:
        return resolvents[resolvents.index(contradiction)]


def display_resolvent_path(root, scale=1):
    pygame.init()
    clock = pygame.time.Clock()

    h_spacer = 75 * scale
    v_spacer = 25 * scale
    font = pygame.freetype.SysFont("Segoe UI", 15 * scale)
    root.render_texts(font)

    row0 = root.get_all(0)
    w = v_spacer
    for it in row0:
        it.set_pos([w, h_spacer])
        w += it.rendered_text[1].w + v_spacer

    root.calc_pos(h_spacer)

    h = root.row * h_spacer + h_spacer * 2

    screen = pygame.display.set_mode((w, h))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((255, 255, 255))

        root.display(screen)

        pygame.display.update()
        clock.tick(30)


if __name__ == '__main__':
    form = parser.parse("{{A , C, U}, {A , C, ¬U}, {¬A , U}, {¬A , ¬U}, {¬C, U}, {¬C, ¬U}}")
    cl = form.to_clause_list()
    root = get_resolvent_path(cl)
    display_resolvent_path(root, scale=4)

