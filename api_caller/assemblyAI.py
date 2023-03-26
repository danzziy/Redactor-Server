import requests
import time

UPLOAD_ENDPOINT = "https://api.assemblyai.com/v2/upload"
TRANSCRIPT_ENDPOINT = "https://api.assemblyai.com/v2/transcript"
swear_words = ["fuck","fucker","fucks","fucking","fucked","shit","shitter","shitting","bitch","bitches","dick","nigga","nigger","cunt","cock","asshole","whore","shat"]

# Helper for `upload_file()`
def _read_file(filename, chunk_size=5242880):
    with open(filename, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

# TODO - extract out header in upload file to a config moudle
# Uploads a file to AAI servers
def upload_file(audio_file):
    upload_response = requests.post(
        UPLOAD_ENDPOINT,
        headers={
            'authorization': 'cce02bd99aad4aa9924721f4639be93e',
            'content-type': 'application/json'
        }, data=_read_file(audio_file)
    )
    return upload_response.json()


# Request transcript for file uploaded to AAI servers
def request_transcript(upload_url):
    transcript_request = {
        'audio_url': upload_url['upload_url'],
        'word_boost': swear_words,
        'boost_param': 'low'
    }
    transcript_response = requests.post(
        TRANSCRIPT_ENDPOINT,
        json=transcript_request,
        headers={
            'authorization': 'cce02bd99aad4aa9924721f4639be93e',
            'content-type': 'application/json'
        }
    )
    return transcript_response.json()


# Make a polling endpoint
def make_polling_endpoint(transcript_response):
    polling_endpoint = "https://api.assemblyai.com/v2/transcript/"
    polling_endpoint += transcript_response['id']
    return polling_endpoint


# Wait for the transcript to finish
def wait_for_completion(polling_endpoint):
    while True:
        polling_response = requests.get(polling_endpoint, 
            headers={
                'authorization': 'cce02bd99aad4aa9924721f4639be93e',
                'content-type': 'application/json'
            },
        )
        polling_response = polling_response.json()

        if polling_response['status'] == 'completed':
            break

        time.sleep(5)


# Get the paragraphs of the transcript
def get_paragraphs(polling_endpoint):
    paragraphs_response = requests.get(polling_endpoint + "/paragraphs", 
        headers={
            'authorization': 'cce02bd99aad4aa9924721f4639be93e',
            'content-type': 'application/json'
        },
    )
    paragraphs_response = paragraphs_response.json()

    paragraphs = []
    for para in paragraphs_response['paragraphs']:
        paragraphs.append(para)

    return paragraphs_response

def get_json_transcript(polling_endpoint):
    response = requests.get(polling_endpoint, 
        headers={
            'authorization': 'cce02bd99aad4aa9924721f4639be93e',
            'content-type': 'application/json'
        },
    )
    return response.json()