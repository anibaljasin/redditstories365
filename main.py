import logging

from reddit import get_reddit_text
from screenshot_generator import take_submission_title_screenshot, take_submission_comment_screenshot
from tts import generate_audio_from_text
from video_generator import generate_video

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    logger.info("Generating reddit title and comments")
    subreddit = "askreddit"

    title, comments, submission = get_reddit_text()
    url = f"{submission.url}?sort=top"
    html_element_id = f"t3_{submission.id}"
    take_submission_title_screenshot(url=url, html_element_id=html_element_id, base_folder="video_files")
    take_submission_comment_screenshot(url=url, comments=comments, base_folder="video_files")

    logger.info("Generating audio files")
    generate_audio_from_text(title, "video_files/title.mp3")
    for i, comment in enumerate(comments):
        generate_audio_from_text(comment.body, f"video_files/comment-{i}.mp3")

    generate_video("video_files", comments, "video_files/video.mp4")


if __name__ == '__main__':
    logger.info("Starting to create video")
    main()