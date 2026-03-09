from src.bootstrap import app
from src.models.rest import Rest
from src.models.wiki_aves_brasil import WikiAvesBrasil
from src.models.bird_pt_br_data_manager import BirdPtBrDataManager
# from src.models.repository.aves_nomes_pt_br_table import AvesNomesPtBrTable


@app.route("/birds/names", methods=["POST"])
def parse_ptbr_names():

    wiki_aves_brasil = WikiAvesBrasil()
    bird_data_manager = BirdPtBrDataManager()

    birds_list = wiki_aves_brasil.get_bird_list()

    for e in birds_list:
        bird_data_manager.add_bird_data(
            e["nm_cientifico"],
            e["nm_portugues"]
        )

    # table = AvesNomesPtBrTable()
    # table.load_json_into_bq(bird_data_manager.filename)

    return Rest.get_response_default(
        results={},
        message="Captura concluída",
    )
