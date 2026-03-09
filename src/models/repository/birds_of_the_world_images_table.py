import pandas as pd
import pandas_gbq

class BirdsOfTheWorldImagesTable:


    def load_json_into_bq(self, filepath):

        df_birds = pd.read_json(filepath)
        print("JSON file loaded successfully into df_birds.")
        print(df_birds.head())



        pandas_gbq.to_gbq(
            df_birds,
            destination_table='birdbase_bronze.birds_of_the_world_images',
            project_id='mackenzie-engenharia-dados',
            if_exists='replace',
            auth_local_webserver=False
        )
        print("DataFrame successfully loaded into BigQuery table.")