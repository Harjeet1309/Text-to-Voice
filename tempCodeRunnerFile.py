from flask import Flask, render_template, request, send_file
import os
from gtts import gTTS
import subprocess

app = Flask(__name__)

UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to generate AI voice from text
def generate_audio(news_text):
    audio_file = os.path.join(UPLOAD_FOLDER, "news_audio.mp3")
    tts = gTTS(text=news_text, lang="en", slow=False)
    tts.save(audio_file)
    return audio_file

# Function to run Wav2Lip for lip-syncing
def generate_lip_sync(video_file, audio_file):
    output_video = os.path.join(UPLOAD_FOLDER, "output_news.mp4")
    command = [
        "python", "inference.py",
        "--checkpoint_path", "checkpoints/wav2lip.pth",
        "--face", video_file,
        "--audio", audio_file,
        "--outfile", output_video
    ]
    subprocess.run(command)
    return output_video

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        news_text = request.form["news_text"]
        
        # Generate AI voice
        audio_file = generate_audio(news_text)

        # Use a sample video of a news anchor (Replace with your own)
        video_file = "sample_news_anchor.mp4"

        # Generate Lip-Synced Video
        output_video = generate_lip_sync(video_file, audio_file)

        return send_file(output_video, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
