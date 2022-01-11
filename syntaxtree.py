from kv import show_kv_diagramm
from parser import Parser
from termcolor import colored

if __name__ == "__main__":
    show_kv_diagramm(
        [[0, 1, 0, 1],
         [1, 1, 0, 0],
         [1, 1, 0, 0],
         [1, 1, 0, 0]],
        scale=2
    )
