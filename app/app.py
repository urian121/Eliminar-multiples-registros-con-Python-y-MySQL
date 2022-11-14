#Importando  flask y algunos paquetes
from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
from confiDB import *  #Importando conexion BD


#Declarando nombre de la aplicación e inicializando, crear la aplicación Flask
app = Flask(__name__)
application = app

app.secret_key = '32423gfdgdfgdf'
#key = uuid.uuid4().__str__()



#Creando mi Decorador para el Home
@app.route('/', methods=['GET','POST'])
def inicio():
    conexion_MySQLdb = connectionBD() #creando mi instancia a la conexion de BD
    cur      = conexion_MySQLdb.cursor(dictionary=True)
    #Importante uso f para
    querySQL = "SELECT * FROM countries LIMIT 50"
    cur.execute(querySQL) 
    resultadoBusqueda = cur.fetchall() #fetchall () Obtener todos los registros
    totalBusqueda = len(resultadoBusqueda) #Total de busqueda
    
    cur.close() #Cerrando conexion SQL
    conexion_MySQLdb.close() #cerrando conexion de la BD
    return render_template('public/index.html', miData = resultadoBusqueda, total = totalBusqueda)
    


@app.route('/eliminar-pais', methods=['POST'])
def eliminarSeleccionPais():
    if request.method == 'POST':  	
        idSeleccionados = request.json['idCheckbox']
        print(idSeleccionados) #Ejemplo: 41,42
        '''
        #Ejemplo de
        desarrollador = "urian viera desarrollador"
        urian         = desarrollador.split() #split terminar convirtiendo un string en una lista
        print(urian) #['urian', 'viera', 'desarrollador'] 
        '''
        #Comprobar si existe una (,) en la lista es que hay mas de un elemento en la lista
        if ',' in idSeleccionados:		
            idSeleccionados = idSeleccionados.split(',')
            #print(idSeleccionados) # ['45', '46']
            for idPais in idSeleccionados:
                #print(idPais) # 45 para la primera iteracion 46 para la siguiente iteracion y asi sucesivamente
                
                conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
                cur              = conexion_MySQLdb.cursor(dictionary=True)
                cur.execute('DELETE FROM countries WHERE ID=%s', (idPais,))
                conexion_MySQLdb.commit()
                respuesta = cur.rowcount
                #print("Registros Borrados = ", respuesta)
                
                cur.close() #Cerrando conexion SQL
                conexion_MySQLdb.close() #cerrando conexion de la BD
                return jsonify({'resp': respuesta, 'ids':idSeleccionados,  'totalIds': 'x' }) 
        else:
            conexion_MySQLdb = connectionBD() #Hago instancia a mi conexion desde la funcion
            cur              = conexion_MySQLdb.cursor(dictionary=True)
            cur.execute('DELETE FROM countries WHERE ID=%s', (idSeleccionados,))
            conexion_MySQLdb.commit()
            respuesta = cur.rowcount
            #print("Registros Borrados = ", respuesta)
            
            cur.close() #Cerrando conexion SQL
            conexion_MySQLdb.close() #cerrando conexion de la BD
            
            return jsonify({'resp': respuesta, 'ids':idSeleccionados, 'totalIds': 1})  



#Redireccionando cuando la página no existe
@app.errorhandler(404)
def not_found(error):
        return redirect(url_for('inicio'))
    
    

if __name__ == "__main__":
    app.run(debug=True, port=8001)

