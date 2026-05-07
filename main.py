import json
import logging
import time
import requests
from bs4 import BeautifulSoup
from config import URL_TO_SCRAP, BASE_URL, HEADERS
from playwright.sync_api import sync_playwright

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def obtener_html_requests(url, max_retries=3):
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


def obtener_html_playwright(url):
    logger.info("Usando Playwright para obtener HTML")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=HEADERS["User-Agent"])
        page = context.new_page()
        page.goto(url, timeout=60000)
        time.sleep(2)
        html = page.content()
        browser.close()
        return html


def obtener_html(url, usar_playwright=False):
    try:
        if usar_playwright:
            return obtener_html_playwright(url)
        return obtener_html_requests(url)
    except Exception as e:
        logger.warning(f"Requests falló: {e}, intentando con Playwright")
        return obtener_html_playwright(url)


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


def extraer_publicaciones(html):
    soup = BeautifulSoup(html, "lxml")
    publicaciones = []

    for h4 in soup.find_all("h4"):
        titulo = h4.get_text(strip=True)

        pdf_link = None
        for hermano in h4.previous_siblings:
            a = None
            if hermano.name == "a":
                a = hermano
            elif hasattr(hermano, "find"):
                a = hermano.find("a")

            if a and a.get("href", "").endswith(".pdf"):
                pdf_link = a["href"]
                if not pdf_link.startswith("http"):
                    pdf_link = BASE_URL + pdf_link
                break

        div_fecha = h4.find_next("div", class_="data_editorial")
        fecha = div_fecha.get_text(strip=True) if div_fecha else None

        if titulo and pdf_link:
            publicaciones.append({
                "titulo": titulo,
                "fecha": fecha,
                "pdf": pdf_link
            })

    return publicaciones


def ejecutar_scraper():
    logger.info("="*50)
    logger.info("INICIANDO SCRAPER COMPLETO")
    logger.info("="*50)

    logger.info("Paso 1: Obteniendo categorías")
    html = obtener_html(URL_TO_SCRAP)
    categorias = extraer_categorias(html)
    logger.info(f"Categorías encontradas: {len(categorias)}")

    todas_publicaciones = []

    for i, cat in enumerate(categorias):
        logger.info(f"Procesando categoría {i+1}/{len(categorias)}: {cat['nombre']}")
        
        try:
            html_cat = obtener_html(cat["url"])
            publicaciones = extraer_publicaciones(html_cat)
            logger.info(f"  Publicaciones encontradas: {len(publicaciones)}")
            
            for pub in publicaciones:
                todas_publicaciones.append({
                    "categoria": cat["nombre"],
                    "url_categoria": cat["url"],
                    "titulo": pub["titulo"],
                    "fecha": pub["fecha"],
                    "pdf": pub["pdf"]
                })
        except Exception as e:
            logger.error(f"  Error al procesar categoría: {e}")
        
        time.sleep(1)

    resultado = {
        "total_categorias": len(categorias),
        "total_publicaciones": len(todas_publicaciones),
        "categorias": categorias,
        "publicaciones": todas_publicaciones
    }

    with open("resultado.json", "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    logger.info(f"="*50)
    logger.info(f"SCRAPER COMPLETADO")
    logger.info(f"Total categorías: {len(categorias)}")
    logger.info(f"Total publicaciones: {len(todas_publicaciones)}")
    logger.info(f"Resultado guardado en: resultado.json")
    logger.info(f"="*50)
    
    return resultado


if __name__ == "__main__":
    ejecutar_scraper()