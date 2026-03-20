import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


import os
from dotenv import load_dotenv
load_dotenv()
# Initialize LLM
llm=ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4o", temperature=0.5)

# Initialize Prompt for Summarization

prompt=PromptTemplate(
     input_variables=["transcript"],
    template="""
You are an expert Summarizer. Here is the video transcript:
{transcript}
Please generate a clear and concise summary of the main points and topics
"""
)

# LLM Chain creation
chain =  prompt | llm


# Streamlit UI


st.title("Youtube Vide Summarizer")

# Streamlit UI

video_url=st.text_input("Enter an Youtube Video URL:")
ytt_api = YouTubeTranscriptApi()

def get_video_id(url):
    """Entract Video ID from URL"""
    parsed_url=urlparse(url)
    if parsed_url.hostname == 'youtu.be':
            return parsed_url.path[1:]
    elif parsed_url.hostname in( 'www.youtube.com', 'youtube.com'):
          query=parse_qs(parsed_url.query)
          return query.get('v',[None])[0]
    
    return None

if st.button("Summarize"):
    if not video_url:
            st.warning("Enter a valid Youtube Video URL")

    else:
        video_id=get_video_id(video_url)
        
        if not video_id:
            st.error("Invalid Video URL")
        else:
            try:
                #transcript_list=ytt_api.get_transcript(video_id)
                transcript = ytt_api.list(video_id)
                # Pick English transcript (or first available)
                transcript_obj = transcript.find_transcript(['en'])
                # Fetch actual transcript data
                transcript_data = transcript_obj.fetch()


                # Extract text
                full_text = " ".join([item.text for item in transcript_data])
                summary=chain.invoke({"transcript": full_text})
                st.subheader("Video Summary")
                st.write(summary)
            except Exception as e:
                 st.error(f"Error : {str(e)}")  



                  
            


