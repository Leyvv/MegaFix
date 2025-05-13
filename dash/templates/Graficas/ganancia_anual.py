import pandas as pd
import json
from sqlalchemy import create_engine, text

# Configurar conexión a MySQL
host = "localhost"
user = "root"
password = "itsoeh23"
database = "truper_ventas"

# Crear conexión
try:
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    conn = engine.connect()
    conn.execute(text("SELECT 1"))
    print("✅ Conexión a MySQL exitosa.")
except Exception as e:
    print("❌ Error al conectar a la base de datos:", e)
    exit()

# Consulta SQL: ganancia anual por año
query = """
SELECT 
    YEAR(Fecha) AS Año, 
    SUM(GRAN_TOTAL) AS TotalGananciaAnual
FROM Ventas
WHERE Fecha BETWEEN '2020-01-01' AND '2024-12-31'
GROUP BY YEAR(Fecha)
ORDER BY Año;
"""

df = pd.read_sql(query, engine)

with open("dash/static/graficas/ganancia_anual.json", "w", encoding="utf-8") as f:
    json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=4)

print("✅ Datos guardados en 'dash/static/graficas/ganancia_anual.json'")
