import pygame
import chess
import graphics
import logic
import sys
import threading

pygame.init()
ANCHO, ALTO =  graphics.TAM_CASILLA * 8, graphics.TAM_CASILLA * 8
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez")
graphics.mostrar_pantalla_inicio(pantalla)

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
            columna = x // graphics.TAM_CASILLA
            fila = y // graphics.TAM_CASILLA
            juego.seleccionar_casilla(fila, columna)

    graphics.dibujar_tablero(pantalla)
    graphics.cargar_imagenes()
    graphics.dibujar_piezas(pantalla, juego.tablero)

    # si hay una casilla seleccionada se dibujan los movimientos legales 
    if juego.casilla_origen is not None:
        graphics.dibujar_movimientos_legales(pantalla, juego.movimientos_legales)

    # probando los estados de la partida por consola
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
