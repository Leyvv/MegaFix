import pandas as pd
import json
from sqlalchemy import create_engine, text

# Configurar conexión a MySQL
host = "localhost"
user = "root"
password = "itsoeh23"
database = "truper_ventas"

# Crear conexión con SQLAlchemy
try:
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    conn = engine.connect()
    conn.execute(text("SELECT 1"))
    print("✅ Conexión a MySQL exitosa.")
except Exception as e:
    print("❌ Error al conectar a la base de datos:", e)
    exit()

# Consulta SQL: día más vendido por mes entre 2020 y 2024
query = """
SELECT V.Fecha, V.TotalDia
FROM (
    SELECT 
        Fecha,
        SUM(GRAN_TOTAL) AS TotalDia,
        ROW_NUMBER() OVER (
            PARTITION BY YEAR(Fecha), MONTH(Fecha)
            ORDER BY SUM(GRAN_TOTAL) DESC
        ) AS rn
    FROM Ventas
    WHERE Fecha BETWEEN '2020-01-01' AND '2024-12-31'
    GROUP BY Fecha
) AS V
WHERE V.rn <= 5
ORDER BY YEAR(V.Fecha), MONTH(V.Fecha), V.rn;
"""

# Ejecutar consulta y guardar resultado en DataFrame
df = pd.read_sql(query, engine)
print(df)

# Convertir la columna Fecha a string (formato YYYY-MM-DD)
df["Fecha"] = df["Fecha"].astype(str)

# Convertir a lista de diccionarios
resultados = df.to_dict(orient="records")

# Guardar como archivo JSON en la ruta especificada
output_path = "dash/static/graficas/mayores_dias_venta.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(resultados, f, ensure_ascii=False, indent=4)

print(f"✅ Datos guardados en '{output_path}'")
