import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# Configurar conexión a MySQL
host = "localhost"
user = "root"
password = "Candelaria24"
database = "truper_ventas"

# Crear conexión con SQLAlchemy
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# Consulta SQL para obtener ventas de enero 2020
query = """
    SELECT Fecha, GRAN_TOTAL 
    FROM Ventas 
    WHERE Fecha BETWEEN '2020-02-01' AND '2020-02-29';
"""
df = pd.read_sql(query, engine)

# 🔹 Convertir la fecha a tipo datetime
df["Fecha"] = pd.to_datetime(df["Fecha"])

# 🔹 Extraer solo la fecha (sin hora)
df["dia"] = df["Fecha"].dt.date

# 🔹 Agrupar por día y calcular el total de ventas por día
df_grouped = df.groupby("dia")["GRAN_TOTAL"].sum().reset_index()

# 🔹 Crear gráfico de barras por día
fig = px.line_3d(df_grouped, x="dia", y="GRAN_TOTAL", 
             title="Ventas por Día en Febrero 2020", 
             labels={"dia": "Día", "GRAN_TOTAL": "Ventas Totales"})

# 🔹 Establecer tamaño del gráfico
fig.update_layout(
    autosize=False,
    width=800,  # Puedes ajustar el ancho aquí
    height=400,  # Establece la altura en 400px
)

# 🔹 Guardar gráfico como HTML
fig.write_html("dash/static/graficas/grafica_Enero2020.html")

print("Gráfico guardado como 'dash/static/graficas/grafica_Febrero2020.html'")
