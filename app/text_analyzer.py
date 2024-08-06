from transformers import pipeline
from text_processing import preprocess_text

# Load the pre-trained language model for text classification
classifier = pipeline('text-classification', model='distilbert-base-uncased-finetuned-sst-2-english')

def analyze_video_text(title, description, comments):
    # Preprocess the title and description
    clean_title = preprocess_text(title)
    clean_description = preprocess_text(description)
    
    # Combine the title, description, and comments into a single text
    video_text = f"{clean_title} {clean_description} {' '.join(comments)}"
    
    # Use the pre-trained language model to classify the text
    result = classifier(video_text)[0]
    
    # Check if the text is classified as potentially unsafe
    if result['label'] == 'NEGATIVE':
        safety_score = result['score']
        if safety_score >= 0.7:  # Adjust the threshold as needed
            return "Potentially unsafe for children"
    
    return "Safe for children"