import sys
from itertools import count


def stack_size():
    size = 2
    frame = sys._getframe(size)

    for size in count(size):
        frame = frame.f_back
        if not frame:
            return size


initial_stack_size = None


def indented_print(*args, **kwargs):
    global initial_stack_size
    size = stack_size()
    if initial_stack_size is None or size < initial_stack_size:
        initial_stack_size = size
    print("   "*(size-initial_stack_size), end="")
    print(*args, **kwargs)