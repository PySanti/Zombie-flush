def agregar_a_lista(    lista : list, 
                        elementos_y_cantidades : dict) -> list:
    """
    Version moderna de list.append() Recibe por parametro una lista, cadena o tupla, 
    y un diccionario donde las claves seran el valor que se quiere agregar, y el valor de 
    estas claves, la cantidad de veces     
    """
    try:
        if isinstance( lista, list):
            tipo_de_lista_inicial = list 
        elif isinstance(lista, tuple):
            tipo_de_lista_inicial = tuple 
        elif isinstance(lista, str):
            tipo_de_lista_inicial = str 
            from ideas import list_to_str
        else:
            raise Exception
        lista = list(lista)
        elementos_y_cantidades = dict(elementos_y_cantidades)
    except:
        print("""
            Hubo un error en la funcion ideas.agregar_a_lista
            Posibles candidatos
            - Error al importar ideas.list_to_str (en caso de que 'lista' sea una cadena)
            - Mal uso del parametro 'lista'
            - Mal uso del parametro 'elementos y cantidades'
        """)
    try:
        for elemento, cantidad in elementos_y_cantidades.items():
            if not isinstance( cantidad, int):
                raise Exception
            for i in range(cantidad):
                lista.append(elemento)
    except:
        print("""
            Hubo un error en el modulo ideas.agregar_a_lista
            Los valores de las claves deben ser enteros
        """)
        quit()
    if tipo_de_lista_inicial == str:
        return list_to_str(lista)
    elif tipo_de_lista_inicial == tuple:
        return tuple(lista)
    elif tipo_de_lista_inicial == list:
        return lista
