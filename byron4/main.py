from flask import Flask, jsonify
from psycopg import connect
import psycopg
from psycopg.rows import  dict_row
import psycopg.rows

#Instanciar flask
app = Flask(__name__)

#Definir las variables para la cadena de conexion
host = 'localhost'
port = 5432
dbname = 'postgres'
username = 'postgres'
password = None

#Construir la cadena de conexio a la base de datos
def get_connection():
    conn = connect(host=host, port=port,dbname=dbname, user=username, password=password)
    return conn

#Crear el metodo get
@app.get("/")
def get_compania():
    try:
        #Conexion a la base de datos
        with get_connection() as conn:
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                #Ejecutar la consulta
                cur.execute("SELECT * FROM compania")
                #Obtener los datos
                datos = cur.fetchall()
                #Retornar los datos en la respuesta
                return jsonify(datos)
    except Exception as e:
      return jsonify({"error":str(e)})


#Crear el get by id
@app.get("/compania/<int:id>")
def get_compania_id(id):
    try:
        #Conexion a la base de datos
        with get_connection() as conn:
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                #Ejecutar la consulta
                cur.execute("SELECT * FROM compania WHERE id = %s", (id,))
                #Obtener los datos
                datos = cur.fetchone()
                #Retornar los datos en la respuesta
                if datos is None:
                    return jsonify({"message": ("Usuario no encontrado",id)}), 404
                return jsonify(datos)
    except Exception as errores:
      return jsonify({"error":str(errores)})
  
#Habilitar debug
if __name__ == "__main__":
    app.run(debug=True)