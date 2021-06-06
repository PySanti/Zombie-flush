#!/usr/bin/python3
# -*- encoding : utf-8 -*-


#todo: mejorar la administracion de varios enemigos (realizacion de diccionario)
#todo : refactorizar final, optimizar finalmente 
#todo : limpieza de funciones
#todo : adicion de docs y annot + hacer el codigo mas modificable 
#todo : probar finalmente, repasar, y copiar cosas desconocidas anteriormente
#todo : subirlo a github y hacerlo facilmente portable(agregar un tag, descargar modulos si es necesario)


try:
    from ideas  import print_menu
    from os     import system as terminal
    from time   import time
    from random import randint
    from getch  import getch
    from pygame import mixer
    from sys    import exc_info as errores

except:
    print("""
        Hubo un error al importar dependencias ... 
        Revise si tiene instaladas todas las dependencias necesarias :  
        - time
        - os
        - random
        - getch
        - ideas
        - pygame
        - sys 
        En caso de que requiera descargar algunos paquetes, ponga en su terminal
        pip install <paquete>
        """)
    quit()

#!----------------------------------------------------------------------------------------------------------------------------------------------------------
#!                                                               VARIABLES GLOBALES
#!----------------------------------------------------------------------------------------------------------------------------------------------------------

#// VARIABLES GLOBALES NO MODIFICABLES (POSIBLEMENTE)
enemigos_habilitados                                                 = True
tutorial_activo                                                      = False
limite_x                                                             = 180
limite_y                                                             = 40 
puntuacion_para_eliminacion_de_enemigo_mayor                         = 300
velocidad_de_movimiento_en_ordenadas                                 = 3    
velocidad_de_movimiento_en_abscisas                                  = velocidad_de_movimiento_en_ordenadas*2
contador_inicial_para_generacion_de_enemigos                         = 10
controles_para_movimiento_neutral                                    = { 
                                                                's' : 'abajo', 
                                                                'd' : 'derecha', 
                                                                'w' : 'arriba', 
                                                                'a' : 'izquierda'
                                                                }
controles_para_disparo                                               = { 
                                                                ';' : 'derecha', 
                                                                'k' : 'izquierda', 
                                                                'o' : 'arriba', 
                                                                'l' :'abajo' 
                                                                }
controles_para_modificacion_de_volumen                               = {
                                                                '[' : 'mas bajo',                                                                    
                                                                ']' : 'mas alto',
                                                                '\\' : 'volver'
                                                                }
tecla_para_empezar_partida                                           = 't'
tecla_de_pausa                                                       = ' '
inf                                                                  = 1_000_000

#// VARIABLES GLOBALES  MODIFICABLES
cantidad_inicial_de_balas                                            = 15
cantidad_de_balas_por_paquete                                        = 15
cantidad_maxima_de_eliminaciones_para_generacion_de_paquetes         = 20
cantidad_maxima_de_eliminaciones_para_generacion_de_enemigos_mayores = 50
cantidad_maxima_de_enemigos                                          = 5
volumen_actual                                                       = 0.5
puntuacion_para_paso_a_segunda_ronda                                 = 999
puntuacion_para_paso_a_tercera_ronda                                 = 5000
caracter_de_frecuencia_para_volumen                                  = '-'
caracter_de_frecuencia_actual                                        = '||'
forma_de_puntuacion                                                  = '🎯'
forma_de_enemigo                                                     = '🧟'
forma_de_enemigo_mayor                                               = '🧛' 
forma_de_enemigo_mayor_eliminado                                     = '🍀'   
forma_de_bala                                                        = '💥'
forma_de_enemigo_eliminado                                           = '🩸'
forma_de_paquete_de_municion                                         = '🎁'
forma_neutro                                                         =  '😐'
formas_de_disparo                                                    = {
                                                                'derecha'   :'👉',
                                                                'izquierda' :'👈',
                                                                'arriba'    :'☝️ ',
                                                                'abajo'     :'👇'}
formas_de_ataque_para_sin_balas                                      = {

        }




#!----------------------------------------------------------------------------------------------------------------------------------------------------------
#!                                                                  CLASES
#!----------------------------------------------------------------------------------------------------------------------------------------------------------


