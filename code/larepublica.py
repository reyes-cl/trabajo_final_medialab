from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time
import os


# =========================
# LA REPÚBLICA - SCRAPING COMPLETO (SCROLL + FECHA)
# =========================


def scroll_hasta_el_final(driver, pausa=1.5, max_intentos=20):
    """
    Hace scroll hasta que no se carguen más noticias
    """
    ultimo_alto = driver.execute_script("return document.body.scrollHeight")
    intentos = 0

    while intentos < max_intentos:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(pausa)

        nuevo_alto = driver.execute_script("return document.body.scrollHeight")
        if nuevo_alto == ultimo_alto:
            break

        ultimo_alto = nuevo_alto
        intentos += 1


def extraer_fecha(driver, wait):
    """
    Extrae la fecha desde la página individual de la noticia
    """
    try:
        time_tag = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "time"))
        )
        return time_tag.get_attribute("datetime")
    except Exception:
        return ""


def main():

    options = Options()
    options.add_argument("--start-maximized")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 15)

    try:
        url = "https://larepublica.pe/politica"
        driver.get(url)

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href]")))

        # 1️⃣ Scroll completo
        scroll_hasta_el_final(driver)

        # 2️⃣ Recolectar links
        anchors = driver.find_elements(By.CSS_SELECTOR, "a[href]")

        noticias = []
        vistos = set()

        for a in anchors:
            titulo = a.text.strip()
            link = a.get_attribute("href") or ""

            if not titulo or len(titulo) < 25:
                continue
            if "larepublica.pe" not in link:
                continue
            if "/politica/" not in link:
                continue
            if link in vistos:
                continue

            vistos.add(link)

            noticias.append({
                "medio": "La República",
                "seccion": "Política",
                "titular": titulo,
                "url": link
            })

        print(f"🔗 Noticias encontradas: {len(noticias)}")

        # 3️⃣ Entrar a cada noticia y sacar fecha
        resultados = []

        for i, n in enumerate(noticias, start=1):
            print(f"📄 ({i}/{len(noticias)}) {n['titular'][:60]}...")

            driver.get(n["url"])
            fecha = extraer_fecha(driver, wait)

            resultados.append({
                **n,
                "fecha": fecha
            })

            time.sleep(0.8)

        # 4️⃣ DataFrame
        df = pd.DataFrame(resultados)
        df.drop_duplicates(subset=["url"], inplace=True)

        # 5️⃣ Guardar CSV
        carpeta = os.path.expanduser("~/Desktop/MediaLab/selenium_clase")
        os.makedirs(carpeta, exist_ok=True)

        ruta = os.path.join(carpeta, "posts_python_blog.csv")
        df.to_csv(ruta, index=False, encoding="utf-8")

        print("\n✅ CSV guardado en:")
        print(ruta)

    finally:
        driver.quit()


if __name__ == "__main__":
    main()

