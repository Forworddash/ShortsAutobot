from celery import shared_task
from .models import Video
from .utils import get_hot_reddit_posts, text_to_speech, create_video_with_text_overlay, upload_to_instagram, upload_to_youtube

@shared_task
def create_and_post_videos():
    hot_posts = get_hot_reddit_posts(limit=5)
    for post in hot_posts:
        video = Video.objects.filter(status='pending').first()
        if video:
            text_to_speech(post['selftext'], 'audio.mp3')
            create_video_with_text_overlay(video.video_file.path, post['title'], 'output.mp4')
            youtube_url = upload_to_youtube('output.mp4', post['title'], post['selftext'])
            instagram_url = upload_to_instagram('output.mp4', post['title'])
            video.youtube_url = youtube_url
            video.instagram_url = instagram_url
            video.status = 'completed'
            video.save()