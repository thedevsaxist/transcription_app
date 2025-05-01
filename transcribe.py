from openai import OpenAI
import os
from dotenv import load_dotenv
from remote_transcription import transcribe_audio_remote
from local_transcription import transcribe_audio_local


def load_api_key():
    load_dotenv()
    api_key = os.environ.get("OPEN_AI_API_KEY")
    if not api_key:
        raise ValueError("OPEN_AI_API_KEY is not set in the environment variables.")
    return api_key


def main():
    try:
        # api_key = load_api_key()
        # client = OpenAI(api_key=api_key)
        # transcribe_audio_remote(client, input_dir, output_file)

        input_dir = "chunked_audio"
        output_file = "transcribed_audio.txt"
        model_size = "base"
        transcribe_audio_local(model_size, input_dir, output_file)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
