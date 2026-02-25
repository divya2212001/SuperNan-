"""
Text-to-Speech module for SuperNan project.
Generates speech from text using Edge TTS.
"""

import asyncio
import edge_tts
from typing import Optional


class TTSService:
    """Service for converting text to speech."""
    
    def __init__(self, voice: str = "hi-IN-SwaraNeural"):
        """
        Initialize the TTS service.
        
        Args:
            voice: Edge TTS voice name
        """
        self.voice = voice
    
    async def generate_speech_async(self, text: str, output_path: str) -> str:
        """
        Generate speech from text asynchronously.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            
        Returns:
            Path to generated audio file
        """
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
        return output_path
    
    def generate_speech(self, text: str, output_path: str) -> str:
        """
        Generate speech from text.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            
        Returns:
            Path to generated audio file
        """
        return asyncio.run(self.generate_speech_async(text, output_path))
    
    async def generate_speech_with_subs_async(self, text: str, output_path: str) -> dict:
        """
        Generate speech and get subtitle timing information.
        
        Args:
            text: Text to convert to speech
            output_path: Path to save audio file
            
        Returns:
            Dictionary with audio path and subtitle information
        """
        subs = []
        communicate = edge_tts.Communicate(text, self.voice)
        
        with open(output_path, "wb") as audio_file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_file.write(chunk["data"])
                elif chunk["type"] == "WordBoundary":
                    subs.append({
                        "text": chunk["text"],
                        "offset": chunk["offset"],
                        "duration": chunk["duration"]
                    })
        
        return {
            "audio_path": output_path,
            "subtitles": subs
        }


# Available Hindi voices
HINDI_VOICES = {
    "swara": "hi-IN-SwaraNeural",
    "arya": "hi-IN-AryaNeural",
}

# Available English voices
ENGLISH_VOICES = {
    "jenny": "en-US-JennyNeural",
    "guy": "en-US-GuyNeural",
    "aria": "en-US-AriaNeural",
}


def generate_hindi_speech(text: str, output_path: str = "hindi_speech.wav") -> str:
    """
    Generate Hindi speech from text.
    
    Args:
        text: Text to convert to Hindi speech
        output_path: Path to save audio file
        
    Returns:
        Path to generated audio file
    """
    service = TTSService(voice="hi-IN-SwaraNeural")
    return service.generate_speech(text, output_path)


async def generate_hindi_speech_async(text: str, output_path: str = "hindi_speech.wav") -> str:
    """
    Generate Hindi speech from text (async version).
    
    Args:
        text: Text to convert to Hindi speech
        output_path: Path to save audio file
        
    Returns:
        Path to generated audio file
    """
    service = TTSService(voice="hi-IN-SwaraNeural")
    return await service.generate_speech_async(text, output_path)

