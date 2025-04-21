import requests
import os
from gtts import gTTS
from tkinter import Tk, filedialog
import ffmpeg
from transformers import pipeline
import torch  # To check GPU availability

# 🔐 API Keys (Replace with your own where needed)
DID_API_KEY = "your_did_api_key"
RUNWAY_API_KEY = "your_runway_api_key"

# 🖼️ Open file dialog to choose images
def choose_image(prompt_text):
    root = Tk()
    root.withdraw()
    print(prompt_text)
    file_path = filedialog.askopenfilename(
        title=prompt_text, filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
    )
    return file_path

# ✍️ Generate story using Hugging Face model (GPT-Neo)
def generate_story(animal, location):
    prompt = f"Mylo the dog will meet a {animal} in the {location}. What will happen?"
    print(f"Generating story with prompt: {prompt}")

    # Set device for Hugging Face model to use GPU if available, else CPU
    device = 0 if torch.cuda.is_available() else -1  # Use GPU if available, otherwise CPU
    print(f"Device set to: {'GPU' if device == 0 else 'CPU'}")

    try:
        generator = pipeline("text-generation", model="EleutherAI/gpt-neo-1.3B", device=device)
        
        # Explicit truncation enabled and handling padding token
        result = generator(prompt, max_length=200, do_sample=True, temperature=0.8, truncation=True, pad_token_id=50256)
        
        generated_text = result[0]['generated_text']
        print(f"Generated story: {generated_text}")
        return generated_text
    except Exception as e:
        print("Error generating story:", e)
        return "Sorry, I couldn't generate the story."

# 🔊 Convert story to speech
def text_to_speech(text, filename="voice.mp3"):
    tts = gTTS(text, lang="en")
    tts.save(filename)

# 🗣️ Animate character talking using D-ID
def animate_character(image_path, voice_path):
    uploaded_image_url = "file://" + os.path.abspath(image_path)  # Local path for image
    uploaded_audio_url = "file://" + os.path.abspath(voice_path)  # Local path for audio

    url = "https://api.d-id.com/talks"
    headers = {
        "Authorization": f"Bearer {DID_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "source_url": uploaded_image_url,
        "audio_url": uploaded_audio_url
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json().get("result_url", "No result URL returned")
    except Exception as e:
        print(f"Error in character animation: {e}")
        return "Error generating character animation"

# 🌌 Generate portal animation using RunwayML
def generate_portal_animation():
    url = "https://api.runwayml.com/v1/generate/video"
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": "A glowing magical portal opens with swirling blue and purple energy, cinematic style",
        "fps": 24,
        "duration": 4
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json().get("video_url", "No video URL returned")
    except Exception as e:
        print(f"Error generating portal animation: {e}")
        return "Error generating portal animation"

# 🎬 Generate scene video
def generate_ai_video(scene_prompt):
    url = "https://api.runwayml.com/v1/generate/video"
    headers = {
        "Authorization": f"Bearer {RUNWAY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": scene_prompt,
        "fps": 24,
        "duration": 5
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json().get("video_url", "No video URL returned")
    except Exception as e:
        print(f"Error generating scene video: {e}")
        return "Error generating scene video"

# 🎞️ Merge audio with video
def merge_video_audio(video_path, audio_path, output_path="final_video.mp4"):
    try:
        ffmpeg.input(video_path).output(output_path, v=1, a=1, acodec='aac', vcodec='libx264', strict='experimental').run(overwrite_output=True)
        print(f"✅ Video and audio merged: {output_path}")
    except Exception as e:
        print(f"Error merging video and audio: {e}")

# 🚀 Main program
if __name__ == "__main__":
    # Check if GPU is available
    if torch.cuda.is_available():
        print("GPU is available")
    else:
        print("GPU is NOT available")

    # Check which device will be used (0 for GPU, -1 for CPU)
    device = 0 if torch.cuda.is_available() else -1
    print(f"Device set to use: {'GPU' if device == 0 else 'CPU'}")

    # Paths for images and final output video
    downloads_folder = os.path.expanduser('~/Downloads')
    mylo_image_path = os.path.join(downloads_folder, "milo.jpeg")  # Choose your image path here
    output_video_path = os.path.join(downloads_folder, "final_video.mp4")

    animal = "Lion"  # You can set these values directly or ask user input
    location = "forest"  # You can set these values directly or ask user input

    # 1. Generate story
    story = generate_story(animal, location)
    print("\n📖 Generated Story:\n", story)

    # 2. Convert story to voice
    voice_path = os.path.join(downloads_folder, "voice.mp3")
    text_to_speech(story, filename=voice_path)

    # 3. Animate characters (D-ID)
    animated_mylo = animate_character(mylo_image_path, voice_path)
    print("\n🎥 Mylo Video URL:", animated_mylo)

    # 4. Generate scene animation
    scene_description = f"Mylo and a {animal} explore the {location} together."
    scene_video_url = generate_ai_video(scene_description)
    print("🎞️ Scene Video URL:", scene_video_url)

    # Assuming you download the video and save it as 'scene_video.mp4' (adjust accordingly)
    scene_video_path = os.path.join(downloads_folder, "scene_video.mp4")

    # 5. Merge video & voice locally
    merge_video_audio(scene_video_path, voice_path, output_path=output_video_path)

    print("\n✅ Done! Your final video is saved at:", output_video_path)
