from functools import lru_cache
import time

print("hello")

@lru_cache(maxsize=None)
def compositions_iter(n):
    dp = [[] for _ in range(n+1)]
    dp[0] = [()]  # base case
    for i in range(1, n+1):
        for k in range(1, i+1):
            for comp in dp[i - k]:
                dp[i].append(comp + (k,))
    return dp[n]

for x in range(100):
    start = time.time()

    all_combinations = compositions_iter(x)

    end = time.time()
    print(f"{x}:{end - start}")
