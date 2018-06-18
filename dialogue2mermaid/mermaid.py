from bs4 import BeautifulSoup

TEMPLATE_FILE_PATH = 'template.html'


def mermaid_to_html(mermaid: str) -> str:
    template = ''
    with open(TEMPLATE_FILE_PATH, 'r') as template_file:
        template += template_file.read()
    soup = BeautifulSoup(template, 'html.parser')
    mermaid_container = soup.find('div', {'class': 'mermaid'})
    if mermaid_container is None:
        raise TypeError(f"mermaid' class <div> tag not found in '{TEMPLATE_FILE_PATH}'")
    mermaid_container.string = f"graph TB\n{mermaid}"
    return str(soup)
