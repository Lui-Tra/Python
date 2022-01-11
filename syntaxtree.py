from parser import Parser
from termcolor import colored


if __name__ == "__main__":
    f = Parser().parse("not A")

    f.print_truth_table()
