"""
SuperNan - Video Dubbing & Lip Sync Package

A powerful video dubbing and lip-syncing pipeline that translates 
videos from English to Hindi with realistic voice cloning and 
automatic lip synchronization.
"""

from .video_processor import extract_chunk, extract_audio, merge_audio_video
from .audio_processor import get_duration, adjust_duration, match_audio_duration
from .transcriber import TranscriptionService, transcribe_auto
from .translator import TranslationService, translate_to_hindi
from .tts import TTSService, generate_hindi_speech
from .pipeline import VideoDubbingPipeline, run_pipeline

__version__ = "1.0.0"
__author__ = "SuperNan Team"

__all__ = [
    # Video processing
    "extract_chunk",
    "extract_audio", 
    "merge_audio_video",
    # Audio processing
    "get_duration",
    "adjust_duration",
    "match_audio_duration",
    # Transcription
    "TranscriptionService",
    "transcribe_auto",
    # Translation
    "TranslationService",
    "translate_to_hindi",
    # TTS
    "TTSService",
    "generate_hindi_speech",
    # Pipeline
    "VideoDubbingPipeline",
    "run_pipeline",
]

