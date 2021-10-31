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
subreddit = reddit.subreddit("askreddit")


def get_reddit_text():
    logger.info("Starting to get reddit submission info...")
    title = ""
    comments = []
    submission = None
    got_comments = False
    for submission in subreddit.hot(limit=5):
        logger.info(f"title: {submission.title}")

        if submission.over_18:
            continue

        title = submission.title
        submission.comment_sort = "top"
        for top_level_comment in submission.comments[:3]:
            if isinstance(top_level_comment, MoreComments):
                continue
            logger.info(f"comment: {top_level_comment.body}, score:{top_level_comment.score}")
            comments.append(top_level_comment)
            got_comments = True

        if got_comments:
            break

    return title, comments, submission
