import pdfplumber
import pandas as pd
import os

def procesar_pdf(pdf_path):
    """Extrae el texto del PDF y lo retorna como una lista de líneas."""
    with pdfplumber.open(pdf_path) as pdf:
        texto = ""
        for page in pdf.pages:
            texto += page.extract_text() or ""
    return texto.split("\n")

def guardar_en_excel(df_total, excel_path):
    """Guarda los datos en el archivo Excel usando el motor openpyxl."""
    df_total.to_excel(excel_path, index=False, engine='openpyxl')

def main():
    carpeta_entrada = "entrada"
    excel_path = os.path.join(carpeta_entrada, "acumulador.xlsx")
    registro_path = os.path.join(carpeta_entrada, "procesados.txt")


    if os.path.exists(registro_path):
        with open(registro_path, "r") as f:
            archivos_ya_procesados = set(f.read().splitlines())
    else:
        archivos_ya_procesados = set()

    # Si el Excel ya existe, lo cargamos
    if os.path.exists(excel_path):
        df_total = pd.read_excel(excel_path)
    else:
        df_total = pd.DataFrame(columns=["contenido"])


    archivos_pdf = [f for f in os.listdir(carpeta_entrada) if f.endswith('.pdf')]

    for archivo_pdf in archivos_pdf:
        if archivo_pdf in archivos_ya_procesados:
            print(f"Saltando {archivo_pdf}, ya fue procesado.")
            continue

        pdf_path = os.path.join(carpeta_entrada, archivo_pdf)
        print(f"Procesando {archivo_pdf}...")

        lines = procesar_pdf(pdf_path)

        for line in lines:
            df_total = pd.concat([df_total, pd.DataFrame([{"contenido": line}])], ignore_index=True)


        with open(registro_path, "a") as f:
            f.write(archivo_pdf + "\n")

    guardar_en_excel(df_total, excel_path)
    print(f"¡Todos los PDFs han sido procesados y guardados en {excel_path}!")

if __name__ == "__main__":
    main()

