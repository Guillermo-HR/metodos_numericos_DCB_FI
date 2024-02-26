# ------------------- Importar bibliotecas -------------------
from typing import List
import sympy as sp
from sympy import Symbol, Poly
import numpy as np
import pandas as pd
from IPython.display import display, Math
#import matplotlib.pyplot as plt
#import plotly.graph_objects as go
from pathlib import Path
import json
import string

# ------------------- Definir constantes -------------------
colores = ['blue', 'red', 'green', 'orange', 'purple', 'magenta', 'yellow', 'black']
letras_latinas = list(string.ascii_letters)
letras_griegas = [chr(i) for i in range(0x3b1, 0x3ca)] + [chr(i) for i in range(0x3ca, 0x3d6)] + [chr(i) for i in range(0x391, 0x3a2)] + [chr(i) for i in range(0x3a3, 0x3aa)] + [chr(i) for i in range(0x3aa, 0x3b1)]
maxIteraciones = 20
idioma = 'es'
text = {}

def leerTextos()->None:
    """
    Lee el archivo de texto correspondiente al idioma especificado y carga su contenido en la variable global 'text'.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        FileNotFoundError: Si no se encuentra el archivo de texto correspondiente al idioma especificado.
        json.JSONDecodeError: Si ocurre un error al decodificar el archivo de texto.

    Retorno:
        No retorna ningún valor.

    Ejemplo:
        leer_textos()
    """
    current_dir = Path(__file__).resolve().parent
    text_file = current_dir / '..' / 'data' / f'text_{idioma}.json'
    global text
    try:
        with open(text_file, 'r', encoding='utf-8') as file:
            text = json.load(file)
    except FileNotFoundError:
        raise Exception(f'No se puede leer el archivo text_{idioma}.json\nCan\'t read the file text_{idioma}.json')
    except json.JSONDecodeError:
        raise Exception(f'Error al decodificar el archivo text_{idioma}.json\nFailed to decode the file text_{idioma}.json')

def cambiarIdioma(nuevo_idioma:str)->None:
    '''
    Cambia el idioma actual del programa al idioma especificado.

    Parámetros:
        nuevo_idioma (str): El nuevo idioma al que se desea cambiar. Debe ser uno de los idiomas disponibles.

    Excepciones:
        Exception: Si el nuevo idioma no está en la lista de idiomas disponibles [es].

    Retorno:
        No retorna ningún valor.

    Ejemplo:
        cambiar_idioma('es')
    '''
    nuevo_idioma = nuevo_idioma.lower()
    idiomas_disponibles = ['es']
    if nuevo_idioma in idiomas_disponibles:
        global idioma
        idioma = nuevo_idioma
        leerTextos()
    else:
        raise Exception(f'{text["Util"]["Errores"]["idioma"].replace("{1}", ", ".join(idiomas_disponibles)).replace("{2}", nuevo_idioma)}')
    
def cambiarMaxIteraciones(nuevo_max_iteraciones:int)->None:
    '''
    Cambia el número máximo de iteraciones permitidas en el programa.

    Parámetros:
        nuevo_max_iteraciones (int): El nuevo número máximo de iteraciones permitidas.

    Excepciones:
        ValueError: Si el nuevo número máximo de iteraciones no es un entero positivo.

    Retorno:
        No retorna ningún valor.

    Ejemplo:
        cambiar_max_iteraciones(30)
    '''
    if not isinstance(nuevo_max_iteraciones, int):
        raise Exception(f'{text["Util"]["Errores"]["tipo_entrada"].replace("{1}", "int").replace("{2}", type(nuevo_max_iteraciones))}')
    if nuevo_max_iteraciones < 1 or nuevo_max_iteraciones > 70:
        raise Exception(f'{text["Util"]["Errores"]["max_iteraciones"].replace("{1}", str(nuevo_max_iteraciones))}')
    global maxIteraciones
    maxIteraciones = nuevo_max_iteraciones

# ------------------- Validar entradas -------------------
def validarTipo(valor:any, tipo:type)->None:
    """
    Función: validarTipo

    Descripción:
    Esta función se utiliza para validar si un valor dado es de un tipo específico. Si el valor no es del tipo especificado, se lanza una excepción.

    Parámetros:
    - valor: cualquier valor que se desee validar.
    - tipo: el tipo específico que se desea comprobar.

    Excepciones:
    - Exception: se lanza una excepción si el valor no es del tipo especificado.

    Retorno:
    - None

    Ejemplo de uso:
    validarTipo(5, int)
    """
    if not (isinstance(valor, tipo)):
        raise Exception(f'{text["Util"]["Errores"]["tipo_entrada"].replace("{1}", f"{tipo}").replace("{2}", str(type(valor)))}')