class enemigos:
    """
    Clase creada para la administracion de los enemigos
    """
    def __init__(self,
        contador_inicial_para_generacion_de_enemigos : int) -> None:
        self.forma_de_enemigo_normal_eliminado                                     = forma_de_enemigo_eliminado
        self.forma_de_enemigo_mayor_eliminado                                      = forma_de_enemigo_mayor_eliminado
        self.forma_de_enemigo_normal                                               = forma_de_enemigo
        self.forma_enemigo_mayor                                                   = forma_de_enemigo_mayor       

        self.contador_para_generacion_de_enemigos                                 = contador_inicial_para_generacion_de_enemigos
        self.click_despues_de_la_generacion_de_ultimos_enemigos                    = time() # contador incial para la generacion de enemigos normales
        self.diccionario_de_posiciones_enemigos                                               = {
                                                                                'normales'      : [],
                                                                                'mayores'       : []
                }
        self.cantidad_de_enemigos_eliminados                                       = 0
        self.cantidad_de_eliminaciones_necesarias_para_generacion_de_enemigo_mayor  = randint(1,cantidad_maxima_de_eliminaciones_para_generacion_de_enemigos_mayores)
    def es_tiempo_de_enemigos_normales(self) -> bool:
        """
        Devuelve True en caso de que se deba generar enemigos normales
        """
        t1 = self.click_despues_de_la_generacion_de_ultimos_enemigos
        t2 = time()
        if (t2 - t1) >= self.contador_para_generacion_de_enemigos:
            self.click_despues_de_la_generacion_de_ultimos_enemigos = time()
            return True
        else:
            return False
    def es_tiempo_de_enemigos_mayores(self) -> bool:
        """
        Retorna True en caso de que se deban generar enemigos mayores
        """
        return (self.cantidad_de_eliminaciones_necesarias_para_generacion_de_enemigo_mayor  <= 0)
    def efecto_zombie_normal_generado(self):
        reproducir_efecto(4)
    def efecto_zombie_mayor_generado(self):
        reproducir_efecto(8)

    def generar_enemigo_mayor(self):
        '''
        Genera un enemigo mayor 
        '''
        self.diccionario_de_posiciones_enemigos['mayores'].append((randint(1,limite_x-1), randint(1,limite_y-1)))
        self.efecto_zombie_mayor_generado()
    def generar_enemigo_normal(self) -> None:
        '''
        Genera un enemigo normal
        '''
        self.diccionario_de_posiciones_enemigos['normales'].append((randint(1,limite_x-1), randint(1,limite_y-1)))
        self.efecto_zombie_normal_generado()

    def actualizar_contador_para_generacion_de_enemigos_normales(self,
                                                                puntuacion : int) -> None:
        """
        Actualiza el contador de tiempo para la generacion de 
        enemigos en funcion de la puntuacion del personaje
        """
        if   puntuacion <= puntuacion_para_paso_a_segunda_ronda:
            # generacion de enemigos en primera ronda
            self.contador_para_generacion_de_enemigos = randint(1,5)
        elif puntuacion_para_paso_a_segunda_ronda <= puntuacion <= puntuacion_para_paso_a_tercera_ronda:
            # generacion de enemigos en segunda ronda
            self.contador_para_generacion_de_enemigos = randint(1,3)
        elif puntuacion > puntuacion_para_paso_a_tercera_ronda:
            # generacion de enemigos en tercera ronda
            self.contador_para_generacion_de_enemigos = 1
    def actualizar_contador_para_generacion_de_enemigos_mayores(self, 
                                                                cantidad_de_elminaciones : int):
        self.cantidad_de_eliminaciones_necesarias_para_generacion_de_enemigo_mayor = randint(1,cantidad_maxima_de_eliminaciones_para_generacion_de_enemigos_mayores)
    def cantidad_de_enemigos(self) -> int:
        """
        Retorna la longitud de la lista de posiciones de los enemigos 
        """
        # se recorre de este modo la lista por la 
        # posibilidad de encontrar a un enemigo muerto
        return len([i for i in self.diccionario_de_posiciones_enemigos['normales'] if isinstance(i, tuple)])+len([i for i in self.diccionario_de_posiciones_enemigos['mayores'] if isinstance(i, tuple)])
class bala:
    """
    Clase creada para la administracion de la 
    bala y de los paquetes
    """
    def __init__(self) -> None:
        self.x, self.y                                                    = None,None # posicion de la bala
        self.forma                                                        = forma_de_bala
        self.cantidad_de_balas                                            = cantidad_inicial_de_balas
        self.paquete_de_municiones_forma                                  = forma_de_paquete_de_municion
        self.cantidad_maxima_de_eliminaciones_para_generacion_de_paquetes = cantidad_maxima_de_eliminaciones_para_generacion_de_paquetes
        self.cantidad_eliminaciones_para_municion                         = randint(1,self.cantidad_maxima_de_eliminaciones_para_generacion_de_paquetes)
        self.posiciones_de_paquetes                                       = []
    def eliminar_paquete_de_munciones(  self, 
                                        paquete_a_eliminar : tuple) -> None:
        """
        Recibe la posicion del paquete que se desea eliminar y lo elimina
        """
        self.posiciones_de_paquetes.remove(paquete_a_eliminar)
    def redefinir_cantidad_eliminaciones_para_municion(self) -> None:
        """
        Define la cantidad de eliminaciones necesarias para la siguiente generacion
        """
        self.cantidad_eliminaciones_para_municion = randint(1,self.cantidad_maxima_de_eliminaciones_para_generacion_de_paquetes)
    def generar_paquete_de_municiones(self) -> None:
        """
        Agrega un paquete nuevo a la lista de posiciones de paquetes
        """
        self.posiciones_de_paquetes.append(    (randint(1,limite_x), randint(1,limite_y) )   )
        if len( self.posiciones_de_paquetes) > 3:                    
            # se elimina el primer paquete de la lista cuando hay 4 para evitar abundancia de los mismos y ademas agregar dificultad 
            self.posiciones_de_paquetes.pop(0)
    def desaparecer_bala(self) -> None:
        """
        Sobreescribe la posicion de la 
        bala para que desaparezca
        """
        self.posicion_actual = (None, None)
    def efecto_recargar_balas(self):
        reproducir_efecto(7)
    def recargar_balas(self) -> None:
        """
        Aumenta la cantidad de balas una vez que se toma el paquete
        """
        self.cantidad_de_balas += cantidad_de_balas_por_paquete
        self.efecto_recargar_balas()
    def se_requiere_generar_paquete_de_munciones(self) -> bool:
        """
        Retorna true en caso de que la cantidad_de_eliminaciones_para_muncion
        sea igual a 0
        """
        if  self.cantidad_eliminaciones_para_municion <= 0:
            return True
        else:
            return False
    def cantidad_de_paquetes(self) -> int:
        '''
        Retorna la cantidad de paquetes 
        '''
        return len(self.posiciones_de_paquetes)
    @property
    def posicion_actual(self) -> tuple:
        """
        Retorna la posicion de la bala en fornma de tupla
        """
        return (self.x,self.y) 
    @posicion_actual.setter
    def posicion_actual(self, nueva_posicion) -> None:
        self.x,self.y = nueva_posicion
    @posicion_actual.deleter
    def posicion_actual(self):
        del self.x, self.y
