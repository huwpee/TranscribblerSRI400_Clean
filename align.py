import json
import pandas as pd

def align_transcript_with_speakers(transcript_data, speaker_segments, output_path=None):
    """
    Merge transcript with speaker information
    
    Args:
        transcript_data (dict): Whisper transcription result
        speaker_segments (list): Speaker diarization segments
        output_path (str, optional): Path to save aligned transcript
        
    Returns:
        list: Aligned transcript with speaker information
    """
    print("Aligning transcription with speaker information...")
    
    # Load from files if paths are provided
    if isinstance(transcript_data, str):
        with open(transcript_data, 'r') as f:
            transcript_data = json.load(f)
    
    if isinstance(speaker_segments, str):
        with open(speaker_segments, 'r') as f:
            speaker_segments = json.load(f)
    
    aligned_segments = []
    
    for segment in transcript_data["segments"]:
        # Find the dominant speaker for this segment
        segment_start = segment["start"]
        segment_end = segment["end"]
        segment_speaker = find_dominant_speaker(segment_start, segment_end, speaker_segments)
        
        # Add segment with speaker info
        aligned_segments.append({
            "start": segment_start,
            "end": segment_end,
            "speaker": segment_speaker,
            "text": segment["text"]
        })
    
    if output_path:
        # Save as CSV for easy viewing
        df = pd.DataFrame(aligned_segments)
        df.to_csv(output_path, index=False)
        print(f"Aligned transcript saved to {output_path}")
        
        # Also save as JSON
        json_path = output_path.replace('.csv', '.json')
        with open(json_path, 'w') as f:
            json.dump(aligned_segments, f, indent=2)
    
    return aligned_segments

def find_dominant_speaker(start_time, end_time, speaker_segments):
    """Find the dominant speaker for a given time range"""
    speakers = {}
    
    for segment in speaker_segments:
        # Check for overlap
        overlap_start = max(start_time, segment["start"])
        overlap_end = min(end_time, segment["end"])
        
        if overlap_end > overlap_start:
            duration = overlap_end - overlap_start
            speakers[segment["speaker"]] = speakers.get(segment["speaker"], 0) + duration
    
    # Return speaker with most speaking time in this segment
    if speakers:
        return max(speakers, key=speakers.get)
    return "Unknown"

if __name__ == "__main__":
    # Example usage
    transcript_file = "data/transcription.json"
    speakers_file = "data/speakers.json"
    
    aligned_transcript = align_transcript_with_speakers(
        transcript_file,
        speakers_file,
        output_path="data/aligned_transcript.csv"
    )
    
    # Print preview
    for segment in aligned_transcript[:3]:
        print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['speaker']}: {segment['text']}")