def validarDatosBiseccion(x_i:float, x_s:float, tol:float)->tuple[float, float, float]:
    '''
    Función: validarDatosBiseccion

    Descripción:
    Esta función se utiliza para validar los datos de entrada para el método de bisección. Verifica si los valores de x_i, x_s y tol son números de tipo float. Además, comprueba si x_i es menor que x_s y si tol es mayor que cero. Si alguna de estas validaciones falla, se lanza una excepción.

    Parámetros:
    - x_i: número de tipo float que representa el límite inferior del intervalo.
    - x_s: número de tipo float que representa el límite superior del intervalo.
    - tol: número de tipo float que representa la tolerancia.

    Excepciones:
    - ValueError: se lanza una excepción si x_i es mayor o igual que x_s, o si tol es menor o igual que cero.
    - Exception: se lanza una excepción si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - Una tupla que contiene los valores de x_i, x_s y tol.

    Ejemplo de uso:
    validarDatosBiseccion(1.0, 2.0, 0.001)
    '''
    validarTipo(x_i, (int, float))
    validarTipo(x_s, (int, float))
    if x_i >= x_s:
        raise ValueError(f'{text["Util"]["Errores"]["biseccion"].replace("{1}", x_i).replace("{2}", x_s)}')
    validarTipo(tol, (int, float))
    if tol <= 0:
        raise ValueError(f'{text["Util"]["Errores"]["tolerancia"].replace("{1}", tol)}')
    return x_i, x_s, tol

def validarDatosNR(x_0:str, tol:str):
    '''
    Función: validarDatosNR

    Descripción:
    Esta función se utiliza para validar los datos de entrada para el método Newton Raphson. Verifica si los valores de x_0 y tol son de tipo int o float, y si la tolerancia es mayor que cero. Si alguno de los valores no cumple con estas condiciones, se lanza una excepción.

    Parámetros:
    - x_0: valor inicial para el método.
    - tol: tolerancia para el método.

    Excepciones:
    - ValueError: se lanza una excepción si la tolerancia es menor o igual a cero.
    - Exception: se lanza una excepción si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - Tuple: una tupla que contiene los valores de x_0 y tol.

    Ejemplo de uso:
    validarDatosN_R(5, 0.001)
    '''
    validarTipo(x_0, (int, float))
    validarTipo(tol, (int, float))
    if tol <= 0:
        raise ValueError(f'{text["Util"]["Errores"]["tolerancia"].replace("{1}", tol)}')
    return x_0, tol

# ------------------- Calculo de errores -------------------
def calcularErrorRelativo(valorReal: float, valorAproximado: float) -> float:
    '''
    Calcula el error relativo entre un valor real y un valor aproximado.

    Parámetros:
        - valorReal (float): El valor real.
        - valorAproximado (float): El valor aproximado.

    Excepciones:
        - Exception: Se genera una excepción si alguno de los valores no es de tipo int o float.

    Retorno:
        - float: El error relativo entre los dos valores.

    Ejemplo:
        calcular_error_relativo(10.5, 10.2) -> 2.85714
    '''
    if not (isinstance(valorReal, (int, float))):
        raise Exception(f'{text["Util"]["Errores"]["tipo_entrada"].replace("{1}", "int, float").replace("{2}", type(valorReal))}')
    if not (isinstance(valorAproximado, (int, float))):
        raise Exception(f'{text["Util"]["Errores"]["tipo_entrada"].replace("{1}", "int, float").replace("{2}", type(valorAproximado))}')
    if valorReal == 0:
        return round(abs(valorReal - valorAproximado),5)
    return round(abs((valorReal - valorAproximado) / valorReal) * 100,5)

def calcularErrorAbsoluto(valorReal: float, valorAproximado: float) -> float:
    """
    Calcula el error absoluto entre un valor real y un valor aproximado.

    Parámetros:
        valorReal (float): El valor real.
        valorAproximado (float): El valor aproximado.

    Excepciones:
        Exception: Si alguno de los valores no es de tipo int o float.

    Retorno:
        float: El valor del error absoluto.

    Ejemplo:
        calcular_error_absoluto(10.5, 9.8) -> 0.7
    """
    validarTipo(valorReal, (int, float))
    validarTipo(valorAproximado, (int, float))
    return round(abs(valorReal - valorAproximado),5)