class personaje:
    """
    Clase creada para la 
    administracion de los personajes
    """
    def __init__(   self, 
                    x : int,
                    y : int) -> None:
        self.pistola_arriba         = formas_de_disparo['arriba']
        self.pistola_izquierda      = formas_de_disparo['izquierda']
        self.pistola_abajo          = formas_de_disparo['abajo']
        self.pistola_derecha        = formas_de_disparo['derecha']
        self.posicion_de_arma       =  (None,None) 
        self.forma_neutro           = forma_neutro
        self.puntuacion             = 0
        self.x                      = x
        self.y                      = y 
        self.orientacion_de_disparo = None
    def efecto_disparo(self):
        reproducir_efecto(2)
    def __eliminar_enemigo( self,
                            indice_de_enemigo_a_eliminar : int, 
                            enemigos_1                   : enemigos,
                            tipo_de_enemigo              : str) -> None:
        """
        Recibe el indice del enemigo que se desea 
        eliminar y lo elimina de la lista ,
        en caso de que el tipo de enemigo sea 1,
        se tratara de un enemigo normal, en caso contrario
        se tratara de un enemigo mayor
        """
        if tipo_de_enemigo == 'normal':
            enemigos_1.diccionario_de_posiciones_enemigos['normales'][indice_de_enemigo_a_eliminar] = list(enemigos_1.diccionario_de_posiciones_enemigos['normales'][indice_de_enemigo_a_eliminar])
            enemigos_1.cantidad_de_enemigos_eliminados += 1
        elif tipo_de_enemigo == 'mayor':
            enemigos_1.diccionario_de_posiciones_enemigos['mayores'][indice_de_enemigo_a_eliminar] = list(enemigos_1.diccionario_de_posiciones_enemigos['mayores'][indice_de_enemigo_a_eliminar])
            enemigos_1.cantidad_de_enemigos_eliminados += puntuacion_para_eliminacion_de_enemigo_mayor/100
    def comprobar_blancos_acertados(self,   
                                    enemigos_1             : enemigos,   
                                    bala_1                 : bala,   
                                    orientacion_de_disparo : str ):
        """
        Comprueba si se le acerto a algun blanco y 
        lo elimina en caso de haber acertado
        """
        if (enemigos_1.cantidad_de_enemigos() > 0)  :
            lista_de_ordenadas_de_enemigos         = [i[1] for i in enemigos_1.diccionario_de_posiciones_enemigos['normales']]
            lista_de_ordenadas_de_enemigos_mayores = [i[1] for i in enemigos_1.diccionario_de_posiciones_enemigos['mayores']]
            lista_de_abscisas_de_enemigos          = [i[0] for i in enemigos_1.diccionario_de_posiciones_enemigos['normales']]
            lista_de_abscisas_de_enemigos_mayores  = [i[0] for i in enemigos_1.diccionario_de_posiciones_enemigos['mayores']]
            blanco_acertado                        = None
            enemigo_mayor_acertado                 = False
            enemigo_normal_acertado                = False
            # si disparamos hacia los laterales comprobamos si hay un enemigo en un rango cercano 
            if   orientacion_de_disparo == 'derecha' or orientacion_de_disparo == 'izquierda':
                for y in range(self.y-2, self.y+3):
                    if (y in lista_de_ordenadas_de_enemigos) or (y in lista_de_ordenadas_de_enemigos_mayores):
                        if y in lista_de_ordenadas_de_enemigos:
                            enemigo_normal_acertado       = True
                            indice_de_enemigo_coincidente = lista_de_ordenadas_de_enemigos.index(y)
                            abscisa_de_enemigo            = enemigos_1.diccionario_de_posiciones_enemigos['normales'][indice_de_enemigo_coincidente][0]
                        else:
                            enemigo_mayor_acertado = True
                            indice_de_enemigo_coincidente = lista_de_ordenadas_de_enemigos_mayores.index(y)
                            abscisa_de_enemigo = enemigos_1.diccionario_de_posiciones_enemigos['mayores'][indice_de_enemigo_coincidente][0]
                        if (orientacion_de_disparo == 'derecha' and abscisa_de_enemigo > self.x) or (orientacion_de_disparo == 'izquierda' and abscisa_de_enemigo < self.x) :
                            blanco_acertado = True
                        else:
                            blanco_acertado = False
                        break
            elif orientacion_de_disparo == 'arriba' or orientacion_de_disparo == 'abajo':
                for x in range(self.x-3, self.x+4):
                    if (x in lista_de_abscisas_de_enemigos) or (x in lista_de_abscisas_de_enemigos_mayores):
                        if x in lista_de_abscisas_de_enemigos:
                            enemigo_normal_acertado = True
                            indice_de_enemigo_coincidente = lista_de_abscisas_de_enemigos.index(x)
                            ordenada_de_enemigo = enemigos_1.diccionario_de_posiciones_enemigos['normales'][indice_de_enemigo_coincidente][1]
                        else:
                            enemigo_mayor_acertado = True
                            indice_de_enemigo_coincidente = lista_de_abscisas_de_enemigos_mayores.index(x)
                            ordenada_de_enemigo = enemigos_1.diccionario_de_posiciones_enemigos['mayores'][indice_de_enemigo_coincidente][1]
                        if (orientacion_de_disparo == 'arriba' and ordenada_de_enemigo < self.y) or (orientacion_de_disparo == 'abajo'  and ordenada_de_enemigo > self.y) :
                            blanco_acertado = True
                        else:
                            blanco_acertado = False
                        break
            if blanco_acertado:
                suma_de_puntuacion = None
                if enemigo_mayor_acertado:
                    suma_de_puntuacion = puntuacion_para_eliminacion_de_enemigo_mayor
                elif enemigo_normal_acertado:
                    suma_de_puntuacion = 100
                self.__eliminar_enemigo(indice_de_enemigo_coincidente, enemigos_1, 'mayor' if suma_de_puntuacion == puntuacion_para_eliminacion_de_enemigo_mayor else 'normal' )
                self.puntuacion += suma_de_puntuacion
                bala_1.desaparecer_bala()
                bala_1.cantidad_eliminaciones_para_municion -= suma_de_puntuacion//100
                enemigos_1.cantidad_de_eliminaciones_necesarias_para_generacion_de_enemigo_mayor -= 1
                if bala_1.se_requiere_generar_paquete_de_munciones():
                    bala_1.generar_paquete_de_municiones()
                    bala_1.redefinir_cantidad_eliminaciones_para_municion()
    def disparar(   self, 
                    orientacion : str, 
                    bala_1      : bala, 
                    enemigos_1  : enemigos ) -> None:
        """
        Define la posicion de la bala 
        y la forma del personaje dependiendo 
        de la orientacion del disparo
        """
        if bala_1.cantidad_de_balas == 0:
            pass
        else:
            if not tutorial_activo:
                bala_1.cantidad_de_balas-=1
            self.efecto_disparo()
            self.orientacion_de_disparo = orientacion
            if   orientacion == 'derecha':
                if self.x+1 >= limite_x:
                    self.x -= 3
                self.posicion_de_arma = (self.x+1, self.y)
                bala_1.posicion_actual = (limite_x , self.y)
            elif orientacion  == 'izquierda':
                if self.x - 1 <= 0:
                    self.x += 3
                self.posicion_de_arma = (self.x - 1, self.y)
                bala_1.posicion_actual = (0, self.y)
            elif orientacion == 'arriba':
                if self.y - 1 <= 0:
                    self.y += 3
                self.posicion_de_arma = (self.x, self.y-1)
                bala_1.posicion_actual  = (self.x, 0)
            elif orientacion == 'abajo':
                if self.y +1 >= limite_y:
                    self.y -= 3
                self.posicion_de_arma = self.x,self.y + 1
                bala_1.posicion_actual = (self.x, limite_y)
            if enemigos_habilitados:
                self.comprobar_blancos_acertados(enemigos_1 = enemigos_1, bala_1 = bala_1, orientacion_de_disparo = orientacion)
    def mover(  self, 
                orientacion : str,
                cantidad    = None) -> None: 
        """
        Mueve el personaje  hacia la orientacion que se le indica,
        en base a eso, determina la cantidad de veces que se mueve 
        el personje en caso de que cantidad no se especifique 
        """
        if cantidad == None:
            cantidad = velocidad_de_movimiento_en_abscisas if orientacion == 'derecha' or orientacion == 'izquierda' else velocidad_de_movimiento_en_ordenadas
        self.posicion_de_arma = (None,None)
        self.orientacion_de_disparo = None
        if orientacion == 'arriba':
            nueva_ordenada = self.y - cantidad 
            self.y =   nueva_ordenada  if nueva_ordenada >= 0 else  0
        elif orientacion == 'abajo':
            nueva_ordenada = self.y + cantidad 
            self.y =  nueva_ordenada if nueva_ordenada <= limite_y else limite_y  
        elif orientacion == 'derecha':
            nueva_abscisa = self.x + cantidad 
            self.x = nueva_abscisa if nueva_abscisa <= limite_x else limite_x
        elif orientacion == 'izquierda':
            nueva_abscisa = self.x - cantidad 
            self.x = nueva_abscisa if nueva_abscisa > 0 else 0
    def esta_disparando(self) -> bool:
        """
        Retorna True en caso de que el personaje este disparando
        """
        return self.posicion_de_arma != (None,None)
    @property
    def posicion_actual(self):
        """
        Devuelve una tupla con la posicion del personaje en el momento
        """
        return (self.x, self.y)
    @posicion_actual.setter
    def posicion_actual(self, 
                        nueva_posicion : int):
        self.x,self.y = nueva_posicion
    @posicion_actual.deleter
    def posicion_actual(self):
        del self.x, self.y
    def personaje_posicionado_en_limite_y_se_quiere_mover_mas_alla_de_el(   self, 
                                                                            tecla_de_entrada : str) -> bool:
        """
        Funcion creada con fines de optimizacion, retorna True si el 
        jugador se quiere mover mas alla de un limite
        """
        global controles_para_movimiento_neutral
        if self.y   == 0 and controles_para_movimiento_neutral[tecla_de_entrada]        == 'arriba' :
            return True
        elif self.y == limite_y and controles_para_movimiento_neutral[tecla_de_entrada] == 'abajo':
            return True
        elif self.x == limite_x and controles_para_movimiento_neutral[tecla_de_entrada] == 'derecha':
            return True
        elif self.x == 0 and  controles_para_movimiento_neutral[tecla_de_entrada]       == 'izquierda':
            return True
        else:
            return False




