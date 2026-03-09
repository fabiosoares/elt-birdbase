import pandas as pd
import pandas_gbq

class AvesNomesPtBrTable:


    def load_json_into_bq(self, filepath):

        df_birds = pd.read_json(filepath)
        print("JSON file loaded successfully into df_birds.")
        print(df_birds.head())



        pandas_gbq.to_gbq(
            df_birds,
            destination_table='birdbase_bronze.aves_nomes_pt_br',
            project_id='mackenzie-engenharia-dados',
            if_exists='replace',
            auth_local_webserver=False
        )
        print("DataFrame successfully loaded into BigQuery table.")