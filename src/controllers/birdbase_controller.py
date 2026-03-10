from src.bootstrap import app
from src.models.rest import Rest


@app.route("/birds/birdbase", methods=["POST"])
def parse_birdbase():

    # https://springernature.figshare.com/articles/dataset/BIRDBASE_A_Global_Database_of_Avian_Biogeography_Conservation_Ecology_and_Life_History_Traits/27051040?file=55634729
    
    # baixar xlsx /tmp

    # converter para parquet

    # carregar no https://console.cloud.google.com/storage/browser/birdbase_databse;tab=objects?project=mackenzie-engenharia-dados&prefix=&forceOnObjectsSortingFiltering=false

    # colunas no bq
    # https://console.cloud.google.com/bigquery?referrer=search&project=mackenzie-engenharia-dados&ws=!1m5!1m4!4m3!1smackenzie-engenharia-dados!2sbirdbase_bronze!3sdata

    # https://cloud.google.com/sdk?utm_source=google&utm_medium=cpc&utm_campaign=latam-BR-all-pt-dr-BKWS-all-all-trial-e-dr-1605194-LUAC0008672&utm_content=text-ad-none-any-DEV_c-CRE_526696106061-ADGP_Hybrid%20%7C%20BKWS%20-%20EXA%20%7C%20Txt%20~%20Dev-Tools_SDK-KWID_43700040369790130-kwd-610235859304&utm_term=KW_google%20cloud%20sdk-ST_Google%20Cloud%20SDK&gclid=Cj0KCQjwiIOmBhDjARIsAP6YhSVKjAjopS3ryD-myeprNpCK20IfHcZ9mLoWaVv-fQq5dDsw0_oIO5caAtDzEALw_wcB&gclsrc=aw.ds&hl=pt-br
    
    return Rest.get_response_default(
        results={},
        message="Captura concluída",
    )


   