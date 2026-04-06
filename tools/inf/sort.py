import random
import time

class UnsortedArrayError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Timer:
    def __init__(self):
        self.time_s = 0
    
    def start(self):
        self.time_s = time.time()

    def end(self) -> float:
        return round((time.time() - self.time_s)*1000, ndigits=5)


class Sort:
    def check_if_sorted(input_list:list[int|float])->bool:
        for n in range(len(input_list) - 1):
            if input_list[n] <= input_list[n+1]:
                pass
            else: 
                raise UnsortedArrayError(f"Array: {input_list} at {n}: {input_list[n]}x{input_list[n+1]}")
        return True
    def gen_random_array(n:int, m:int|float)->list[int|float]:
        return [random.randint(0,m) for _ in range(n)]
    
    def sort_1(input_list:list[int|float])->list[int,float]:
        """complexity: o²/2 -> n(n + 1) / 2"""
        n = len(input_list)
        for i in range(n-1):
            sord = True
            for ii in range(n-i-1):
                a, b = input_list[ii], input_list[ii+1]
                if a>b:#swich ii and ii+1
                    input_list[ii], input_list[ii+1] = b, a
                    sord = False
            if sord:
                break
        
        return input_list

tmr = Timer()
for _ in range(1000):
    
    a1 = Sort.gen_random_array(1000, 1000)
    
    tmr.start()
    Sort.sort_1(a1)
    print(f"miliseconds: {tmr.end()}")
    
    print(Sort.check_if_sorted(a1))

