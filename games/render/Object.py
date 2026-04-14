import random

liste1 = [random.randint(0,5)*"67" for i in range(100)]
print(liste1)

for i in range(len(liste1)):
    print(i, liste1[i])