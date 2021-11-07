import logging

from praw import Reddit
from praw.models import MoreComments

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

reddit = Reddit(
    client_id="t2YZA68CzGoOx9c0Vdl-DQ",
    client_secret="4t6H1VLFlHwiwzO0NxWt4aiL70hUzA",
    user_agent="reddit-stories",
)


def get_reddit_text(submission_url: str, number_of_comments: int = 3):
    logger.info("Starting to get reddit submission info...")
    submission = reddit.submission(url=submission_url)
    comments = []
    got_comments = False

    submission.comment_sort = "top"  # this needs to be on top, because if will fetch the submission with top comments
    title = submission.title

    if submission.over_18:
        raise Exception("Cannot parse over 18 submissions")

    for top_level_comment in submission.comments[:number_of_comments]:
        if isinstance(top_level_comment, MoreComments):
            continue
        logger.info(f"comment: {top_level_comment.body}, score:{top_level_comment.score}")
        comments.append(top_level_comment)
        got_comments = True

    if not got_comments:
        raise Exception("Couldn't get any comments")

    return title, comments, submission
