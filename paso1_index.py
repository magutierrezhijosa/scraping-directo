
# paso1_index.py
import requests
from bs4 import BeautifulSoup

# Importamos las CONSTANTES
from config import URL_TO_SCRAP,BASE_URL

# Paso 1 : Descargar la pagina
# request.get() hace una peticion HTTP GET - como cuando tu navegador carga la pagina
respuesta = requests.get(URL_TO_SCRAP)

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
    