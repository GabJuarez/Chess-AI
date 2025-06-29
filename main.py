import pygame
import graphics
import logic
import sys
import random
import chess


def main():
    pygame.init()
    ANCHO_TABLERO, ALTO_TABLERO = graphics.TAM_CASILLA * 8, graphics.TAM_CASILLA * 8
    ANCHO_VENTANA = ANCHO_TABLERO + 600
    ALTO_VENTANA = ALTO_TABLERO + 100

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
    graphics.mostrar_pantalla_inicio(pantalla)
    fondo = pygame.image.load("assets/fondoeditado.png")
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))
    pantalla.blit(fondo, (0, 0))
    pygame.display.set_caption("Ajedrez")

    #eligiendo sesgo al inicio de la partida
    color_sesgo = chess.WHITE if random.random() < 0.5 else chess.BLACK

    #cambiando el tamanio de los elementos dependiendo si la ventana esta maximizada o no
    def get_dimensiones_botones_panel():
        if maximizado:
            ancho_panel = 500
            alto_boton = 90
            ancho_boton = 300
            espacio_entre = 40
            x_botones = int(graphics.OFFSET_X * 0.5)  
        else:
            ancho_panel = 200
            alto_boton = 60
            ancho_boton = 220
            espacio_entre = 30
            x_botones = 50
        total_botones = 3
        alto_total = total_botones * alto_boton + (total_botones - 1) * espacio_entre
        y_inicio = (ALTO_VENTANA - alto_total) // 2
        return ancho_panel, ancho_boton, alto_boton, espacio_entre, y_inicio, x_botones

    def crear_botones(x_botones, y_inicio, ancho_boton, alto_boton, espacio_entre, texto_maximizar):
        boton_regresar_jugada = graphics.Button(x_botones, y_inicio, "<-", ancho_boton, alto_boton)
        boton_recomendar = graphics.Button(x_botones, y_inicio + alto_boton + espacio_entre, 'Recomendar', ancho_boton, alto_boton)
        boton_maximizar = graphics.Button(x_botones, y_inicio + 2 * (alto_boton + espacio_entre), texto_maximizar, ancho_boton, alto_boton)
        return boton_regresar_jugada, boton_recomendar, boton_maximizar

    maximizado = False
    texto_maximizar = 'Maximizar'
    ancho_panel, ancho_boton, alto_boton, espacio_entre, y_inicio, x_botones = get_dimensiones_botones_panel()
    boton_regresar_jugada, boton_recomendar, boton_maximizar = crear_botones(x_botones, y_inicio, ancho_boton, alto_boton, espacio_entre, texto_maximizar)
    
    # Inicializando la lógica del juego
    juego = logic.JuegoAjedrez()

    juego.color_sesgo = color_sesgo

    clock = pygame.time.Clock()
    corriendo = True

    # Recalcular dimensiones al inicio y tras cada cambio de tamaño
    graphics.actualizar_dimensiones(ANCHO_VENTANA, ALTO_VENTANA)

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.VIDEORESIZE:
                ANCHO_VENTANA, ALTO_VENTANA = evento.w, evento.h
                pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), pygame.RESIZABLE)
                ancho_panel, ancho_boton, alto_boton, espacio_entre, y_inicio, x_botones = get_dimensiones_botones_panel()
                graphics.actualizar_dimensiones(ANCHO_VENTANA, ALTO_VENTANA, ancho_panel=ancho_panel)
                fondo = pygame.transform.scale(pygame.image.load("assets/fondoeditado.png"), (ANCHO_VENTANA, ALTO_VENTANA))
                boton_regresar_jugada, boton_recomendar, boton_maximizar = crear_botones(x_botones, y_inicio, ancho_boton, alto_boton, espacio_entre, texto_maximizar)
            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                fila = (y - graphics.OFFSET_Y) // graphics.TAM_CASILLA
                columna = (x - graphics.OFFSET_X) // graphics.TAM_CASILLA
                if 0 <= fila < 8 and 0 <= columna < 8:
                    juego.seleccionar_casilla(fila, columna)

        # Dibujo de fondo y elementos
        pantalla.blit(fondo, (0, 0))
        graphics.actualizar_dimensiones(ANCHO_VENTANA, ALTO_VENTANA)
        graphics.dibujar_tablero(pantalla)
        graphics.cargar_imagenes()
        graphics.dibujar_piezas(pantalla, juego.tablero)

        if juego.movimiento_sugerido is not None:
            graphics.dibujar_movimiento_recomendado(pantalla, juego.movimiento_sugerido)

        graphics.dibujar_movimientos_realizados(pantalla, juego.movimientos_realizados)
        graphics.dibujar_botones_funcionalidades(pantalla, boton_regresar_jugada, juego)
        boton_recomendar.update()
        boton_recomendar.draw(pantalla)
        boton_maximizar.update()
        boton_maximizar.draw(pantalla)


        if boton_recomendar.clicked:
            mejor_movimiento = logic.recomendar_movimiento(juego)
            if mejor_movimiento:
                print(f'Mejor movimiento sugerido: {mejor_movimiento}')
                juego.movimiento_sugerido = mejor_movimiento

        # toggle maximizar/restaurar SOLO cuando se detecta el click
        if boton_maximizar.clicked:
            maximizado = not maximizado
            texto_maximizar = 'Restaurar' if maximizado else 'Maximizar'
            if maximizado:
                pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            else:
                pantalla = pygame.display.set_mode((ANCHO_TABLERO + 600, ALTO_TABLERO + 100), pygame.RESIZABLE)
            ANCHO_VENTANA, ALTO_VENTANA = pantalla.get_size()
            ancho_panel, ancho_boton, alto_boton, espacio_entre, y_inicio, x_botones = get_dimensiones_botones_panel()
            graphics.actualizar_dimensiones(ANCHO_VENTANA, ALTO_VENTANA, ancho_panel=ancho_panel)
            fondo = pygame.transform.scale(pygame.image.load("assets/fondoeditado.png"), (ANCHO_VENTANA, ALTO_VENTANA))
            boton_regresar_jugada, boton_recomendar, boton_maximizar = crear_botones(x_botones, y_inicio, ancho_boton, alto_boton, espacio_entre, texto_maximizar)

        if juego.casilla_origen is not None:
            graphics.dibujar_movimientos_legales(pantalla, juego.movimientos_legales)

        # estados de partida
        if juego.tablero.is_checkmate():
            print("Jaque mate!")
            corriendo = False
        elif juego.tablero.is_check():
            print("Jaque!")
        elif juego.tablero.is_stalemate():
            print("Empate!")
            corriendo = False
        elif juego.tablero.is_repetition():
            print("Empate por repetición!")
            corriendo = False
        elif juego.tablero.is_insufficient_material():
            print("Empate por material insuficiente!")
            corriendo = False
        elif juego.tablero.is_seventyfive_moves():
            print("Empate por 75 movimientos!")
            corriendo = False
        elif juego.tablero.is_variant_draw():
            print("Empate por variante!")
            corriendo = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
