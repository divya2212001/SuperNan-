#!/usr/bin/env python3
"""
SuperNan - Video Dubbing & Lip Sync

Main entry point for the video dubbing pipeline.
"""

import argparse
import os

from src import (
    extract_chunk,
    extract_audio,
    transcribe_auto,
    translate_to_hindi,
    generate_hindi_speech,
    match_audio_duration,
    merge_audio_video,
    VideoDubbingPipeline
)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="SuperNan - Video Dubbing & Lip Sync Pipeline"
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Input video file"
    )
    parser.add_argument(
        "--output", "-o",
        default="final_output.mp4",
        help="Output video file (default: final_output.mp4)"
    )
    parser.add_argument(
        "--start", "-s",
        default="00:00:15",
        help="Start time for chunk (default: 00:00:15)"
    )
    parser.add_argument(
        "--end", "-e",
        default="00:00:30",
        help="End time for chunk (default: 00:00:30)"
    )
    parser.add_argument(
        "--target-lang", "-t",
        default="hi",
        help="Target language code (default: hi for Hindi)"
    )
    parser.add_argument(
        "--use-pipeline",
        action="store_true",
        help="Use the complete pipeline (vs manual steps)"
    )
    
    args = parser.parse_args()
    
    # Check if input file exists
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        return 1
    
    if args.use_pipeline:
        # Use the complete pipeline
        print("Running complete pipeline...")
        pipeline = VideoDubbingPipeline()
        
        lang_map = {
            "hi": "hin_Deva",
            "en": "eng_Latn",
            "es": "spa_Latn",
            "fr": "fra_Latn",
        }
        target_lang = lang_map.get(args.target_lang, "hin_Deva")
        
        result = pipeline.run(
            args.input,
            args.output,
            args.start,
            args.end,
            target_lang
        )
        
        if result["success"]:
            print("\n=== Pipeline Complete ===")
            print(f"Output saved to: {result['output_video']}")
            print(f"Original duration: {result['original_duration']:.2f}s")
            print(f"Final duration: {result['final_duration']:.2f}s")
        else:
            print("Pipeline failed!")
            return 1
    else:
        # Manual step-by-step execution
        print("Running step-by-step dubbing...")
        
        # Create temp directory
        temp_dir = "temp_outputs"
        os.makedirs(temp_dir, exist_ok=True)
        
        # Step 1: Extract chunk
        chunk_path = os.path.join(temp_dir, "chunk.mp4")
        print(f"\n[1/7] Extracting chunk {args.start} to {args.end}...")
        extract_chunk(args.input, chunk_path, args.start, args.end)
        
        # Step 2: Extract audio
        audio_path = os.path.join(temp_dir, "audio.wav")
        print("[2/7] Extracting audio...")
        extract_audio(chunk_path, audio_path)
        
        # Step 3: Transcribe
        print("[3/7] Transcribing to English...")
        transcript = transcribe_auto(audio_path)
        print(f"Transcript: {transcript}")
        
        # Step 4: Translate
        print("[4/7] Translating to Hindi...")
        hindi_text = translate_to_hindi(transcript)
        print(f"Hindi: {hindi_text}")
        
        # Step 5: Generate speech
        tts_path = os.path.join(temp_dir, "hindi_speech.wav")
        print("[5/7] Generating Hindi speech...")
        generate_hindi_speech(hindi_text, tts_path)
        
        # Step 6: Match duration
        adjusted_path = os.path.join(temp_dir, "adjusted_hindi.wav")
        print("[6/7] Matching duration...")
        match_audio_duration(audio_path, tts_path, adjusted_path)
        
        # Step 7: Merge
        print("[7/7] Creating final output...")
        merge_audio_video(chunk_path, adjusted_path, args.output)
        
        print(f"\n=== Complete ===")
        print(f"Output saved to: {args.output}")
    
    return 0


if __name__ == "__main__":
    exit(main())

