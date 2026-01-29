# =========================
# IMPORTS
# =========================
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import os
import time

# =========================
# CONFIG
# =========================
URL = "https://andina.pe/agencia/seccion-politica-17.aspx"
MAX_NOTICIAS = 30
SCROLLS = 8

# =========================
# CHROME
# =========================
options = Options()
options.add_argument("--start-maximized")
# options.add_argument("--headless=new")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

def obtener_fecha(url):
    """Extrae la fecha desde la noticia individual"""
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        fecha = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.fecha"))
        ).text.strip()

        return fecha
    except:
        return None

try:
    driver.get(URL)
    wait = WebDriverWait(driver, 20)

    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h1 a, h2 a, h3 a"))
    )

    # =========================
    # SCROLL
    # =========================
    for _ in range(SCROLLS):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    # =========================
    # FASE 1: recolectar datos "seguros"
    # =========================
    candidatos = driver.find_elements(By.CSS_SELECTOR, "h1 a, h2 a, h3 a")

    noticias = []
    vistos = set()

    for a in candidatos:
        try:
            href = (a.get_attribute("href") or "").strip()
            if "/agencia/noticia-" not in href:
                continue
            if href in vistos:
                continue

            titular = (a.get_attribute("textContent") or "").strip()
            if not titular:
                titular = (a.get_attribute("title") or "").strip()

            if not titular:
                continue

            vistos.add(href)
            noticias.append({
                "medio": "Andina",
                "titular": titular,
                "url": href
            })

            if len(noticias) >= MAX_NOTICIAS:
                break

        except:
            continue

    # =========================
    # FASE 2: entrar a cada noticia
    # =========================
    for n in noticias:
        n["fecha"] = obtener_fecha(n["url"])
        time.sleep(0.5)

    df = pd.DataFrame(noticias)

    print(f"\n📰 Noticias extraídas: {len(df)}")
    print(df.head(10))

    # =========================
    # GUARDAR
    # =========================
    carpeta = os.path.expanduser("~/Desktop/MediaLab")
    os.makedirs(carpeta, exist_ok=True)

    ruta = os.path.join(carpeta, "agenda_andina.csv")
    df.to_csv(ruta, index=False, encoding="utf-8")

    print("\n✅ Archivo guardado en:")
    print(ruta)

finally:
    driver.quit()
