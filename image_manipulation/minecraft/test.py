import pickle

with open("outputs/3.png.pkl", "rb") as f:
    my_dict = pickle.load(f)

print(my_dict)