import pygame
import chess
import graphics
import logic
import sys

pygame.init()
ANCHO, ALTO = 480, 480
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez")
graphics.mostrar_pantalla_inicio(pantalla)

#inicializando la logica
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
            casilla = chess.square(columna, 7 - fila)  # invertir fila porque chess usa 0 abajo
            juego.seleccionar_casilla(fila, columna)
            casilla_origen = juego.casilla_origen

    graphics.dibujar_tablero(pantalla)
    graphics.cargar_imagenes()
    graphics.dibujar_piezas(pantalla, juego.tablero)

#imprimiendon en consola solo para probar

    
    if juego.tablero.is_checkmate():
            print("Jaque mate!")
            ejecutando = False

    elif juego.tablero.is_check():
            print("Jaque!")

    elif juego.tablero.is_stalemate():
            print("Empate!")
            ejecutando = False

    elif juego.tablero.is_repetition():
            print("Empate por repetición!")
            ejecutando = False

    elif juego.tablero.is_insufficient_material():
            print("Empate por material insuficiente!")
            ejecutando = False

    elif juego.tablero.is_seventyfive_moves():
            print("Empate por 75 movimientos!")
            ejecutando = False

    elif juego.tablero.is_variant_draw():
            print("Empate por variante!")
            ejecutando = False

    

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
