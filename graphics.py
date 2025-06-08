import chess
import pygame

#dimensiones del tablero
ANCHO, ALTO = 480, 480
TAM_CASILLA = ANCHO // 8

#diccionario para las imagenes de las piezas
IMAGENES = {}

def cargar_imagenes():
    tipos_piezas = ['r', 'n', 'b', 'q', 'k', 'p']  # rook, (k)night, bishop, queen, king, pawn
    for tipo in tipos_piezas:
        IMAGENES['w' + tipo] = pygame.transform.scale(
            pygame.image.load(f"assets/w{tipo.upper()}.png"),
            (TAM_CASILLA, TAM_CASILLA)
        )
        IMAGENES['b' + tipo] = pygame.transform.scale(
            pygame.image.load(f"assets/b{tipo.upper()}.png"),
            (TAM_CASILLA, TAM_CASILLA)
        )

def dibujar_tablero(pantalla):
    colores = [pygame.Color("white"), pygame.Color("grey")]
    for fila in range(8):
        for columna in range(8):
            color = colores[(fila + columna) % 2] #para alternar el color en cada casilla
            pygame.draw.rect(
                pantalla,
                color,
                pygame.Rect(columna * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)
            )

def dibujar_piezas(pantalla, tablero_chess):
    for casilla in chess.SQUARES:
        tablero_chess = chess.Board()
        pieza = tablero_chess.piece_at(casilla)
        if pieza:
            columna = chess.square_file(casilla) #piece_at devuelve la pieza que esta en una casilla especifica del tablero
            fila = 7 - chess.square_rank(casilla)  # invertir eje Y para pygame
            color = 'w' if pieza.color == chess.WHITE else 'b'
            clave_imagen = color + pieza.symbol().lower() #.lower porque la libreria de chess devuelve mayuscula o no dependiendo del color
            imagen = IMAGENES[clave_imagen]
            pantalla.blit(imagen, pygame.Rect(columna * TAM_CASILLA, fila * TAM_CASILLA, TAM_CASILLA, TAM_CASILLA)) #block image tansfer

def dibujar_juego(pantalla, tablero_chess):
    dibujar_tablero(pantalla)
    dibujar_piezas(pantalla, tablero_chess)

#probando, el tablero real se tiene que crear desde el main
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Ajedrez con IA")
reloj = pygame.time.Clock()
tablero = chess.Board()

cargar_imagenes()
ejecutando = True

while ejecutando:
    dibujar_juego(pantalla, tablero)
    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    reloj.tick(30)

pygame.quit()
