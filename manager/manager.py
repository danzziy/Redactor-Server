# from argument_parser.argument_parser import ArgumentParser
from transcriber.transcriber import Transcriber
from file_editor.file_editor import FileEditor
from gcloud.storage import GCStorage
from pathlib import Path
import subprocess
import shutil
import os
import re


# TODO - Get swear words from a database down the line
# TODO - Allow "." to be in the file name
# TODO - Remove all of the subfolders

class Manager:

    def transcribe_file(input_file):
        try:
            transcriber = Transcriber()
            json_transcript = transcriber.transcribe_audio_file_without_timestamps(input_file)
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
    
    def add_closed_captions(video_file):
        directory_path = os.path.dirname(video_file)
        file_name_with_extension = os.path.basename(video_file)
        file_name, _ = os.path.splitext(file_name_with_extension)
        try:
            transcriber = Transcriber()
            json_transcript = transcriber.transcribe_audio_file_without_timestamps(video_file)
            
            # TODO: Create the close caption file
            subtitle_file = os.path.join(directory_path, f'{file_name}_subtitles.srt')

            emoji_pattern = re.compile("["
                    u"\U0001F600-\U0001F64F"  # emoticons
                    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                    u"\U0001F680-\U0001F6FF"  # transport & map symbols
                    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "]+", flags=re.UNICODE)
            with open(subtitle_file, "w") as file:
                for index, segment in enumerate(json_transcript["segments"]):
                    file.write(f"{index + 1}\n")
                    file.write(seconds_to_srt_time(segment['start']) + ' --> ' + seconds_to_srt_time(segment['end']) + "\n")
                    text = emoji_pattern.sub(r'', segment['text']) # no emoji
                    file.write(f"{text}\n\n")
                    
            # TODO: Use close caption file to update the video
            # Define the output video file with captions
            subtitle_file = subtitle_file.replace("\\", "/")
            FileEditor.caption_video(video_file, subtitle_file)

            # Upload the file to GCStorage
            GCStorage().upload_file(video_file, video_file.replace("\\", "/"))
        finally:
            print("st")
            # Remove the directory containing the file, whether the censoring and uploading passed or failed
            # shutil.rmtree(directory_path)

def censor_audio_file(audio_file):
    original_format = FileEditor().get_audio_format(audio_file)
    transcriber = Transcriber()
    json_transcript = transcriber.transcribe_audio_file_with_timestamps(audio_file)
    
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

def seconds_to_srt_time(seconds):
    # Calculate hours, minutes, seconds, and milliseconds
    hours, remainder = divmod(seconds, 3600)
    minutes, remainder = divmod(remainder, 60)
    seconds, milliseconds = divmod(remainder, 1)
    milliseconds = int(milliseconds * 1000)

    # Format the time as HH:MM:SS,mmm
    time_str = f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{milliseconds:03d}"

    return time_str