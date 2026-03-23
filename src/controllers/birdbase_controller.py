from src.bootstrap import app
from src.models.rest import Rest

import pandas as pd
from google.cloud import storage, bigquery


@app.route("/birds/birdbase", methods=["POST"])
def parse_birdbase():

    try:

        # =============================
        # CONFIGURAÇÕES
        # =============================
        xlsx_path = "data/birdbase.xlsx"
        parquet_path = "/tmp/birdbase.parquet"

        bucket_name = "birdbase-database"
        gcs_file_name = "birdbase.parquet"

        project_id = "mackenzie-engenharia-dados"
        dataset_id = "birdbase_bronze"
        table_id = "data_parquet"

        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        gcs_uri = f"gs://{bucket_name}/{gcs_file_name}"

        # =============================
        # 1. LER EXCEL (HEADER CORRETO)
        # =============================
        df = pd.read_excel(
            xlsx_path,
            engine="openpyxl",
            header=1  # 👈 usa a segunda linha (97 colunas)
        )

        print("TOTAL COLUNAS FINAL:", len(df.columns))

        # =============================
        # 2. LIMPEZA
        # =============================

        df = df.dropna(axis=1, how="all")
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"[^\w]", "_", regex=True)  # substitui especiais por _
            .str.replace(r"_+", "_", regex=True)     # remove duplicados
            .str.replace(r"_$", "", regex=True)      # remove _ no final
)

        # =============================
        # 3. AJUSTE DE TIPOS
        # =============================

        for col in df.columns:

            converted = pd.to_numeric(df[col], errors="coerce")

            if converted.notna().sum() > len(df) * 0.7:
                df[col] = converted
            else:
                df[col] = df[col].astype(str)

        # =============================
        # 4. PARQUET
        # =============================
        df.to_parquet(parquet_path, index=False)

        # =============================
        # 5. UPLOAD GCS
        # =============================
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_file_name)
        blob.upload_from_filename(parquet_path)

        # =============================
        # 6. BIGQUERY
        # =============================
        bq_client = bigquery.Client()

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            autodetect=True,
            write_disposition="WRITE_TRUNCATE"
        )

        load_job = bq_client.load_table_from_uri(
            gcs_uri,
            table_ref,
            job_config=job_config
        )

        load_job.result()

        # =============================
        # RESPOSTA
        # =============================
        return Rest.get_response_default(
            results={
                "rows": len(df),
                "columns": list(df.columns),
                "total_columns": len(df.columns),
                "table_created": table_ref
            },
            message="Pipeline executado com sucesso (Excel → Parquet → GCS → BigQuery)",
        )

    except Exception as e:

        return Rest.get_response_default(
            results={},
            message=str(e),
        )