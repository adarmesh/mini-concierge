import sys
from datetime import datetime
from pathlib import Path
from openai import OpenAI


def main():
    if len(sys.argv) < 2:
        print("Usage: python transcribe.py <path-to-media>", file=sys.stderr)
        sys.exit(1)

    media_path = Path(sys.argv[1])

    client = OpenAI()

    with open(media_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="gpt-transcribe", file=audio_file
        )

    ts = datetime.now().strftime("%y_%m_%d")
    stem = media_path.stem
    out_path = media_path.with_name(f"{ts}_{stem}.txt")

    with open(out_path, "w") as f:
        f.write(transcription.text)

    print(transcription.text)


if __name__ == "__main__":
    main()