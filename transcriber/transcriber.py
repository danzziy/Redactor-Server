import api_caller.assemblyAI as assemblyAI
import whisper_timestamped as whisper
import json
import time

""" 
Transcriber is responsible for connecting to AssemblyAI sending the 
audio file to it and recieving the json transcript of said file
"""

# TODO - This does not ha have to be a class
class Transcriber:

    def transcribe_audio_file(self, audio_file):
        audio = whisper.load_audio(audio_file)
        model = whisper.load_model("small")

        result = whisper.transcribe(model, audio)
        return json.loads(json.dumps(result, indent = 2, ensure_ascii = False))
