"""
Audio processing utilities for SuperNan project.
Handles duration adjustment and audio manipulation.
"""

import os
import librosa


def get_duration(audio_path: str) -> float:
    """
    Get duration of an audio file.
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Duration in seconds
    """
    return librosa.get_duration(path=audio_path)


def adjust_duration(input_audio: str, output_audio: str, target_duration: float):
    """
    Adjust audio duration to match target duration using tempo change.
    
    Args:
        input_audio: Path to input audio
        output_audio: Path to save adjusted audio
        target_duration: Target duration in seconds
    """
    current_duration = librosa.get_duration(path=input_audio)
    
    if current_duration <= 0:
        raise ValueError("Invalid audio duration")
    
    speed_factor = target_duration / current_duration
    
    # Clamp speed factor to valid range for atempo
    speed_factor = max(0.5, min(2.0, speed_factor))
    
    os.system(f"ffmpeg -y -i {input_audio} -filter:a 'atempo={speed_factor}' {output_audio}")


def match_audio_duration(orig_audio: str, new_audio: str, output_audio: str):
    """
    Match new audio duration to original audio duration.
    
    Args:
        orig_audio: Path to original audio file
        new_audio: Path to new audio file
        output_audio: Path to save duration-matched audio
    """
    orig_duration = get_duration(orig_audio)
    new_duration = get_duration(new_audio)
    
    speed_factor = new_duration / orig_duration
    
    os.system(f"ffmpeg -y -i {new_audio} -filter:a 'atempo={speed_factor}' {output_audio}")

