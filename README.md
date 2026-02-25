# 🔄 SuperNan

<div align="center">


_A powerful video dubbing and lip-syncing pipeline that translates videos from English to Hindi with realistic voice cloning and automatic lip synchronization._

</div>

---

## Features

| Feature                    | Description                                      |
| -------------------------- | ------------------------------------------------ |
| **Video Extraction**    | Extract specific segments from longer videos     |
|  **Audio Extraction**    | Pull audio tracks from video files               |
| **Speech Recognition**  | Transcribe audio to English using Faster Whisper |
| **Machine Translation** | Translate English text to Hindi using NLLB-200   |
|  **Voice Synthesis**     | Generate natural Hindi speech using Edge TTS     |
| **Duration Matching**   | Adjust speech duration to match original audio   |
|  **Lip Sync**            | Replace original audio with translated audio     |

---

## 📁 Project Structure

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
│   ├── translator.py      # Translation (NLLB)
│   ├── tts.py             # Text-to-Speech (Edge TTS)
│   └── pipeline.py        # Complete dubbing pipeline
```

---

## Quick Start

### Installation

```bash
# System dependencies
apt-get update -y && apt-get install -y ffmpeg

# Install Python packages
pip install -r requirements.txt
```

### Usage

```bash
# Run with default settings
python main.py --input input.mp4 --output final_output.mp4

# Specify custom time range
python main.py --input input.mp4 --output final.mp4 --start 00:01:00 --end 00:01:30
```

---

## Detailed Usage

### Option 1: Using CLI

```bash
python main.py --input input.mp4 --output final_output.mp4
python main.py --input input.mp4 --output final.mp4 --start 00:01:00 --end 00:01:30
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

---

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT VIDEO                               │
│                      input.mp4 (RAW)                            │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Extract Chunk                                        │
│  ffmpeg -i input.mp4 -ss 00:00:15 -to 00:00:30 -c copy          │
└─────────────────────────────────────────────────────────────────┘
                                │ chunk.mp4
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│   STEP 2: Extract Audio                                        │
│  ffmpeg -i chunk.mp4 -q:a 0 -map a audio.wav                     │
└─────────────────────────────────────────────────────────────────┘
                                │ audio.wav
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Transcription (Whisper)                            │
│  Audio → English Text                                            │
└─────────────────────────────────────────────────────────────────┘
                                │ "Hello everyone..."
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Translation (NLLB-200)                             │
│  English → Hindi                                                 │
└─────────────────────────────────────────────────────────────────┘
                                │ "नमस्ते सभी को..."
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Text-to-Speech (Edge TTS)                          │
│  Hindi Text → Hindi Audio                                       │
└─────────────────────────────────────────────────────────────────┘
                                │ hindi_speech.wav
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 6: Duration Adjustment                                 │
│  Match original audio duration                                  │
└─────────────────────────────────────────────────────────────────┘
                                │ adjusted_hindi.wav
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 7: Merge + Output                                      │
│  ffmpeg -i chunk.mp4 -i adjusted_hindi.wav                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FINAL OUTPUT                              │
│                   final_output.mp4                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Models Used

| Component             | Model                                                                                | Description               |
| --------------------- | ------------------------------------------------------------------------------------ | ------------------------- |
| Speech Recognition | [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) (medium)                 | Multilingual ASR model    |
| Translation        | [NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M) (distilled-600M) | Meta's multilingual model |
| Text-to-Speech     | [Edge TTS](https://github.com/rany2/edge-tts) (hi-IN-SwaraNeural)                    | Microsoft neural voice    |
| Lip Sync           | [Wav2Lip](https://github.com/Rudrabha/Wav2Lip)                                       | Audio-driven lip sync     |

---

## Requirements

- **Python**: 3.8+
- **GPU**: CUDA-capable (recommended for faster inference)
- **System**: ffmpeg
- **RAM**: At least 8GB for model loading

---

## Dependencies

```
ffmpeg                    # System dependency
opencv-python           # Video processing
librosa                 # Audio analysis
faster-whisper          # Speech recognition
transformers           # ML models
sentencepiece           # Tokenization
accelerate              # Model acceleration
torch                   # Deep learning
edge-tts               # Text-to-speech
TTS                    # Voice cloning
gdown                  # File downloads
gfpgan                 # Face restoration
```


