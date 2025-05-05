

import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine




# Configurar conexión a MySQL
host = "localhost"
user = "root"
password = "itsoeh23"
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
fig = px.bar(df_grouped, x="mes", y="GRAN_TOTAL", 
             title="Ventas por Mes en 2020", barmode="stack")

# 🔹 Guardar gráfico como HTML
fig.write_html("dash/static/graficas/grafica_2020.html")


print("Gráfico guardado como '../Graficas/grafica_2020.html'")
