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
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


hot_posts = [
    {'title': 'Multiple Spirits, Good and Bad in Apartment', 'url': 'https://www.reddit.com/r/Ghoststories/comments/1dncis2/multiple_spirits_good_and_bad_in_apartment/', 'selftext': "I moved to an apartment about a year ago. With my partner M(25), me F (22) and my daughter who is (1). We didn't have any sort of experience until 3 months after we moved in. We would hear creaking on the wooden floors but blamed it on heat. Doors shutting, but we blamed it on wind. Until one day my partner and his friend was over, we have a fan in our bedroom which was turned off. They both decided to go for a smoke and my partner entered our bedroom to make sure the fan was off, cause ya know, electricity bills and all. When they came back, the fan was on full high, and on the turn setting. So they both shrugged it off. The second time, me and my partner was getting ready to go to bed - by this point im in bed on my phone and he goes to the kitchen to take some medication til suddenly there was the most loudest bang on the floor. He runs in and he was like “WTF did you just hear that?” and I was said “what the fuck did you drop, your gonna wake our daughter up?” and he said “a fucking knife literally threw off the counter onto the other side of the kitchen” so we both run in and the knife was just there on the otherside. Just to add, my partner had a lot of experiences in his childhood home of some paranormal stuff going down and hasn’t since we moved here. That same night with the knife, I had a dream of these two shadow spirits trying to move me out of my apartment and i’m telling them to leave and they wouldn’t, they tried to hurt me and then I woke up, checked the baby monitor and my daughter was fine. I went back asleep, the same dream this time, my eyes are on the monitor staring right at the baby monitor. These two spirits, dark shadows. One was definitely a male, teenager, slim build, the other one was a little girl watching over him. This male shadow, kept sticking his hands into my daughter cot and I said “don’t you dare fucking touch her” and he kept pulling his hand away, putting it back in, pulling it out. Until he touched her, I immediately woke up and my daughter was SCREAMING. So me and my partner went into her, fed her she was fine. That same night, we woke up in the morning to find the monitor was disconnected - the baby monitor, when out of charge will make an alarm sound to alert you it’s about to die, we didn’t hear any of that. We checked the camera on my phone and she woke up multiple times, screaming, staring at the wall where the M teenager and the F girl was stood. Since after that, multiple things happen, orbs being caught on camera, shadows walking around her room and cot, flashing lights on the camera, her building blocks in her draw being messed with. Me and my daughter was home alone and we both fell asleep on the sofa, my mother was coming up from london, and she told me to keep an eye out for an amazon parcel that was getting delivered to my apartment. So whilst I was asleep, I dreamt of me and my daughter going to the lobby in our apartment and getting this amazon parcel, I walk back to the lift and a woman comes next to me who i’ve never seen before and she says to me “If you want to see him, go to floor 6” and I was like “see who?”. “If you want to see the demon, go to floor 6” and I immediately woke up to my doorbell going off by my mother waiting for me to open the door. The same things happened again, multiple things going on in my daughter’s room and by this point we contacted our local church for a house blessing. We learnt about the apartment blocks being built on what used to be a massive church and several graveyards, which one of them are still there at the top of the gardens by the shops, which are from the 1600s, 1800s. After the house blessing we did get a couple of weird things like the building blocks being played with but nothing since. Until the past couple weeks after the blessing the apartment still has something here and I can feel it. Same how it started with the creaking, things suddenly falling on the floor, the door handle on the front door being messed with."},
    {'title': 'I just want to share my experience', 'url': 'https://www.reddit.com/r/Ghoststories/comments/1dm7atm/i_just_want_to_share_my_experience/', 'selftext': 'My house is a semi detached house, my neighbour had a son who was 21 when he committed sucide nearly 2 years ago at the start of winter. His son grew up in that house as a child and has spend a large amount of his life there. At the start of winter this year it was 8pm at night I was upstairs watching TV in my bedroom (my bedroom is opposite his dad’s bedroom). I heard a lot of noise coming from his dad’s bedroom the noise was of movement. The noise was so loud I could hear it over the Tv. So I messaged my neighbour asking him what he was doing he said it was nothing to do with him. The noise then travelled downstairs into my front room, I then heard a man walking up every step of my stairs and across the landing. I know it was a man because of how heavy the footsteps were on the stairs yet there was no one in the house (my stairs and landing are wooden and creek). I then heard the wooden bed creek in the other bedroom (the bed was near a wardrobe with a very narrow gap to walk through his son was very broad so I believed he bumped the bed because he didn’t release how narrow the gap was) and the noise disappeared. The bedroom the noise disappeared in is opposite his son’s bedroom. I also have a dog that didn’t once react to the sound. I very strongly believe his son’s ghost was here that night I also believe he will be drawn to the house while his father is still here on earth.'},
]

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
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
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


