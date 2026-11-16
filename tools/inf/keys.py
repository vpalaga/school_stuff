p = 11
g = 2

a = 3
x = pow(g, a, p)

b = 4
y = pow(g, b, p)

S_ab = pow(y, a, p)
S_ba = pow(x, b, p)

print(S_ab)
