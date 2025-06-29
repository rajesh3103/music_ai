import torch
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write

def generate_music(prompt, output_file="output.wav", duration=5):
    # Load the pre-trained MusicGen model (medium size)
    model = MusicGen.get_pretrained('small')
    
    # Set the duration of generated audio (seconds)
    model.set_generation_params(duration=duration)
    
    # Generate audio tensor from text prompt
    audio = model.generate([prompt])
    
    # Save audio to a WAV file
    audio_write(output_file, audio[0].cpu(), model.sample_rate, strategy="loudness")
    print(f"Generated audio saved to {output_file}")

if __name__ == "__main__":
    text_prompt = "A calm piano melody with gentle background strings"
    generate_music(text_prompt, "calm_piano.wav", duration=5)
