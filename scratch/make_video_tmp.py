from pathlib import Path

from cathsim_controller.camera import Camera
from cathsim_controller.utils import videos_path
import cv2

FPS = 15
FILE_PATH = videos_path
FILE_PATH.mkdir(exist_ok=True)
FILE_NAME = "make_video.mp4"


def main():
    camera = Camera(width=1280, height=720, fps=FPS)
    fourcc=cv2.VideoWriter_fourcc(*'mp4v')
    out=cv2.VideoWriter(FILE_PATH/FILE_NAME,fourcc,FPS,(1280,720))

    frames_directory = Path("frames")
    if not frames_directory.exists():
        frames_directory.mkdir()

    try: 
        while True:
            frame=camera.get_image()
            if frame is not None:
                out.write(frame)
                cv2.imshow('Image',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
