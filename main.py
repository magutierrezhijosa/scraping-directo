# Importamos playright
from playwright.sync_api import sync_playwright


# Creamos el contxt manager 
with sync_playwright() as p:

    
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://cmfdoc.funchal.pt/publicitações")

    print(page.title())

    browser.close()


