from moviepy.editor import *
from moviepy.video.fx.crop import crop
from moviepy.video.fx.loop import loop

screensize = (1080, 1920)
screen_width, screen_height = screensize


def crop_video(bg_video: str = "sea.mp4", output_file: str = "bg_video2.mp4"):
    clip = VideoFileClip(bg_video)

    width, height = clip.size
    x_start = (width // 2) - (screen_width // 2)
    cropped_clip = crop(clip, x1=x_start, width=screen_width, y1=0, height=screen_height)

    cropped_clip.write_videofile(output_file, fps=25)

