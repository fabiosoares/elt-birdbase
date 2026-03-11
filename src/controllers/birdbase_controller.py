from src.bootstrap import app
from src.models.rest import Rest

import pandas as pd
from google.cloud import storage
import os


@app.route("/birds/birdbase", methods=["POST"])
def parse_birdbase():

    try:

        # caminho do excel local
        xlsx_path = "data/birdbase.xlsx"

        # arquivo parquet temporário
        parquet_path = "/tmp/birdbase.parquet"

        # bucket GCS
        bucket_name = "birdbase_databse"

        # 1️⃣ Ler Excel
        df = pd.read_excel(xlsx_path, engine="openpyxl")

        # 2️⃣ Corrigir tipos mistos (erro comum ao converter para parquet)
        df = df.astype(str)

        # 3️⃣ Converter para parquet
        df.to_parquet(parquet_path, index=False)

        # 4️⃣ Conectar ao Google Cloud Storage
        client = storage.Client()
        bucket = client.bucket(bucket_name)

        # 5️⃣ Upload do parquet
        blob = bucket.blob("birdbase.parquet")
        blob.upload_from_filename(parquet_path)

        return Rest.get_response_default(
            results={
                "rows": len(df),
                "file_uploaded": "birdbase.parquet"
            },
            message="Captura concluída com sucesso",
        )

    except Exception as e:

        return Rest.get_response_default(
            results={},
            message=str(e),
        )