import pandas as pd
import plotly.express as px
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

# Consulta SQL para obtener ventas de enero 2020
query = """
    SELECT Fecha, GRAN_TOTAL 
    FROM Ventas 
    WHERE Fecha BETWEEN '2022-12-01' AND '2022-12-31';
"""
df = pd.read_sql(query, engine)
print(df.head())
print("Total de registros:", len(df))

# Procesamiento
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["dia"] = df["Fecha"].dt.strftime("%Y-%m-%d")  # Convertimos a string para evitar problemas con eje y

df_grouped = df.groupby("dia")["GRAN_TOTAL"].sum().reset_index()

# 🔹 Crear gráfico de barras horizontales
fig = px.bar(
    df_grouped,
    x="GRAN_TOTAL",
    y="dia",
    title="Ventas por Día en Diciembre 2022",
    orientation="h",
    labels={"dia": "Día", "GRAN_TOTAL": "Ventas Totales"}
)

fig.update_layout(
    autosize=False,
    width=800,
    height=600,
    yaxis=dict(categoryorder='category ascending')  # Opcional: ordena los días
)

# Guardar como HTML
fig.write_html("dash/static/graficas/grafica_Diciembre2022.html")
print("Gráfico horizontal guardado como 'dash/static/graficas/grafica_Diciembre2022.html'")
