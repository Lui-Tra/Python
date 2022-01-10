from abc import ABC
from abc import abstractmethod


class Token(ABC):
    def __init__(self, children):
        self.children = children

    @abstractmethod
    def negate(self):
        pass

    @abstractmethod
    def traverse(self):
        pass

    @abstractmethod
    def simplify(self):
        pass
