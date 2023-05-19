from flask import Flask, request, render_template
from metodos import Metodos

app = Flask(__name__)
metodos = Metodos()

@app.route("/",methods=['GET'])
def hello_world():
  # ecuacion = "0.089*x**4-2.55*x**3+22.48*x**2-59.68*x+19"
  # metodos.validarEcuacion(ecuacion)
  # metodos.establecerFuncion(ecuacion)
  # grafica = metodos.graficar(-1,12,0.5)
  return render_template('index.html')

@app.route("/aproximaciones",methods=['GET','POST'])
def aproximaciones():
  if request.method == 'GET':
    return render_template('aproximaciones.html',data = {})
  elif request.method == 'POST':
    data = {}
    try:
      if (len(request.form['ecuacion']) == 0 or
          len(request.form['x0']) == 0 or
          len(request.form['delta']) == 0 or
          len(request.form['epsilon']) == 0 or
          len(request.form['limiteInferior']) == 0 or
          len(request.form['limiteSuperior']) == 0):
        data['error'] = 'Debe enviar todos los campos!'
        return render_template('aproximaciones.html',data = data)

      ecuacion = request.form['ecuacion']
      x0 = float(request.form['x0'])
      deltaX = float(request.form['delta'])
      epsilon = float(request.form['epsilon'])
      limiteInf = float(request.form['limiteInferior'])
      limiteSup = float(request.form['limiteSuperior'])

      metodos.validarEcuacion(ecuacion)
      metodos.establecerFuncion(ecuacion)
      resultado = metodos.aproximacionesSucesivas(x0,epsilon,deltaX)
      print(resultado)
      if resultado == False:
        data['error'] = 'No se encontró la raiz, verifique que envió datos correctos!'
        return render_template('aproximaciones.html',data = data)
      
      if resultado[1] > limiteSup:
        limiteSup = resultado[1] + 1
      elif resultado[1] < limiteInf:
        limiteInf = resultado[1] - 1

      imagen = metodos.graficar(limiteInf,limiteSup,resultado[1])
      data['df'] = resultado[0]
      data['imagen'] = imagen
      return render_template('aproximaciones.html',data = data)
    except Exception as e:
      return render_template('aproximaciones.html',data = {'error':e})
  

@app.route("/newthon",methods=['POST','GET'])
def newthon():
  if request.method == 'GET':
    return render_template('newthon.html',data = {})
  elif request.method == 'POST':
    data = {}
    try:
      if (len(request.form['ecuacion']) == 0 or
          len(request.form['xi']) == 0 or
          len(request.form['epsilon']) == 0 or
          len(request.form['limiteInferior']) == 0 or
          len(request.form['limiteSuperior']) == 0):
        data['error'] = 'Debe enviar todos los campos!'
        return render_template('newthon.html',data = data)

      ecuacion = request.form['ecuacion']
      x0 = float(request.form['xi'])
      epsilon = float(request.form['epsilon'])
      limiteInf = float(request.form['limiteInferior'])
      limiteSup = float(request.form['limiteSuperior'])

      metodos.validarEcuacion(ecuacion)
      metodos.establecerFuncion(ecuacion)
      metodos.establecerDerivada()
      resultado = metodos.newthonRhapson(x0,epsilon)
      
      if resultado == False:
        data['error'] = 'No se encontró la raiz, verifique que envió datos correctos!'
        return render_template('newthon.html',data = data)
      
      
      if resultado[1] > limiteSup:
        limiteSup = resultado[1] + 1
      elif resultado[1] < limiteInf:
        limiteInf = resultado[1] - 1

      imagen = metodos.graficar(limiteInf,limiteSup,resultado[1])
      data['df'] = resultado[0]
      data['imagen'] = imagen
      return render_template('newthon.html',data = data)
    except Exception as e:
      return render_template('newthon.html',data = {'error':e})

@app.route("/biseccion",methods=['POST','GET'])
def biseccion():
  if request.method == 'GET':
    return render_template('biseccion.html',data = {})
  elif request.method == 'POST':
    data = {}
    try:
      if (len(request.form['ecuacion']) == 0 or
          len(request.form['x0']) == 0 or
          len(request.form['x1']) == 0 or
          len(request.form['epsilon']) == 0 or
          len(request.form['limiteInferior']) == 0 or
          len(request.form['limiteSuperior']) == 0):
        data['error'] = 'Debe enviar todos los campos!'
        return render_template('biseccion.html',data = data)

      ecuacion = request.form['ecuacion']
      x0 = float(request.form['x0'])
      x1 = float(request.form['x1'])
      epsilon = float(request.form['epsilon'])
      limiteInf = float(request.form['limiteInferior'])
      limiteSup = float(request.form['limiteSuperior'])

      metodos.validarEcuacion(ecuacion)
      metodos.establecerFuncion(ecuacion)
      resultado = metodos.biseccion(x0,x1,epsilon)
      
      if resultado == False:
        data['error'] = 'No se encontró la raiz, verifique que envió datos correctos!'
        return render_template('biseccion.html',data = data)
      
      
      if resultado[1] > limiteSup:
        limiteSup = resultado[1] + 1
      elif resultado[1] < limiteInf:
        limiteInf = resultado[1] - 1

      imagen = metodos.graficar(limiteInf,limiteSup,resultado[1])
      data['df'] = resultado[0]
      data['imagen'] = imagen
      return render_template('biseccion.html',data = data)
    except Exception as e:
      return render_template('biseccion.html',data = {'error':e})

@app.route("/graficar",methods=['POST','GET'])
def graficar():
  if request.method == 'GET':
    return render_template('graficar.html',data = {})
  elif request.method == 'POST':
    data = {}
    try:
      if (len(request.form['ecuacion']) == 0 or
          len(request.form['limiteInferior']) == 0 or
          len(request.form['limiteSuperior']) == 0):
        data['error'] = 'Debe enviar todos los campos!'
        return render_template('graficar.html',data = data)

      ecuacion = request.form['ecuacion']
      limiteInf = float(request.form['limiteInferior'])
      limiteSup = float(request.form['limiteSuperior'])
      
      metodos.validarEcuacion(ecuacion)
      metodos.establecerFuncion(ecuacion)
      imagen = metodos.graficar(limiteInf,limiteSup)
      
      data['ecuacion'] = ecuacion
      data['imagen'] = imagen
      return render_template('graficar.html',data = data)
    except Exception as e:
      return render_template('graficar.html',data = {'error':e})


if __name__ == "__main__":
  app.run(host='0.0.0.0',port=8080)