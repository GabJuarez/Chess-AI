import chess
from evaluator import ArbolMinimax

class JuegoAjedrez:
    def __init__(self):
        self.tablero = chess.Board()
        self.casilla_origen = None
        self.movimientos_legales = []
        self.movimientos_realizados = []
        self.se_mueve = False
        self.movimiento_sugerido = None

    # si la casilla origen es None, significa que no se ha seleccionado una pieza
    def seleccionar_casilla(self, fila, columna):
        casilla = chess.square(columna, 7 - fila)
        if self.casilla_origen is None:
            pieza = self.tablero.piece_at(casilla)
            if pieza and pieza.color == self.tablero.turn: 
                self.casilla_origen = casilla

                # se guardan los legal moves para ponerlos de manera visual al seleccionar una pieza
                for movimiento in self.tablero.legal_moves:
                    if movimiento.from_square == casilla:
                        self.movimientos_legales.append(movimiento.to_square)
        else:
            movimiento = chess.Move(self.casilla_origen, casilla)

            if self.casilla_origen == casilla:
                self.casilla_origen = None
                self.movimientos_legales = []
                return

            pieza_origen = self.tablero.piece_at(self.casilla_origen)
            es_promocion = (
                pieza_origen.piece_type == chess.PAWN and 
                (chess.square_rank(casilla) == 0 or chess.square_rank(casilla) == 7)
            )

            if es_promocion:
                movimiento = chess.Move(self.casilla_origen, casilla, promotion=chess.QUEEN)
            else:
                movimiento = chess.Move(self.casilla_origen, casilla, promotion=None)

            if movimiento in self.tablero.legal_moves:
                self.tablero.push(movimiento)
                self.se_mueve = True
                self.movimiento_sugerido = None
                
            self.movimientos_legales = []

            if self.se_mueve:
                self.movimientos_realizados.append(movimiento)

            self.casilla_origen = None
            self.se_mueve = False

    def es_jaque(self):
        return self.tablero.is_check()

    def es_jaque_mate(self):
        return self.tablero.is_checkmate()

    def es_empate(self):
        return self.tablero.is_stalemate()

    def coronar_pieza(self, casilla):
        if self.tablero.piece_type_at(casilla) == chess.PAWN and (chess.square_rank(casilla) == 0 or chess.square_rank(casilla) == 7):
            self.tablero.set_piece_at(casilla, chess.Piece(chess.QUEEN, self.tablero.color_at(casilla)))

    def deshacer_ultimo_movimiento(self):
        if self.movimientos_realizados and self.tablero.move_stack:
            self.movimientos_realizados.pop()
            self.tablero.pop()

def recomendar_movimiento(juego):
    color_turno = juego.tablero.turn
    profundidad = 3  # Menor profundidad para mejor rendimiento
    prob_error = 0.8  # 80% de error para el color sesgado
    arbol = ArbolMinimax(juego.tablero, profundidad, color_turno, probabilidad_error=prob_error)
    arbol.construir_arbol(arbol.raiz, profundidad, True)
    return arbol.obtener_mejor_movimiento()
