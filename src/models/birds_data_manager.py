import json
import os
from google.cloud import storage

class BirdDataManager:
    def __init__(self, filename="birds_of_the_world.json"):
        self.filename = filename
        self.project_id = "mackenzie-engenharia-dados"
        self.bucket_name = "birdbase-birds-of-the-world"
        self._storage_client = None
        self._existing_blobs = None
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the JSON file exists and is initialized as an empty list if not."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def _get_storage_client(self):
        """Returns a cached Storage client."""
        if self._storage_client is None:
            self._storage_client = storage.Client(project=self.project_id)
        return self._storage_client

    def _load_existing_blobs(self):
        """Loads the set of existing blob names from GCS (cached per instance)."""
        if self._existing_blobs is None:
            client = self._get_storage_client()
            bucket = client.bucket(self.bucket_name)
            blobs = bucket.list_blobs()
            self._existing_blobs = {blob.name for blob in blobs}
            print(f"Loaded {len(self._existing_blobs)} existing images from GCS bucket.")
        return self._existing_blobs

    def _load_data(self):
        """Loads existing data from the JSON file."""
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, data):
        """Saves data to the JSON file."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def cientific_name_exists(self, nm_cientifico):
        """Checks if the image for a scientific name already exists in the GCS bucket."""
        existing = self._load_existing_blobs()
        blob_name = nm_cientifico.lower().replace(" ", "_") + ".jpg"
        return blob_name in existing

    def add_bird_data(self, nm_cientifico, ds_imagem_url, nm_arquivo, nm_gcp_path):
        """
        Adds new bird data to the JSON file, preventing duplicates based on scientific name.

        Args:
            nm_cientifico (str): The scientific name of the bird.
            ds_imagem_url (str): The URL of the bird image.
            nm_arquivo (str): The filename of the bird image.
            nm_gcp_path (str): The Google Cloud Storage path to the image.

        Returns:
            bool: True if data was added, False if it was a duplicate.
        """
        if self.cientific_name_exists(nm_cientifico):
            print(f"Scientific name '{nm_cientifico}' already exists in GCS. Skipping.")
            return False

        data = self._load_data()
        new_entry = {
            "nm_cientifico": nm_cientifico,
            "ds_imagem_url": ds_imagem_url,
            "nm_arquivo": nm_arquivo,
            "nm_gcp_path": nm_gcp_path,
        }
        data.append(new_entry)
        self._save_data(data)

        # Add to the in-memory cache so subsequent checks within
        # the same run also skip this species.
        blob_name = nm_cientifico.lower().replace(" ", "_") + ".jpg"
        self._existing_blobs.add(blob_name)

        print(f"Successfully added data for '{nm_cientifico}'.")
        return True
