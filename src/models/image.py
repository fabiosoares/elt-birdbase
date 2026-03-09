import requests
import os

class Image:

    def __init__(self, image_url, file_name):
        self.save_directory = "images"
        self.image_url = image_url
        self.file_name = file_name

    def download_image(self):
  
        os.makedirs(self.save_directory, exist_ok=True)

        file_path = os.path.join(self.save_directory, self.file_name)

        try:
            response = requests.get(self.image_url, stream=True)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Imagem baixada com sucesso para: {file_path}")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao baixar a imagem: {e}")
        return False


if __name__ == "__main__":
    test_image_url = "https://cdn.download.ams.birds.cornell.edu/api/v1/asset/153083261/160"
    test_file_name = "test_bird_image"
    image = Image(test_image_url, test_file_name)
    image.download_image()