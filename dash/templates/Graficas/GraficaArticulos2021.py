import pandas as pd
import plotly.graph_objects as go
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

# Consulta SQL para obtener las 10 mejores ventas por artículo de 2021
query = """
    SELECT 
        Articulo,
        SUM(Unidades) AS TotalUnidades
    FROM (
        -- Enero usa Articulo
        SELECT Articulo, Unidades FROM articulos_enero2021
        UNION ALL
        -- Febrero usa Articulo
        SELECT Articulo, Unidades FROM articulos_febrero2021
        UNION ALL
        -- Marzo usa Articulo
        SELECT Articulo, Unidades FROM articulos_marzo2021
        UNION ALL
        -- Abril usa MyUnknownColumn (se renombra a Articulo)
        SELECT MyUnknownColumn AS Articulo, Unidades FROM articulos_abril2021
        UNION ALL
        -- Mayo usa Articulo
        SELECT Articulo, Unidades FROM articulos_mayo2021
        UNION ALL
        -- Junio usa Articulo
        SELECT Articulo, Unidades FROM articulos_junio2021
        UNION ALL
        -- Julio usa Articulo
        SELECT Articulo, Unidades FROM articulos_julio2021
        UNION ALL
        -- Agosto usa Articulo
        SELECT Articulo, Unidades FROM articulos_agosto2021
        UNION ALL
        -- Septiembre usa Articulos (se renombra a Articulo)
        SELECT Articulos AS Articulo, Unidades FROM articulos_septiembre2021
        UNION ALL
        -- Octubre usa Articulo
        SELECT Articulo, Unidades FROM articulos_octubre2021
        UNION ALL
        -- Diciembre usa Articulo
        SELECT Articulo, Unidades FROM articulos_diciembre2021
    ) AS Todo2021
    GROUP BY Articulo
    ORDER BY TotalUnidades DESC
    LIMIT 10;
"""
df = pd.read_sql(query, engine)
print(df.head())
print("Total de registros:", len(df))

# 🔹 Crear gráfico de barras horizontales con mejoras estéticas

# Colores personalizados
colors = ['#ff8000', '#ff963e', '#ffab66', '#ffc08c', '#ffd5b1', '#ffead8', '#ff8000', '#ff963e', '#ffab66', '#ffc08c']

fig = go.Figure()

# Añadir traza para las barras
fig.add_trace(go.Bar(
    x=df["TotalUnidades"],
    y=df["Articulo"],
    orientation='h',
    marker=dict(
        color=df["TotalUnidades"],  # Colorear barras según el valor de TotalUnidades
        colorscale=[[0, '#ff8000'], [0.2, '#ff963e'], [0.4, '#ffab66'], [0.6, '#ffc08c'], [0.8, '#ffd5b1'], [1, '#ffead8']],  # Nueva escala de colores personalizada
        colorbar=dict(title="Unidades Vendidas"),
        line=dict(color='rgba(0, 0, 0, 0.2)', width=1)  # Añadir borde sutil a las barras
    ),
    hoverinfo='x+y+text',
    hoverlabel=dict(
        bgcolor="rgba(255, 255, 255, 0.9)",  # Fondo blanco para el texto de hover
        font_size=14,
        font_color="black"
    ),
    text=df["TotalUnidades"].apply(lambda x: f"{x:,.0f} Unidades"),  # Mostrar el valor en el hover
    textposition='inside',  # Posición de texto dentro de las barras
    textfont=dict(size=12, color="white"),  # Texto dentro de las barras
))

# Actualizar el layout con mejoras en estética
fig.update_layout(
    title=dict(
        text="<b>Top 10 Artículos Más Vendidos en 2021</b>",
        x=0.5,
        xanchor='center',
        font=dict(
            family="Roboto, sans-serif",  # Fuente más moderna
            size=24,
            color="black"
        ),
    ),
    xaxis_title="Unidades Vendidas",
    yaxis_title="Artículo",
    autosize=False,
    width=1000,
    height=700,
    margin=dict(l=100, r=50, t=80, b=50),
    yaxis=dict(
        categoryorder='category ascending',
        tickfont=dict(size=12)
    ),
    xaxis=dict(
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',  # Fondo blanco del área del gráfico
    paper_bgcolor='white',  # Fondo blanco fuera del gráfico
    barmode='group',  # Modo de agrupamiento
    showlegend=False,  # Desactivar la leyenda
    hovermode='closest',  # Modo de hover más cercano
)

# Agregar animación suave (opcional)
fig.update_traces(marker=dict(line=dict(width=2, color='rgb(0,0,0)')),
                  selector=dict(type='bar'))

# Guardar el gráfico como un archivo HTML interactivo
fig.write_html("dash/static/graficas/grafica_top_10_articulos_2021.html")

print("Gráfico de top 10 artículos guardado como 'dash/static/graficas/grafica_top_10_articulos_2021.html'")