def print_menu(  lista_a_imprimir : list, 
                    caracter_de_seleccion = ' <', 
                    caracter_arriba = 'w',
                    caracter_abajo = 's' , 
                    caracter_de_ejecucion = '\n',
                    caracter_de_guionizacion = '~ ',
                    indice_de_comienzo = None, 
                    mensaje = None,
                    color_para_linea_seleccionada = True,
                    efecto_de_movimiento = True) -> int:
    """
    Imprime la lista que se le pase en el primer parametro en forma de menu
    permitiendo acceder a las opciones interactivamente
    Arg[1] : lista que se desea imprimir
    Arg[2] : caracter que se desea emplear 
    para simbolizar la opcion seleccionada en el momento,
    ' < ' en caso de no especificarse
    Arg[3] : caracter que debera presionarse para
    mover el cursor a la opcion de arriba, 'w' en caso 
    de no especificarse 
    Arg[4] : caracter que debera presionarse para 
    mover el cursor a la opcion de abajo, 's' en caso de 
    no especificarse
    Arg[5]: caracter que debera presionarse para ejecutar 
    la opcion que se desee. 'r' en caso de no especificarse
    Arg[6] : caracter que se desea colocar a la izquierda de cada 
    una de las opciones, '~ ' por defecto
    Arg[7] : indice de la lista de seleccion por default, en caso 
    de no especificarse, se empieza por la mitad
    Agr[8] : mensaje que se desee imprimir de guia para el usuario
    Arg[9] : en caso de que sea True, la linea que este seleccionada
    se pondra a color (solo valido para listas de una longitud menor a 
    30), notese que, en caso de que esta opcion se seleccione, el caracter 
    de seleccion no se empleara
    Arg[10]: en caso de que esta opcion sea True, al seleccionarse una opcion esta
    hara un leve movimiento que permitira visualizar facilmente la linea que se seleccione

    Retorna el numero de la eleccion que fue seleccionada (indice + 1)
    
    Nota: enviar None para emplear los valores por defecto en caso de querer usarlos
    """
    try:
        from getch import getch 
        from os import system
        caracter_de_seleccion    = caracter_de_seleccion if caracter_de_seleccion == ' <' else str(caracter_de_seleccion)
        indice_de_comienzo       = len(lista_a_imprimir)//2 if indice_de_comienzo ==  None else int(indice_de_comienzo)
        caracter_arriba          = caracter_arriba if caracter_arriba == 'w' else str(caracter_arriba)
        caracter_abajo           = caracter_abajo if caracter_abajo == 's' else str(caracter_abajo)
        caracter_de_ejecucion    = caracter_de_ejecucion if caracter_de_ejecucion == '\n' else str(caracter_de_ejecucion)
        caracter_de_guionizacion = caracter_de_guionizacion if caracter_de_guionizacion == '~' else str(caracter_de_guionizacion)
        mensaje                  = None if mensaje == None else str(mensaje)
        lista_a_imprimir_copia   = [str(i) for i in lista_a_imprimir]
        if color_para_linea_seleccionada:
            import colorama
            from colorama import Back, Fore, Style
            colorama.init()
        if len(lista_a_imprimir) == 0:
            raise Exception
    except Exception:
        print("""
            Error en la funcion ideas.imprimir_menu
            Posibles candidatos ...
                - Mal uso del parametro caracter_de_seleccion
                - Mal uso del parametro caracter_arriba
                - Mal uso del parametro caracter_abajo
                - Mal uso del parametro caracter_de_ejecucion
                - Mal uso del parametro caracter_de_guionizacion
                - Mal uso del parametro indice_de_comienzo
                - Mal uso del parametro mensaje
                - Lista a imprimir vacia 
                - Error al importar la funcion getch.getch
                - Error al importar la funcion os.systema
                - Error al importar el modulo colorama (en caso de que la opcion color_para_linea_seleccionada este activada)
            """)
        quit()

    if len(lista_a_imprimir_copia) == 1:
        pass
    else:
        def seleccion_actual():
            # Revisa toda la lista en busca de la cadena 
            # seleccionada en ese momento en caso de encontrar 
            # una seleccionada retorna el numero de indice en 
            # cuestion, en caso contrario retorna False
            iterador = 0
            for i in lista_a_imprimir_copia:
                if cadena_seleccionada(i):
                    return iterador
                else:
                    iterador += 1
            return False
        def sobreescribir_puntero(indice : int) -> None:
            # recibe el indice de la cadena que se desea sobrescribir y lo sobreescribe
            cadena_actual = lista_a_imprimir_copia[indice][:len(caracter_de_seleccion)*-1]
            lista_a_imprimir_copia[indice] = cadena_actual
        def cadena_seleccionada(cadena):
            # retorna True si la cadena esta seleccionada
            return (cadena[len(caracter_de_seleccion)*-1:] == caracter_de_seleccion)
        def redefinir(indice : int) -> None:
            # recibe el indice de la cadena que se quiere redefinir y la redefine
            cadena_actual = lista_a_imprimir_copia[indice]
            a = 0
            for i in lista_a_imprimir_copia:
                if cadena_seleccionada(i) and (i != cadena_actual):
                    sobreescribir_puntero(a)
                else:
                    a+=1
            lista_a_imprimir_copia[indice] = cadena_actual if cadena_seleccionada(cadena_actual) else cadena_actual + caracter_de_seleccion
        def mover_abajo(indice : int) -> None:
            # recibe el indice de la seleccion actual y mueve el cursor hacia abajo
            sobreescribir_puntero(indice)
            cadena_actual = lista_a_imprimir_copia[indice + 1] + caracter_de_seleccion
            lista_a_imprimir_copia[indice + 1] = cadena_actual
        def mover_arriba(indice : int) -> None:
            # recibe el indice de la cadena actual y mueve el cursor hacia arriba
            sobreescribir_puntero(indice)
            cadena_actual = lista_a_imprimir_copia[indice - 1] + caracter_de_seleccion
            lista_a_imprimir_copia[indice - 1] = cadena_actual
        def mover_al_principio(indice : int) -> None:
            # recibe el indice de la cadena actual y la mueve al inicio de la lista
            sobreescribir_puntero(indice)
            cadena_actual = lista_a_imprimir_copia[0] + caracter_de_seleccion
            lista_a_imprimir_copia[0] = cadena_actual
        def mover_al_final(indice : int) -> None:
            # recibe el indice de la cadena actual y la mueve al final de la lista
            sobreescribir_puntero(indice)
            cadena_actual = lista_a_imprimir_copia[-1] + caracter_de_seleccion
            lista_a_imprimir_copia[-1] = cadena_actual
    def main():
        redefinir(indice_de_comienzo)
        while True:
            system('clear')
            print('\n\n\n\t\t\t\t\t\t' + mensaje + '\n\n\n' if mensaje != None else '')
            if len(lista_a_imprimir_copia) >= 30:
                # codigo en caso de que la lista sea muy 
                # larga para que se imprima horizontalmente
                i = 0
                for cadena in lista_a_imprimir_copia:
                    if i == 5:
                        print()
                        i = 0
                    print(f'{caracter_de_guionizacion}   {cadena:30}', end='')
                    i+=1
                print()
            else:
                caracter_de_guionizacion_para_cadena_seleccionada = caracter_de_guionizacion
                if efecto_de_movimiento:
                    caracter_de_guionizacion_para_cadena_seleccionada  = '   ' + caracter_de_guionizacion 
                for cadena in lista_a_imprimir_copia:
                    if cadena_seleccionada(cadena):
                        if color_para_linea_seleccionada:
                            print(f'{Fore.BLACK}{Back.WHITE}{caracter_de_guionizacion_para_cadena_seleccionada}   {cadena[:len(caracter_de_seleccion)*-1]}        {Fore.RESET}{Back.RESET}')                    
                        else:
                            print(f'{caracter_de_guionizacion_para_cadena_seleccionada}   {cadena}')                    
                    else:
                        print(f'{caracter_de_guionizacion}   {cadena}')
            entrada = getch().lower()
            if len(lista_a_imprimir_copia) == 1:
                if entrada == caracter_de_ejecucion:
                    return seleccion_actual() + 1   
                else:
                    pass    
            else:
                indice_de_seleccion_actual = seleccion_actual()
                if isinstance(indice_de_seleccion_actual, bool):
                    # comprobacion en caso de que la funcion no logre encontrar la seleccion actual
                    # en caso de que no se encuentre, no se movera el cursor 
                    pass
                else:
                    if entrada == caracter_arriba:
                                if indice_de_seleccion_actual == 0:
                                    mover_al_final(indice_de_seleccion_actual)
                                else:
                                    mover_arriba(indice_de_seleccion_actual)
                    elif entrada == caracter_abajo:
                                if indice_de_seleccion_actual == len(lista_a_imprimir_copia) - 1:
                                    mover_al_principio(indice_de_seleccion_actual)
                                else:
                                    mover_abajo(indice_de_seleccion_actual)
                    elif entrada == caracter_de_ejecucion:
                            return seleccion_actual() + 1
    return main()
