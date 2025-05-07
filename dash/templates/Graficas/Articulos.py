import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import mysql.connector

# Configurar conexión a MySQL
conexion = mysql.connector.connect(
host = "localhost",
user = "root",
password = "Candelaria24",
database = "truper_ventas"
)

# Crear conexión con SQLAlchemy
cursor = conexion.cursor()


query = """
SELECT Articulo, Unidades, Venta
FROM articulos_marzo2020
ORDER BY Unidades DESC
LIMIT 6;
"""

cursor.execute(query)
resultados = cursor.fetchall()

# Crear contenido HTML
html = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Top 6 Productos Más Vendidos</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4; }
        table { border-collapse: collapse; width: 80%; margin: auto; background-color: white; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
        th { background-color: #4CAF50; color: white; }
        h2 { text-align: center; }
    </style>
</head>
<body>
    <h2>Top 6 Productos Más Vendidos - Abril 2021</h2>
    <table>
        <tr>
            <th>Producto</th>
            <th>Unidades</th>
            <th>Total</th>
        </tr>
"""

# Agregar filas con los resultados
for producto, unidades, total in resultados:
    html += f"""
        <tr>
            <td>{producto}</td>
            <td>{unidades}</td>
            <td>{total}</td>
        </tr>
    """

html += """
    </table>
</body>
</html>
"""

# Guardar archivo HTML
ruta_html = "dash/static/graficas/Top6Productos.html"
with open(ruta_html, "w", encoding="utf-8") as archivo:
    archivo.write(html)

print(f"✅ Archivo HTML generado en: {ruta_html}")

# Cierre de conexión
cursor.close()
conexion.close()
