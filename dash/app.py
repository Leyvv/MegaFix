from flask import Flask, jsonify, render_template
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datos')
def obtener_datos():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="itsoeh23",
        database="truper_ventas"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, gran_total FROM ventas WHERE fecha BETWEEN '2020-01-02' AND '2020-01-31'")
    resultados = cursor.fetchall()
    conn.close()

    datos = {
        "fechas": [fila[0].strftime('%Y-%m-%d') for fila in resultados],
        "totales": [float(fila[1]) for fila in resultados]
    }
    return jsonify(datos)

if __name__ == '__main__':
    app.run(debug=True)
