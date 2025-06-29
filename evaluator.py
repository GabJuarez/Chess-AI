import chess

class Nodo:
    def __init__(self, tablero, movimiento=None, padre=None):
        self.tablero = tablero
        self.movimiento = movimiento
        self.padre = padre
        self.hijos = []
        self.valor = None

class ArbolMinimax:
    def __init__(self, tablero, maxDepth, color):
        self.raiz = Nodo(tablero.copy())
        self.maxDepth = maxDepth
        self.color = color  # Color que queremos que gane

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
                eval_hijo = self.construir_arbol(
                    hijo, profundidad - 1, nuevo_tablero.turn == self.color
                )
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
                eval_hijo = self.construir_arbol(
                    hijo, profundidad - 1, nuevo_tablero.turn == self.color
                )
                min_eval = min(min_eval, eval_hijo)
            nodo.valor = min_eval
            return min_eval

    def obtener_mejor_movimiento(self):
        mejor_movimiento = None
        mejor_valor = float('-inf') if self.color == chess.WHITE else float('inf')

        for hijo in self.raiz.hijos:
            if self.color == chess.WHITE:
                if hijo.valor is not None and hijo.valor > mejor_valor:
                    mejor_valor = hijo.valor
                    mejor_movimiento = hijo.movimiento
            else:
                if hijo.valor is not None and hijo.valor < mejor_valor:
                    mejor_valor = hijo.valor
                    mejor_movimiento = hijo.movimiento

        return mejor_movimiento

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

        return score