#!----------------------------------------------------------------------------------------------------------------------------------------------------------
#!                                                               FUNCIONES
#!----------------------------------------------------------------------------------------------------------------------------------------------------------

#// MANUALES
def manual_de_tutorial() -> None:
    """
    Similiar a 'status_de_partida' solo que se 
    ejecuta unicamente cuando el tutorial esta inactivo
    """
    print(" Movimientos neutrales ... ", end='') 
    for tecla, direccion in controles_para_movimiento_neutral.items():
        print(f" {direccion.capitalize()} : '{tecla}' ", end=' , ')
    print(f'Si hay mas de {cantidad_maxima_de_enemigos} zombies vivos pierdes, matalos a todos !!')
    print(' Disparos              ... ',end='')
    for tecla,direccion in controles_para_disparo.items():
        print(f" {direccion.capitalize()} : '{tecla}' ", end=' , ')
    print(f"Pausar : '{'space' if tecla_de_pausa == ' ' else tecla_de_pausa}', Empezar : '{tecla_para_empezar_partida}'")
def manual_de_control_de_volumen(volumen):
    salto_de_linea(4)
    for tecla, accion in controles_para_modificacion_de_volumen.items():
        salto_de_linea()
        tab(3)
        print(f"{accion.capitalize()} : '{tecla}'")
    salto_de_linea()
    tab(3)
    print(f'Volumen   : {volumen}')

