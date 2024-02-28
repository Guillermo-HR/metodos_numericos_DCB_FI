# ------------------- Importar módulos -------------------
from metodos_numericos_dcb_fi.utilidades.configuracion import text
from metodos_numericos_dcb_fi.utilidades.validacion import validarTipo

# ------------------- Importar bibliotecas -------------------
import sympy as sp

# ------------------- Funciones -------------------
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
