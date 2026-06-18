# Importamos Flask y las librerias que necesitamos
from flask import Flask, render_template, request
import joblib
import pandas as pd

# Creamos la aplicacion de Flask
app = Flask(__name__)

# Cargamos el modelo que entrenamos y guardamos con joblib
modelo = joblib.load('modelo_estudiantes.pkl')

# Ruta principal: muestra el formulario
@app.route('/')
def inicio():
    return render_template('index.html')

# Ruta que recibe los datos del formulario y predice la nota
@app.route('/predecir', methods=['POST'])
def predecir():
    # Leemos cada dato que escribio el usuario en el formulario
    age = float(request.form['age'])
    Fedu = float(request.form['Fedu'])
    studytime = float(request.form['studytime'])
    activities = float(request.form['activities'])
    famrel = float(request.form['famrel'])
    health = float(request.form['health'])
    absences = float(request.form['absences'])
    G1 = float(request.form['G1'])
    G2 = float(request.form['G2'])
    reason_home = float(request.form['reason_home'])

    # Armamos una tabla con los datos en el mismo orden que espera el modelo
    columnas = ['age', 'Fedu', 'studytime', 'activities', 'famrel',
                'health', 'absences', 'G1', 'G2', 'reason_home']
    datos = pd.DataFrame([[age, Fedu, studytime, activities, famrel,
                           health, absences, G1, G2, reason_home]], columns=columnas)

    # Hacemos la prediccion y la redondeamos a 1 decimal
    prediccion = modelo.predict(datos)
    nota = round(prediccion[0], 1)

    # Mostramos el formulario otra vez pero ahora con el resultado
    return render_template('index.html', resultado=nota)

# Esto permite correr la app en local con: python app.py
if __name__ == '__main__':
    app.run(debug=True)
