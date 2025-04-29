#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      lasso
#
# Created:     29/04/2025
# Copyright:   (c) lasso 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import pdfplumber
import pandas as pd
import os

# Ruta del archivo PDF
pdf_path = "ruta/del/archivo.pdf"

# Crear (o cargar si existe) el Excel acumulador
excel_path = "acumulador.xlsx"
if os.path.exists(excel_path):
    df_total = pd.read_excel(excel_path)
else:
    df_total = pd.DataFrame()

# Extraer texto de PDF (esto depende de cómo está estructurado tu PDF)
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if text:
            lines = text.split("\n")
            for line in lines:
                df_total = df_total._append({"contenido": line}, ignore_index=True)

# Guardar el archivo Excel con los datos acumulados
df_total.to_excel(excel_path, index=False)
print("¡PDF procesado y guardado en Excel!")

