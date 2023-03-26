import api_caller.assemblyAI as assemblyAI

""" 
Transcriber is responsible for connecting to AssemblyAI sending the 
audio file to it and recieving the json transcript of said file
"""

# TODO - This does not ha have to be a class
class Transcriber:

    def transcribe_audio_file(self, audio_file):
        upload_url = assemblyAI.upload_file(audio_file)
        transcript_response = assemblyAI.request_transcript(upload_url)
        # Create a polling endpoint that will let us check when the transcription is complete
        polling_endpoint = assemblyAI.make_polling_endpoint(transcript_response)

        # Wait until the transcription is complete
        assemblyAI.wait_for_completion(polling_endpoint)

        # Request the paragraphs of the transcript
        json = assemblyAI.get_json_transcript(polling_endpoint)
        return json