# ------------------- Mostrar resultados -------------------
def mostrarPolinomio(a:list[float], variable:str='x', titulo:str='')->None:
    '''
    Muestra un polinomio en formato matemático.

    Parámetros:
        a (list): Lista de coeficientes del polinomio.
        variable (str, opcional): Variable del polinomio. Por defecto es 'x'.
        titulo (str, opcional): Título que se mostrará antes del polinomio. Por defecto es ''.

    Excepciones:
        TypeError: Si 'a' no es una lista o si los coeficientes no son números.
        ValueError: Si la variable contiene caracteres que no son letras latinas o griegas.

    Retorno:
        None. Muestra el polinomio en formato matemático.

    Ejemplo:
        mostrarPolinomio([1, -2, 3], 'p', 'Polinomio de grado 2')
    '''
    # validar que a sea una lista
    validarTipo(a, list)
    # validar que los coeficientes sean números
    for coeficiente in a:
        validarTipo(coeficiente, (int, float))
    # validar que la variable sea al menos un caracter
    if len(variable) == 0:
        raise ValueError(f'{text["Util"]["Errores"]["len_variable"].replace("{1}", 1).replace("{2}", len(variable))}')
    # validar si todos los caracteres de la variable son letras latinas o griegas
    for letra in variable:
        if not (letra in letras_latinas + letras_griegas):
            raise ValueError(f'{text["Util"]["Errores"]["variable"].replace("{1}", variable)}')
    # Si la variable es mas de 1 caracter poerla entre parentesis en el polinomio 
    if len(variable)>1:
        variable = f'({variable})'
    polinomio = ''
    grad = len(a) - 1
    for i, coeficiente in enumerate(a[:-2]):
        if coeficiente != 0:
            sign = '-' if coeficiente < 0 else '+'
            polinomio += f'{sign} {abs(round(coeficiente, 3))}*{variable}**{grad - i} '
    if a[-2] != 0:
        sign = '-' if a[-2] < 0 else '+'
        polinomio += f'{sign} {abs(round(a[-2], 3))}*{variable} '
    if a[-1] != 0:
        sign = '-' if a[-1] < 0 else '+'
        polinomio += f'{sign} {abs(round(a[-1], 3))}'
    # Eliminar los parentesis que se agregaron para la variable
    if len(variable)>1:
        variable = variable[1:-1]
    var = Symbol(f'{variable}')
    polinomio = Poly(polinomio, var)
    if titulo != '': print(titulo)
    display(Math(f'P_{grad}({variable}) = ' + sp.latex(polinomio.as_expr())))

def crearTablaFactoresCuadraticos(a: List[float]) -> pd.DataFrame:
    '''
    Crea una tabla vacía para almacenar los coeficientes del método factores cuadráticos.

    Parámetros:
        a (List[float]): Una lista de coeficientes.

    Excepciones:
        TypeError: Si 'a' no es una lista o si alguno de los coeficientes no es un número.

    Retorno:
        pd.DataFrame: Una tabla vacía con las columnas 'Iteracion', 'p', 'q', 'b_0', 'b_1', ..., 'R', 'S', 'Δp', 'Δq'.

    Ejemplo:
        crearTablaFactoresCuadraticos([1, 2, 3])
    '''
    # validar que a sea una lista
    validarTipo(a, list)
    # validar que los coeficientes sean números
    for coeficiente in a:
        validarTipo(coeficiente, (int, float))
    
    columnas = ['Iteracion','p','q'] + [f'b_{k}' for k in range(len(a) - 2)] + ['R', 'S', '\u0394p','\u0394q']
    tabla = pd.DataFrame(columns=columnas)
    tabla.set_index('Iteracion', inplace=True)
    return tabla

