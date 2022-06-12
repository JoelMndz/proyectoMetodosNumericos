import io
import numpy as np
import pandas as pd
import sympy as sp
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64

x = sp.symbols('x')

class Metodos:
  def __init__(self) -> None:
    self.funcion = None

  def validarEcuacion(self,ecuacion:str):
    try:
      if 'x' not in ecuacion:
        raise Exception('La ecuacion debe tener la x')
      eval(ecuacion)
    except:
      raise Exception("La ecuacion ingresada no es soportada!")

  def establecerFuncion(self,cadena:str):
    try:
      self.funcion = cadena
      self.f = lambda x: eval(cadena)
    except:
      raise Exception("La funcion no es valida!")

  def establecerDerivada(self):
    self.derivada = sp.diff(eval(self.funcion))

  def diff(self,n):
    return self.derivada.evalf(subs={x:n})

  def cambioDeSigno(self,n1:float,n2:float):
    """
    Función que determina si hay un cambio de signo entre dos numeros
    """
    if (n1 > 0 and n2 > 0) or (n1 < 0 and n2 < 0):
      return False
    
    return True

  def graficar(self,limiteInferior:float,limiteSuperior:float,punto:float=None):
    x = np.linspace(limiteInferior,limiteSuperior,100)
    y = [self.f(i) for i in x]

    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(x, y, x, np.zeros(len(x)))
    axis.set_title('Gráfica')
    if punto != None:
      axis.plot(punto,0,'ro',label=f'raiz = {round(punto,4)}')
      fig.legend()

    img = io.BytesIO()
    FigureCanvas(fig).print_png(img)
    plot_url = base64.b64encode(img.getvalue()).decode()
    
    return plot_url
    


  def aproximacionesSucesivas(self,xi=0,esp=0.0001,deltaX=0.1,iteracionMaxima=1000):
    """
    Funcion que encuentra la raiz por el método de aproximaciones sucesivas
    """
    contador = 0
    resultados = []

    #El bucle como maximo iteracionMaxima
    while contador < iteracionMaxima:
      resultados.append([round(xi,5), round(xi+deltaX,5), round(self.f(xi),2), round(self.f(xi+deltaX),2), deltaX, abs(xi-(xi+deltaX))])
      if abs(xi-(xi+deltaX)) <= esp:
        break
      if(self.cambioDeSigno(self.f(xi),self.f(xi+deltaX))):
        deltaX /= 10
        continue

      contador += 1
      xi += deltaX
    
    if contador >= iteracionMaxima:
      return False
    else:
      df = pd.DataFrame(resultados,columns=['xi','xi+dx','f(xi)','f(xi+dx)','dx','Ea'],index=range(1,len(resultados)+1))
      return df,float(xi)

  def newthonRhapson(self,xi=0,esp=0.0001,iteracionMaxima=1000):
    i = 1
    resultados = []
    while i < iteracionMaxima:
        xf = xi - (self.f(xi) / self.diff(xi))
        Ea = abs(xi-xf)
        resultados.append([xi,xf,Ea])  
        if Ea <= esp:
            break
        xi = xf
        i += 1

    if i >= iteracionMaxima:
        return False
    else:
        df = pd.DataFrame(resultados,columns=['xi','xf','Ea'],index=range(1,len(resultados)+1))
        return df,float(xf)

  def biseccion(self,xi,xf,esp=0.0001,iteracionMaxima=1000):
    """
    Funcion que encuetra la raiz por el método de bisección
    """
    i = 0
    resultados = []
    while i < 1000:
      xr = (xi + xf) / 2
      Ea = abs(xi-xf)
      resultados.append([xi,xf,xr,round(self.f(xi),2),round(self.f(xf),2),round(self.f(xr),2),Ea])  
      if self.cambioDeSigno(self.f(xr),self.f(xi)) == False:
          xi = xr
      else:
          xf = xr
      if Ea <= esp:
          break
      i += 1
    
    if i >= iteracionMaxima:
      return None
    else:
      columnas = ['xi','xf','xr','f(xi)','f(xf)','f(xr)','Ea']
      df = pd.DataFrame(resultados,columns=columnas,index=range(1,len(resultados)+1))
      return df,float(xr)

#0.089*x**4-2.55*x**3+22.48*x**2-59.68*x+19