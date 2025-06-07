from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import json

app = Flask(__name__)

#  Conexión a MySQL
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="quicioprime"
    )
@app.route('/')
def index():
    return redirect(url_for('registrar_cartera'))

@app.route('/registrarCartera')
def registrar_cartera():
    return render_template("registrarCartera.html")

@app.route('/GrabarCartera', methods=['POST'])
def insertar_cartera():
    try:
        descripcion = request.form['txtdescripcion']
        tipo = request.form['txttipocartera']
        precio = request.form['txtprecio']
        fecha = request.form['fecha']
            
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""INSERT INTO Cartera (descripcion, tipo, precio, fecha)VALUES (%s, %s, %s, %s)""", (descripcion, tipo, precio, fecha))
        
        conn.commit()
        mensaje = "Se grabó el registro satisfactoriamente"
    except mysql.connector.Error as err:
        mensaje = f"Error al grabar en la base de datos: {err}"
    except Exception as e:
        mensaje = f"Error inesperado: {str(e)}"
    finally:
        cursor.close()
        conn.close()
    
    return render_template("registrarCartera.html", mensaje=mensaje)

#  Función nueva para consultar 
@app.route('/ConsultarCartera', methods=['GET', 'POST'])
def consultar_cartera():
    tipo_filtro = request.args.get('tipo') or request.form.get('tipo')  # Recibe el filtro por GET o POST
    
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        
        if tipo_filtro:
            # Búsqueda exacta del tipo 
            cursor.execute("""
                SELECT * FROM Cartera 
                WHERE LOWER(tipo) = LOWER(%s)
                ORDER BY id DESC
            """, (tipo_filtro,))
        else:
            # Mostrar todos si no hay filtro
            cursor.execute("SELECT * FROM Cartera ORDER BY id DESC")
            
        carteras = cursor.fetchall()
        error = None
    except mysql.connector.Error as err:
        carteras = []
        error = f"Error al consultar: {err}"
    finally:
        cursor.close()
        conn.close()
    
    return render_template('ConsultarCartera.html', 
                        carteras=carteras,
                        error=error,
                        tipo_filtro=tipo_filtro)
if __name__ == '__main__':
    app.run(debug=True)