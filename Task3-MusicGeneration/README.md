# Task 3 - Music Generation with AI

## Project Overview

This project generates music from a text description using an AI music generation model.

The project uses Meta's MusicGen model through the Hugging Face Transformers library.

## Technologies Used

- Python 3.12
- PyTorch
- Hugging Face Transformers
- MusicGen
- SciPy
- SoundFile
- NumPy

## How It Works

1. The user enters a text description of the desired music.
2. MusicGen processes the text prompt.
3. The AI model generates an audio waveform.
4. The generated audio is saved as a WAV file.
5. The output file is stored in the `output` folder.

## Example

### Input

relaxing piano music with a calm melody

### Output

`output/generated_music.wav`

## Project Structure

```text
Task3-MusicGeneration/
├── src/
│   └── main.py
├── output/
│   └── generated_music.wav
├── README.md
├── requirements.txt
├── .gitignore
└── venv/