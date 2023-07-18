import os
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcloud/audio-censor-test-46a73980f2c8.json"

storage_client = storage.Client()

bucket = storage_client.bucket("censor-uploads")

class GCStorage:

    def upload_file(self, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)

        print(
            f"File {source_file_name} uploaded to {destination_blob_name}."
        )
    
    def download_file_stream(self, filename):
        print("todo")

        blob = bucket.blob(filename)
        blob.reload()
        content_type = blob.content_type

        file_stream = blob.download_as_bytes()
        print(f"Content type: {content_type}")

        return file_stream, content_type