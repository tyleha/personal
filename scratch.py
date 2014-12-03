# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

def nthfib(n):
    if n <=1: return n
    p2 = 0
    p1 = 1
    for i in range(n):
        fib = p2+p1
        p2 = p1
        p1 = fib
    return p1

nthfib(1)

# <codecell>

xx = np.cos(np.arange(-np.pi, np.pi, 2*np.pi/400))
plt.plot(xx)

# <codecell>

np.savetxt("foo.csv", xx, delimiter=",")

# <codecell>

def msort3(x):
    result = []
    if len(x) < 2:
        return x
    mid = int(len(x)/2)
    y = msort3(x[:mid])
    z = msort3(x[mid:])
    i = 0
    j = 0
    import pdb;pdb.set_trace()
    while i < len(y) and j < len(z):
            if y[i] > z[j]:
                result.append(z[j])
                j += 1
            else:
                result.append(y[i])
                i += 1
    result += y[i:]
    result += z[j:]
    return result

# <codecell>

x = [5,3,6,7,1,2,3,9,8,0]

# <codecell>

msort3(x)c

# <codecell>


