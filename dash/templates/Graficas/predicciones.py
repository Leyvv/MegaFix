import pandas as pd
import altair as alt
from prophet import Prophet
from sqlalchemy import create_engine

# Conectar y cargar datos desde septiembre 2024
engine = create_engine('mysql+mysqlconnector://root:Candelaria24@localhost/truper_ventas')
query = "SELECT Fecha, GRAN_TOTAL FROM ventas WHERE Fecha >= '2024-09-01'"
df = pd.read_sql(query, engine)
df.rename(columns={'Fecha': 'ds', 'GRAN_TOTAL': 'y'}, inplace=True)

# Modelo Prophet
modelo = Prophet()
modelo.fit(df)

# Generar fechas para todo 2025
futuro = pd.date_range('2025-01-01', '2025-12-31', freq='D')
df_futuro = pd.DataFrame(futuro, columns=['ds'])
predicciones = modelo.predict(df_futuro)

# Preparar DataFrame para graficar
df_real = df.copy()
df_real['Tipo'] = 'Real'
df_real = df_real[['ds', 'y', 'Tipo']]

df_pred = predicciones[['ds', 'yhat']].copy()
df_pred.rename(columns={'yhat': 'y'}, inplace=True)
df_pred['Tipo'] = 'Predicción'

df_comb = pd.concat([df_real, df_pred], ignore_index=True)
df_comb.rename(columns={'ds': 'Fecha', 'y': 'Ventas'}, inplace=True)
df_comb['Fecha'] = pd.to_datetime(df_comb['Fecha'])

# Crear gráfica Altair con estilo
chart = alt.Chart(df_comb).mark_line().encode(
    x=alt.X('Fecha:T', title='Fecha'),
    y=alt.Y('Ventas:Q', title='Ventas'),
    color=alt.Color('Tipo:N', legend=alt.Legend(title="Tipo"))
).properties(
    title='Predicción de Ventas 2025',
    width=800,
    height=500
).configure_title(
    fontSize=16,
    font='Arial',
    anchor='start',
    color='black'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
)


# Guardar como HTML para incluir en otros templates
with open("dash/static/graficas/predicciones.html", "w", encoding="utf-8") as f:
    f.write(chart.to_html(embed_options={'actions': False}, fullhtml=True))

print("✅ Gráfica guardada como 'grafica_prediccion.html'")


