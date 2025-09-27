import streamlit as st
import whisper

# Load Whisper model
model = whisper.load_model("base")

st.title("Speech Recognition App (File-Based with Whisper)")

st.write("""
Upload a `.wav` or `.flac` audio file, and get the transcribed text using OpenAI's Whisper model.
""")

# Upload audio file
audio_file = st.file_uploader("Upload audio file", type=["wav", "flac"])

if audio_file is not None:
    # Save uploaded file temporarily
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_file.getbuffer())

    # Load and process the audio file
    audio = whisper.load_audio("temp_audio.wav")
    audio = whisper.pad_or_trim(audio)

    # Make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Detect language
    _, probs = model.detect_language(mel)
    st.write(f"Detected language: {max(probs, key=probs.get)}")

    # Decode the audio
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)

    st.success("Transcription successful!")
    st.text_area("Transcribed Text", value=result.text, height=200)

    # Option to save the transcription
    if st.button("Save Transcription"):
        with open("transcription.txt", "w", encoding="utf-8") as f:
            f.write(result.text)
        st.success("Transcription saved as transcription.txt")
