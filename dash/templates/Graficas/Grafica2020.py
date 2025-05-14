

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

query = "SELECT Fecha,GRAN_TOTAL FROM Ventas WHERE YEAR(Fecha) = 2020;"
df = pd.read_sql(query, engine)


# 🔹 Convertir la fecha a tipo datetime
df["Fecha"] = pd.to_datetime(df["Fecha"])

# 🔹 Extraer el mes en formato 'YYYY-MM'
df["mes"] = df["Fecha"].dt.to_period("M")

# 🔹 Convertir la columna 'mes' de Period a string
df["mes"] = df["mes"].astype(str)

# 🔹 Agrupar por mes y categoría
df_grouped = df.groupby("mes")["GRAN_TOTAL"].sum().reset_index()

# 🔹 Crear gráfico de barras apiladas por mes
#fig = px.bar(df_grouped, x="Mes", y="Total", 
 #            title="Ventas por Mes en 2020", barmode="stack")

import plotly.graph_objects as go

fig = go.Figure()

fig.add_trace(go.Bar(
    x=df_grouped["mes"],
    y=df_grouped["GRAN_TOTAL"],
  
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
        text="<b>Ventas por Mes en 2020 </b>",
        x=0.5,
        xanchor='center',
        font=dict(
            family="Arial",
            size=20,
            color="black"
        )
    ),
    xaxis_title="Mes",
    yaxis_title="Total",
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





# 🔹 Guardar gráfico como HTML
fig.write_html("dash/static/graficas/grafica_2020.html")


print("Gráfico guardado como '../Graficas/grafica_2020.html'")
