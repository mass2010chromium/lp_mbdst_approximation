import random
import timeit
import matplotlib.pyplot as plt

def perf(n, n_runs=10000):
    x = tuple(range(n))
    y = set(x)
    d = random.sample(tuple(range(2*n)), n)
    
    t1 = timeit.timeit(lambda: [a in x for a in d], number=n_runs)
    t2 = timeit.timeit(lambda: [a in y for a in d], number=n_runs)
    return t1, t2

N = [3, 4, 5, 6, 7, 8, 9, 10, 20, 40, 80, 160, 320, 640]
T1 = []
T2 = []
for n in N:
    print(n)
    t1, t2 = perf(n)
    print(t1, t2)
    T1.append(t1)
    T2.append(t2)

plt.figure()
plt.plot(N, T1, label="tuple")
plt.plot(N, T2, label="set")
plt.legend()
plt.show()
