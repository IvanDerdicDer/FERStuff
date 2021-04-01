l = []
a = 1
def foo(a, l:list):
    for i in range(10):
        l.append(i)
        a += i
foo(a, l)
print(f"{l} {a}")