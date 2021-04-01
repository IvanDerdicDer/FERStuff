import ctypes
import random

def recFuc(n, p:ctypes.pointer):
    if not n:
        return
    p.contents.value = random.randint(1, 10)
    print(p.contents)
    recFuc(n - 1, p)

pl = ctypes.pointer(ctypes.py_object([]))
print(pl.contents)
recFuc(10, pl)
#recFuc(10, ctypes.pointer(ctypes.py_object(l)))
print(pl.contents)