def agregarRenglonFactoresCuadraticos(tabla:pd.DataFrame, p:float, q:float, b:list[float], R:float, S:float, dp:float, dq:float)->pd.DataFrame:
    '''
    Agrega un nuevo renglón a una tabla de datos que contiene factores cuadráticos.

    Parámetros:
    - tabla: DataFrame de pandas que representa la tabla de datos.
    - p: Valor numérico (int o float) que representa el factor p.
    - q: Valor numérico (int o float) que representa el factor q.
    - b: Lista de valores numéricos (int o float) que representa los coeficientes b.
    - R: Valor numérico (int o float) que representa el factor R.
    - S: Valor numérico (int o float) que representa el factor S.
    - dp: Valor numérico (int o float) que representa el factor dp.
    - dq: Valor numérico (int o float) que representa el factor dq.

    Excepciones:
    - Exception: Se lanza una excepción si alguno de los parámetros no cumple con el tipo de dato esperado.

    Retorno:
    - DataFrame de pandas: La tabla de datos actualizada con el nuevo renglón agregado.

    Ejemplo de uso:
    tabla = agregarRenglonFactoresCuadraticos(tabla, 0.5, 0.2, [1, 2, 3], 0.8, 0.6, 0.1, 0.3)
    '''
    # validar los tipos de los parámetros
    validarTipo(tabla, pd.DataFrame)
    validarTipo(p, (int, float))
    validarTipo(q, (int, float))
    validarTipo(b, list)
    for coeficiente in b:
        validarTipo(coeficiente, (int, float))
    validarTipo(R, (int, float))
    validarTipo(S, (int, float))
    validarTipo(dp, (int, float))
    validarTipo(dq, (int, float))
    # validar la longitud de b
    if len(b) != len(tabla.columns) - 6:
        raise Exception(f'{text["Util"]["Errores"]["len_b_FC"].replace("{1}", len(tabla.columns) - 6).replace("{2}", len(b))}')
    # agregar un renglón a la tabla
    nuevo_renglon = [p, q]
    nuevo_renglon.extend(b)
    nuevo_renglon.extend([R, S, dp, dq])
    tabla.loc[len(tabla)+1] = nuevo_renglon
    return tabla

def mostrarMatriz(matriz:np.ndarray[float], nombre:str)->None:
    """
    Función: mostrarMatriz

    Descripción:
    Esta función se utiliza para mostrar una matriz en forma de tabla en la consola. La matriz se muestra con un nombre dado y se formatea de manera que los valores estén alineados correctamente.

    Parámetros:
    - matriz: una matriz representada como un array de numpy con valores de tipo float.
    - nombre: el nombre que se desea mostrar junto a la matriz.

    Retorno:
    - None

    Ejemplo de uso:
    mostrarMatriz(np.array([[1.234, 2.345], [3.456, 4.567]]), 'Matriz A')
    """
    validarTipo(matriz, np.ndarray)
    validarTipo(nombre, str)
    if len(nombre) == 0:
        nombre = 'M'
    n = len(matriz)
    mitad = int(n / 2)
    len_nombre = len(nombre)
    espacio = ' ' * (len_nombre + 3)
    
    for (i, j), value in np.ndenumerate(matriz):
        validarTipo(value, (int, float))
        if i == mitad:
            print(nombre + ' = ', end='')
        else:
            print(espacio, end='')
        if value >= 0:
            print(' ', end='')
        print(f'{np.around(value, decimals = 3)}   ', end='\t')
        if j == n-1:
            print('')
    print('\n')

def mostrarVector(vector:np.ndarray[float], nombre:str):
    '''
    Función: mostrarVector

    Descripción:
    Esta función se utiliza para mostrar un vector en forma de columna, con su respectivo nombre. Cada elemento del vector se redondea a 3 decimales y se valida que sea de tipo entero o flotante antes de imprimirlo.

    Parámetros:
    - vector: un arreglo de numpy que representa el vector a mostrar.
    - nombre: una cadena de texto que representa el nombre del vector.

    Retorno:
    - None

    Ejemplo de uso:
    mostrarVector(np.array([1, 2, 3]), "Vector A")
    '''
    validarTipo(vector, np.ndarray)
    validarTipo(nombre, str)
    if len(nombre) == 0:
        nombre = 'v'
    n = len(vector)
    mitad = n // 2
    len_nombre = len(nombre)
    espacio = ' ' * (len_nombre + 3)
    columna = np.around(vector, decimals = 3)
    for i in range(n):
        validarTipo(vector[i], (int, float))
        if i == mitad:
            print(nombre + ' = ', end='')
        else:
            print(espacio, end='')
        if vector[i] >= 0:
            print(' ', end='')
        print(f'{columna[i]}   ')
    print('\n')

