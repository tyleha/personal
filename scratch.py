# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import praw
import time 

# <codecell>

def make_logger(name):
    """
    Make a logging instance that logs to both stdout and a log file.
    Min logging level is INFO for stdout, DEBUG for log file
    :name: the name of the log file (full path)
    """
    import logging
    fmt ='%(asctime)s -- %(levelname)-8s%(message)s'
    datefmt = '%m/%d/%Y %H:%M:%S'

    # create logger with 'spam_application'
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(name)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(fmt=fmt, datefmt=datefmt)
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

# <codecell>

def have_already_commented(comment):
    for subcomment in comment.replies:
        if subcomment.author.name == bot_name:
            return True
    return False

#### Constants and setup ####
log = make_logger("jensonbot_log")
bot_name = "Jenson_Botton"
bot_password = "pythonhsss"
string_to_match = " Jensen "
r = praw.Reddit(user_agent='Jenson_correction_and_education_bot')
r.login(bot_name, bot_password)
log.info("Successfully logged in")
post_text = """[Jensen](http://i.imgur.com/wGcGuLa.jpg)

[Jenson](http://i.imgur.com/uRnLTPt.jpg)

\"Teach the Controversy\""""

subredditName = 'formula1'
sub = r.get_subreddit(subredditName)
lookbackTime = time.mktime(time.gmtime()) - 60*60*24 #24 hours

#### The actual bot code ####
try:
    posts = [p for p in sub.get_new(limit=10)]
    # Find all posts since the "lookbackTime" (in seconds)
    while posts[-1].created_utc > lookbackTime:
        posts += [p for p in sub.get_new(params={"after":posts[-1].name})]
        
    log.info("Found %s posts in the last 24 hours"%len(posts))
    for post in posts:
        log.info("Looking at post %s"%post.title)
        submission = r.get_submission(submission_id=post.id)
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            if isinstance(comment, praw.objects.MoreComments):
                log.debug("This comment is actually a MoreComments?")
                continue
            if string_to_match.lower() in comment.body.lower():
                # Check to see if we've already replied to this comment, or if it's ours!
                if not have_already_commented(comment) and comment.author.name != bot_name:
                    log.info("Found new comment mentioning %s - comment id=%s"%(string_to_match, comment.id))
                    try:
                        comment.reply(post_text)
                        log.info("----------------------\nSuccessfully commented!\n----------------------")
                    except Exception as e:
                        log.error("Couldn't post a comment for some reason...")
                        log.exception(e)
                else: 
                    log.info("--------------------------\nalready replied to this comment or is ours, moving on\n"+
                        "-------------------------")
                    continue
except Exception as e:
    log.error("Ran into an unknown error")
    import pdb
    log.exception(e)

