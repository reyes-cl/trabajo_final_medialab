import re
import pandas as pd

# =========================
# STOPWORDS
# =========================
STOPWORDS_ES = {"de","la","el","y","en","a","un","una","para","por","con","del","los","las"}
STOPWORDS_EN = {"the","and","to","of","in","for","on","with","a","an"}

# =========================
# TOKENIZACIÓN
# =========================
def tokenizar(texto: str):
    texto = texto.lower()
    texto = re.sub(r"[^a-záéíóúüñ0-9\s-]", " ", texto)
    tokens = [t for t in texto.split() if len(t) >= 3]
    tokens = [t for t in tokens if t not in STOPWORDS_ES and t not in STOPWORDS_EN]
    return tokens

# =========================
# MAIN
# =========================
def main():
    # =========================
    # RUTAS COMPLETAS
    # =========================
    ruta_andina = r"C:\Users\USER\Documents\00MEDIALAB00\andina.csv"
    ruta_lr = r"C:\Users\USER\Documents\00MEDIALAB00\larepublica.csv"

    # =========================
    # LEER CSVs
    # =========================
    df_andina = pd.read_csv(ruta_andina)
    df_lr = pd.read_csv(ruta_lr)

    # =========================
    # MEDIO / FECHA
    # =========================
    # Asegurarse que la columna 'fecha' existe
    if 'fecha' not in df_andina.columns:
        df_andina['fecha'] = pd.NaT

    # =========================
    # LONGITUD DEL TITULAR
    # =========================
    df_andina['len_titular'] = df_andina['titular'].fillna("").astype(str).str.len()
    df_lr['len_titular'] = df_lr['titular'].fillna("").astype(str).str.len()

    # =========================
    # TOP PALABRAS POR MEDIO
    # =========================
    def top_palabras(df, columna='titular', n=20):
        all_tokens = []
        for t in df[columna].fillna("").astype(str):
            all_tokens.extend(tokenizar(t))
        freq = (
            pd.Series(all_tokens)
            .value_counts()
            .head(n)
            .reset_index()
            .rename(columns={"index": "palabra", 0: "conteo"})
        )
        return freq

    top_andina = top_palabras(df_andina)
    top_lr = top_palabras(df_lr)

    # =========================
    # GUARDAR CSVs
    # =========================
    df_andina.to_csv(r"C:\Users\USER\Documents\00MEDIALAB00\andina_procesado.csv",
                     index=False, encoding="utf-8")
    df_lr.to_csv(r"C:\Users\USER\Documents\00MEDIALAB00\larepublica_procesado.csv",
                 index=False, encoding="utf-8")

    top_andina.to_csv(r"C:\Users\USER\Documents\00MEDIALAB00\top_palabras_andina.csv",
                      index=False, encoding="utf-8")
    top_lr.to_csv(r"C:\Users\USER\Documents\00MEDIALAB00\top_palabras_larepublica.csv",
                  index=False, encoding="utf-8")

    # =========================
    # CSV COMBINADO
    # =========================
    df_combinado = pd.concat([df_andina, df_lr], ignore_index=True)
    df_combinado.to_csv(r"C:\Users\USER\Documents\00MEDIALAB00\combinado_procesado.csv",
                        index=False, encoding="utf-8")

    print("✅ Procesamiento completado.")
    print("Archivos generados:")
    print("- andina_procesado.csv")
    print("- larepublica_procesado.csv")
    print("- top_palabras_andina.csv")
    print("- top_palabras_larepublica.csv")
    print("- combinado_procesado.csv")

if __name__ == "__main__":
    main()
