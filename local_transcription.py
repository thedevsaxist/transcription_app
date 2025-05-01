import whisper
import os
import logging

logging.basicConfig(level=logging.INFO)


def format_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def transcribe_file(model, filepath):
    try:
        model = model.to(dtype="float32")
        result = model.transcribe(filepath, verbose=False, fp16=False)
        return [
            {"start": seg["start"], "end": seg["end"], "text": seg["text"]}
            for seg in result["segments"]
        ]
    except Exception as e:
        logging.error(f"Error transcribing {filepath}: {e}")
        return []


def transcribe_audio_local(model_size, input_dir, output_file):
    if not os.path.exists(input_dir):
        logging.error(f"Chunk directory '{input_dir}' does not exist.")
        return

    chunk_files = sorted(
        f for f in os.listdir(input_dir) if f.endswith((".mp3", ".wav", ".m4a", ".mp4"))
    )
    if not chunk_files:
        logging.warning(f"No audio files found in directory '{input_dir}'.")
        return

    logging.info(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size, device="cpu")

    segments_with_timestamps = []
    for filename in chunk_files:
        filepath = os.path.join(input_dir, filename)
        logging.info(f"Transcribing {filename}...")
        segments_with_timestamps.extend(transcribe_file(model, filepath))

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            for seg in segments_with_timestamps:
                start = format_timestamp(seg["start"])
                end = format_timestamp(seg["end"])
                f.write(f"[{start} - {end}] {seg['text']}\n")
        logging.info(f"✅ Transcription complete. Saved to: {output_file}")
    except Exception as e:
        logging.error(f"Error writing to output file '{output_file}': {e}")
