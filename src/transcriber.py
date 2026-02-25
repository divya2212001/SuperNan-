"""
Speech recognition module for SuperNan project.
Transcribes audio to text using Faster Whisper.
"""

from faster_whisper import WhisperModel


class TranscriptionService:
    """Service for transcribing audio to text."""
    
    def __init__(self, model_size: str = "medium", compute_type: str = "float32"):
        """
        Initialize the transcription service.
        
        Args:
            model_size: Whisper model size (tiny, base, small, medium, large)
            compute_type: Computation type (float32, float16, int8)
        """
        self.model = WhisperModel(model_size, compute_type=compute_type)
    
    def transcribe(self, audio_path: str, task: str = "translate", language: str = None) -> dict:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            task: "transcribe" or "translate"
            language: Source language (auto-detected if None)
            
        Returns:
            Dictionary with transcript, language, and language probability
        """
        segments, info = self.model.transcribe(
            audio_path,
            task=task,
            language=language
        )
        
        print(f"Detected language: {info.language}")
        print(f"Language probability: {info.language_probability}")
        
        full_text = ""
        for segment in segments:
            full_text += segment.text + " "
        
        return {
            "text": full_text.strip(),
            "language": info.language,
            "language_probability": info.language_probability
        }
    
    def transcribe_to_english(self, audio_path: str) -> str:
        """
        Transcribe and translate audio to English.
        
        Args:
            audio_path: Path to audio file
            
        Returns:
            English transcript
        """
        result = self.transcribe(audio_path, task="translate")
        return result["text"]


def transcribe_auto(audio_path: str, model_size: str = "medium") -> str:
    """
    Convenience function to transcribe audio to English.
    
    Args:
        audio_path: Path to audio file
        model_size: Whisper model size
        
    Returns:
        English transcript
    """
    service = TranscriptionService(model_size=model_size)
    return service.transcribe_to_english(audio_path)

