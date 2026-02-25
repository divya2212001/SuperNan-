"""
Main pipeline module for SuperNan project.
Orchestrates the complete video dubbing workflow.
"""

from .video_processor import extract_chunk, extract_audio, merge_audio_video
from .audio_processor import get_duration, adjust_duration, match_audio_duration
from .transcriber import TranscriptionService, transcribe_auto
from .translator import TranslationService, translate_to_hindi
from .tts import TTSService, generate_hindi_speech


class VideoDubbingPipeline:
    """
    Complete video dubbing pipeline that:
    1. Extracts audio from video
    2. Transcribes to English
    3. Translates to target language
    4. Generates speech
    5. Matches duration
    6. Merges with video
    """
    
    def __init__(
        self,
        whisper_model: str = "medium",
        translator_model: str = "facebook/nllb-200-distilled-600M",
        tts_voice: str = "hi-IN-SwaraNeural"
    ):
        """
        Initialize the pipeline.
        
        Args:
            whisper_model: Whisper model size
            translator_model: NLLB model name
            tts_voice: Edge TTS voice
        """
        self.transcriber = TranscriptionService(model_size=whisper_model)
        self.translator = TranslationService(model_name=translator_model)
        self.tts = TTSService(voice=tts_voice)
    
    def run(
        self,
        input_video: str,
        output_video: str,
        start_time: str = "00:00:15",
        end_time: str = "00:00:30",
        target_lang: str = "hin_Deva"
    ) -> dict:
        """
        Run the complete dubbing pipeline.
        
        Args:
            input_video: Path to input video
            output_video: Path to save dubbed video
            start_time: Start time for chunk extraction
            end_time: End time for chunk extraction
            target_lang: Target language code
            
        Returns:
            Dictionary with pipeline results and metadata
        """
        import os
        import tempfile
        
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Step 1: Extract chunk
            chunk_path = os.path.join(temp_dir, "chunk.mp4")
            print("Step 1: Extracting video chunk...")
            extract_chunk(input_video, chunk_path, start_time, end_time)
            
            # Step 2: Extract audio
            audio_path = os.path.join(temp_dir, "original_audio.wav")
            print("Step 2: Extracting audio...")
            extract_audio(chunk_path, audio_path)
            
            # Step 3: Transcribe
            print("Step 3: Transcribing audio...")
            transcript = self.transcriber.transcribe_to_english(audio_path)
            print(f"English transcript: {transcript}")
            
            # Step 4: Translate
            print(f"Step 4: Translating to {target_lang}...")
            translated_text = self.translator.translate(transcript, target_lang=target_lang)
            print(f"Translated text: {translated_text}")
            
            # Step 5: Generate speech
            tts_path = os.path.join(temp_dir, "generated_speech.wav")
            print("Step 5: Generating speech...")
            self.tts.generate_speech(translated_text, tts_path)
            
            # Step 6: Match duration
            adjusted_path = os.path.join(temp_dir, "adjusted_speech.wav")
            print("Step 6: Matching duration...")
            match_audio_duration(audio_path, tts_path, adjusted_path)
            
            # Step 7: Merge audio and video
            print("Step 7: Creating final output...")
            merge_audio_video(chunk_path, adjusted_path, output_video)
            
            return {
                "success": True,
                "input_video": input_video,
                "output_video": output_video,
                "transcript": transcript,
                "translated_text": translated_text,
                "original_duration": get_duration(audio_path),
                "final_duration": get_duration(adjusted_path)
            }
            
        finally:
            # Cleanup temp files
            import shutil
            shutil.rmtree(temp_dir, ignore_errors=True)


def run_pipeline(
    input_video: str,
    output_video: str,
    start_time: str = "00:00:15",
    end_time: str = "00:00:30"
) -> dict:
    """
    Convenience function to run the complete dubbing pipeline.
    
    Args:
        input_video: Path to input video
        output_video: Path to save dubbed video
        start_time: Start time for chunk
        end_time: End time for chunk
        
    Returns:
        Pipeline results
    """
    pipeline = VideoDubbingPipeline()
    return pipeline.run(input_video, output_video, start_time, end_time)

