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
    # Ruta donde se encuentran los PDFs
    carpeta_entrada = "entrada"
    excel_path = os.path.join(carpeta_entrada, "acumulador.xlsx")  # Guardar dentro de la carpeta 'entrada'

    # Si el archivo Excel ya existe, lo cargamos; si no, creamos uno nuevo
    if os.path.exists(excel_path):
        df_total = pd.read_excel(excel_path)
    else:
        df_total = pd.DataFrame(columns=["contenido"])

    # Recorremos los archivos PDF en la carpeta de entrada
    archivos_pdf = [f for f in os.listdir(carpeta_entrada) if f.endswith('.pdf')]

    for archivo_pdf in archivos_pdf:
        pdf_path = os.path.join(carpeta_entrada, archivo_pdf)
        print(f"Procesando {archivo_pdf}...")

        # Extraemos el texto del PDF
        lines = procesar_pdf(pdf_path)

        # Añadimos las líneas al DataFrame
        for line in lines:
            df_total = pd.concat([df_total, pd.DataFrame([{"contenido": line}])], ignore_index=True)

    # Guardamos el archivo Excel con los datos acumulados
    guardar_en_excel(df_total, excel_path)
    print(f"¡Todos los PDFs han sido procesados y guardados en {excel_path}!")

if __name__ == "__main__":
    main()
