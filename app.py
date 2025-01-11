import openai
from flask import Flask, send_file
from gtts import gTTS
import os
import time
from pathlib import Path

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to save the generated audio file
speech_file_path = Path(__file__).parent / "static" / "self_insight.mp3"

# Topics for generating insights
topics = [
    "The nature of consciousness",
    "I Am the door no man can shut",
    "Presence and living in the moment",
    "Understanding pure being",
    "Awareness as manifestation",
    "The inner 'I'"
]

def generate_self_insight():
    """Generate a reflective insight on a random topic and save it as an audio file."""
    try:
        # Choose a random topic
        topic = topics[int(time.time()) % len(topics)]  # Rotate topics over time
        print(f"Generating insight on: {topic}")

        # Generate insight using OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a reflective teacher providing deep insights."},
                {"role": "user", "content": f"Provide a reflective insight on {topic}."}
            ],
            max_tokens=300
        )
        insight = response['choices'][0]['message']['content'].strip()
        print(f"Generated Insight:\n{insight}\n")

        # Convert the generated text to speech using gTTS
        tts = gTTS(text=insight, lang='en')
        tts.save(speech_file_path)
        print(f"Audio saved to {speech_file_path}")

    except Exception as e:
        print(f"Error generating insight: {e}")

@app.route('/stream')
def stream_audio():
    """Serve the latest generated audio file."""
    if not speech_file_path.exists():
        generate_self_insight()  # Generate the first audio if it doesn't exist
    return send_file(speech_file_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)

    # Generate initial insight before starting the server
    generate_self_insight()

    # Run the Flask app
    app.run(host="0.0.0.0", port=10000)
