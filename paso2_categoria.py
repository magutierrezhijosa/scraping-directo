import logging
import requests
from bs4 import BeautifulSoup
from config import BASE_URL, HEADERS

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


def extraer_publicaciones(html):
    soup = BeautifulSoup(html, "lxml")
    publicaciones = []

    for h4 in soup.find_all("h4"):
        titulo = h4.get_text(strip=True)

        pdf_link = None
        for hermano_a_pdf in h4.previous_siblings:
            a = None
            if hermano_a_pdf.name == "a":
                a = hermano_a_pdf
            elif hasattr(hermano_a_pdf, "find"):
                a = hermano_a_pdf.find("a")

            if a and a.get("href", "").endswith(".pdf"):
                pdf_link = a["href"]
                if not pdf_link.startswith("http"):
                    pdf_link = BASE_URL + pdf_link
                break

        div_fecha = h4.find_next("div", class_="data_editorial")
        fecha = div_fecha.get_text(strip=True) if div_fecha else None

        publicaciones.append({
            "titulo": titulo,
            "fecha": fecha,
            "pdf": pdf_link
        })

    return publicaciones


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        logger.error("Uso: python paso2_categoria.py <url_categoria>")
        sys.exit(1)

    url_categoria = sys.argv[1]
    logger.info(f"Extrayendo publicaciones de: {url_categoria}")
    html = obtener_html(url_categoria)

    if html:
        publicaciones = extraer_publicaciones(html)
        logger.info(f"Publicaciones encontradas: {len(publicaciones)}")
        for pub in publicaciones[:3]:
            print(f"Titulo: {pub['titulo']}")
            print(f"Fecha: {pub['fecha']}")
            print(f"PDF: {pub['pdf']}")
            print()