#// MENUS
def menu_de_seleccion_de_dificultad():
    global cantidad_inicial_de_balas, cantidad_de_balas_por_paquete,cantidad_maxima_de_eliminaciones_para_generacion_de_paquetes 
    global cantidad_maxima_de_enemigos, puntuacion_para_paso_a_segunda_ronda ,puntuacion_para_paso_a_tercera_ronda     
    menu = ['Facil', 'Medio', 'Rompe culos']
    eleccion = print_menu(menu, mensaje = 'Selecciona la dificultad ...')
    if eleccion == 1:
        cantidad_inicial_de_balas                                    = 30
        cantidad_de_balas_por_paquete                                = 10
        cantidad_maxima_de_eliminaciones_para_generacion_de_paquetes = 10
        cantidad_maxima_de_enemigos                                  = 10
        puntuacion_para_paso_a_segunda_ronda                         = 3000
        puntuacion_para_paso_a_tercera_ronda                         = 7000
    elif eleccion == 2:
        pass
    elif eleccion == 3:
        cantidad_de_balas_por_paquete                                = 15
        cantidad_maxima_de_enemigos                                  = 5
        puntuacion_para_paso_a_segunda_ronda                         = 1000
        puntuacion_para_paso_a_tercera_ronda                         = 2000
    reproducir_efecto(3)
def menu_de_seleccion_de_formas():
    global forma_neutro
    lista_de_formas = {
        1  : '🕵️ ',
        2  : '👨',
        3  : '👩',
        4  : '💩',
        5  : '🤡',
        6  : '🧞',
        7  : '⛸ ',
        8  : '🤹',
    }
    menu = [i[1] for i in lista_de_formas.items()]
    eleccion = print_menu(menu, mensaje = 'Selecciona a tu personaje ...')
    reproducir_efecto(3)
    forma_neutro = lista_de_formas[eleccion]
