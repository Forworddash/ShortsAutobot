from django.conf import settings

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