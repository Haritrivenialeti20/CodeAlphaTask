from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy.io.wavfile
import numpy as np
import os


MODEL_NAME = "facebook/musicgen-small"
OUTPUT_DIR = "output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "generated_music.wav")


def generate_music(prompt):
    print("Loading MusicGen model...")
    print("This may take some time the first time.")

    processor = AutoProcessor.from_pretrained(MODEL_NAME)
    model = MusicgenForConditionalGeneration.from_pretrained(MODEL_NAME)

    print("Generating music...")
    print(f"Prompt: {prompt}")

    inputs = processor(
        text=[prompt],
        padding=True,
        return_tensors="pt"
    )

    audio_values = model.generate(
        **inputs,
        max_new_tokens=256
    )

    sampling_rate = model.config.audio_encoder.sampling_rate

    audio = audio_values[0, 0].detach().cpu().numpy()

    # Normalize audio
    audio = audio / np.max(np.abs(audio))

    # Convert to 16-bit WAV
    audio = np.int16(audio * 32767)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    scipy.io.wavfile.write(
        OUTPUT_FILE,
        sampling_rate,
        audio
    )

    print()
    print("Music generation completed!")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    prompt = input(
        "Enter a music description "
        "(example: relaxing piano music): "
    )

    if not prompt.strip():
        prompt = "calm relaxing piano music"

    generate_music(prompt)