

class Car:
    def __init__(self):
        self.actions = []
        self.functions = self.Functions(self)

    def add_action(self,a):
        self.actions.append(a)

    class Functions:
        def __init__(self, car:Car):
            self.car = car

        def honk(self):
            self.car.add_action("honk")

car1 = Car()
car1.functions.honk()
print(car1.actions)