def mostrarValoresCaracteristicos(valores:np.ndarray):
    '''
    Función: mostrarValoresCaracteristicos

    Descripción:
    Esta función se utiliza para mostrar los valores característicos de una matriz.

    Parámetros:
    - valores: un arreglo de numpy que contiene los valores característicos de la matriz.

    Excepciones:
    - Exception: se lanza una excepción si el parámetro 'valores' no es un arreglo de numpy.

    Retorno:
    - None

    Ejemplo de uso:
    mostrarValoresCaracteristicos(np.array([1, 2, 3]))
    '''
    validarTipo(valores, np.ndarray)
    for i, valor in enumerate(valores, start=1):
        if isinstance(valor, np.complex):
            display(Math(f'λ_{i} = {np.round(valor.real, 3)}'))
        else:
            display(Math(f'λ_{i} = {np.round(valor.real, 3)}'))

# ------------------- Leer entradas -------------------
def leerFuncion():
    '''
    Lee una función ingresada por el usuario y la convierte en una expresión simbólica utilizando la biblioteca sympy.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        Exception: Si ocurre un error al convertir la función en una expresión simbólica.

    Retorno:
        Una expresión simbólica de la función ingresada por el usuario.

    Ejemplo:
        leerFuncion()
    '''
    print(text["Util"]["Entrada"]["funcion_1"])
    funcion = input(f'{text["Util"]["Entrada"]["funcion_2"]}')
    x = sp.Symbol('x')
    try:
        funcion = sp.sympify(funcion)
        return funcion
    except:
        raise Exception(f'{text["Util"]["Errores"]["funcion"].replace("{1}", funcion)}')
    
def leerTolerancia()->float:
    '''
    Lee la tolerancia ingresada por el usuario y la devuelve como un número de punto flotante.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        ValueError: Si la tolerancia ingresada es menor o igual a cero.

    Retorno:
        float: La tolerancia ingresada por el usuario.

    Ejemplo:
        leerTolerancia()
    '''
    print(text["Util"]["Entrada"]["tolerancia_1"])
    tol = input(f'{text["Util"]["Entrada"]["tolerancia_2"]}')
    validarTipo(tol, (int, float))
    if tol <= 0:
        raise ValueError(f'{text["Util"]["Errores"]["tolerancia"].replace("{1}", tol)}')
    return tol

def leerPolinomio():
    '''
    Función: leerPolinomio

    Descripción:
    Esta función se utiliza para leer un polinomio desde la entrada estándar. Solicita al usuario el grado del polinomio y los coeficientes correspondientes, validando que los valores ingresados sean del tipo correcto.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        ValueError: se lanza una excepción si el grado del polinomio es menor o igual a cero.
        Exception: se lanza una excepción si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
        Una lista de coeficientes del polinomio.

    Ejemplo de uso:
        leerPolinomio()
    '''
    print(text["Util"]["Entrada"]["polinomio_1"])
    grado = input(f'{text["Util"]["Entrada"]["polinomio_2"]}')
    validarTipo(grado, int)
    if grado <= 0:
        raise ValueError(f'{text["Util"]["Errores"]["grado_polinomio"].replace("{1}", grado)}')
    coeficientes = []
    contador = 0
    for i in range(grado + 1):
        coeficiente = input(f'{text["Util"]["Entrada"]["coeficiente"].replace("{1}", grado-i)}')
        validarTipo(coeficiente, (int, float))
        if i == contador and coeficiente == 0:
            contador += 1
        else:
            coeficientes.append(coeficiente)
    if len(coeficientes) < 2:
        raise ValueError(text["Util"]["Errores"]["grado_final_polinomio"])
    return coeficientes

def leerMatriznxn()->np.array:
    """
    Lee una matriz cuadrada de tamaño nxn y la devuelve como un array de numpy.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        ValueError: Si el valor de n es menor o igual a cero.
        Exception: Si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
        np.array: La matriz cuadrada de tamaño nxn.

    Ejemplo:
        matriz = leerMatriznxn()
    """
    print(text["Util"]["Entrada"]["matriz_nxn_1"])
    n = input(f'{text["Util"]["Entrada"]["matriz_nxn_2"]}')
    validarTipo(n, int)
    if n <= 0:
        raise ValueError(f'{text["Util"]["Errores"]["matriz_nxn"].replace("{1}", n)}')
    matriz = []
    for i in range(n):
        fila = []
        for j in range(n):
            elemento = input(f'{text["Util"]["Entrada"]["matriz_nxn_3"].replace("{1}", i+1).replace("{2}", j+1)}')
            validarTipo(elemento, (int, float))
            fila.append(elemento)
        matriz.append(fila)
    return np.array(matriz)

