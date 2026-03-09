import json
import os

class BirdPtBrDataManager:
    def __init__(self, filename="birds_pt_br.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Ensures the JSON file exists and is initialized as an empty list if not."""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f) # Initialize with an empty list

    def _load_data(self):
        """Loads existing data from the JSON file."""
        with open(self.filename, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_data(self, data):
        """Saves data to the JSON file."""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def cientific_name_exists(self, nm_cientifico):
        """Checks if a scientific name already exists in the JSON file."""
        data = self._load_data()
        for entry in data:
            if entry.get("nm_cientifico") == nm_cientifico:
                return True
        return False

    def add_bird_data(self, nm_cientifico, nm_portugues):
        """
        Adds new bird data to the JSON file, preventing duplicates based on scientific name.

        Args:
            nm_cientifico (str): The scientific name of the bird.
            nm_portugues (str): The portuguese name.

        Returns:
            bool: True if data was added, False if it was a duplicate.
        """
        data = self._load_data()
        
        # Check for duplicates based on nm_cientifico
        if self.cientific_name_exists(nm_cientifico):
            print(f"Scientific name '{nm_cientifico}' already exists. Skipping insertion.")
            return False # Indicate that no new data was added
                

        new_entry = {
            "nm_cientifico": nm_cientifico,
            "nm_portugues": nm_portugues,
        }
        data.append(new_entry)
        self._save_data(data)
        print(f"Successfully added data for '{nm_cientifico}'.")
        return True # Indicate that data was successfully added