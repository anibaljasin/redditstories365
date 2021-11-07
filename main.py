import os
import logging

import click

from reddit import get_reddit_text
from screenshot_generator import take_submission_title_screenshot, take_submission_comment_screenshot, \
    ScreenshotGenerator
from tts import generate_audio_from_text
from video_generator import generate_video

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@click.command()
@click.option('-u', '--url', required=True, help="Reddit submission url")
@click.option('-s', '--sort-type', default='top', help="Reddit submission sort type")
@click.option('-c', '--number-of-comments', default=3, help="Amount of comments to use from the reddit post")
@click.option('-b', '--background-video', default="assets/default.mp4", help="Background video to use")
@click.option('-f', '--base-folder', default="video_files", help="Base folder used to save screenshots and audio files")
def main(url: str, sort_type: str, number_of_comments: int, background_video: str, base_folder: str):
    logger.debug("Generating reddit title and comments")
    logger.warning(f"Using config: "
                   f"url:{url}, "
                   f"sort_type:{sort_type}, "
                   f"number_of_comments: {number_of_comments}, "
                   f"background_video: {background_video}, "
                   f"base_folder: {base_folder}")

    title, comments, submission = get_reddit_text(submission_url=url, number_of_comments=number_of_comments)
    screenshot_url = f"{submission.url}?sort={sort_type}"
    html_element_title_id = f"t3_{submission.id}"
    html_elements_comment_ids = [c.id for c in comments]

    logger.debug("Generating screenshots...")
    screenshot = ScreenshotGenerator(url=screenshot_url, base_folder=base_folder)
    screenshot.take_submission_title_screenshot(html_element_title_id=html_element_title_id)
    screenshot.take_submission_comment_screenshot(comments=html_elements_comment_ids)
    screenshot.quit_driver()

    logger.debug("Generating audio files...")
    generate_audio_from_text(title, os.path.join(base_folder, "title.mp3"))
    for i, comment in enumerate(comments):
        generate_audio_from_text(comment.body, os.path.join(base_folder, f"comment-{i}.mp3"))

    generate_video(comments=comments, background_video=background_video)


if __name__ == '__main__':
    logger.info("Starting to create video")
    main()
