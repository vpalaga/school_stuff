from typing import List
import random


class Person:
    def __init__(self, name:str, age:int):
        self.name = name
        self.age = age
    def __eq__(self, other):
        if isinstance(other, Person):
            if other.name == self.name and other.age == self.age:
                return True
        return False

    def __repr__(self):
        return f"person: {self.name} age: {self.age}"

class ClassRoom:
    def __init__(self, teacher:Person):
        self.members: List[Person] = []
        self.teacher = teacher
    def __repr__(self):
        return f"{self.members}"
    def __setitem__(self, key:int, value:Person):
        self.members[key] = value
    def __getitem__(self, item):
        return self.members[item]
    def __iter__(self):
        return self.members.__iter__()
    def __delitem__(self, key):
        del self.members[key]
    def __contains__(self, item):
        for member in self.members:
            if member == item:
                return True
        return False

class Generator:
    def __init__(self):
        self.names = open("first-names.txt", "r").readlines()
        self.names_len = self.names.__len__()

    def random_person(self)->Person:
        name = self.names[random.randint(0, self.names_len - 1)].strip()
        age = random.randint(4,89)
        return Person(name,age)

    def random_classroom(self, members_len:int)->ClassRoom:
        classroom = ClassRoom(teacher=self.random_person())

        classroom.members = [self.random_person() for _ in range(members_len)]
        return classroom


if __name__ == "__main__":
    gen = Generator()

    c = gen.random_classroom(5)

    for member in c:
        print(member)