def leerVector(n:int, reglas:str='')->np.array:
    """
    Lee un vector de números ingresados por el usuario.

    Parámetros:
    - n: int, la longitud del vector.
    - reglas: str opcional, reglas adicionales para ingresar los elementos del vector.

    Excepciones:
    - Exception: Si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - np.array, un arreglo numpy que contiene los elementos ingresados por el usuario.

    Ejemplo de uso:
    leerVector(5, 'Ingrese números enteros o decimales: ')
    """
    print(f'{text["Util"]["Entrada"]["vector_1"]}{reglas}')
    vector = []
    for i in range(n):
        elemento = input(f'{text["Util"]["Entrada"]["vector_2"].replace("{1}", i+1)}')
        validarTipo(elemento, (int, float))
        vector.append(elemento)
    return np.array(vector)

def leerVectorKrilov(n:int)->np.array:
    """
    Función: leerVectorKrilov

    Descripción:
    Esta función se utiliza para leer un vector de números ingresados por el usuario para el metodo de Krilov.

    Parámetros:
    - n: int, la longitud del vector.

    Excepciones:
    - Exception: Si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
    - np.array, un arreglo numpy que contiene los elementos ingresados por el usuario.

    Ejemplo de uso:
    leerVectorKrilov(5)
    """
    print(text["Util"]["Entrada"]["vector_K_1"])
    opcion = input(f'{text["Util"]["Entrada"]["opcion"]}')
    if opcion == '0':
        vector = np.zeros(n) # Vector de ceros de tamaño n
        vector[0] = 1 # Primer elemento igual a 1
    else:
        vector = leerVector(n, text["Util"]["Entrada"]["vector_K_2"])
        # si todos los elementos son cero
        if np.all(vector == 0):
            print(text["Util"]["Errores"]["vector_K"])
            vector = leerVectorKrilov(n)
    return vector

def leerDatosLU()->tuple[np.array, np.array]:
    '''
    Lee los datos necesarios para realizar la factorización LU de una matriz y su vector de términos independientes.

    Parámetros:
        No recibe ningún parámetro.

    Excepciones:
        ValueError: Si el valor de n es menor o igual a cero.
        Exception: Si ocurre un error al validar el tipo de los valores ingresados.

    Retorno:
        tuple: Una tupla que contiene la matriz y el vector ingresados por el usuario.

    Ejemplo:
        matriz, vector = leerDatosLU()
    '''
    print(text["Util"]["Entrada"]["LU_1"])
    matriz = leerMatriznxn()
    print(text["Util"]["Entrada"]["LU_2"])
    vector = leerVector(len(matriz))
    return matriz, vector

# ------------------- Otros -------------------
def quitarNan(valores_x:list, valores_y:list) -> tuple[list, list]:
    """
    Función: quitarNan

    Descripción:
    Esta función se utiliza para eliminar los valores NaN (Not a Number) de dos listas de valores, 'valores_x' y 'valores_y'. Los valores NaN son reemplazados por None en las listas actualizadas.

    Parámetros:
    - valores_x: una lista de valores.
    - valores_y: una lista de valores.

    Excepciones:
    - Exception: se lanza una excepción si las listas 'valores_x' y 'valores_y' no tienen la misma longitud o si alguno de los valores no es de tipo int o float.

    Retorno:
    - Una tupla que contiene dos listas actualizadas: 'valores_x_actualizado' y 'valores_y_actualizado'.

    Ejemplo de uso:
    quitarNan([1, 2, 3, np.nan], [4, np.nan, 6, 7])
    """
    validarTipo(valores_x, list)
    validarTipo(valores_y, list)
    if len(valores_x) != len(valores_y):
        raise Exception(f'{text["Util"]["Errores"]["quitar_nan"].replace("{1}", len(valores_x)).replace("{2}", len(valores_y))}')
    valores_x_actualizado = []
    valores_y_actualizado = []
    len_y = len(valores_y)
    for i in range(len_y):
        validarTipo(valores_x[i], (int, float))
        validarTipo(valores_y[i], (int, float))
        if np.isfinite(valores_y[i]):
            valores_x_actualizado.append(valores_x[i])
            valores_y_actualizado.append(valores_y[i])
    return valores_x_actualizado, valores_y_actualizado