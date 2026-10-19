forEach = ["input", "output", "code", "test", "graphics"]
tasks = 10
src = r"C:\Users\vit\IdeaProjects\Olympiad26\src"

from pathlib import Path
import os

for task in range(tasks):
    task_pth = os.path.join(src, "task_" + str(task))
    print(task_pth)
    Path(task_pth).mkdir(parents=True, exist_ok=True)
    for sub in forEach:
        sub_pth = path = os.path.join(task_pth, sub)
        Path(sub_pth).mkdir(parents=True, exist_ok=True)

        if sub == "test":
            try:
                open(sub_pth + "/test_in.txt", "x")
                open(sub_pth + "/test_out.txt", "x")

            except FileExistsError:
                continue