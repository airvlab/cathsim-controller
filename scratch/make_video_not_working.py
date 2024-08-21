from pathlib import Path

from cathsim_controller.camera import Camera
from moviepy.editor import ImageSequenceClip

FPS = 15
FILE_PATH = Path.cwd() / "movies"
FILE_PATH.mkdir(exist_ok=True)
FILE_NAME = "output_movie.mp4"


def main():
    camera = Camera(width=1280, height=720, fps=FPS)

    frames_directory = Path("frames")
    if not frames_directory.exists():
        frames_directory.mkdir()

    frames = []
    try: 
        while True:
            frames.append(camera.get_image())
    except KeyboardInterrupt:
        clip = ImageSequenceClip(frames, fps=FPS)
        clip.write_videofile((FILE_PATH / FILE_NAME).as_posix(), codec="libx264")


if __name__ == "__main__":
    main()
