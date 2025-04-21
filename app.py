import gradio as gr
from video import generate_story, text_to_speech

def run_mylo(animal, location):
    story = generate_story(animal, location)
    text_to_speech(story, "voice.mp3")
    return story, "voice.mp3"

gr.Interface(
    fn=run_mylo,
    inputs=[gr.Textbox(label="Animal Mylo meets"), gr.Textbox(label="Location Mylo visits")],
    outputs=[gr.Textbox(label="Generated Story"), gr.Audio(label="Voice Story")],
    title="🐶 Mylo's Adventure Generator",
    description="Create a short AI-generated story and narration where Mylo meets an animal in a magical place!"
).launch()