def menu_de_pausa():
    '''
    Menu de accion en caso de quue el jugador pulse la tecla de pausa ...

    Nota: recibe a los elementos para el caso en 
    el que el jugador quiera volver a empezar
    '''
    while True:
        terminal('clear')
        menu = ['Continuar', 'Configurar Volumen', 'Salir']
        eleccion = print_menu(menu, indice_de_comienzo = 0)
        if eleccion == 1 or eleccion == 2:
            reproducir_efecto(3)
            if eleccion == 1:
                break
            else:
                menu_de_configuracion_de_volumen()
        elif eleccion == 3:
            terminal('clear')
            quit()
def menu_de_derrota():
    global tutorial_activo
    terminal('clear')
    salto_de_linea(10)
    tab(6)
    print('👎 Has sido derrotad@, pulsa enter para continuar 👎')
    reproducir_efecto(6)
    while True:
        tecla_entrada,_ = getch()
        if tecla_entrada == '\n':
            reproducir_efecto(3)
            break
    menu = ['Volver a jugar','Ir al tutorial', 'Salir']
    eleccion = print_menu(menu)
    if eleccion != 3:
        reproducir_efecto(3)
        if eleccion == 2:
            tutorial_activo = True
    else:
        terminal('clear')
        quit() 
def menu_de_inicio():
    """
    Imprime por pantalla el menu de inicio
    """
    global tutorial_activo
    terminal('clear')
    salto_de_linea(10)
    tab(5)
    print('                     🧟  Bienvenido, pulsa enter para empezar  🧟     ')
    intro = reproducir_efecto(1, loops=inf)
    while True:
        tecla_de_entrada,_ = getch()
        if tecla_de_entrada == '\n':
            # en este caso, la funcion 'reproducir_cancion no habra retornado None'
            if volumen_actual != 0:
                intro.stop()
            reproducir_efecto(3)
            break
    menu_de_seleccion_de_formas()
    menu_de_seleccion_de_dificultad()
    menu = ['Tutorial (recomendado para noobs)', 'Empezar la partida', 'Salir']
    eleccion = print_menu(menu)
    if eleccion == 3:
        terminal('clear')
        quit()
    else:
        reproducir_efecto(3)
        tutorial_activo = True if eleccion == 1 else False
def menu_de_configuracion_de_volumen():
    global volumen_actual, caracter_de_frecuencia_para_volumen, caracter_de_frecuencia_actual
    def imprimir_calibrador_de_volumen():
        nonlocal iterador
        iterador = 0
        terminal('clear')
        manual_de_control_de_volumen(frecuencia_actual)
        salto_de_linea(4)
        tab(9)
        for frecuencia in frecuencias_de_volumen:
            print(frecuencia,end='')
            if  iterador == frecuencia_actual:
                print(caracter_de_frecuencia_actual,end='')
            iterador += 1
        print(frecuencia)
    frecuencias_de_volumen =  [caracter_de_frecuencia_para_volumen for i in range(11)]
    frecuencia_actual = int(volumen_actual*10)
    cancion_intro = reproducir_efecto(1, loops = inf)
    while True:
        imprimir_calibrador_de_volumen()
        entrada,_ = getch()
        iterador = 0
        if entrada in controles_para_modificacion_de_volumen:
            if (controles_para_modificacion_de_volumen[entrada] == 'mas alto') and (not frecuencia_actual + 1 > len(frecuencias_de_volumen)-1):
                frecuencia_actual+= 1  
                volumen_actual   += 0.1
                cancion_intro.set_volume(volumen_actual)
            elif (controles_para_modificacion_de_volumen[entrada] == 'mas bajo') and (not frecuencia_actual - 1 < 0):
                frecuencia_actual-= 1
                volumen_actual   -= 0.1
                cancion_intro.set_volume(volumen_actual)
            elif controles_para_modificacion_de_volumen[entrada] == 'volver':
                if volumen_actual != 0:
                    # en este caso, la funcion 'reproducir_efecto' no habra retornado None
                    cancion_intro.stop()
                reproducir_efecto(3)
                break







#// FUNCIONES LARGAS
def comprobar_superposicion(personaje_1                     : personaje,
                            bala_1                          : bala,
                            lista_de_posiciones_de_enemigos : list,
                            enemigos_1                      : enemigos):
    """
    Comprueba superposicion entre los elementos y actua en respuesta 
    """
    orientacion_de_movimiento = None
    orientacion_de_disparo    = None
    # comprobamos superposicion con paquetes
    for y in range(personaje_1.y-3, personaje_1.y+3):
        for x in range(personaje_1.x-3, personaje_1.x+3):
            if (x,y) in bala_1.posiciones_de_paquetes:
                bala_1.recargar_balas()
                bala_1.efecto_recargar_balas()
                bala_1.eliminar_paquete_de_munciones((x,y))
                break
    # No comprobamos superposicion con balas ya que es imposible que se superponga con algo
    # comprobamos superposicion con enemigos de todo tipo
    if enemigos_habilitados and enemigos_1.cantidad_de_enemigos() > 0:
        while True:
            if personaje_1.posicion_actual in lista_de_posiciones_de_enemigos :
                personaje_1.mover(cantidad = 1, orientacion = orientacion_de_disparo)
                if personaje_1.esta_disparando:
                    personaje_1.disparar(orientacion = orientacion_de_disparo, bala_1 = bala_1, enemigos_1 = enemigos_1)
            else:
                break
