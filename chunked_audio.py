from pydub import AudioSegment
import math
import os
import sys


def load_audio(input_file, format):
    """Load the audio file."""
    try:
        return AudioSegment.from_file(input_file, format=format)
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)


def ensure_output_directory(output_dir):
    """Ensure the output directory exists."""
    os.makedirs(output_dir, exist_ok=True)


def calculate_chunks(audio_length, chunk_length):
    """Calculate the total number of chunks."""
    return math.ceil(audio_length / chunk_length)


def split_and_export_chunks(audio, output_dir, chunk_length):
    """Split the audio into chunks and export them."""
    total_length = len(audio)
    total_chunks = calculate_chunks(total_length, chunk_length)

    for i in range(total_chunks):
        start = i * chunk_length
        end = min((i + 1) * chunk_length, total_length)
        chunk = audio[start:end]

        output_file = os.path.join(output_dir, f"chunk_{i:04d}.mp4")
        chunk.export(output_file, format="mp4")

    print(f"Exported {total_chunks} chunks to '{output_dir}/'")


def main():
    # Configurable variables
    input_file = "audio1913038809.m4a"  # Input audio file
    output_dir = "chunked_audio"  # Directory to save chunks
    chunk_length = 60 * 1000  # Chunk length in milliseconds (60 seconds)

    # Load the audio file
    audio = load_audio(input_file)

    # Ensure the output directory exists
    ensure_output_directory(output_dir)

    # Split and export chunks
    split_and_export_chunks(audio, output_dir, chunk_length)


if __name__ == "__main__":
    main()