def prueba_de_seguridad(usuario_real : str  , 
            clave_real               : str  ,
            modalidad                = 2    , 
            caracter_de_incognita    = '*'  , 
            tiempo_maximo            =  10  ,
            intentos                 = None ,
            ) -> None:


    """
    Recibe el nombre de usuario y la clave
    
    Retorna True en caso de que el usuario logre superar la prueba de seguridad, False en caso contrario 
    
    Nota: enviar None para aprovechar los valores por default de los parametros
    
    
    Arg[1] : nombre del usuario, (obligatorio) 
    Arg[2] : clave del usuario (obligatorio) 
    Arg[3] : modalidad, en este caso, existen tres 
    modalidades que puede emplear
    

    modalidad 1 : aquella sin una entrada de datos interactiva,
    en esta solo se emplearia los parametros obligatorios y el parametro
    'intentos' (3 intentos por default)

    modalidad 2 : aquella con una entrada de datos interactiva, ningun 
    parametro obligatorio, en esta solo se emplearian los parametros 
    obligatorios y los parametros 'tiempo_maximo'(10s por default), 
    'caracter_de_incognita'('*' por default)
    
    Modalidad 3 : lo mismo que modalidad 1 solo que con una 
    entrada de datos invisible

    Como se menciono, ninguno de los parametros (ademas de los obligatorios)
    son necesarios, en caso de no querer enviar, algun parametro, simplemente 
    ponga None en su lugar
    """


    # comprobando parametros para el funcionamiento 
    # general del modulo
    try:
            from os import system as command
            if len(usuario_real ) == 0 or len(clave_real) == 0 or usuario_real == None or clave_real == None:
                raise Exception
            usuario_real, clave_real = str(usuario_real), str(clave_real)
            modalidad = 2 if modalidad == None else int(modalidad)
            if not 1 <= modalidad <= 3:
                raise Exception
    except Exception:
        print("""
            Hubo un error en el modulo security ...
            Posibles candidatos ...
                - Mal uso del parametro "usuario_real"
                - Mal uso del parametro "clave_real"
                - Mal uso del parametro "modalidad"
                - Error al importar el modulo os
            """)
        quit()
    if modalidad == 1 or modalidad == 3:
        # comprobando parametros necesarios para modalidad == 1 o modalidad == 3
        try:
            if modalidad == 3:
                from getpass import getpass
            else:
                pass
            intentos = 3 if intentos == None else int(intentos)
        except Exception:
            if modalidad == 3:
                print("""
                    Hubo un eror en el modulo security ...
                    Posibles candidatos ...
                    - Error al importar el modulo getpass
                    - Mal uso del parametro intentos   
                    """)
            elif modalidad == 1:
                print("""
                    Hubo un eror en el modulo security ...
                    Posibles candidatos ...
                    - Mal uso del parametro intentos   
                    """)
            quit()
        del caracter_de_incognita, tiempo_maximo 
    elif modalidad == 2 :
        # comprobando parametros necesarios para modalidad == 2 
        try:
                from time import time
                from getch import getch 
                caracter_de_incognita = '*' if caracter_de_incognita == None else str(caracter_de_incognita)
                tiempo_maximo = 10 if tiempo_maximo == None else int(tiempo_maximo)
        except Exception:
                print("""
                    Hubo un error en el modulo security
                    Posibles candidatos ...
                    - Error al importar el modulo time 
                    - Error al importar el modulo getch
                    - Mal uso del parametro "caracter_de_incognita"
                    - Mal uso del parametro "tiempo_maximo"
                    """)
                quit()
        del intentos
    def limpiar_pantalla():
        """
        Limpia la pantalla y situa al cursor en el medio de la misma 
        """
        command('clear')
        print('\n\n\n\n\t\t\t\t\t', end='')
    if modalidad == 1 or modalidad == 3:
        intento_fallido = None
        while True:
            limpiar_pantalla()
            print(f' Incorrecto, intentos restantes : {intentos}' if intento_fallido == True else '')
            usuario_inminente = input('\t\t\t\t\t Usuario : ')
            if modalidad == 1:
                clave_inminente   = input('\t\t\t\t\t Clave   : ')
            elif  modalidad == 3:
                clave_inminente   = getpass('\t\t\t\t\t Clave   : ')
            if usuario_real != usuario_inminente or clave_real != clave_inminente:
                intentos -= 1
                if intentos == 0:
                    return False
                else:
                    intento_fallido = True
            elif usuario_real == usuario_inminente and clave_inminente == clave_real:
                return True
    elif modalidad == 2:
        def imprimir_usuario_y_clave() :
            nonlocal usuario_inminente, clave_inminente, caracter_de_incognita
            """
            Imprime el usuario y la clave (la ulima con el caracter de incognita)
            en el medio de la pantalla
            """
            limpiar_pantalla()
            if usuario_inminente == None:
                usuario_inminente = input('   Usuario : ')
            else:
                print(f'   Usuario : {usuario_inminente}')
            print('\t\t\t\t\t   Clave   : ', end='')
            for i in clave_inminente:
                print(caracter_de_incognita, end='')
            print()
        def tiempo_transcurrido():
            return time() - t1
        clave_inminente  = []
        backspace = '\x7f'
        t1 = time()
        usuario_inminente = None
        while True:
            imprimir_usuario_y_clave()
            if tiempo_transcurrido() >= tiempo_maximo:
                return False
            else:
                if tiempo_transcurrido() < tiempo_maximo and  list(clave_real) == clave_inminente and usuario_real == usuario_inminente:
                    return True
                else:
                    entrada = getch()
                    if entrada == backspace :
                        if len(clave_inminente) > 0:
                            clave_inminente.pop()
                        else:
                            pass
                    else:
                        clave_inminente.append(entrada)
