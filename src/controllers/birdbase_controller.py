from src.bootstrap import app
from src.models.rest import Rest

import requests
import pandas as pd
from google.cloud import storage


@app.route("/birds/birdbase", methods=["POST"])
def parse_birdbase():

    # URL do dataset
    url = "https://springernature.figshare.com/ndownloader/files/55634729"

    # caminhos locais
    xlsx_path = "/tmp/birdbase.xlsx"
    parquet_path = "/tmp/birdbase.parquet"

    # baixar xlsx
    response = requests.get(url)

    with open(xlsx_path, "wb") as f:
        f.write(response.content)

    # ler xlsx
    df = pd.read_excel(xlsx_path)

    # converter para parquet
    df.to_parquet(parquet_path)

    # enviar para Google Cloud Storage
    client = storage.Client()
    bucket = client.bucket("birdbase_databse")

    blob = bucket.blob("birdbase.parquet")
    blob.upload_from_filename(parquet_path)

    return Rest.get_response_default(
        results={"file": "birdbase.parquet"},
        message="Captura concluída",
    )