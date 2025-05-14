import pandas as pd
import altair as alt
from prophet import Prophet
from sqlalchemy import create_engine


engine = create_engine('mysql+mysqlconnector://root:Candelaria24@localhost/truper_ventas')
query = "SELECT Fecha, GRAN_TOTAL FROM ventas WHERE Fecha >= '2024-09-01'"
df = pd.read_sql(query, engine)

# 2. Preparar datos para Prophet
df.rename(columns={'Fecha': 'ds', 'GRAN_TOTAL': 'y'}, inplace=True)
df['ds'] = pd.to_datetime(df['ds'])

# 3. Crear y entrenar el modelo Prophet
modelo = Prophet()
modelo.fit(df)

# 4. Generar fechas futuras para todo 2025
futuro = pd.date_range('2025-01-01', '2025-12-31', freq='D')
df_futuro = pd.DataFrame(futuro, columns=['ds'])
predicciones = modelo.predict(df_futuro)

# 5. Crear gráfica 
df_real = df.copy()
df_real['Tipo'] = 'Real'
df_real = df_real[['ds', 'y', 'Tipo']]

df_pred = predicciones[['ds', 'yhat']].copy()
df_pred.rename(columns={'yhat': 'y'}, inplace=True)
df_pred['Tipo'] = 'Predicción'

df_comb = pd.concat([df_real, df_pred], ignore_index=True)
df_comb.rename(columns={'ds': 'Fecha', 'y': 'Ventas'}, inplace=True)
df_comb['Fecha'] = pd.to_datetime(df_comb['Fecha'])

chart = alt.Chart(df_comb).mark_line().encode(
    x=alt.X('Fecha:T', title='Fecha'),
    y=alt.Y('Ventas:Q', title='Ventas'),
    color=alt.Color('Tipo:N', legend=alt.Legend(title="Tipo")),
    tooltip=[
        alt.Tooltip('Fecha:T', title='Fecha'),
        alt.Tooltip('Ventas:Q', title='Ventas'),
        alt.Tooltip('Tipo:N', title='Tipo')
    ]
).properties(
    title='Predicción de Ventas 2025',
    width='container',
    height=500
)
with open("dash/static/graficas/predicciones.html", "w", encoding="utf-8") as f:
    f.write(chart.to_html(
        embed_options={
            'actions': False,
            'responsive': True
        },
        fullhtml=True
    ))
chart.save("dash/static/graficas/predicciones.html")
print("✅ Gráfica guardada como 'predicciones.html'\n")

# 6. Cálculo total 2025
total_2025 = predicciones[(predicciones['ds'] >= '2025-01-01') & 
                          (predicciones['ds'] <= '2025-12-31')]['yhat'].sum()

# 7. Cálculo total 2024 (parcial desde septiembre)
total_2024 = df[(df['ds'] >= '2024-01-01') & 
                (df['ds'] <= '2024-12-31')]['y'].sum()

# 8. 
print("📊 RESUMEN DE PREDICCIÓN\n-----------------------------")
if total_2024 > 0:
    incremento_pct = ((total_2025 - total_2024) / total_2024) * 100
    print(f"🟩 Total real de 2024 (desde septiembre): ${total_2024:,.2f}")
    print(f"🔮 Total estimado para 2025:                ${total_2025:,.2f}")
    print(f"📈 Incremento estimado en 2025:             {incremento_pct:.2f}%")
else:
    print("⚠️ No hay suficientes datos de 2024 para calcular incremento.")

# 9. Agrupar predicción por mes de 2025
predicciones_2025 = predicciones[(predicciones['ds'] >= '2025-01-01') & 
                                 (predicciones['ds'] <= '2025-12-31')].copy()

predicciones_2025['Mes'] = predicciones_2025['ds'].dt.to_period('M')
ventas_mensuales = predicciones_2025.groupby('Mes')['yhat'].sum().reset_index()
ventas_mensuales['Mes'] = ventas_mensuales['Mes'].astype(str)

# 10. Calcular % de crecimiento mes a mes
ventas_mensuales['Crecimiento_%'] = ventas_mensuales['yhat'].pct_change() * 100

# 11. 
print("\n📆 CRECIMIENTO MENSUAL ESTIMADO EN 2025")
print("------------------------------------------")
for i, row in ventas_mensuales.iterrows():
    mes = row['Mes']
    total_mes = row['yhat']
    crecimiento = row['Crecimiento_%']
    if pd.isna(crecimiento):
        print(f"📍 {mes}: ${total_mes:,.2f} (mes inicial)")
    else:
        signo = "📈" if crecimiento >= 0 else "📉"
        print(f"{signo} {mes}: ${total_mes:,.2f} ({crecimiento:.2f}%)")
