# YouTube Video Translator with Voice

This project provides a web application that allows users to input a YouTube video URL, fetch its transcript, translate it into the user's preferred language, and generate a voice-over audio in the selected language. The goal is to help break language barriers and provide an immersive experience for global audiences.

## Key Features:
- **Transcript Extraction**: Automatically fetches the transcript of a YouTube video.
- **Multi-language Support**: Translates the transcript into multiple languages, including English, Spanish, French, German, Hindi, Tamil, and Arabic.
- **Voice-over Generation**: Converts the translated text into an audio file using Google Text-to-Speech (gTTS).
- **Seamless User Experience**: Users can listen to the translated audio and download it for offline use.

## Tech Stack:
- **Streamlit**: For building the web interface.
- **Pytube**: To extract YouTube video information and transcript.
- **Google Translate API**: For translating the transcript into the selected language.
- **gTTS (Google Text-to-Speech)**: To generate voice-over audio from the translated text.

## Installation:

### 1. Clone the repository:

```bash
git clone https://github.com/yourusername/youtube-video-translator-with-voice.git
cd youtube-video-translator-with-voice
