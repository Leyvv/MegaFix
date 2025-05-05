import pandas as pd
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
    conn.close()
except Exception as e:
    print("❌ Error al conectar a la base de datos:", e)

# Consulta SQL para obtener el día más vendido por mes y su total
query = """
SELECT V.Fecha, V.TotalDia
FROM (
    SELECT 
        Fecha,
        SUM(GRAN_TOTAL) AS TotalDia,
        ROW_NUMBER() OVER (PARTITION BY YEAR(Fecha), MONTH(Fecha) ORDER BY SUM(GRAN_TOTAL) DESC) AS rn
    FROM Ventas
    WHERE Fecha BETWEEN '2020-01-01' AND '2024-12-31'
    GROUP BY Fecha
) AS V
WHERE V.rn = 1;
"""

# Leer los resultados a un DataFrame
df = pd.read_sql(query, engine)
print("✅ Datos obtenidos correctamente.")
print("Total de días más vendidos:", len(df))

# Procesar datos para formato JSON
df["Fecha"] = pd.to_datetime(df["Fecha"]).dt.strftime("%Y-%m-%d")
df["TotalDia"] = df["TotalDia"].map(lambda x: round(x, 2))

# Guardar los resultados como JSON
output_file = "dias_mas_vendidos.json"
df.to_json(output_file, orient="records", indent=4, force_ascii=False)

print(f"✅ Datos guardados en el archivo {output_file}")

