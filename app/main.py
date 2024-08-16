from video_analyzer import analyze_video_mood
from text_analyzer import analyze_video_text
from youtube_api import fetch_video_info, fetch_video_comments

from flask import Flask, render_template, request, send_file
import os
import datetime

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET', 'POST'])
def index():
    video_url = ''
    if request.method == 'POST':

        video_url = request.form.get('video_url')

        print('video_url', video_url)

    else:
        return render_template('index.html', error='')
        
    if video_url:
        is_valid, video_ids = check_youtube_link(video_url)
        if not is_valid:
            return render_template('index.html', error='Invalid YouTube link: ' + video_url)
        
        for i,video_id in enumerate(video_ids[:4], start=1): # REMOVE "video_ids" slicing [:4] - JUST FOR TESTING!!

            raw_text = ''

            try:
                transcript_parts = download_youtube_transcript(video_id)
                for transcript_part in transcript_parts:
                    raw_text += transcript_part['text'] + ' '
                raw_text += '\n\n'

            except: # (TranscriptsDisabled, NoTranscriptFound):
                failed_transcripts += [video_id]
                # transcript_text = "Transcript not available for this video."
                # return render_template('transcript.html', transcript=transcript_text, video_id=video_id)

            chapters.append(
                {
                    'number': i,
                    'title' : get_youtube_title(video_id),
                    'text' : raw_text,
                }
            )

            # if video_id:
            #     save_submission(video_id)  # Save the video ID and the date
            #     return redirect(url_for('transcript', video_id=video_id))
            

        if chapters:

            book_path = process_chapters(book_title=book_title, chapters=chapters, failed_transcripts=failed_transcripts, prompt=prompt)

            # return redirect(url_for('process_chapters', book_title=book_title, chapters=chapters, failed_transcripts=failed_transcripts))
            return render_template('download_book.html', book_path=book_path)

    return render_template('index.html', error='')




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