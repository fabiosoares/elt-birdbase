import json

class Taxonomy:

    def __init__(self, filepath):
        self.filepath = filepath

    def get_taxonomy_list(self):
        """
        Carrega o arquivo JSON e retorna uma lista de URLs que contêm '/taxonomy'.
        """
        requisicoes_taxonomy = []

        try:

            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado no caminho: {self.filepath}")
            return []
        except json.JSONDecodeError:
            print("Erro: Não foi possível decodificar o arquivo JSON. Verifique se o formato está correto.")
            return []

        # Verifica se existe log.entries
        if "log" not in data or "entries" not in data["log"]:
            print("Formato inesperado. A estrutura HAR não possui 'log.entries'.")
            return []

        for entry in data["log"]["entries"]:
            # Verifica se existe request.url
            if "request" in entry and "url" in entry["request"]:
                url = entry["request"]["url"]
                if "/taxonomy" in url:
                    requisicoes_taxonomy.append(url)

        return requisicoes_taxonomy

if __name__ == "__main__":
    filename = "/var/www/elt-birds-of-the-world/birdsoftheworld.org.har"
    taxonomy = Taxonomy(filename)
    taxonomy_list = taxonomy.get_taxonomy_list()

    # Imprime as requisições encontradas
    for req in taxonomy_list:
        print(req)

    print(f"\nTotal de requisições /taxonomy encontradas: {len(taxonomy_list)}")