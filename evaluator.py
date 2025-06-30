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
    def __init__(self, tablero, maxDepth, color, probabilidad_error=0.0, color_sesgo=None):
        self.raiz = Nodo(tablero.copy())
        self.maxDepth = maxDepth
        self.color = color
        self.probabilidad_error = probabilidad_error  
        # Elegir aleatoriamente el color al que se le aplicará el sesgo si no se especifica
        if color_sesgo is None:
            self.color_sesgo = random.choice([chess.WHITE, chess.BLACK])
        else:
            self.color_sesgo = color_sesgo

    def construir_arbol(self, nodo, profundidad, es_maximizador, alpha=float('-inf'), beta=float('inf')):
        if profundidad == 0 or nodo.tablero.is_game_over():
            nodo.valor = self.evaluar_tablero(nodo.tablero)
            return nodo.valor

        # Ordenar movimientos para mejorar la poda alpha-beta
        movimientos = list(nodo.tablero.legal_moves)
        # Ordena primero por capturas y promociones (más prometedores)
        movimientos.sort(key=lambda m: nodo.tablero.is_capture(m) or nodo.tablero.is_en_passant(m) or nodo.tablero.is_castling(m), reverse=True)

        if es_maximizador:
            max_eval = float('-inf')
            for movimiento in movimientos:
                nuevo_tablero = nodo.tablero.copy()
                nuevo_tablero.push(movimiento)
                hijo = Nodo(nuevo_tablero, movimiento, nodo)
                nodo.hijos.append(hijo)
                eval_hijo = self.construir_arbol(hijo, profundidad - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_hijo)
                alpha = max(alpha, eval_hijo)
                if beta <= alpha:
                    break  # poda beta
            nodo.valor = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for movimiento in movimientos:
                nuevo_tablero = nodo.tablero.copy()
                nuevo_tablero.push(movimiento)
                hijo = Nodo(nuevo_tablero, movimiento, nodo)
                nodo.hijos.append(hijo)
                eval_hijo = self.construir_arbol(hijo, profundidad - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_hijo)
                beta = min(beta, eval_hijo)
                if beta <= alpha:
                    break  # poda alpha
            nodo.valor = min_eval
            return min_eval

    def obtener_mejor_movimiento(self):
        hijos_validos = [h for h in self.raiz.hijos if h.valor is not None]
        if not hijos_validos:
            return None

        reverse = self.color == chess.WHITE
        hijos_ordenados = sorted(hijos_validos, key=lambda h: h.valor, reverse=reverse)

        # 80% de las veces el color sesgado elige cualquier movimiento aleatorio (no solo entre los no óptimos)
        if self.color == self.color_sesgo and random.random() < self.probabilidad_error:
            return random.choice(hijos_ordenados).movimiento
        else:
            return hijos_ordenados[0].movimiento

    def evaluar_tablero(self, tablero):
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3.2,
            chess.BISHOP: 3.33,
            chess.ROOK: 5.1,
            chess.QUEEN: 9.5,
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
            score += 0.3 * (atacantes_color - atacantes_oponente)

        # Desarrollo de piezas
        piezas_inicio = [chess.B1, chess.G1, chess.C1, chess.F1] if self.color == chess.WHITE else [chess.B8, chess.G8, chess.C8, chess.F8]
        for pieza in piezas_inicio:
            if tablero.piece_at(pieza) is None:
                score += 0.25

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

        # Movilidad
        score += 0.1 * (len(list(tablero.legal_moves)) if tablero.turn == self.color else -len(list(tablero.legal_moves)))

        # Peones pasados
        for square in chess.SQUARES:
            pieza = tablero.piece_at(square)
            if pieza and pieza.piece_type == chess.PAWN and pieza.color == self.color:
                if self._es_peon_pasado(tablero, square, pieza.color):
                    score += 0.4

        # Seguridad del rey (penaliza si el rey está expuesto)
        king_square = tablero.king(self.color)
        if king_square is not None:
            attackers = len(tablero.attackers(not self.color, king_square))
            score -= 0.3 * attackers

        return score

    def _es_peon_pasado(self, tablero, square, color):
        # Determina si un peón es pasado
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        direction = 1 if color == chess.WHITE else -1
        for df in [-1, 0, 1]:
            f = file + df
            if 0 <= f < 8:
                for r in range(rank + direction, 8 if color == chess.WHITE else -1, direction):
                    sq = chess.square(f, r)
                    pieza = tablero.piece_at(sq)
                    if pieza and pieza.piece_type == chess.PAWN and pieza.color != color:
                        return False
        return True
