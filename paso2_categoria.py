
# paso2_categoria.py
import requests
from bs4 import BeautifulSoup
from config import BASE_URL,HEADERS

# Usamos Cemiterior como categoria de prueba 
URL_CATEGORIA = "https://cmfdoc.funchal.pt/publicitações/mm-editais-cemiterios.html"

# Descargamos la pagina de la categoria
respuesta = requests.get(URL_CATEGORIA, headers=HEADERS)

# Comprobamos que la solicitud esta bien co u prit del status_code
print(f"Codigo de respuesta: {respuesta.status_code}")

# Paso para transformar el HTML en ua estructura de arbol avegable
soup = BeautifulSoup(respuesta.text, "html.parser") 

# Declaramos la variable para guardar las publicaciones
publicaciones = []

# La estructura HTML de cada publicacion es :
#  1. <a href="enlace_al_pdf"><img...></a> =====> enlace al PDF
#  2. <h>Titulo de la publicacio</h4>  =========>  titulo
#  3. Fecha e texto suelto   ===================> fecha

# Buscamos todos los <h4> - cada uno es una publicacion 
for h4 in soup.find_all("h4"):

    # Recogemos el valor del titulo 
    titulo = h4.get_text(strip=True)

    # El PDF esta en el <a> que hay ANTES del <h4>
    # previous_sibling navega hacia atras en el HTML
    pdf_link = None

    # Bucle para recoger los enlaces al PDF
    # Iteramos hacia atras el arbol HTML desde el <h4>
    for hermano_a_pdf in h4.previous_siblings:

        # Cada iteracion se reinicia la variable a
        a = None

        # El hermano puede ser directamente un <a> o contenerlo
        if hermano_a_pdf.name == "a":

            a = hermano_a_pdf
        # Comprueba que el hermano sea un Tag de BeautifulSoup antes de llamar a .find()
        elif hasattr(hermano_a_pdf , "find"):

            a = hermano_a_pdf.find("a")

        # Si se encontro un <a> comprueba que su atributo:
        # 1. Existe guardamos en variable , si no existe devulve "" 
        # 2. Termina en .pdf 
        if a and a.get("href", "").endswith(".pdf"):
            pdf_link = a["href"]
            
            if not pdf_link.startswith("http"):
                pdf_link = BASE_URL + pdf_link

            break

    # La fecha esta justo DESPUES del <h4> como texto suelto
    fecha = None

    # Vamos a buscar la etiqueta de la fecha dentro del h4 que recogemos del BeutifulSoup
    div_fecha = h4.find_next("div", class_="data_editorial")
    fecha = div_fecha.get_text(strip=True) if div_fecha else None