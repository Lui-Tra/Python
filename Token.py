from abc import ABC
from abc import abstractmethod


class Token(ABC):
    @abstractmethod
    def nnf(self):
        pass

    def __repr__(self):
        return str(self)
