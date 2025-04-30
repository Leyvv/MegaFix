import mysql.connector
import pandas as pd
from sqlalchemy import create_engine

# Configurar conexión a MySQL
host = "localhost"
user = "root"
password = "Candelaria24"
database = "truper_ventas"

# Crear conexión con SQLAlchemy
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# Consulta
query = """
SELECT fecha, gran_total 
FROM ventas
WHERE fecha BETWEEN '2020-01-02' AND '2020-01-31'
"""
df = pd.read_sql(query, engine)

# Día con mayor total
max_row = df.loc[df['gran_total'].idxmax()]
dia_maximo = max_row['fecha'].strftime('%Y-%m-%d')
gran_total_maximo = max_row['gran_total']

# Crear HTML con los datos incrustados
html = f"""
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Resumen</title>
    <style>
      .box {{
        padding: 2px;
        border: 1px solid #aaa;
        margin-bottom: 5px;
        width: fit-content;
      }}
    </style>
</head>
<body>
    <div class="box">Día con más total: <span id="dia-mayor">{dia_maximo}</span></div>
    <div class="box">Valor: <span id="valor-mayor">{gran_total_maximo}</span></div>
</body>
</html>
"""

# Guardar HTML
with open("dash/static/graficas/resumen_datos.html", "w", encoding="utf-8") as f:
    f.write(html)