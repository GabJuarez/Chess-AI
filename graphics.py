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

def mostrar_pantalla_inicio(pantalla):
    fuente = pygame.font.Font('res/fonts/Silkscreen-Bold.ttf', 40)
    fuente2 = pygame.font.Font('res/fonts/Silkscreen-Bold.ttf', 8)
    texto = 'Ajedrez'
    autores= ['Gabriel Juárez', 
              'Silvio Mejía',
              'Adriano Almanza',
              'Juan Castellón']
    
    ts = fuente.render(texto, True , (255,255,255))
    rect_texto = ts.get_rect(center=(240,150))

    fondo = pygame.transform.scale(pygame.image.load('assets/fondo.png'), (480,480))
    pygame.display.set_caption("Pantalla de incio")
    boton_jugar = Button(x= 140, y = 380, text = "JUGAR")

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

def iniciar_juego(pantalla):
    pygame.display.set_caption("Ajedrez")
    clock = pygame.time.Clock()
    tablero = chess.Board()

    cargar_imagenes()
    ejecutando = True

    while ejecutando == True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
                sys.exit()

        dibujar_juego(pantalla, tablero)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

