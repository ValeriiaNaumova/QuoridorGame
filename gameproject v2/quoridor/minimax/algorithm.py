RED = (255, 0, 0)
BLACK = (0, 0, 0)


def minimax(board, depth, max_player, alpha=float("-inf"), beta=float("+inf")):
    if depth == 0 or board.winner() is not None:
        return board.evaluate(), board

    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(board, RED):
            evaluation = minimax(move, depth - 1, False, alpha, beta)[0]
            maxEval = max(evaluation, maxEval)
            alpha = max(alpha, maxEval)
            if (maxEval >= beta):
                break
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(board, BLACK):
            evaluation = minimax(move, depth - 1, True, alpha, beta)[0]
            minEval = min(evaluation, minEval)
            beta = min(beta, minEval)
            if (minEval <= alpha):
                break
            if minEval == evaluation:
                best_move = move
        return minEval, best_move


def simulate_move(pawn, move, temp_board):
    temp_board.move(pawn, int(move.row), int(move.col))
    return temp_board


def simulate_move_bar(bar_1, bar_2, temp_board, temp_pawn):
    temp_board.change_bar(bar_1)
    temp_board.change_bar(bar_2)
    temp_pawn.walls -= 1
    return temp_board


# FIXME tahle metoda je volaná hoooooooodněkrát, je to v rámci toho rekurzivního minimaxu,
# je potřeba se zaměřit na co největší optimalizaci, např. ty vnořenný enumerate co jsou stejný jde optimalizovat,
# nebo určitě i ty ify jdou nějak udělat lépe (jen to nejde pořádně přečíst)
def get_all_moves(board, color):
    moves = []
    valid_moves_bars = []
    count = len(list((x for x in board.bar_list if (x.color == "black"))))
    for index, item in enumerate((x for x in board.bar_list if (x.color == "black"))):
        for index1, item1 in enumerate((x for x in board.bar_list if (x.color == "black"))):
            # FIXME napište si nějakou metodu na ověření, že je něco na okraji, hodí se to i do main.py
            if ((index != count - 1) and item.width == item1.width and (
                    (item.row == item1.row + 1 and item.col == item1.col and item.width == 5) or (
                    item.row == item1.row - 1 and item.col == item1.col and item.width == 5) or (
                            item.col == item1.col - 1 and item.row == item1.row and item.width == 50) or (
                            item.col == item1.col + 1 and item.row == item1.row and item.width == 50))):
                if (valid_moves_bars == []):
                    valid_moves_bars.append((item, item1))
                    # FIXME proč je tento if tak ošklivě zarovnaný, že tam je taková megamezera? to se nedá luštit
                elif (len(list((x for x in valid_moves_bars if (((x[0].row, x[0].col) == (item.row, item.col) and (
                        x[1].row, x[1].col) == (item1.row, item1.col)) or ((x[0].row, x[0].col) == (
                        item1.row, item1.col) and (
                                                                                   x[1].row, x[1].col) == (
                                                                                   item.row, item.col)))))) == 0):
                    valid_moves_bars.append((item, item1))

    for pawn in (x for x in board.player_list if (x.color == color)):
        valid_moves_pawns = board.get_possible_spots(pawn)
        for move in valid_moves_pawns:
            # TODO viz bakalářka, board.copy() a pawn.copy() i překresluje, to by bylo vhodné změnit, ale chápu,
            # že už to snadno nepůjde
            temp_board = board.copy()
            temp_pawn = temp_board.get_pawn(pawn.row, pawn.col)
            new_board = simulate_move(temp_pawn, move, temp_board)
            moves.append(new_board)

    for pawn in (x for x in board.player_list if (x.color == color)):
        for move in (x for x in valid_moves_bars if (((x[0].row - pawn.row) < 1 and (x[0].col - pawn.col) < 1) or (
                (x[1].row - pawn.row) < 1 and (x[1].col - pawn.col) < 1))):
            temp_board = board.copy()
            temp_bar_1 = temp_board.get_bar(move[0])
            temp_bar_2 = temp_board.get_bar(move[1])
            temp_pawn = temp_board.get_pawn(pawn.row, pawn.col)
            new_board = simulate_move_bar(temp_bar_1, temp_bar_2, temp_board, temp_pawn)
            moves.append(new_board)

    return moves
