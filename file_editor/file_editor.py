import re
from pydub import AudioSegment
import moviepy.editor as mp
import sys
import os
import subprocess
from shutil import move

SWEAR_WORDS = ["fuck","shit","bitch","dick","nigga","nigger","asshole","whore","pussy"]
# TODO: Break up the file editor into FileSanitizer and Redactor.
# TODO: Make a list of swear words as a csv file.

class FileEditor:
    def convert_audio_file_into_wav(self, audio_file): 
        audio = AudioSegment.from_file(audio_file)
        os.remove(audio_file)
        audio.export(audio_file, format="wav")
        # return new_file_path_name

    def convert_audio_file_into_format(self, audio_file, format): 
        audio = AudioSegment.from_file(audio_file)
        os.remove(audio_file)
        audio.export(audio_file, format=format)

    def get_audio_format(self, file_path):
        command = ['ffmpeg', '-i', file_path]
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stderr
        audio_format = None

        # Parsing the FFmpeg output to extract the audio format
        for line in output.split('\n'):
            if 'Audio:' in line:
                codec_match = re.search(r'Audio: (\w+)', line)
                audio_format = codec_match.group(1)
                break

        return get_output_format_from_codec(audio_format)

    def seperate_audio_from_video(self, input_video):
        video_file = mp.VideoFileClip(input_video)
        path = os.path.dirname(input_video)
        path = os.path.join(path, '')

        video_file.audio.write_audiofile(f"{path}seperated_audio.wav")
        return f"{path}seperated_audio.wav"

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
        video.close()
        audio.close()

        os.remove(video_file)
        os.rename(output_file_name, video_file)

    def censor_file(self, file_path, json_transcript):
        for segments in json_transcript["segments"]:
            for word_info in segments["words"]:
                word = re.sub(r'[^a-zA-Z ]+', '', word_info['text'].lower())
                for swear in SWEAR_WORDS:
                    if swear in word:
                        censor_word(file_path, word_info)

def get_output_format_from_codec(audioCodec):
    if "pcm" in audioCodec:
        return "wav"
    
    outputFormat = {
        'mp3': 'mp3',
        'aac': 'm4a',
        'm4a': 'm4a',
        'vorbis': 'ogg',
    }
    try:
        result = outputFormat[audioCodec]
        return result
    except: 
        raise KeyError(f"Unsupported format type: {audioCodec}")

def censor_word(file_path, word_info):
    swear_word_start_time = word_info['start']*1000
    swear_word_end_time = word_info['end']*1000

    full_audio = AudioSegment.from_file(file_path)
    audio_before_swear = full_audio[0:swear_word_start_time]
    audio_after_swear = full_audio[swear_word_end_time:int(full_audio.duration_seconds*1000)]

    #segment the beep to be the right length
    beep_file = "beep.wav"
    beep_audio =  AudioSegment.from_file(beep_file)
    audio_during_swear = beep_audio[0:(swear_word_end_time-swear_word_start_time)]

    # combined = before_swear + during_swear + after_swear
    combined = audio_before_swear + audio_during_swear + audio_after_swear
    combined.export(file_path , format="wav")

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
