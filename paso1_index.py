
# paso1_index.py
import logging
import requests
from bs4 import BeautifulSoup
from config import URL_TO_SCRAP, BASE_URL, HEADERS

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def obtener_html(url, max_retries=3):
    for intento in range(max_retries):
        try:
            respuesta = requests.get(url, headers=HEADERS, timeout=30)
            respuesta.raise_for_status()
            logger.info(f"Request exitosa: {respuesta.status_code}")
            return respuesta.text
        except requests.RequestException as e:
            logger.warning(f"Intento {intento + 1}/{max_retries} falló: {e}")
            if intento == max_retries - 1:
                raise
    return None


def extraer_categorias(html):
    soup = BeautifulSoup(html, "lxml")
    categorias = []

    for h2 in soup.find_all("h2"):
        enlace = h2.find("a")
        if enlace and "/publicitações" in enlace.get("href", ""):
            nombre = enlace.get_text(strip=True)
            url = enlace.get("href", "")
            if not url.startswith("http"):
                url = BASE_URL + url
            categorias.append({"nombre": nombre, "url": url})

    return categorias


if __name__ == "__main__":
    logger.info("Iniciando extracción de categorías")
    html = obtener_html(URL_TO_SCRAP)
    if html:
        categorias = extraer_categorias(html)
        logger.info(f"Categorías encontradas: {len(categorias)}")
        for cat in categorias:
            print(f"  - {cat['nombre']}: {cat['url']}")