import json

class TaxonomyCode:

    def __init__(self, filepath):
        self.filepath = filepath
        self.family_taxon_codes = []

    def extract_family_taxon_codes(self, node):
        if isinstance(node, dict):
            if node.get('category') == 'family':
                self.family_taxon_codes.append(f"https://birdsoftheworld.org/bow/api/v1/taxonomy?depth=2&rootTaxonCode={node.get('taxonCode')}&locale=en")
            if 'subTaxa' in node and isinstance(node['subTaxa'], list):
                for sub_node in node['subTaxa']:
                    self.extract_family_taxon_codes(sub_node)
        elif isinstance(node, list):
            for item in node:
                self.extract_family_taxon_codes(item)

    def get_taxonomy_list(self):
        """
        Carrega o arquivo JSON e retorna uma lista de URLs que contêm '/taxonomy'.
        """
        self.family_taxon_codes = []

        try:

            with open(self.filepath, 'r') as f:
                data = json.load(f)
                
        except FileNotFoundError:
            print(f"Erro: Arquivo não encontrado no caminho: {self.filepath}")
            return []
        except json.JSONDecodeError:
            print("Erro: Não foi possível decodificar o arquivo JSON. Verifique se o formato está correto.")
            return []

        self.extract_family_taxon_codes(data)


        return self.family_taxon_codes

if __name__ == "__main__":
    filename = "/var/www/elt-birds-of-the-world/birdsoftheworld_taxonomy_code.json"
    taxonomy = TaxonomyCode(filename)
    taxonomy_list = taxonomy.get_taxonomy_list()

    # Imprime as requisições encontradas
    for req in taxonomy_list:
        print(req)

    print(f"\nTotal de requisições /taxonomy encontradas: {len(taxonomy_list)}")