from abc import ABC
from abc import abstractmethod


class Token(ABC):
    @abstractmethod
    def simplify(self):
        pass

    @abstractmethod
    def traverse(self):
        pass
