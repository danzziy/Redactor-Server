import whisper_timestamped
import whisper
import json
import time

""" 
Transcriber is responsible for connecting to AssemblyAI sending the 
audio file to it and recieving the json transcript of said file
"""

# TODO - This does not ha have to be a class
class Transcriber:

    def transcribe_audio_file_with_timestamps(self, audio_file):
        audio = whisper_timestamped.load_audio(audio_file)
        model = whisper_timestamped.load_model("small")

        result = whisper_timestamped.transcribe(model, audio)

        value = json.loads(json.dumps(result, indent = 2, ensure_ascii = True))
        print(value)
        return value
    
    def transcribe_audio_file_without_timestamps(self, file):
        audio = whisper.load_audio(file)
        model = whisper.load_model("small.en")

        result = whisper.transcribe(model, audio)

        value = json.loads(json.dumps(result, indent = 2, ensure_ascii = True))
        print(value)
        return value