import os

def transcribe_audio_remote(client, input_dir, output_file):
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"The directory '{input_dir}' does not exist.")

    with open(output_file, "w") as transcript_file:
        for filename in sorted(os.listdir(input_dir)):
            filepath = os.path.join(input_dir, filename)
            if not os.path.isfile(filepath):
                print(f"Skipping non-file: {filepath}")
                continue

            try:
                with open(filepath, "rb") as audio_file:
                    transcription = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        response_format="text",
                        language="en",
                    )
                    transcript_file.write(f"File: {filename}\n")
                    transcript_file.write(transcription["text"] + "\n\n")
                    print(f"Transcribed: {filename}")
            except Exception as e:
                print(f"An error occurred while transcribing {filename}: {e}")
