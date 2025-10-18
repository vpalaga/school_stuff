abc = ("A, B, C, D, E, F, G, H, I, J, K, L, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z")
y = "QWERTZUIOPASDFGHJKLYXCVBNM"

abc = abc.split(", ")

msg = "00111100110010100101101010100101111001111010000101000011001110101010000110001001011110011110100"
msg = list(msg)
msg_n = []

tmp = ""
for i in range(len(msg)):
    if i%5==0:
        if tmp != "":
            msg_n.append(tmp)
        tmp =""
    tmp += msg[i]

look_up = {}
for n, letter in enumerate(abc):
    b = f"{n + 1:b}"
    pre = (5 - len(b))*"0"
    look_up[pre+b] = letter

def decode(msg):
    out = ""
    for bit in msg:
        out += look_up[bit]
    return out
print(look_up)
print(msg_n)
print(decode(msg_n))
