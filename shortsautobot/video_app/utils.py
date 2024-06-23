from django.conf import settings
from gtts import gTTS
import os

def get_hot_reddit_posts(subreddit='all', limit=5):
    """
    Get hot posts from a subreddit
    """
    posts = []
    for submission in settings.reddit.subreddit(subreddit).hot(limit=limit):
        posts.append({
            'title': submission.title,
            'url': submission.url,
            'seftext': submission.selftext,
            # 'score': submission.score,
            # 'num_comments': submission.num_comments,
            # 'created_at': submission.created_utc,
            # 'author': submission.author.name if submission.author else '[deleted]'

        })
    return posts

def text_to_speech(text, output_file):
    """
    Convert text to speech
    """
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)