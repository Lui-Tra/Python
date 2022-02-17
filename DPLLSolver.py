import pygame

import parser
from Operator import NotOperator


class DpllNode:
    def __init__(self, text, children=None):
        if children is None:
            children = []
        self.text = text.replace("[", "{").replace("]", "}")
        self.children = children
        self.render_text = None

    def traverse(self, indent=0):
        print(" " * (indent * 2) + self.text)
        for c in self.children:
            c.traverse(indent + 1)

    def display(self):
        pass

    def render_texts(self, font):
        if self.render_text is None:
            self.render_text = font.render(self.text, (0, 0, 0))
        for c in self.children:
            c.render_texts(font)

    def depth(self):
        if len(self.children) == 0:
            return 1
        return max([c.depth() for c in self.children]) + 1

    def display_draw(self, screen, pos, h_spacer, width):
        screen.blit(self.render_text[0], (pos[0] - self.render_text[1].width // 2, pos[1]))
        if len(self.children) == 1:
            pygame.draw.line(screen, (0, 0, 0),
                             (pos[0], pos[1] + h_spacer * 0.25),
                             (pos[0], pos[1] + h_spacer * 0.9),
                             6)
            self.children[0].display_draw(screen, (pos[0], pos[1] + h_spacer), h_spacer, width)
        elif len(self.children) == 2:
            pygame.draw.line(screen, (0, 0, 0),
                             (pos[0], pos[1] + h_spacer * 0.25),
                             (pos[0] - width // 4, pos[1] + h_spacer * 0.9),
                             6)
            pygame.draw.line(screen, (0, 0, 0),
                             (pos[0], pos[1] + h_spacer * 0.25),
                             (pos[0] + width // 4, pos[1] + h_spacer * 0.9),
                             6)
            self.children[0].display_draw(screen, (pos[0] - width // 4, pos[1] + h_spacer), h_spacer, width // 2)
            self.children[1].display_draw(screen, (pos[0] + width // 4, pos[1] + h_spacer), h_spacer, width // 2)


def display_dpll_tree(root, scale=1, w=1000):
    pygame.init()
    clock = pygame.time.Clock()

    w *= scale

    h_spacer = 75 * scale

    font = pygame.freetype.SysFont("Segoe UI", 15 * scale)
    root.render_texts(font)

    h = root.depth() * h_spacer + h_spacer * scale

    screen = pygame.display.set_mode((w, h))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        screen.fill((255, 255, 255))

        root.display_draw(screen, (w // 2, h_spacer), h_spacer, w)

        pygame.display.update()
        clock.tick(30)


def create_dpll_tree(clause_list):
    def remove_var(lst, vr):
        neg_vr = vr.children[0] if isinstance(vr, NotOperator) else NotOperator(vr)
        rem = []
        for item in lst:
            if vr in item:
                rem.append(item)
            elif neg_vr in item:
                item.remove(neg_vr)
        for item in rem:
            lst.remove(item)

    if len(clause_list) == 0:
        return DpllNode("Erfüllbar")
    elif len(clause_list[0]) == 0:
        return DpllNode("Unerfüllbar")
    else:
        if len(clause_list[0]) == 1:
            var = clause_list[0][0]
            text = str(clause_list)
            remove_var(clause_list, var)
            return DpllNode(text, [DpllNode("OLR: " + str(var) + " := true", [create_dpll_tree(clause_list)])])
        else:
            all_vars = set()
            for it in clause_list:
                for i in it:
                    all_vars.add(i)
            all_vars = sorted(list(all_vars))

            for var in all_vars:
                neg_var = var.children[0] if isinstance(var, NotOperator) else NotOperator(var)
                if neg_var not in all_vars:
                    text = str(clause_list)
                    remove_var(clause_list, var)
                    return DpllNode(text, [DpllNode("PLR: " + str(var) + " := true", [create_dpll_tree(clause_list)])])

            var = all_vars[0]
            neg_var = var.children[0] if isinstance(var, NotOperator) else NotOperator(var)

            text = str(clause_list)

            clause_list_copy = [[i for i in it] for it in clause_list]
            remove_var(clause_list, var)
            remove_var(clause_list_copy, neg_var)

            if isinstance(var, NotOperator):
                case1 = DpllNode(str(neg_var) + ":= true", [create_dpll_tree(clause_list_copy)])
                case2 = DpllNode(str(neg_var) + ":= false", [create_dpll_tree(clause_list)])
            else:
                case1 = DpllNode(str(var) + ":= true", [create_dpll_tree(clause_list)])
                case2 = DpllNode(str(var) + ":= false", [create_dpll_tree(clause_list_copy)])
            return DpllNode(text, [case1, case2])


if __name__ == '__main__':
    form = parser.parse("{{p, ¬r},{p, ¬q},{r, q},{¬r, ¬q},{q, ¬p},{r, ¬q, ¬p},{r, q, p}}")
    form.dpll(2)
