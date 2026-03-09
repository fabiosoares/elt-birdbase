from flask import jsonify, make_response


class Rest:
    """
    Abstração para criar respostas de uma API RESTful.
    """

    STATUS_ERROR = "ERROR"
    STATUS_SUCCESS = "SUCCESS"

    CODE_SUCCESS = "200"
    CODE_BAD_REQUEST = "400"
    CODE_UNAUTHORIZED = "401"
    CODE_TOO_MANY_REQUEST = "429"
    CODE_INTERNAL_SERVER_ERROR = "500"
    CODE_BAD_GATEWAY = "502"
    CODE_SERVICE_UNVAILABLE = "503"

    @staticmethod
    def get_response_default(
        results: dict,
        message="",
        code=None,
        status=None,
    ):
        """
        Método auxiliar para criar uma resposta JSON padronizada.

        Args:
            results (dict): Os dados que serão enviados na resposta. Este é
            o único parâmetro obrigatório.
            message (str, optional): Uma mensagem opcional que pode ser
            incluída na resposta. Default é uma string vazia.
            code (str, optional): Um código opcional que representa o
            status da resposta HTTP. Default é '200' (sucesso).
            status (str, optional): Um status opcional que representa o
            estado da operação. Default é 'SUCCESS'.

        Returns:
            dict: Retorna um jsonify que padroniza a saída da requisição.
        """

        return Rest.get_response_pattern(results, code, status, message)

    @staticmethod
    def get_response_pattern(
        results,
        code=None,
        status=None,
        message=None,
    ):
        """
        Método auxiliar para criar uma resposta JSON padronizada.

        Args:
            results (dict): Os dados que serão enviados na resposta. Este é
            o único parâmetro obrigatório.
            code (str, optional): Um código opcional que representa o
            status da resposta HTTP. Default é '200' (sucesso).
            status (str, optional): Um status opcional que representa o
            estado da operação. Default é 'SUCCESS'.

        Returns:
            dict: Retorna um jsonify que padroniza a saída da requisição.
        """

        code = Rest.CODE_SUCCESS if code is None else code
        status = Rest.STATUS_SUCCESS if status is None else status

        return jsonify(
            {
                "code": code,
                "status": status,
                "results": results,
                "message": message,
            }
        )

    @staticmethod
    def get_response_error(message, code, header={}):
        status = Rest.STATUS_ERROR
        return make_response(
            Rest.get_response_pattern(
                results={},
                code=code,
                status=status,
                message=message,
            ),
            code,
            header,
        )
