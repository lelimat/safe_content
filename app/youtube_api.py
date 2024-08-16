import subprocess
from googleapiclient.discovery import build
from text_processing import preprocess_text
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import json
import re

# Set up YouTube API client
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

def is_valid_youtube_url(url):
    """Check if the URL is a valid YouTube URL."""
    youtube_regex = (
        r'(https?://)?(www\.)?'
        '(youtube|youtu|youtube-nocookie)\.(com|be)/'
        '(watch\?v=|embed/|v/|.+\?v=|youtu\.be/)?([^&=%\?]{11})')
    return re.match(youtube_regex, url)


def extract_video_id(url):
    """Extract the YouTube video ID from the URL."""
    patterns = [
        r'(?:https?://)?(?:www\.)?youtube\.com/watch\?v=([a-zA-Z0-9_-]{11})', # Standard URL
        r'(?:https?://)?youtu\.be/([a-zA-Z0-9_-]{11})',                       # Short URL
        r'(?:https?://)?(?:www\.)?youtube\.com/v/([a-zA-Z0-9_-]{11})',        # Embed URL
        r'(?:https?://)?(?:www\.)?youtube\.com/embed/([a-zA-Z0-9_-]{11})',    # Another Embed URL
        r'(?:https?://)?youtube\.com/shorts/([a-zA-Z0-9_-]{11})'              # Shorts URL
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


def get_playlist_video_ids(playlist_url):
    # Running yt-dlp as a subprocess
    command = ["yt-dlp", "-j", "--flat-playlist", playlist_url]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()

    # Extracting video IDs from the output
    video_ids = []
    for line in out.splitlines():
        video_data = json.loads(line)
        video_ids.append(video_data.get('id'))

    return video_ids


def check_youtube_link(link):
    video_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/watch\?v=[\w-]+'
    playlist_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.?be)/playlist\?list=[\w-]+'

    if re.match(video_pattern, link):
        print('video_id', extract_video_id(link))
        return True, [extract_video_id(link)]
    elif re.match(playlist_pattern, link):
        print('video_ids', get_playlist_video_ids(link))
        return True, get_playlist_video_ids(link)
    else:
        return False, "This is not a valid YouTube video link."


def download_youtube_transcript(video_id):

    try:
        # Attempt to download the transcript
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # transcript = transcript_list.find_transcript(['en']).fetch()
        for transcript in transcript_list:
            #transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript = transcript_list.find_transcript([transcript.language_code]).fetch()
            print('transcript:', transcript[0]['text'][:100])

            return transcript

    except (TranscriptsDisabled, NoTranscriptFound):
        # If no transcript available, use Whisper for transcription
        return f"No transcript found for video {video_id}"




"""
def fetch_video_info(video_id):
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    
    video_info = response['items'][0]['snippet']
    return {
        'title': video_info['title'],
        'description': video_info['description']
    }

def fetch_video_comments(video_id):
    comments = []
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        maxResults=100,
        textFormat='plainText'
    ).execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
        comments.append(preprocess_text(comment))

    return comments

"""