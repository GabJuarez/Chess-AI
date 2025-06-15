import chess
import pygame 
import sys

class Button:
    def __init__(self, x=0, y=0, text="", width=200, height=50, elev=6):
        self.font = pygame.font.Font('res/fonts/Silkscreen-Bold.ttf', 24)
        self.text = self.font.render(text, True, "#ffffff")
        self.text_rect = self.text.get_rect()

        self.bottom_rect = pygame.Rect((x+elev, y+elev), (width, height))
        self.top_rect = pygame.Rect((x, y), (width, height))
        self.text_rect.center = self.top_rect.center

        self.hover = False
        self.pressed = False
        self.clicked = False

    
    def update(self):
        # Siempre supondremos que el botón no está clicado
        self.clicked = False
        # Luego comprobaremos si estamos encima
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.hover = True
            # Si presionamos mientras estamoas sobre el botón
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            else:
                # Si dejamos de presionar mientras estamos sobre el botón
                if self.pressed is True:
                    self.pressed = False
                    self.clicked = True
                    # print("Botón clicado")
        else:
            self.pressed = False
            self.hover = False

    def draw(self, display):
        top_rect_color = "#317bcf" if self.hover else "#3194cf"
        if not self.pressed:
            # Si no pulsamos dibujamos todo en su posición original
            pygame.draw.rect(display, "#1a232e", self.bottom_rect)
            pygame.draw.rect(display, top_rect_color, self.top_rect)
            self.text_rect.center = self.top_rect.center
        else:
            # Si pulsamos cambiamos la posición de dibujado abajo
            pygame.draw.rect(display, top_rect_color, self.bottom_rect)
            self.text_rect.center = self.bottom_rect.center
        display.blit(self.text, self.text_rect)


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

#variables globales para ajustar el dibujo del tablero y las piezas en la ventana
OFFSET_X = 285
OFFSET_Y = 50

def dibujar_tablero(pantalla):
    colores = [pygame.Color("white"), (107, 42,220)]
    for fila in range(8):
        for columna in range(8):
            color = colores[(fila + columna) % 2] #para alternar el color en cada casilla
            pygame.draw.rect(
                pantalla,
                color,
                pygame.Rect(
                    columna * TAM_CASILLA + OFFSET_X,
                    fila * TAM_CASILLA  + OFFSET_Y,
                    TAM_CASILLA, 
                    TAM_CASILLA)
            )

def dibujar_piezas(pantalla, tablero_chess):
    for casilla in chess.SQUARES:
        pieza = tablero_chess.piece_at(casilla)
        if pieza:
            columna = chess.square_file(casilla) #piece_at devuelve la pieza que esta en una casilla especifica del tablero
            fila = 7 - chess.square_rank(casilla)  # invertir eje Y para pygame
            color = 'w' if pieza.color == chess.WHITE else 'b'
            clave_imagen = color + pieza.symbol().lower() #.lower porque la libreria de chess devuelve mayuscula o no dependiendo del color
            imagen = IMAGENES[clave_imagen]
            pantalla.blit(imagen,
                         pygame.Rect(
                            columna * TAM_CASILLA + OFFSET_X,
                            fila * TAM_CASILLA + OFFSET_Y,
                            TAM_CASILLA,
                            TAM_CASILLA)) #block image tansfer a la pantalla

def mostrar_pantalla_inicio(pantalla):
    fuente = pygame.font.Font('res/fonts/Silkscreen-Bold.ttf', 90)
    fuente2 = pygame.font.Font('res/fonts/Silkscreen-Bold.ttf', 8)
    texto = 'Ajedrez'
    autores= ['Gabriel Juárez', 
              'Silvio Mejía',
              'Adriano Almanza',
              'Juan Castellón']
    
    ts = fuente.render(texto, True , (255,255,255))
    rect_texto = ts.get_rect(center=(520,220))

    fondo = pygame.transform.scale(pygame.image.load('assets/fondoeditado.png'), (1080,580))
    pygame.display.set_caption("Pantalla de incio")
    boton_jugar = Button(x= 430, y = 320, text = "JUGAR")

    esperando = True
    while esperando == True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pantalla.blit(fondo, (0,0))
        pantalla.blit(ts, rect_texto)
        """  y_inicial = 0  # posición vertical inicial
        for nombre in autores:
            ts2 = fuente2.render(nombre, True, (255, 255, 255))
            rect_texto2 = ts2.get_rect(topright=(470, y_inicial))  # margen derecho un poco adentro
            pantalla.blit(ts2, rect_texto2)
            y_inicial += rect_texto2.height + 3  # espacio entre líneas"""
        

        boton_jugar.update()
        boton_jugar.draw(pantalla)
        pygame.display.flip()
        
        if boton_jugar.clicked:
            esperando = False
        pygame.display.flip()


def dibujar_movimientos_legales(pantalla, movimientos):
    color = (0, 160, 154)
    r = 4 #tamano del radio de los circulos

    for casilla in movimientos:
        columna = chess.square_file(casilla)
        fila = 7 - chess.square_rank(casilla)
        centro_x = columna * TAM_CASILLA + TAM_CASILLA // 2 + OFFSET_X
        centro_y = fila * TAM_CASILLA + TAM_CASILLA // 2 + OFFSET_Y
        pygame.draw.circle(pantalla, color, (centro_x, centro_y), r)

def dibujar_movimientos_realizados(pantalla, movimientos_realizados):
    pygame.draw.rect(pantalla, (107, 42, 220), (800, OFFSET_Y, 200, 480), 0, 10, 10,10,10,10)
    fuente = pygame.font.Font('res/fonts/Silkscreen-Bold.ttf', 20)
    texto = fuente.render("Movimientos", True, (255, 255, 255))
    texto2 = fuente.render("Realizados", True, (255, 255, 255))
    texto_rect = texto.get_rect(center=(900, 30 + OFFSET_Y))
    texto_rect2 = texto2.get_rect(center=(900, 60 + OFFSET_Y))
    pantalla.blit(texto, texto_rect)
    pantalla.blit(texto2, texto_rect2)

    fuente2 = pygame.font.Font('res/fonts/Silkscreen-Regular.ttf', 17)

    if movimientos_realizados:
        texto = fuente.render("Movimientos", True, (255, 255, 255))
        texto2 = fuente.render("Realizados", True, (255, 255, 255))
        movimientos = []
        movimientos = movimientos_realizados[-13:]

        for i in range (13):
            pygame.draw.rect(pantalla, (107, 42, 220), (800, OFFSET_Y, 200, 480), 0, 10, 10,10,10,10)
            for j, movimiento in enumerate(movimientos):
                texto_movimiento = fuente2.render(str(movimiento), True, (255, 255, 255))
                posmovemiento = texto_movimiento.get_rect(center=(900, 90 + j*30 + OFFSET_Y))
                pantalla.blit(texto, texto_rect)
                pantalla.blit(texto2, texto_rect2)
                pantalla.blit(texto_movimiento, posmovemiento)

            
            
def dibujar_botones_funcionalidades(pantalla, boton_regresar_jugada,juego):
    boton_regresar_jugada.update()
    boton_regresar_jugada.draw(pantalla)
    if boton_regresar_jugada.clicked:
        if len(juego.movimientos_realizados) > 0 and len(juego.tablero.move_stack) > 0:
            juego.movimientos_realizados.pop()
            juego.tablero.pop()
        else:
            return
        





