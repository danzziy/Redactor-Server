import re
from pydub import AudioSegment
import moviepy.editor as mp
import sys
import os
from shutil import move

SWEAR_WORDS = ["fuck","shit","bitch","dick","nigga","nigger","asshole","whore","pussy"]

class FileEditor:
   
    def seperate_audio_from_video(self, file_path):
        video_file = mp.VideoFileClip(file_path)

        video_file.audio.write_audiofile(r"seperated_audio.wav")
        return "seperated_audio.wav"

    def replace_audio_of_video(self, audio_file, video_file):
        audio = mp.AudioFileClip(audio_file)
        #Input video file
        video = mp.VideoFileClip(video_file)
        #adding external audio to video
        final_video = video.set_audio(audio)
        #Extracting final output video
        file_name, file_extension = os.path.splitext(video_file)
        output_file_name = file_name+ "_censored" + file_extension
        
        final_video.write_videofile(output_file_name)
        print("WE ARE DONE CENSORING")
        # Move allows for a rename plus overwrite without causing the error [WinError 32]
        # However, this function may not work on linux
        move(output_file_name, video_file)

    def censor_file(self, file_path, json_transcript):
        for segments in json_transcript["segments"]:
            for word_info in segments["words"]:
                word = re.sub(r'[^a-zA-Z ]+', '', word_info['text'].lower())
                print(word_info)
                for swear in SWEAR_WORDS:
                    if swear in word:
                        censor_word(file_path, word_info)
        # for word_info in json_transcript["words"]:
        #     word = re.sub(r'[^a-zA-Z ]+', '', word_info['text'].lower())
        #     for swear in SWEAR_WORDS:
        #         if swear in word:
        #             censor_word(file_path, word_info)

def censor_word(file_path, word_info):
    file_extension = file_path.split(".")[-1]
    swear_word_start_time = word_info['start']*1000
    swear_word_end_time = word_info['end']*1000

    full_audio = read_audio_file(file_path, file_extension)
    audio_before_swear = full_audio[0:swear_word_start_time]
    audio_after_swear = full_audio[swear_word_end_time:int(full_audio.duration_seconds*1000)]

    #segment the beep to be the right length
    beep_file = "beep." + file_extension
    beep_audio = read_audio_file(beep_file, file_extension)
    audio_during_swear = beep_audio[0:(swear_word_end_time-swear_word_start_time)]

    # combined = before_swear + during_swear + after_swear
    combined = audio_before_swear + audio_during_swear + audio_after_swear
    combined.export(file_path , format=file_extension)

# Read audio file created to handle error found in this link
# https://stackoverflow.com/questions/70660431/couldntdecodeerror-decoding-failed-ffmpeg-returned-error-code-69
def read_audio_file(file_name, extension):
    try:
        audio = AudioSegment.from_file(file=file_name, format=extension)
    except:
        if extension=="mp3":
            audio = AudioSegment.from_file(file=file_name, format="mp4")
        else:
            sys.exit("Could not get the audio file: " + file_name)

    return audio

# TODO - Handle cases where file has special characters in name or multiple '.'
# TODO - Extract this out to a helper function