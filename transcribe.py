from openai import OpenAI

client = OpenAI()

with open("record.ogg", "rb") as audio_file:
    transcription = client.audio.transcriptions.create(
        model="gpt-transcribe", file=audio_file
    )

with open("transcription.txt", "w") as f:
    f.write(transcription.text)

print(transcription.text)