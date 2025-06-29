import chess
import random

class Nodo:
    def __init__(self, tablero, movimiento=None, padre=None):
        self.tablero = tablero
        self.movimiento = movimiento
        self.padre = padre
        self.hijos = []
        self.valor = None

class ArbolMinimax:
    def __init__(self, tablero, maxDepth, color, probabilidad_error=0.0):
        self.raiz = Nodo(tablero.copy())
        self.maxDepth = maxDepth
        self.color = color
        self.probabilidad_error = probabilidad_error  # Sesgo: 0.3 = 30% de error

    def construir_arbol(self, nodo, profundidad, es_maximizador):
        if profundidad == 0 or nodo.tablero.is_game_over():
            nodo.valor = self.evaluar_tablero(nodo.tablero)
            return nodo.valor

        if es_maximizador:
            max_eval = float('-inf')
            for movimiento in nodo.tablero.legal_moves:
                nuevo_tablero = nodo.tablero.copy()
                nuevo_tablero.push(movimiento)
                hijo = Nodo(nuevo_tablero, movimiento, nodo)
                nodo.hijos.append(hijo)
                eval_hijo = self.construir_arbol(hijo, profundidad - 1, False)
                max_eval = max(max_eval, eval_hijo)
            nodo.valor = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for movimiento in nodo.tablero.legal_moves:
                nuevo_tablero = nodo.tablero.copy()
                nuevo_tablero.push(movimiento)
                hijo = Nodo(nuevo_tablero, movimiento, nodo)
                nodo.hijos.append(hijo)
                eval_hijo = self.construir_arbol(hijo, profundidad - 1, True)
                min_eval = min(min_eval, eval_hijo)
            nodo.valor = min_eval
            return min_eval

    def obtener_mejor_movimiento(self):
        hijos_validos = [h for h in self.raiz.hijos if h.valor is not None]
        if not hijos_validos:
            return None

        reverse = self.color == chess.WHITE
        hijos_ordenados = sorted(hijos_validos, key=lambda h: h.valor, reverse=reverse)

        if self.color == chess.WHITE or random.random() > self.probabilidad_error:
            return hijos_ordenados[0].movimiento

        if len(hijos_ordenados) > 1:
            indice_random = random.randint(1, len(hijos_ordenados) - 1)
            return hijos_ordenados[indice_random].movimiento
        else:
            return hijos_ordenados[0].movimiento

    def evaluar_tablero(self, tablero):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9,
            chess.KING: 0
        }

        score = 0
        for square in chess.SQUARES:
            pieza = tablero.piece_at(square)
            if pieza:
                valor = piece_values[pieza.piece_type]
                if pieza.color == self.color:
                    score += valor
                else:
                    score -= valor

        # Control del centro
        casillas_centro = [chess.D4, chess.E4, chess.D5, chess.E5]
        for casilla in casillas_centro:
            atacantes_color = len(tablero.attackers(self.color, casilla))
            atacantes_oponente = len(tablero.attackers(not self.color, casilla))
            score += -.5 * (atacantes_color - atacantes_oponente)

        # Desarrollo de piezas
        piezas_inicio = [chess.B1, chess.G1, chess.C1, chess.F1] if self.color == chess.WHITE else [chess.B8, chess.G8, chess.C8, chess.F8]
        for pieza in piezas_inicio:
            if tablero.piece_at(pieza) is None:
                score += 0.3

        # Penalización por caballos en la orilla
        casillas_orilla = [
            chess.A1, chess.H1, chess.A8, chess.H8,
            chess.A2, chess.H2, chess.A7, chess.H7,
            chess.A3, chess.H3, chess.A6, chess.H6
        ]
        for casilla in casillas_orilla:
            pieza = tablero.piece_at(casilla)
            if pieza and pieza.piece_type == chess.KNIGHT and pieza.color == self.color:
                score -= 0.5

        return score
