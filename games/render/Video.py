import imageio

from pathlib import Path


class Video:
    def __init__(self,fps=60):
        self.fps = fps
        self.output_dir = "games/render/outputs"

        directory = Path(self.output_dir)
        files = []

        for file in directory.iterdir():
            if file.is_file():
                try:
                     files.append(int(file.name.split(".")[0]))

                except ValueError:
                    continue

        self.number = max(files) + 1
        print(f"{self.number=}")

    def render(self, frames):
        imageio.mimsave(f"{self.output_dir}/{self.number}.mp4", frames, fps=self.fps)