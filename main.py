import pygame
import chess
import graphics
import sys


pygame.init()
ANCHO, ALTO = 480, 480

pantalla = pygame.display.set_mode((ANCHO, ALTO))
graphics.mostrar_pantalla_inicio(pantalla)
graphics.iniciar_juego(pantalla)
pygame.quit()
sys.exit()
