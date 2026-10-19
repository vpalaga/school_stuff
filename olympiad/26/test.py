import string
alphabet = list(string.ascii_lowercase)
alphabet.append(" ")
d = {}
for i, l in enumerate(alphabet):
    d[l] = i

m = input("enc:")
key = 5
out = []

for l in [int(x) for x in m.split(",")]:
    out.append(alphabet[l - key])

print(out)

