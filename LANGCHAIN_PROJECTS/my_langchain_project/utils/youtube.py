from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_id):
    try:
        ytt_api = YouTubeTranscriptApi()

        transcript = ytt_api.list(video_id)
        transcript_obj = transcript.find_transcript(['en'])
        transcript_data = transcript_obj.fetch()
        full_text = " ".join([item.text for item in transcript_data])
        return full_text
    

    except Exception as e:
        return f"Error fetching transcript: {str(e)}"