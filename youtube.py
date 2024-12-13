import streamlit as st
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from googletrans import Translator
from gtts import gTTS
import os
import tempfile

# Function to fetch the transcript using youtube-transcript-api
def fetch_transcript(youtube_url, language_code="en"):
    try:
        video_id = YouTube(youtube_url).video_id
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code, "en"])
        return " ".join([entry['text'] for entry in transcript])
    except TranscriptsDisabled:
        st.error("This video does not have transcripts enabled.")
        return None
    except NoTranscriptFound:
        st.error("No transcripts were found for this video.")
        return None
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

# Function to translate text
def translate_text(text, target_language):
    # Add more robust input validation
    if not text:
        st.error("No text provided for translation.")
        return None
    
    # Ensure text is a string
    if not isinstance(text, str):
        st.error(f"Expected string for translation, got {type(text)}")
        return None

    # Split long texts to avoid translation limits
    max_chunk_size = 5000  # Adjust based on translation service limits
    text_chunks = [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]
    
    translator = Translator()
    try:
        # Translate each chunk
        translated_chunks = []
        for chunk in text_chunks:
            st.write(f"Translating chunk: {chunk[:100]}...")  # Log first 100 chars of chunk
            translated_chunk = translator.translate(chunk, dest=target_language)
            translated_chunks.append(translated_chunk.text)
        
        # Combine translated chunks
        full_translated_text = " ".join(translated_chunks)
        
        st.write(f"Full translation preview: {full_translated_text[:200]}...")  # Log preview
        return full_translated_text
    
    except Exception as e:
        st.error(f"Error translating text: {e}")
        # Log more details about the error
        st.error(f"Text type: {type(text)}")
        st.error(f"Text length: {len(text) if text else 'N/A'}")
        return None

# Function to generate audio from text
def generate_audio(text, language_code):
    try:
        tts = gTTS(text=text, lang=language_code)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts.save(temp_file.name)
        return temp_file.name
    except Exception as e:
        st.error(f"Error generating audio: {e}")
        return None

# Streamlit UI
st.title("YouTube Video Translator with Voice")
st.write("Provide a YouTube link, and this app will fetch the transcript, translate it, and generate audio in the desired language.")

# Input fields
youtube_url = st.text_input("Enter YouTube video URL:")
target_language = st.selectbox(
    "Select the language for translation and audio:",
    [("English", "en"), ("Spanish", "es"), ("French", "fr"), ("German", "de"), ("Hindi", "hi"), ("Tamil", "ta"), ("Arabic", "ar")],
    format_func=lambda x: x[0]
)

if st.button("Process"):
    if not youtube_url:
        st.error("Please enter a valid YouTube URL.")
    else:
        # Reset any previous temporary files
        import glob
        for f in glob.glob("/tmp/*.mp3"):
            os.unlink(f)
        
        # Display the YouTube video
        try:
            st.video(youtube_url)
        except Exception as e:
            st.error(f"Error displaying video: {e}")
        
        st.write("Fetching transcript...")
        transcript = fetch_transcript(youtube_url)
        if transcript:
            st.success("Transcript fetched successfully!")
            st.text_area("Original Transcript:", transcript, height=200)
            st.write("Translating transcript...")
            target_language_code = target_language[1]
            
            # Debug print to verify transcript
            st.write(f"Transcript type: {type(transcript)}")
            st.write(f"Transcript length: {len(transcript)}")
            st.write(f"First 100 characters: {transcript[:100]}")
            
            translated_text = translate_text(transcript, target_language_code)
            if translated_text:
                st.success("Transcript translated successfully!")
                st.text_area("Translated Transcript:", translated_text, height=200)
                st.write("Generating audio...")
                audio_file = generate_audio(translated_text, target_language_code)
                if audio_file:
                    st.success("Audio generated successfully!")
                    st.audio(audio_file, format="audio/mp3")
                    st.write("Download the audio file below:")
                    with open(audio_file, "rb") as file:
                        st.download_button("Download Audio", file, file_name="translated_audio.mp3")
                    
                    # Optional: Clean up the temporary file after download
                    os.unlink(audio_file)