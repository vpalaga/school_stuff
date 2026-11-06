s = """IZH QJWTLZWTR UZLI PALOHQ YLCHT JQ IHQ FARHQ
CHFHLOHFHQ. HL UJLRHR JQ IHL JXRHQ FLCHWNH QHFHQ IHP
OJLRHQ CQI QHQQR IJD OHTHZPH NHQQUALR."""

l = list(s.strip())

d = {}

for n in l:
    if n in d.keys():
        d[n] += 1
    else:
        d[n] = 1

for k,v in d.items():
    print(k, v, v / len(l)*100)