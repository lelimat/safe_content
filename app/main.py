from video_analyzer import analyze_video_mood
from text_analyzer import analyze_video_text
from youtube_api import fetch_video_info, fetch_video_comments

def main():
    video_id = 'VIDEO_ID'
    video_info = fetch_video_info(video_id)
    
    video_title = video_info['title']
    video_description = video_info['description']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Download the video (replace with your preferred method)
    video_path = 'path/to/downloaded/video.mp4'
    
    comments = fetch_video_comments(video_id)
    text_safety_analysis = analyze_video_text(video_title, video_description, comments)
    video_mood_analysis = analyze_video_mood(video_path)
    
    print("Text Safety Analysis:", text_safety_analysis)
    print("Video Mood Analysis:", video_mood_analysis)

if __name__ == "__main__":
    main()