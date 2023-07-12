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
        # start_time = time.time()

        # upload_url = assemblyAI.upload_file(audio_file)
        # transcript_response = assemblyAI.request_transcript(upload_url)
        # # Create a polling endpoint that will let us check when the transcription is complete
        # polling_endpoint = assemblyAI.make_polling_endpoint(transcript_response)

        # # Wait until the transcription is complete
        # assemblyAI.wait_for_completion(polling_endpoint)

        # # Request the paragraphs of the transcript
        # return assemblyAI.get_json_transcript(polling_endpoint)
        # end_time = time.time()

        # # Calculate the elapsed time
        # elapsed_time = end_time - start_time

        # # Print the timestamps and elapsed time
        # print("Start time:", time.ctime(start_time))
        # print("End time:", time.ctime(end_time))
        # print("Elapsed time:", elapsed_time, "seconds")
        
        
        start_time = time.time()

        audio = whisper.load_audio(audio_file)
        model = whisper.load_model("small")

        result = whisper.transcribe(model, audio)
        # print(json.dumps(result, indent = 2, ensure_ascii = False))
        # After the segment of code
        end_time = time.time()

        # Calculate the elapsed time
        elapsed_time = end_time - start_time

        # Print the timestamps and elapsed time
        print("Start time:", time.ctime(start_time))
        print("End time:", time.ctime(end_time))
        print("Elapsed time:", elapsed_time, "seconds")
        # print(json.dumps(result, indent = 2, ensure_ascii = False))   
        return json.loads(json.dumps(result, indent = 2, ensure_ascii = False))
