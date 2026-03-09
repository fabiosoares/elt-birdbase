from google.cloud import storage
import os

class ImageUploader:
    def __init__(self):
        self.project_id = "mackenzie-engenharia-dados"
        self.bucket_name = "birdbase_birds_of_the_world"

    def upload_image(self, source_file_name):

        destination_blob_name = os.path.basename(source_file_name)

        def upload_blob(bucket_name, source_file_name, destination_blob_name):
            """Uploads a file to the Google Cloud Storage bucket."""
            storage_client = storage.Client(project=self.project_id )
            bucket = storage_client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_filename(source_file_name)

            print(f"File {source_file_name} uploaded to {destination_blob_name} in bucket {bucket_name}.")

        try:
            upload_blob(self.bucket_name, source_file_name, destination_blob_name)
        except Exception as e:
            print(f"Error uploading file: {e}")

if __name__ == "__main__":
    uploader = ImageUploader()
    test_file_path = "images/arses_insularis.jpg"
    uploader.upload_image(test_file_path)