import streamlit as st
import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

st.title("Speech Recognition App (File-Based, No Microphone Needed)")

# Upload audio file
audio_file = st.file_uploader("Upload an audio file (wav or flac)", type=["wav", "flac"])

# Select language
language = st.selectbox("Select language", ["en-US", "fr-FR", "es-ES", "de-DE"])

# Select API
api_choice = st.selectbox("Select API", ["Google", "Sphinx"])

if audio_file is not None:
    # Save uploaded file temporarily
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.getbuffer())

    # Process audio
    with sr.AudioFile("temp_audio.wav") as source:
        audio_data = recognizer.record(source)
        try:
            if api_choice.lower() == "google":
                text = recognizer.recognize_google(audio_data, language=language)
            elif api_choice.lower() == "sphinx":
                text = recognizer.recognize_sphinx(audio_data, language=language)
            else:
                text = recognizer.recognize_google(audio_data, language=language)
            
            st.success("Transcription successful!")
            st.text_area("Transcribed Text", value=text, height=200)

            # Option to save
            if st.button("Save Transcription"):
                with open("transcription.txt", "w", encoding="utf-8") as f:
                    f.write(text)
                st.success("Transcription saved as transcription.txt")
            
        except sr.UnknownValueError:
            st.error("Could not understand the audio.")
        except sr.RequestError as e:
            st.error(f"API request failed: {e}")