def list_to_str(lista : list) -> str:
    """
    Recibe una lista de elementos y la 
    devuelve en forma de cadena
    """
    cadena = None
    for i in lista:
        if cadena == None:
            cadena = str(i)
        else:
            cadena = cadena[:] + str(i)
    return cadena if cadena != None else '' 
def big_number_input(mensaje,
                    rango_menor,
                    rango_mayor) -> int:
    """
    Funcion creada para una entrada de datos de numeros grandes con comodidad
    
    Arg[1]: mensaje que se desea imprimir en conjunto con 
    la entrada de datos
    
    Arg[2] : rango mayor de entrada, no se permitira introducir numeros mayores (opcional)
    
    Arg[3] : rango menor de entrada, no se permitiran introducir numeros menores (opcional) 
    
    Retorna el numero introducido despues del enter
    
    Nota: solo valido para la entrada de numeros, no hace nada en caso contrario
    """

    # comprobamos parametros y dependencias 
    # para el funcionamiento general del programa

    try:
        from os import system as  command
        from  getch import getch
        mensaje = str(mensaje)
        rango_mayor = int(rango_mayor)
        rango_menor = int(rango_menor)
    except Exception:
        print("""
            Error en el modulo ideas.big_number_input
            Posibles candidatos ..
            - Error al importar os.system
            - Error al importar getch.getch
            - Mal uso de parametro 'mensaje'
            - Mal uso del parametro 'rango_menor' 
            - Mal uso del  parametro 'rango_menor'
            """)
        quit()


    def lista_vacia(lista):
        return (len(lista) == 0) 
    def imprimir_input(enteros : list, flotantes = None, mensaje_de_advertencia = None):
        """
        Imprime las teclas introducidas hasta el momento,
        Recibe un mensaje de advertencia en caso de que se supere el rango (opcional)
        Retorna None en caso de que se de a enter sin haber introducido nada
        """
        command('clear')
        print(mensaje, end='')
        if lista_vacia(enteros):
            print()
        else: 
            if enteros[0] == '-':
                print('-', end='')
                enteros = enteros[1:]
                # en caso de que el numero sea negativo se empieza a contar 
                # desde el segundo elemento para evitar que el '-' moleste
            iterator = 0
            for i in enteros:
                print(i,end='')
                iterator += 1
                sublista = enteros[iterator:] 
                if (len(sublista) > 0) and ((len(sublista) %3) == 0):
                    print('.',end='')
            if flotantes != None:
                print(',',end='')
                for i in flotantes:
                    print(i, end='')
            print(mensaje_de_advertencia if mensaje_de_advertencia != None else '')
            print()

    # funcion principal
    enteros = []
    flotantes = None    
    backspace = '\x7f'
    enter = '\n'
    mensaje_de_advertencia = None
    # inicializamos el bucle de impresion
    print(mensaje)


    while True:
        entrada = getch()
        if entrada == enter:
            if flotantes != None and len(flotantes) > 0:
                return (float( list_to_str(enteros + ['.'] + flotantes)))
            else:
                if not lista_vacia(enteros):
                    return int(list_to_str(enteros))
                else:
                    return None
        elif entrada == backspace:
            if flotantes != None:
                if not lista_vacia( flotantes): 
                    flotantes.pop()
                else: 
                    flotantes = None
            else:
                if not lista_vacia(enteros):
                    enteros.pop()
                else:
                    continue
        elif entrada == '-':
            if len(enteros) == 0:
                enteros.append('-')
            else:
                continue
        elif entrada == ',' or entrada == '.':
            if lista_vacia(enteros):
                continue
            else:
                if flotantes == None:
                    flotantes = []
                else:
                    continue
        else:
            try:
                entrada = int(entrada)
                if flotantes != None:
                    flotantes.append(entrada)
                else:
                    enteros.append(entrada)
            except Exception:
                continue
        if (not lista_vacia(enteros) and (not list_to_str(enteros) == '-')) and  (not rango_menor <= float(list_to_str( enteros + ['.'] + flotantes if flotantes != None and len(flotantes) > 0  else enteros)) <= rango_mayor):
            if flotantes != None and not lista_vacia(flotantes):
                flotantes.pop()
            else:
                enteros.pop()
            if mensaje_de_advertencia != None:
                continue
            else:
                mensaje_de_advertencia = '\t\t\t\t Valor fuera de rango ...'
        else:
            mensaje_de_advertencia = None
        imprimir_input(enteros, flotantes,mensaje_de_advertencia)