def imprimir(personaje_1: personaje, 
            bala_1      : bala, 
            enemigos_1  : enemigos):
    """
    Imprime los elementos en pantalla (enemigos, personajes, balas) ...
    """
    terminal('clear')
    for y in range(limite_y + 1):
        for x in range(limite_x+1):
            if   (x,y) == personaje_1.posicion_actual :
                print(personaje_1.forma_neutro, end='')
            elif (x,y) == bala_1.posicion_actual:
                print(bala_1.forma, end='')
            elif (x,y) in enemigos_1.diccionario_de_posiciones_enemigos['normales']  and enemigos_habilitados:
                print(enemigos_1.forma_de_enemigo_normal,end='')
            # en caso de que la posicion del enemigo este en una lista, querra decir que esta eliminado
            elif [x,y] in enemigos_1.diccionario_de_posiciones_enemigos['normales'] :
                print(enemigos_1.forma_de_enemigo_normal_eliminado, end='')
                enemigos_1.diccionario_de_posiciones_enemigos['normales'].remove([x,y])
            elif (x,y) in bala_1.posiciones_de_paquetes:
                print(bala_1.paquete_de_municiones_forma, end='')  
            elif (x,y) == personaje_1.posicion_de_arma:
                print(formas_de_disparo[personaje_1.orientacion_de_disparo], end='')
            elif (x,y) in enemigos_1.diccionario_de_posiciones_enemigos['mayores']:
                print(enemigos_1.forma_enemigo_mayor,end = '')
            elif [x,y] in enemigos_1.diccionario_de_posiciones_enemigos['mayores']:
                print(enemigos_1.forma_de_enemigo_mayor_eliminado, end  = '')
                enemigos_1.diccionario_de_posiciones_enemigos['mayores'].remove([x,y])
            else:
                print(' ', end='')
        print()
    if tutorial_activo:
        manual_de_tutorial()
    else:
        status_de_partida(personaje_1, enemigos_1, bala_1)
def accionar_teclas(tecla_de_entrada          : str,
                    personaje_1               : personaje,
                    bala_1                    : bala,
                    enemigos_1                : enemigos) -> None:
    """
    Recibe la tecla pulsada y actua en respuesta
    """
    global tutorial_activo, enemigos_habilitados
    if tutorial_activo:
        enemigos_habilitados = False
    else:
        enemigos_habilitados = True
    if tecla_de_entrada in controles_para_movimiento_neutral:
        bala_1.desaparecer_bala()
        personaje_1.mover(orientacion = controles_para_movimiento_neutral[tecla_de_entrada])
    elif  tecla_de_entrada in controles_para_disparo:
        personaje_1.disparar(orientacion = controles_para_disparo[tecla_de_entrada], bala_1 = bala_1, enemigos_1 = enemigos_1)
    elif tecla_de_entrada == tecla_para_empezar_partida and tutorial_activo:
        reproducir_efecto(3)
        tutorial_activo = False
        enemigos_habilitados = True
