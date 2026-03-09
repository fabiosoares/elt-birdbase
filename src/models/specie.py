# https://birdsoftheworld.org/bow/api/v1/taxonomy?depth=2&rootTaxonCode=monarc2&locale=en
import requests

class Specie:

    def _get_response_json(self, url):
        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    def _extract_species(self, entry, result_list):
        """Percorre a árvore e coleta espécies (category='species')."""
        if entry.get("category") == "species":
            sci = entry.get("sciName")
            asset = entry.get("illusAssetId")
            result_list.append((sci, asset))

        # Se houver subtaxa, percorrer recursivamente
        sub = entry.get("subTaxa", [])
        for item in sub:
            self._extract_species(item, result_list)

    def get_species(self, url):
        species = []
        data = self._get_response_json(url)
        self._extract_species(data, species)
        species = self._parse_species(species)
        return species

    def _parse_species(self, data):
        species = []
        for sci, asset in data:
            species.append({
                "nm_cientifico": sci,
                "nm_cientifico_minusculo": sci.lower(),
                "nm_arquivo": sci.lower().replace(" ", "_") + ".jpg",
                "id_imagem": asset,
                "ds_imagem_url": f"https://cdn.download.ams.birds.cornell.edu/api/v1/asset/{asset}/160",
                "nm_gcp_path": f"https://storage.cloud.google.com/birdbase_birds_of_the_world/{sci.lower().replace(' ', '_')}.jpg"
            })
        return species

if __name__ == "__main__":
    species = Specie().get_species()
    print(species)
