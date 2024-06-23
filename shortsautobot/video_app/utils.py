from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from django.conf import settings
from dotenv import load_dotenv
from instabot import Bot
from gtts import gTTS
import os

# load in env variables here
load_dotenv()

# initialize the environment variables here for usage in this file
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Get hot posts from a subreddit (in this case, we are using 'all' to get posts from all subreddits)
def get_hot_reddit_posts(subreddit='all', limit=5):
    posts = []
    for submission in settings.reddit.subreddit(subreddit).hot(limit=limit):
        posts.append({
            'title': submission.title,
            'url': submission.url,
            'seftext': submission.selftext,
            ## Test variables below for future Usage
            # 'score': submission.score,
            # 'num_comments': submission.num_comments,
            # 'created_at': submission.created_utc,
            # 'author': submission.author.name if submission.author else '[deleted]'

        })
    return posts

# Convert text to speech
def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)

# Create a video with text overlay
def create_video_with_text_overlay(video_path, text, output_path):
    video = VideoFileClip(video_path)
    txt_clip = TextClip(text, fontsize=24, color='white')
    txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(video.duration)
    video = CompositeVideoClip([video, txt_clip])
    video.write_videofile(output_path, codec='libx264')

# Upload video to Instagram
def upload_to_instagram(video_path, caption):
    bot = Bot()
    bot.login(username=INSTAGRAM_USERNAME, password=INSTAGRAM_PASSWORD)
    bot.upload_video(video_path, caption=caption)

# Upload to YouTube
def upload_to_youtube(video_path, title, description, tags):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': 22
        },
        'status': {
            'privacyStatus': 'public'
        }
    }
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    )
    response = request.execute()
    return response.get('id')