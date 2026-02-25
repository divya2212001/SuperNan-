"""
Video processing utilities for SuperNan project.
Handles video chunk extraction and audio extraction.
"""

import os


def extract_chunk(input_path: str, output_path: str, start_time: str = "00:00:15", end_time: str = "00:00:30"):
    """
    Extract a specific time chunk from a video file.
    
    Args:
        input_path: Path to input video file
        output_path: Path to save extracted chunk
        start_time: Start time in HH:MM:SS format
        end_time: End time in HH:MM:SS format
    """
    os.system(f"ffmpeg -i {input_path} -ss {start_time} -to {end_time} -c copy {output_path}")


def extract_audio(video_path: str, audio_path: str):
    """
    Extract audio from a video file.
    
    Args:
        video_path: Path to video file
        audio_path: Path to save extracted audio
    """
    os.system(f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path}")


def merge_audio_video(video_path: str, audio_path: str, output_path: str):
    """
    Merge audio with video file.
    
    Args:
        video_path: Path to video file
        audio_path: Path to audio file
        output_path: Path to save final output
    """
    command = (
        f"ffmpeg -y -i {video_path} -i {audio_path} "
        f"-c:v copy -map 0:v:0 -map 1:a:0 -shortest {output_path}"
    )
    os.system(command)

