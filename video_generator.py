import logging
import os
from typing import List

from moviepy.editor import *


def generate_video(base_folder: str, comments: List, output_video: str = "video.mp4"):
    screensize = (1080, 1920)
    margin = 0.5

    # Add audio
    audio_files = []
    title_audio = AudioFileClip(os.path.join(base_folder, "title.mp3"))
    for i in range(len(comments)):
        audio = AudioFileClip(os.path.join(base_folder, f"comment-{i}.mp3"))
        audio_start = title_audio.duration + margin
        if i:
            audio_start = audio_files[i - 1].start + audio_files[i - 1].duration + margin
        logging.debug(f"audio start [{i}]: {audio_start}")
        audio_files.append(audio.set_start(audio_start))

    # Add video
    video_images = []
    title_img = ImageClip("video_files/title.png").set_position(("center", "center")).set_duration(title_audio.duration)
    for i, audio in enumerate(audio_files):
        video = ImageClip(os.path.join(base_folder, f"comment-{i}.png")) \
            .set_position(("center", "center")) \
            .set_duration(audio.duration)

        video_start = title_audio.duration + margin
        if i:
            video_start = audio_files[i - 1].start + audio_files[i - 1].duration + margin
        video_images.append(video.set_start(video_start))

    video_clip = CompositeVideoClip([title_img] + video_images, size=screensize)

    composite_title_audio = CompositeAudioClip([title_audio] + audio_files)

    video_clip.audio = composite_title_audio
    video_clip.write_videofile(output_video, fps=25, codec='mpeg4')

