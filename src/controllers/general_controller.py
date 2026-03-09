import json
import os
import re

from src.bootstrap import app

from src.models.rest import Rest


@app.route("/", methods=["GET"])
def hello_world():
    """Hello World
    gcloud functions deploy hello_world --runtime python39 \
        --trigger-http --allow-unauthenticated
    """
    return Rest.get_response_default({"data": "hello world!"})


@app.route("/conf", methods=["GET"])
def get_conf():
    """Exibe as atuais configurações do sistema"""

    config = (
        str(app.config)
        .replace("<Config ", "")[0:-1]
        .replace("'", '"')
        .replace("None", "null")
        .replace("False", "false")
        .replace("True", "true")
    )
    config = re.sub(r"(datetime\.[^,]+)", r'"\1"', config)

    return Rest.get_response_default(
        {
            "data": {
                "FLASK_ENV": os.environ.get("FLASK_ENV"),
                "CONFIG_ENV": app.config["ENV"],
                "CONFIG_STR": str(config),
                "CONFIG": json.loads(str(config)),
            }
        }
    )
