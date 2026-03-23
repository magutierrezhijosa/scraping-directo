
# paso1_index.py
import requests
from bs4 import BeautifulSoup

# Importamos las CONSTANTES
from config import URL_TO_SCRAP,BASE_URL,HEADERS

# Simulamos ser u avegador real co cabeceras HTTP
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# Paso 1 : Descargar la pagina
# request.get() hace una peticion HTTP GET - como cuando tu navegador carga la pagina
respuesta = requests.get(URL_TO_SCRAP,headers=HEADERS)

# Verificamos que fue bien (codigo 200 = OK)
print(f"Codigo de respuesta:{respuesta.status_code}")

# Paso 2: Parsear el HTML con BeautifulSoup
# "html.parser" es el motor incluido en Python - no ne cesita instalar nada
soup = BeautifulSoup(respuesta.text, "html.parser")

# Paso 3 : Buscar todas las categorias 
# Mirando el HTML , cada categoria esta en un <h2> dentro del area de  contenido
# y tiene un enlace <a> con la URL de la categoria 
categorias =  []

# Buscamos todos los <h2>  que contienen un <a>
for h2 in soup.find_all("h2"):
    # Recogemos el enlace a la pagina en detalle 
    enlace = h2.find("a")

    # Si exisate enlacxe y si contiene la URL que queremos entra
    if enlace and "/publicitações" in enlace.get("href",""):

        # Guardamos en la variable nombre el texto del titulo
        nombre = enlace.get_text(strip=True)

        # Guardamos el "href" del enlace en una variable
        url = enlace["href"]

        # Si la URL no empieza por http , le agregamos el dominio base
        if not url.startswith("http"):

            url = BASE_URL + url

        # Agregamos los valores a nuestra lista para mostrala
        categorias.append({"nombre": nombre, "url": url})

# Mostramos los resultados que hemos encontrado
print(f"\nCategorias encotradas: {len(categorias)}")
# Creamos un bucle para recorrer los datos y mostrarlos
for cat in categorias:
    
    print(f"  - {cat['nombre']}")
    print(f"  - {cat['url']}")