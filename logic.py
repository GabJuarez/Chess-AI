import chess

class JuegoAjedrez:
    def __init__(self):
        self.tablero = chess.Board()
        self.casilla_origen = None
        self.movimientos_legales = []
        self.movimientos_realizados = []
        self.se_mueve = False

    #si la casilla origen es None, significa que no se ha seleccionado una pieza
    def seleccionar_casilla(self, fila, columna):
        casilla = chess.square(columna, 7 - fila)
        if self.casilla_origen is None:
            pieza = self.tablero.piece_at(casilla)
            if pieza and pieza.color == self.tablero.turn: 
                self.casilla_origen = casilla

    #se guardan los legal moves para ponerlos de manera visual al seleccionar una pieza
                for movimiento in self.tablero.legal_moves:
                    if movimiento.from_square == casilla:
                        self.movimientos_legales.append(movimiento.to_square)
    #si la pieza es del color del jugador actual se guarda la casilla como origen
    #si no es none significa que ya hay casilla de origen
        else:
            movimiento = chess.Move(self.casilla_origen, casilla)

            if self.casilla_origen == casilla:
                self.casilla_origen = None
                self.movimientos_legales = []
                return

            pieza_origen = self.tablero.piece_at(self.casilla_origen)

            es_promocion = (
            pieza_origen.piece_type == chess.PAWN and 
            (chess.square_rank(casilla) == 0 or chess.square_rank(casilla) == 7) #parentesis para que no se confunda con los operadores
            )

            if es_promocion:
                movimiento = chess.Move(self.casilla_origen, casilla, promotion=chess.QUEEN)
            else:
                movimiento = chess.Move(self.casilla_origen, casilla, promotion=None)

            if movimiento in self.tablero.legal_moves:
                self.tablero.push(movimiento)
                self.se_mueve = True
                
            self.movimientos_legales = []

            if self.se_mueve == True:
                self.movimientos_realizados.append(movimiento)

            self.casilla_origen = None
            self.se_mueve = False
    #si el movimiento es legal, se pushea el movimiento
    #se limpia la lista de legal moves

    def es_jaque(self):
        return self.tablero.is_check()

    def es_jaque_mate(self):
        return self.tablero.is_checkmate()

    def es_empate(self):
        return self.tablero.is_stalemate()


#buscar como implementarlo en el main
    def coronar_pieza(self, casilla):
        if self.tablero.piece_type_at(casilla) == chess.PAWN and (chess.square_rank(casilla) == 0 or chess.square_rank(casilla) == 7):
            self.tablero.set_piece_at(casilla, chess.Piece(chess.QUEEN, self.tablero.color_at(casilla)))

    def deshacer_ultimo_movimiento(self):
        self.movimientos_realizados.pop()
        self.tablero.move_stack.pop()
        
        