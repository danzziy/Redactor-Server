# from argument_parser.argument_parser import ArgumentParser
from transcriber.transcriber import Transcriber
from file_editor.file_editor import FileEditor
from gcloud.storage import GCStorage
from pathlib import Path
import shutil
import os


# TODO - Get swear words from a database down the line
# TODO - Allow "." to be in the file name
# TODO - Remove all of the subfolders

class Manager:

    def transcribe_file(input_file, mime_type):
        try:
            json_transcript = transcribe_file(input_file)
            return json_transcript["text"]
        finally:
            # Remove the directory containing the file, whether the censoring and uploading passed or failed
            directory_path = os.path.dirname(input_file)
            shutil.rmtree(directory_path)

    def censor_file(input_file, mime_type):
        try:
            is_video_file = "video" in mime_type
            if is_video_file:
                censor_video_file(input_file)
            elif "audio" in mime_type:
                censor_audio_file(input_file)
            else:
                raise TypeError("Invalid File Format, the file must be either an audio or video file")

            # Upload the file to GCStorage
            GCStorage().upload_file(input_file, input_file.replace("\\", "/"))
        finally:
            # Remove the directory containing the file, whether the censoring and uploading passed or failed
            directory_path = os.path.dirname(input_file)
            shutil.rmtree(directory_path)
       
def transcribe_file(file):
    transcriber = Transcriber()
    return transcriber.transcribe_audio_file(file)

def censor_audio_file(audio_file):
    original_format = FileEditor().get_audio_format(audio_file)
    transcriber = Transcriber()
    json_transcript = transcriber.transcribe_audio_file(audio_file)
    
    if "wav" not in original_format:
        FileEditor().convert_audio_file_into_wav(audio_file)
        FileEditor().censor_file(audio_file, json_transcript)
        FileEditor().convert_audio_file_into_format(audio_file, original_format)
    else:
        FileEditor().censor_file(audio_file, json_transcript)

def censor_video_file(video_file):
    audio_file = FileEditor().seperate_audio_from_video(video_file)
    censor_audio_file(audio_file)
    FileEditor().replace_audio_of_video(audio_file, video_file)


def download_censored_file(input_file):
    return GCStorage().download_file_stream(input_file)