def imprimir_tabla( diccionario : dict,
                    carcater_de_division_horizontal = '-',
                    carcater_de_division_vertical = '|'):
    '''
    Funcion creada para la impresion de tablas, recibe un 
    diccionario donde las claves son enunciados de las columnas
    y los valores de las claves (iterable) los elementos de las columnas
    '''
    carcater_de_division_horizontal = str(carcater_de_division_horizontal)
    carcater_de_division_vertical = str(carcater_de_division_vertical)
    class ColumnaFormal:
        def __init__(self, enunciado, elementos, logitud_maxima) -> None:
            '''
            Clase creada para agrupar informacion de las columnas 
            '''
            self.enunciado       = enunciado
            self.elementos       = elementos
            self.longitud_maxima = logitud_maxima
    def imprimir_linea(columnas):
        for columna in columnas:
            # espacio arbitrario primario de la columna
            print(carcater_de_division_horizontal,end='')
            # le sumamos 3, 1 por el range y 2 mas por los espacios
            for i in range(columna.longitud_maxima+3):
                print(carcater_de_division_horizontal,end='')
            # espacio arbitrario final de la columna
            print(carcater_de_division_horizontal,end='')
        print()

    lista_de_enunciados                = []
    lista_de_elementos_de_columnas     = []
    lista_de_longitudes_maximas        = []
    for enunciado,elementos_de_columna in diccionario.items():
        lista_de_enunciados.append(str(enunciado))
        if len(elementos_de_columna) == 0:
            elementos_de_columna.append('')
        # para evitar errores en caso se que una de las listas este vacia, le agregamos
        # una cadena vacia, surtiendo el mismo efecto pero sin errores
        elementos_de_columna = [str(elemento) for elemento in elementos_de_columna]
        lista_de_elementos_de_columnas.append(elementos_de_columna)
        longitud_maxima_de_columna = len(max(elementos_de_columna))
        lista_de_longitudes_maximas.append(longitud_maxima_de_columna if longitud_maxima_de_columna > len(enunciado) else len(enunciado))
    columnas = [ColumnaFormal(i[0], i[1], i[2]) for i in zip(lista_de_enunciados,lista_de_elementos_de_columnas, lista_de_longitudes_maximas )]
    longitud_de_columna_mas_larga = len(max(lista_de_elementos_de_columnas))
    elemento_a_imprimir = None
    # le sumamos 1 por el enunciado
    for fila in range(longitud_de_columna_mas_larga+1):
        imprimir_linea(columnas)
        for columna in columnas:
            print(carcater_de_division_vertical,end='')
            print(' ', end='')
            try:
                if fila == 0:
                    elemento_a_imprimir = columna.enunciado
                else:
                    elemento_a_imprimir = columna.elementos[fila-1]
                print(elemento_a_imprimir,end='')
                cantidad_de_espacios_restantes = columna.longitud_maxima - len(elemento_a_imprimir)
            except IndexError:
                cantidad_de_espacios_restantes = columna.longitud_maxima 
            finally:
                for espacio in range(cantidad_de_espacios_restantes+1):
                    print(' ', end='')
                print(' ', end='')
                print(carcater_de_division_vertical,end='')
        print()
    imprimir_linea(columnas)
