from argument_parser.argument_parser import ArgumentParser
from transcriber.transcriber import Transcriber
from file_editor.file_editor import FileEditor
from pathlib import Path
import json
import os

# TODO - Get swear words from a database down the line
# TODO - Allow "." to be in the file name
# TODO - Remove all of the subfolders
def censorAudioFile():
    argument_parser = ArgumentParser()
    input_file = argument_parser.get_file()
    is_video_file = input_file.lower().endswith(('.mp4', '.mov', '.webm'))

    if is_video_file:
        print("TRUE")
        audio_file = FileEditor().seperate_audio_from_video(input_file)
    else:
        audio_file = input_file

    transcriber = Transcriber()
    json_transcript = transcriber.transcribe_audio_file(audio_file)
    # file_to_open = Path('redactor/test_data/bitches.json')
    # jsonF=open(file_to_open)
    # json_transcript = json.load(jsonF)
    
    FileEditor().censor_file(audio_file, json_transcript)

    if is_video_file:
        FileEditor().replace_audio_of_video(audio_file, input_file)
        


if __name__ == '__main__':
    path = os.getcwd()

    print(path)
    print("Begin Censoring File")
    censorAudioFile()
    print("Complete Censoring File")