import random
import time
c = "                           アァカサタナハマヤャラワガザダバパイィキシチニヒミリヰギジヂビピウゥクスツヌフムユュルグズブヅプエェケセテネヘメレヱゲゼデベペオォコソトノホモヨョロヲゴゾドボポヴッン"
c = list(c)

n = "0123456789"
n= list(n)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


while True:
    if random.randint(0,10) > 1:
        chr = random.choice(c)
    else:
        chr = random.choice(n)
    chr = bcolors.OKGREEN + chr + bcolors.ENDC

    if random.randint(0,100) < 2:
        print(chr)
    else:
        print(chr, end="", flush=True)
    time.sleep(0.01)