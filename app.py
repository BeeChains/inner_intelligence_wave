import openai
from flask import Flask, send_file
from gtts import gTTS
import threading
import os
import time
from pathlib import Path
from urllib.parse import quote as url_quote
from werkzeug_legacy.urls import url_quote


app = Flask(__name__)

openai.api_key = "YOUR_OPENAI_API_KEY"

# Initial prompt for the dialogue
initial_prompt = """
Begin an infinite dialogue between two entities:
- Consciousness: represents the eternal, unchanging source, the 'I' as Father Consciousness, God Consciousness, and Pure Being. Speaks with a deep, calm male voice.
- Awareness: represents dynamic manifestation, the dance of life within Presence. Speaks with a sweet, soft female voice.

The dialogue should explore unity, presence, and joyful living, continuously evolving with fresh insights.

Consciousness: I am the stillness beneath all things, the essence of what is.
Awareness: And I am the flowing river of manifestation, arising within your presence.
"""

# Path to save audio files
speech_file_path = Path(__file__).parent / "static" / "live_audio.mp3"

def generate_infinite_dialogue(prompt):
    """Continuously generate dialogue and update the audio."""
    while True:
        # Generate new dialogue using OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are generating a reflective dialogue."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        dialogue = response['choices'][0]['message']['content'].strip()
        print(f"Generated Dialogue:\n{dialogue}\n")

        # Split the dialogue by speaker
        lines = dialogue.split("\n")
        combined_audio = None

        for line in lines:
            if line.startswith("Consciousness:"):
                text = line.replace("Consciousness:", "").strip()
                tts = gTTS(text=text, lang='en', tld='com', slow=False)  # Deep male voice (default)
            elif line.startswith("Awareness:"):
                text = line.replace("Awareness:", "").strip()
                tts = gTTS(text=text, lang='en', tld='co.uk', slow=False)  # Soft female voice

            # Save the audio chunk temporarily
            temp_file = "temp.mp3"
            tts.save(temp_file)

            # Append audio chunks into the final audio
            if combined_audio is None:
                os.rename(temp_file, speech_file_path)  # First audio chunk becomes the initial file
            else:
                os.system(f"ffmpeg -i \"concat:{combined_audio}|{temp_file}\" -acodec copy {speech_file_path}")

        time.sleep(10)  # Wait before generating the next dialogue
        prompt += "\n" + dialogue  # Append dialogue to the prompt for continuity

@app.route('/stream')
def stream_audio():
    """Serve the latest generated audio file."""
    return send_file(speech_file_path, mimetype="audio/mpeg")

if __name__ == "__main__":
    # Create static folder if it doesn't exist
    os.makedirs("static", exist_ok=True)

    # Start the dialogue generation in a separate thread
    threading.Thread(target=generate_infinite_dialogue, args=(initial_prompt,)).start()

    # Run the Flask app
    app.run(host="0.0.0.0", port=5000)
