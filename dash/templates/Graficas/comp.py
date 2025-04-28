import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine
import os

# Configuración de la conexión a MySQL
host = "localhost"
user = "root"
password = "Candelaria24"
database = "truper_ventas"
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

# Función para obtener datos de ventas mensuales para un año dado
def obtener_datos_ventas(year):
    query = f"""
        SELECT 
            MONTH(Fecha) AS mes, 
            SUM(GRAN_TOTAL) AS ventas 
        FROM Ventas 
        WHERE YEAR(Fecha) = {year}
        GROUP BY mes
        ORDER BY mes
    """
    df = pd.read_sql(query, engine)
    df['mes'] = df['mes'].astype(int)
    return df

# Generar la gráfica y guardarla como HTML
def generar_html_comparacion(year1=2022, year2=2023, ruta_salida="dash/static/graficas/comparacion.html"):
    df1 = obtener_datos_ventas(year1)
    df2 = obtener_datos_ventas(year2)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df1['mes'], y=df1['ventas'], mode='lines+markers', name=f"Año {year1}"))
    fig.add_trace(go.Scatter(x=df2['mes'], y=df2['ventas'], mode='lines+markers', name=f"Año {year2}"))

    fig.update_layout(
        title=f"Comparación de Ventas Mensuales: {year1} vs {year2}",
        xaxis=dict(title="Mes", tickmode="linear", dtick=1),
        yaxis=dict(title="Ventas"),
        template="plotly_white"
    )

    html = fig.to_html(full_html=True)

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Gráfica guardada en: {ruta_salida}")

# Ejecutar solo esta función (sin levantar servidor Flask)
if __name__ == "__main__":
    generar_html_comparacion()

