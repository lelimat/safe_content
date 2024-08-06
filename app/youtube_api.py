from googleapiclient.discovery import build
from text_processing import preprocess_text

# Set up YouTube API client
api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

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