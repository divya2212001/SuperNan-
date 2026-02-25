# SuperNan - Video Dubbing & Lip Sync Project

A powerful video dubbing and lip-syncing pipeline that translates videos from English to Hindi with realistic voice cloning and automatic lip synchronization.

## Features

- **Video Chunk Extraction**: Extract specific segments from longer videos
- **Audio Extraction**: Pull audio tracks from video files
- **Speech Recognition**: Transcribe audio to English using Faster Whisper (medium model)
- **Machine Translation**: Translate English text to Hindi using Facebook's NLLB-200 distilled model
- **Voice Synthesis**: Generate natural Hindi speech using Edge TTS (SwaraNeural voice)
- **Duration Matching**: Adjust synthesized speech duration to match original audio
- **Lip Synchronization**: Replace original audio with translated audio while preserving video

## Project Structure

```
SuperNan/
├── main.py                 # CLI entry point
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── Supernan.ipynb          # Original notebook (reference)
├── src/                   # Main source code
│   ├── __init__.py        # Package exports
│   ├── video_processor.py # Video extraction utilities
│   ├── audio_processor.py # Audio manipulation utilities
│   ├── transcriber.py     # Speech-to-text (Whisper)
│   ├── translator.py       # Translation (NLLB)
│   ├── tts.py             # Text-to-Speech (Edge TTS)
│   └── pipeline.py        # Complete dubbing pipeline
```

## Installation

### System Dependencies

```bash
apt-get update -y
apt-get install -y ffmpeg
```

### Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Option 1: Using CLI

```bash
# Run with default settings (English → Hindi)
python main.py --input input.mp4 --output final_output.mp4

# Specify custom time range
python main.py --input input.mp4 --output final.mp4 --start 00:01:00 --end 00:01:30

# Use complete pipeline mode
python main.py --input input.mp4 --use-pipeline
```

### Option 2: Using the Pipeline Class

```python
from src import VideoDubbingPipeline

pipeline = VideoDubbingPipeline()
result = pipeline.run(
    input_video="input.mp4",
    output_video="final_output.mp4",
    start_time="00:00:15",
    end_time="00:00:30"
)
```

### Option 3: Step-by-Step

```python
from src import (
    extract_chunk,
    extract_audio,
    transcribe_auto,
    translate_to_hindi,
    generate_hindi_speech,
    match_audio_duration,
    merge_audio_video
)

# 1. Extract video chunk
extract_chunk("input.mp4", "chunk.mp4", "00:00:15", "00:00:30")

# 2. Extract audio
extract_audio("chunk.mp4", "audio.wav")

# 3. Transcribe to English
transcript = transcribe_auto("audio.wav")

# 4. Translate to Hindi
hindi_text = translate_to_hindi(transcript)

# 5. Generate Hindi speech
generate_hindi_speech(hindi_text, "hindi_speech.wav")

# 6. Match duration
match_audio_duration("audio.wav", "hindi_speech.wav", "adjusted_hindi.wav")

# 7. Merge audio and video
merge_audio_video("chunk.mp4", "adjusted_hindi.wav", "final_output.mp4")
```

### Option 4: Using Individual Services

```python
# Transcription Service
from src import TranscriptionService

transcriber = TranscriptionService(model_size="medium")
result = transcriber.transcribe("audio.wav", task="translate")
print(result["text"])  # English transcript

# Translation Service
from src import TranslationService

translator = TranslationService()
hindi_text = translator.translate_to_hindi("Hello, how are you?")

# TTS Service
from src import TTSService

tts = TTSService(voice="hi-IN-SwaraNeural")
tts.generate_speech("नमस्ते, कैसे हैं आप?", "output.wav")
```

## Pipeline Overview

```
Input Video (input.mp4)
       │
       ▼
┌──────────────────┐
│ Extract Chunk    │ ──► chunk.mp4
│ (00:00:15-30)    │
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Extract Audio    │ ──► audio.wav
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Whisper (EN)    │ ──► English Transcript
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ NLLB (EN→HI)     │ ──► Hindi Text
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Edge TTS (HI)   │ ──► hindi_speech.wav
└──────────────────┘
       │
       ▼
┌──────────────────┐
│ Duration Adjust  │ ──► adjusted_hindi.wav
└──────────────────┘
      ┌────────────────── │
       ▼
┐
│ Merge + Output   │ ──► final_output.mp4
└──────────────────┘
```

## Models Used

| Component          | Model                            | Description                      |
| ------------------ | -------------------------------- | -------------------------------- |
| Speech Recognition | Faster Whisper (medium)          | Multilingual ASR model           |
| Translation        | facebook/nllb-200-distilled-600M | 600M parameter distilled model   |
| Text-to-Speech     | Edge TTS (hi-IN-SwaraNeural)     | Microsoft Edge neural voice      |
| Lip Sync           | Wav2Lip                          | Audio-driven lip synchronization |

## Requirements

- Python 3.8+
- CUDA-capable GPU (recommended for faster inference)
- ffmpeg installed on system
- At least 8GB RAM for model loading

## License

MIT License
