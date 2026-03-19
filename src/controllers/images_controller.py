from src.bootstrap import app
from src.models.rest import Rest
from src.models.specie import Specie
from src.models.birds_data_manager import BirdDataManager
from src.models.image import Image
from src.models.image_uploader import ImageUploader
from src.models.repository.birds_of_the_world_images_table import BirdsOfTheWorldImagesTable
from src.models.taxonomy_code import TaxonomyCode

def get_taxonomy_list():
    filename = "./birdsoftheworld_taxonomy_code.json"
    taxonomy = TaxonomyCode(filename)
    taxonomy_list = taxonomy.get_taxonomy_list()
    return taxonomy_list

def process_images(species, bird_data_manager, uploader):
    new_count = 0
    for e in species:

        if bird_data_manager.cientific_name_exists(e['nm_cientifico']):
            print(f"Nome científico '{e['nm_cientifico']}' já existe no GCS. Pulando.")
            continue
        
        image = Image(e['ds_imagem_url'], e['nm_arquivo'])
        if image.download_image():
            bird_data_manager.add_bird_data(e['nm_cientifico'], e['ds_imagem_url'], e['nm_arquivo'], e['nm_gcp_path'])

            local_file_path = f"images/{ e['nm_arquivo']}"
            uploader.upload_image(local_file_path)
            new_count += 1

    return new_count

@app.route("/birds/images", methods=["POST"])
def parse_images():
    specie = Specie()
    taxonomy_list = get_taxonomy_list()
    bird_data_manager = BirdDataManager()
    uploader = ImageUploader()
    total_new = 0

    for url in taxonomy_list:
        print(f"URL: {url}")
        species = specie.get_species(url)
        total_new += process_images(species, bird_data_manager, uploader)

    # Only load into BigQuery if there are new images
    if total_new > 0:
        table = BirdsOfTheWorldImagesTable()
        table.load_json_into_bq(bird_data_manager.filename)
        print(f"Carregou {total_new} novas imagens no BigQuery.")
    else:
        print("Nenhuma imagem nova encontrada. Carga no BigQuery não necessária.")

    return Rest.get_response_default(
        results={"new_images": total_new},
        message="Captura concluída",
    )


   