import requests
from bs4 import BeautifulSoup
import re

class WikiAvesBrasil:

    def __init__(self):
        self.url  = "https://pt.wikipedia.org/wiki/Lista_de_aves_do_Brasil"

    def get_bird_list(self):
        """
        Pega o HTML de uma página da Wikipedia e retorna uma lista de dicionários
        com o nome científico e o nome em português de aves.

        Args:
            url (str): URL da página da Wikipedia.

        Returns:
            list: Uma lista de dicionários com 'nm_cientifico' e 'nm_portugues'.
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(self.url, headers=headers)
        response.raise_for_status()  # Levanta um erro para status de resposta ruins (4xx ou 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        birds_data = []

        # Find the main content area where bird lists are typically found
        # The 'mw-parser-output' div usually contains the main content of Wikipedia pages
        content_div = soup.find('div', class_='mw-parser-output')
        if not content_div:
            content_div = soup # Fallback if specific div not found

        # Find all list items (<li>) that contain an <i> tag (for scientific name)
        # and an <a> tag inside that <i> tag.
        list_items = content_div.find_all('li')

        for li in list_items:
            scientific_name_tag = li.find('i')
            nm_cientifico = None
            nm_portugues = None

            if scientific_name_tag:
                # Extract scientific name from the <a> tag within the <i> tag
                a_tag_in_i = scientific_name_tag.find('a')
                if a_tag_in_i:
                    nm_cientifico = a_tag_in_i.get_text(strip=True)

                # Now, try to find the Portuguese name
                # It's usually an <a> tag that is not nested inside an <i> tag
                portuguese_name_candidates = []
                for a_tag in li.find_all('a'):
                    # If the parent of <a> is not <i>, it's a candidate for the Portuguese name
                    if a_tag.find_parent('i') is None:
                        # Filter out 'red links' (class='new') and reference numbers like '[1]'
                        if not (a_tag.has_attr('class') and 'new' in a_tag['class']) and not re.match(r'^\[\d+\]$', a_tag.get_text(strip=True)):
                            portuguese_name_candidates.append(a_tag)

                # If there are multiple candidates, the last one is often the correct Portuguese name
                if portuguese_name_candidates:
                    nm_portugues = portuguese_name_candidates[-1].get_text(strip=True)
                    # Clean up the Portuguese name from potential references or extra details
                    nm_portugues = re.sub(r'\s*\([^)]*\)', '', nm_portugues).strip()
                    nm_portugues = re.sub(r'\[\d+\]', '', nm_portugues).strip()

            if nm_cientifico and nm_portugues:
                bird = {
                    "nm_cientifico": nm_cientifico,
                    "nm_portugues": nm_portugues
                }
                birds_data.append(bird)

        return birds_data 


if __name__ == "__main__":
    model = WikiAvesBrasil()
    list = model.get_bird_list()
    print(list)