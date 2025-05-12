import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Configurar conexión a MySQL
host = "localhost"
user = "root"
password = "Candelaria24"
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

    WHERE Fecha BETWEEN '2020-12-01' AND '2020-12-31';

"""
df = pd.read_sql(query, engine)
print(df.head())
print("Total de registros:", len(df))

# Procesamiento
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["dia"] = df["Fecha"].dt.strftime("%Y-%m-%d")  # Convertimos a string para evitar problemas con eje y

df_grouped = df.groupby("dia")["GRAN_TOTAL"].sum().reset_index()

# 🔹 Crear gráfico de barras horizontales

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_grouped["GRAN_TOTAL"],
    y=df_grouped["dia"],
    orientation='h',
    marker=dict(
        color='rgba(249, 94, 22 , 0.6)',
        line=dict(color='rgba(255, 103, 32, 1.0)', width=1.5)
    ),
    hoverinfo='x+y',
    hoverlabel=dict(bgcolor="rgba(255, 103, 32, 1.0)", font_size=16)
)

)

fig.update_layout(
    title=dict(
        text="<b>Ventas por Día en Diciembre 2020</b>",
        x=0.5,
        xanchor='center',
        font=dict(
            family="Arial",
            size=20,
            color="black"
        )
    ),
    xaxis_title="Ventas Totales",
    yaxis_title="Día",
    autosize=False,
    width=900,
    height=600,
    margin=dict(l=100, r=50, t=80, b=50),
    yaxis=dict(
        categoryorder='category ascending',
        tickfont=dict(size=10)
    ),
    xaxis=dict(
        tickfont=dict(size=10)
    ),
    plot_bgcolor='white',   # 🔴 elimina fondo gris del área del gráfico
    paper_bgcolor='white'   # 🔴 elimina fondo gris fuera del gráfico
)

# Guardar como HTML
fig.write_html("dash/static/graficas/grafica_Diciembre2020.html")

print("Gráfico horizontal guardado como 'dash/static/graficas/grafica_Octubre2024.html'")