def main():
    global getch, velocidad_de_movimiento_en_ordenadas, velocidad_de_movimiento_en_abscisas
    # decoramos 'getch' para que retorne la cantidad de tiempo en intervalos de pulsaciones de teclas
    getch = contador_de_input(getch)
    menu_de_inicio()
    personaje_1 = personaje(limite_x//2, limite_y//2)
    bala_1      = bala()
    enemigos_1  = enemigos(contador_inicial_para_generacion_de_enemigos = contador_inicial_para_generacion_de_enemigos)
    # para la primera iteracion
    imprimir(personaje_1, bala_1,enemigos_1)


    while True:
        tecla_de_entrada, tiempo_de_accion_de_tecla = getch()
        if (tecla_de_entrada == tecla_de_pausa):
            reproducir_efecto(3)
            menu_de_pausa()
            # primera iteracion posterior al menu de pausa
            imprimir(personaje_1, bala_1, enemigos_1)  
        elif (enemigos_1.cantidad_de_enemigos() > cantidad_maxima_de_enemigos) or (enemigos_1.cantidad_de_enemigos() > 0 and bala_1.cantidad_de_balas == 0 and bala_1.cantidad_de_paquetes == 0):
            menu_de_derrota()
            # si el jugador sale de la camara de derrota, quiere decir que quiere volver a jugar 
            personaje_1 = personaje(limite_x//2, limite_y//2)
            bala_1 = bala()
            enemigos_1 = enemigos(contador_inicial_para_generacion_de_enemigos)
            # asi que sobreescribimos los punteros
            imprimir(personaje_1, bala_1,enemigos_1)
            # e imprimimos para una nueva iteracion
        elif (tecla_de_entrada in controles_para_movimiento_neutral) or (tecla_de_entrada in controles_para_disparo) or (tecla_de_entrada == tecla_para_empezar_partida):
            if (tecla_de_entrada in controles_para_movimiento_neutral) and (personaje_1.personaje_posicionado_en_limite_y_se_quiere_mover_mas_alla_de_el(tecla_de_entrada)):
                continue
            else:
                # en caso de que el jugador deje la tecla presionada para moverse, aumentamos la velocidad para optimizar
                if tiempo_de_accion_de_tecla < 0.02:
                    continue
                else:
                    accionar_teclas(tecla_de_entrada, bala_1 = bala_1, enemigos_1 = enemigos_1, personaje_1 = personaje_1)
                    if enemigos_habilitados:
                         if enemigos_1.es_tiempo_de_enemigos_normales():
                             enemigos_1.generar_enemigo_normal()
                             enemigos_1.actualizar_contador_para_generacion_de_enemigos_normales(personaje_1.puntuacion)
                         if enemigos_1.es_tiempo_de_enemigos_mayores():
                             enemigos_1.generar_enemigo_mayor()
                             enemigos_1.actualizar_contador_para_generacion_de_enemigos_mayores(enemigos_1.cantidad_de_enemigos_eliminados)
                    comprobar_superposicion(personaje_1, bala_1, enemigos_1.diccionario_de_posiciones_enemigos['normales'] + enemigos_1.diccionario_de_posiciones_enemigos['mayores'], enemigos_1)
                    imprimir(personaje_1, bala_1, enemigos_1)  

#// FUNCIONES CORTAS
def reiniciar_partida(  personaje_1: personaje,
                        bala_1     : bala,
                        enemigos_1 : enemigos):
    '''
    Sobreescribe los punteros de los elementos para empezar una nueva partida
    '''

def salto_de_linea(cantidad = 1):
    for i in range(cantidad+1):
        print()
def tab(cantidad = 1):
    for i in range(cantidad+1):
        print('\t',end='')
def contador_de_input(funcion : getch):
    """
    Decorador creado para calcular la cantidad 
    de tiempo que se tarda el jugador en introducir 
    una tecla 

    Retorna una tupla donde el primer elemento es la 
    cantidad de tiempo y el segundo la entrada
    """
    def wrapper():
        t1 = time()
        entrada = funcion().lower()
        return (entrada, time()-t1)
    return wrapper
def status_de_partida(  personaje_1 : personaje,
                        enemigos_1 : enemigos,
                        bala_1 : bala) -> str:
    """
    Mensaje que establece el status de la partida
    """
    print(f'\n{forma_de_puntuacion} : {int(personaje_1.puntuacion):6}',end='\t\t')
    print(f'{forma_de_enemigo} : {int(enemigos_1.cantidad_de_enemigos())}  ',end='\t\t')
    print(f'{forma_de_bala} : {int(bala_1.cantidad_de_balas):3} ', end='\t\t')
    print(f'{forma_de_enemigo_eliminado} : {int(enemigos_1.cantidad_de_enemigos_eliminados):3}', end='\t\t')
    print(f'{forma_de_paquete_de_municion} : {int(bala_1.cantidad_eliminaciones_para_municion):2}',end='\t\t')
    print(f'{forma_de_enemigo_mayor} : {int(enemigos_1.cantidad_de_eliminaciones_necesarias_para_generacion_de_enemigo_mayor)}')
def reproducir_efecto(cancion : 1 | 2 | 3 | 4 | 5 | 6 | 7  ,                        
                    loops = None):
    """
    Crea el objeto sound con la cancion cargada y lo devuelve

    1 : intro
    2 : disparo
    3 : seleccion
    4 : zombie vivo
    5 : zombie muerto
    6 : game over
    7 : recarga
    8 : vampiro vivo
    """
    if volumen_actual == 0:
        return None
    else:
        if cancion == 1:
            cancion = 'efectos/intro.wav'
        elif cancion == 2:
            cancion =  'efectos/disparo_2.wav'
        elif cancion == 3:
            cancion = 'efectos/seleccion_1.wav'
        elif cancion == 4:
            cancion = 'efectos/zombie_nace.wav'
        elif cancion == 5:
            cancion = 'efectos/zombie_muere.wav'
        elif cancion == 6:
            cancion = 'efectos/game_over.wav'
        elif cancion == 7:
            cancion = 'efectos/recarga_de_balas.wav'
        elif cancion == 8:
            cancion = 'efectos/vampiros_1.wav'
        mixer.init()
        mixer.music.load(cancion)
        mixer.music.set_volume(volumen_actual)
        mixer.music.play(loops if loops != None else 1)
        if loops != None:
            return mixer.music
        else:
            pass
#!------e---------------------------------------------------------------------------------------------------------------------------------------------------

#!                                                                  PROGRAMA PRINCIPAL
#!----------------------------------------------------------------------------------------------------------------------------------------------------------




# try:
main()
# except:
#     print('Hubo un error ...')
#     for error in errores():
#         print(error)
