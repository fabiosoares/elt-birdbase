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
        table_id = "data"

        table_ref = f"{project_id}.{dataset_id}.{table_id}"
        gcs_uri = f"gs://{bucket_name}/{gcs_file_name}"

        # =============================
        # 1. LER EXCEL (HEADER CORRETO)
        # =============================
        df = pd.read_excel(
            xlsx_path,
            engine="openpyxl",
            header=1,
            dtype=str
        )

        print("TOTAL COLUNAS FINAL:", len(df.columns))

        # =============================
        # 2. LIMPEZA (PADRÃO NOMES)
        # =============================
        df = df.dropna(axis=1, how="all")
        df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

        df.columns = (
            df.columns
            .astype(str)
            .str.strip()
            .str.lower()
            .str.replace(r"[^\w]", "_", regex=True)
            .str.replace(r"_+", "_", regex=True)
            .str.replace(r"_$", "", regex=True)
        )

        # =============================
        # 3. AJUSTE DE TIPOS BASEADO NO SCHEMA
        # =============================

        int_cols = [
            "ioc_15_1","rr","isl","lat","female_minmass","male_minmass",
            "male_maxmass","unsexed_minmass","unsexed_maxmass","average_mass",
            "f","bm","wd","sh","sv","g","pl","r","d","a","rv","c","w","se","o",
            "hb","sum_wt","db","diet_lit","esi","mono","poly","coop",
            "brd1","brd2","clutch_min","clutch_max","incu1","incu2",
            "fldg1","fldg2","para_1","brs1","prod1","mig","alt","irreg","disp","sed"
        ]

        float_cols = [
            "female_maxmass"
        ]

        for col in df.columns:

            if col in int_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = (df[col] * 100).round(0)
                df[col] = df[col].astype("Int64")

            elif col in float_cols:
                df[col] = pd.to_numeric(df[col], errors="coerce")

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
        # 6. SCHEMA FIXO BIGQUERY
        # =============================
        bq_client = bigquery.Client()

        schema = [
            bigquery.SchemaField("ioc_15_1", "INTEGER"),
            bigquery.SchemaField("english_name_birdlife_ioc_clements_avilist", "STRING"),
            bigquery.SchemaField("latin_birdlife_ioc_clements_avilist", "STRING"),
            bigquery.SchemaField("hbw_birdlife_international_v9_1", "STRING"),
            bigquery.SchemaField("ioc_world_bird_list_v15_1", "STRING"),
            bigquery.SchemaField("ebird_clements_v2024b", "STRING"),
            bigquery.SchemaField("avilist_v1_2025", "STRING"),
            bigquery.SchemaField("order", "STRING"),
            bigquery.SchemaField("family_ioc_15_1", "STRING"),
            bigquery.SchemaField("family_clements_v2024b", "STRING"),
            bigquery.SchemaField("family_hbw_birdlife_v9_1_2024", "STRING"),
            bigquery.SchemaField("family_avilist_v1_2025", "STRING"),
            bigquery.SchemaField("genus", "STRING"),
            bigquery.SchemaField("species", "STRING"),
            bigquery.SchemaField("source", "STRING"),
            bigquery.SchemaField("2024_iucn_red_list_category", "STRING"),
            bigquery.SchemaField("rr", "INTEGER"),
            bigquery.SchemaField("isl", "INTEGER"),
            bigquery.SchemaField("rlm", "STRING"),
            bigquery.SchemaField("lat", "INTEGER"),
            bigquery.SchemaField("female_minmass", "INTEGER"),
            bigquery.SchemaField("female_maxmass", "FLOAT"),
            bigquery.SchemaField("male_minmass", "INTEGER"),
            bigquery.SchemaField("male_maxmass", "INTEGER"),
            bigquery.SchemaField("unsexed_minmass", "INTEGER"),
            bigquery.SchemaField("unsexed_maxmass", "INTEGER"),
            bigquery.SchemaField("average_mass", "INTEGER"),
            bigquery.SchemaField("xmin", "STRING"),
            bigquery.SchemaField("normmin", "STRING"),
            bigquery.SchemaField("elevational_range", "STRING"),
            bigquery.SchemaField("normmax", "STRING"),
            bigquery.SchemaField("xmax", "STRING"),
            bigquery.SchemaField("f", "INTEGER"),
            bigquery.SchemaField("bm", "INTEGER"),
            bigquery.SchemaField("wd", "INTEGER"),
            bigquery.SchemaField("sh", "INTEGER"),
            bigquery.SchemaField("sv", "INTEGER"),
            bigquery.SchemaField("g", "INTEGER"),
            bigquery.SchemaField("pl", "INTEGER"),
            bigquery.SchemaField("r", "INTEGER"),
            bigquery.SchemaField("d", "INTEGER"),
            bigquery.SchemaField("a", "INTEGER"),
            bigquery.SchemaField("rv", "INTEGER"),
            bigquery.SchemaField("c", "INTEGER"),
            bigquery.SchemaField("w", "INTEGER"),
            bigquery.SchemaField("se", "INTEGER"),
            bigquery.SchemaField("o", "INTEGER"),
            bigquery.SchemaField("o_desc", "STRING"),
            bigquery.SchemaField("primary_habitat", "STRING"),
            bigquery.SchemaField("hb", "INTEGER"),
            bigquery.SchemaField("primary_diet", "STRING"),
            bigquery.SchemaField("in_wt", "STRING"),
            bigquery.SchemaField("fr_wt", "STRING"),
            bigquery.SchemaField("ne_wt", "STRING"),
            bigquery.SchemaField("se_wt", "STRING"),
            bigquery.SchemaField("ve_wt", "STRING"),
            bigquery.SchemaField("fi_wt", "STRING"),
            bigquery.SchemaField("sc_wt", "STRING"),
            bigquery.SchemaField("pl_wt", "STRING"),
            bigquery.SchemaField("ms_wt", "STRING"),
            bigquery.SchemaField("sum_wt", "INTEGER"),
            bigquery.SchemaField("desc", "STRING"),
            bigquery.SchemaField("db", "INTEGER"),
            bigquery.SchemaField("diet_lit", "INTEGER"),
            bigquery.SchemaField("esi", "INTEGER"),
            bigquery.SchemaField("social_1", "STRING"),
            bigquery.SchemaField("social_2", "STRING"),
            bigquery.SchemaField("social_3", "STRING"),
            bigquery.SchemaField("social_4", "STRING"),
            bigquery.SchemaField("social_5", "STRING"),
            bigquery.SchemaField("social_6", "STRING"),
            bigquery.SchemaField("mono", "INTEGER"),
            bigquery.SchemaField("poly", "INTEGER"),
            bigquery.SchemaField("coop", "INTEGER"),
            bigquery.SchemaField("nest_type", "STRING"),
            bigquery.SchemaField("nest_sbs", "STRING"),
            bigquery.SchemaField("brd1", "INTEGER"),
            bigquery.SchemaField("brd2", "INTEGER"),
            bigquery.SchemaField("clutch_min", "INTEGER"),
            bigquery.SchemaField("clutch_max", "INTEGER"),
            bigquery.SchemaField("incu_sex", "STRING"),
            bigquery.SchemaField("incu1", "INTEGER"),
            bigquery.SchemaField("incu2", "INTEGER"),
            bigquery.SchemaField("fldg1", "INTEGER"),
            bigquery.SchemaField("fldg2", "INTEGER"),
            bigquery.SchemaField("para_1", "INTEGER"),
            bigquery.SchemaField("para_2", "STRING"),
            bigquery.SchemaField("brs1", "INTEGER"),
            bigquery.SchemaField("brs2", "STRING"),
            bigquery.SchemaField("prod1", "INTEGER"),
            bigquery.SchemaField("prod2", "STRING"),
            bigquery.SchemaField("flightlessness", "STRING"),
            bigquery.SchemaField("mig", "INTEGER"),
            bigquery.SchemaField("alt", "INTEGER"),
            bigquery.SchemaField("irreg", "INTEGER"),
            bigquery.SchemaField("disp", "INTEGER"),
            bigquery.SchemaField("sed", "INTEGER"),
        ]

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.PARQUET,
            schema=schema,
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