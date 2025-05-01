from pydub import AudioSegment
import math

import os

split_audio = AudioSegment.from_file("audio1913038809.m4a", format="m4a")
chunk_length = 60 * 1000

total_length = len(split_audio)
total_number_of_chunks = math.ceil(total_length / chunk_length)

output_dir = "chunked_audio"

for i in range(total_number_of_chunks):
    start = i * chunk_length
    end = min((i + 1) * chunk_length, total_length)
    chunk = split_audio[start:end]

    chunk.export(f"{output_dir}/chunk_{i:04d}.mp4", format="mp4")

print(f"Exported {total_number_of_chunks} chunks to {output_dir}/")