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

# Procesamiento de datos
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Guardar los resultados en un archivo de texto
output_file = "dias_mas_vendidos.txt"
with open(output_file, "w") as file:
    file.write("Fecha\tTotalDia\n")
    for index, row in df.iterrows():
        file.write(f"{row['Fecha'].strftime('%Y-%m-%d')}\t${row['TotalDia']:,.2f}\n")
        
print(f"✅ Datos guardados en el archivo {output_file}")
