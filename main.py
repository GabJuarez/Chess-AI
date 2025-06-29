import pygame
import graphics
import logic
import sys

def main():
    pygame.init()
    ANCHO_TABLERO, ALTO_TABLERO = graphics.TAM_CASILLA * 8, graphics.TAM_CASILLA * 8
    # espacio extra para agregar más funcionalidades
    ANCHO_VENTANA = ANCHO_TABLERO + 600
    ALTO_VENTANA = ALTO_TABLERO + 100

    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    graphics.mostrar_pantalla_inicio(pantalla)
    fondo = pygame.image.load("assets/fondojuego.png")
    fondo = pygame.transform.scale(fondo, (ANCHO_VENTANA, ALTO_VENTANA))  # CORREGIDO: se debe reasignar
    pantalla.blit(fondo, (0, 0))
    pygame.display.set_caption("Ajedrez")

    # botón deshacer
    boton_regresar_jugada = graphics.Button(50, 425 + graphics.OFFSET_Y, "<-", 200, 50)
    # botón recomendar
    boton_recomendar = graphics.Button(50, 300 + graphics.OFFSET_Y, 'Recomendar', 200, 50)
    
    # Inicializando la lógica del juego
    juego = logic.JuegoAjedrez()

    clock = pygame.time.Clock()
    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                fila = (y - graphics.OFFSET_Y) // graphics.TAM_CASILLA
                columna = (x - graphics.OFFSET_X) // graphics.TAM_CASILLA
                if 0 <= fila < 8 and 0 <= columna < 8:
                    juego.seleccionar_casilla(fila, columna)

        graphics.dibujar_tablero(pantalla)
        graphics.cargar_imagenes()
        graphics.dibujar_piezas(pantalla, juego.tablero)

        if juego.movimiento_sugerido is not None:
            graphics.dibujar_movimiento_recomendado(pantalla, juego.movimiento_sugerido)

        graphics.dibujar_movimientos_realizados(pantalla, juego.movimientos_realizados)
        graphics.dibujar_botones_funcionalidades(pantalla, boton_regresar_jugada, juego)
        
        boton_recomendar.update()
        boton_recomendar.draw(pantalla)

        if boton_recomendar.clicked:
            mejor_movimiento = logic.recomendar_movimiento(juego)
            if mejor_movimiento:
                print(f'Mejor movimiento sugerido: {mejor_movimiento}')
                juego.movimiento_sugerido = mejor_movimiento

        # si hay una casilla seleccionada se dibujan los movimientos legales 
        if juego.casilla_origen is not None:
            graphics.dibujar_movimientos_legales(pantalla, juego.movimientos_legales)

        # Estados de partida
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
