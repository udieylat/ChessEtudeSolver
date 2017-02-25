import copy

BLACK, WHITE = [0, 1]
PLAYERS = [BLACK, WHITE]
KING, QUEEN, KNIGHT, ROOK, BISHOP, PAWN, EMPTY = "kqnrbp-"
PIECES = [KING, QUEEN, KNIGHT, ROOK, BISHOP, PAWN, EMPTY]

MIN_COL = ord('a') # 97
MAX_COL = ord('h') # 104
MIN_ROW = 1
MAX_ROW = 8
COLUMNS = "abcdefgh"

next_turn = lambda turn : 1 - turn

widen = lambda line : ''.join([' '+piece for piece in line])

piece_char_to_player = lambda piece_char : BLACK if piece_char.isupper() else WHITE

piece_to_char = lambda piece : piece.type if piece.player == WHITE else piece.type.upper()

position_to_ord_col_row = lambda position : (ord(position[0]), int(position[1]))

ord_col_row_to_position = lambda ord_col, row : "{}{}".format(chr(ord_col), row)

is_square_in_board = lambda ord_col, row : row >= MIN_ROW and row <= MAX_ROW and ord_col >= MIN_COL and ord_col <= MAX_COL

def get_legal_bishop_moves_no_check(player, position, board):
    col, row = position_to_ord_col_row(position)
    
    moves = []
    
    # Right Up.
    for i in range(1, min(MAX_COL - col, MAX_ROW - row) + 1):
        new_col = col + i
        new_row = row + i
        new_pos = ord_col_row_to_position(new_col, new_row)
        if board.positions_to_pieces[new_pos].type == EMPTY:
            moves.append(new_pos)
        else:
            if board.positions_to_pieces[new_pos].player != player:
                moves.append(new_pos)
            break

    # Right Down.
    for i in range(1, min(MAX_COL - col, row - MIN_ROW) + 1):
        new_col = col + i
        new_row = row - i
        new_pos = ord_col_row_to_position(new_col, new_row)
        if board.positions_to_pieces[new_pos].type == EMPTY:
            moves.append(new_pos)
        else:
            if board.positions_to_pieces[new_pos].player != player:
                moves.append(new_pos)
            break

    # Left Up.
    for i in range(1, min(col - MIN_COL, MAX_ROW - row) + 1):
        new_col = col - i
        new_row = row + i
        new_pos = ord_col_row_to_position(new_col, new_row)
        if board.positions_to_pieces[new_pos].type == EMPTY:
            moves.append(new_pos)
        else:
            if board.positions_to_pieces[new_pos].player != player:
                moves.append(new_pos)
            break

    # Left Down.
    for i in range(1, min(col - MIN_COL, row - MIN_ROW) + 1):
        new_col = col - i
        new_row = row - i
        new_pos = ord_col_row_to_position(new_col, new_row)
        if board.positions_to_pieces[new_pos].type == EMPTY:
            moves.append(new_pos)
        else:
            if board.positions_to_pieces[new_pos].player != player:
                moves.append(new_pos)
            break

    return moves

def get_legal_rook_moves_no_check(player, position, board):
    col, row = position_to_ord_col_row(position)
    
    moves = []
    
    # Right.
    for new_col in range(col + 1, MAX_COL + 1):
        new_pos = ord_col_row_to_position(new_col, row)
        if board.positions_to_pieces[new_pos].type == EMPTY:
            moves.append(new_pos)
        else:
            if board.positions_to_pieces[new_pos].player != player:
                moves.append(new_pos)
            break
    
    # Left.
    for new_col in range(col - 1, MIN_COL - 1, -1):
        new_pos = ord_col_row_to_position(new_col, row)
        if board.positions_to_pieces[new_pos].type == EMPTY:
            moves.append(new_pos)
        else:
            if board.positions_to_pieces[new_pos].player != player:
                moves.append(new_pos)
            break
    
    # Up.
    for new_row in range(row + 1, MAX_ROW + 1):
        new_pos = ord_col_row_to_position(col, new_row)
        if board.positions_to_pieces[new_pos].type == EMPTY:
            moves.append(new_pos)
        else:
            if board.positions_to_pieces[new_pos].player != player:
                moves.append(new_pos)
            break

    # Down.
    for new_row in range(row - 1, MIN_ROW - 1, -1):
        new_pos = ord_col_row_to_position(col, new_row)
        if board.positions_to_pieces[new_pos].type == EMPTY:
            moves.append(new_pos)
        else:
            if board.positions_to_pieces[new_pos].player != player:
                moves.append(new_pos)
            break
            
    return moves


class Piece(object):
    
    def __init__(self, type, position, player):
        self.type = type
        self.position = position
        self.player = player

    def __repr__(self):
        return "Piece: {}, position: {}".format(piece_to_char(self), self.position)
    
    def __eq__(self, piece_char):
        return self.type == piece_char.lower() and self.player == piece_char_to_player(piece_char)


class King(Piece):

    def __init__(self, position, player):
        Piece.__init__(self, KING, position, player)

    def get_all_possible_moves(self):
        moves = []
        col, row = position_to_ord_col_row(self.position)
        for i, j in [(-1, -1), (-1, 1), (1, 1), (1, -1), (-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_col = col + i
            new_row = row + j
            if not is_square_in_board(new_col, new_row):
                continue
            new_pos = ord_col_row_to_position(new_col, new_row)
            moves.append(new_pos)
        return moves
    
    def get_legal_moves(self, board):
        # Don't check if king is in check in new square. Only if it's taken by a piece of the same player.
        # Not including castling.
        return [move for move in self.get_all_possible_moves()
				if board.positions_to_pieces[move].type == EMPTY
				or board.positions_to_pieces[move].player != self.player]


class Queen(Piece):

    def __init__(self, position, player):
        Piece.__init__(self, QUEEN, position, player)
    
    def get_legal_moves(self, board):
        return get_legal_bishop_moves_no_check(self.player, self.position, board) + \
        get_legal_rook_moves_no_check(self.player, self.position, board)
    
class Knight(Piece):

    def __init__(self, position, player):
        Piece.__init__(self, KNIGHT, position, player)

    def get_all_possible_moves(self):
        moves = []
        col, row = position_to_ord_col_row(self.position)
        for i, j in [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]:
            new_col = col+i
            new_row = row+j
            if not is_square_in_board(new_col, new_row):
                continue
            new_pos = ord_col_row_to_position(new_col, new_row)
            moves.append(new_pos)
        return moves
    
    def get_legal_moves(self, board):
        return [move for move in self.get_all_possible_moves() \
        if board.positions_to_pieces[move].type == EMPTY or board.positions_to_pieces[move].player != self.player]
    
class Rook(Piece):

    def __init__(self, position, player):
        Piece.__init__(self, ROOK, position, player)

    def get_legal_moves(self, board):
        return get_legal_rook_moves_no_check(self.player, self.position, board)
        
class Bishop(Piece):

    def __init__(self, position, player):
        Piece.__init__(self, BISHOP, position, player)

    def get_legal_moves(self, board):
        return get_legal_bishop_moves_no_check(self.player, self.position, board)
    
class Pawn(Piece):

    def __init__(self, position, player):
        Piece.__init__(self, PAWN, position, player)

    def next_move_promotes(self, row):
        return (row == 7 and self.player == WHITE) or (row == 2 and self.player == BLACK)

    def get_legal_moves(self, board):
        # Not including promotion and en-passent.
        moves = []
        col, row = position_to_ord_col_row(self.position)

        if row == MIN_ROW or row == MAX_ROW:
            return []

        assert row != MIN_ROW
        assert row != MAX_ROW
        
#        if self.next_move_promotes(row):
#            print " ** Warning: next pawn move promotes! **"
        
        row_const = (1 if self.player == WHITE else -1)
        new_row = row + row_const
        
        # One step forward.
        move = ord_col_row_to_position(col, new_row)
        if board.positions_to_pieces[move].type == EMPTY:
            moves.append(move)
            # Two steps forward:
            if (row == 7 and self.player == BLACK) or (row == 2 and self.player == WHITE):
                move = ord_col_row_to_position(col, new_row + row_const) 
                if board.positions_to_pieces[move].type == EMPTY:
                    moves.append(move)
        
        # Capture.
        for i in [-1, 1]:
            new_col = col + i
            if not is_square_in_board(new_col, new_row):
                continue
            move = ord_col_row_to_position(new_col, new_row)
            if board.positions_to_pieces[move].type != EMPTY and board.positions_to_pieces[move].player != self.player:
                moves.append(move)
        
        return moves


class Empty(Piece):

    def __init__(self, position, player = None):
        Piece.__init__(self, EMPTY, position, player)
        self.player = None

piece_to_class = {KING: King, QUEEN: Queen, KNIGHT: Knight, ROOK: Rook, BISHOP: Bishop, PAWN: Pawn, EMPTY: Empty}

def read_board(filename, turn = WHITE):
    lines = [line.strip() for line in open(filename).readlines() if line.strip()!=""]
    assert len(lines) == 8
    for line in lines:
        assert len(line) == 8
        for piece in line.lower():
            assert piece in PIECES
    assert turn in PLAYERS
    return Board(lines, turn)

def state_to_positions_pieces_dict(state):
    d = {}
    for i, line in enumerate(state):
        for j, piece_char in enumerate(line):
            position = "{0}{1}".format(COLUMNS[j], 8-i)
            piece = piece_to_class[piece_char.lower()](position, piece_char_to_player(piece_char))
            d[position] = piece
    return d

def positions_pieces_dict_to_state(positions_pieces_dict):
    return [''.join([piece_to_char(positions_pieces_dict[ord_col_row_to_position(col, row)]) for col in range(MIN_COL, MAX_COL + 1)]) \
    for row in range(MAX_ROW, MIN_ROW - 1, -1)]

def get_step_string(step, board_before_step):
    # Doesn't include:
    #  Promotion, en-passent, castling.
    #  Ambiguity: two same pieces that can move to the same square.
    old_pos, new_pos = step
    piece = board_before_step[old_pos]
    assert piece.type != EMPTY
    if board_before_step[new_pos].type == EMPTY:
        prefix = piece.type.upper() if piece.type != PAWN else ''
    else:
        prefix = (piece.type.upper() if piece.type != PAWN else old_pos[0]) + 'x'
    
    board_after_step = board_before_step.move(step)
    suffix = ''
    if board_after_step.is_in_check():
        if board_after_step.get_all_legal_moves() == []:
            suffix = '#'
        else:
            suffix = '+'
    
    return prefix + new_pos + suffix
    
    
class Board(object):

    def __init__(self, state, turn):
        self.state = state
        self.turn = turn
        self.positions_to_pieces = state_to_positions_pieces_dict(self.state)
        self.internal_check = False
    
    def is_in_check(self):
        if self.turn == BLACK:
            return self.is_black_in_check()
        return self.is_white_in_check()
    
    def is_mate(self):
        return self.is_in_check() and self.get_all_legal_moves() == []
    
    def get_all_legal_moves(self):
        moves = []
        
        if self.turn == BLACK:
            for move in self.get_all_black_legal_moves_no_check():
                new_board = self.move(move)
                new_board.internal_check = True
                if not new_board.is_black_in_check():
                    moves.append(move)
        else:
            for move in self.get_all_white_legal_moves_no_check():
                new_board = self.move(move)
                new_board.internal_check = True
                if not new_board.is_white_in_check():
                    moves.append(move)
        
        return moves

    def is_black_in_check(self):
        if not self.internal_check:
            assert self.turn == BLACK
        black_king_position = [position for position in self.positions_to_pieces if self.positions_to_pieces[position] == 'K'][0]
        return black_king_position in [new_pos for old_pos, new_pos in self.get_all_white_legal_moves_no_check()]
    
    def is_white_in_check(self):
        if not self.internal_check:
            assert self.turn == WHITE
        white_king_position = [position for position in self.positions_to_pieces if self.positions_to_pieces[position] == 'k'][0]
        return white_king_position in [new_pos for old_pos, new_pos in self.get_all_black_legal_moves_no_check()]
    
    def get_all_black_legal_moves_no_check(self):
        # Legal moves ignore checked king.
        moves = []
        for position in self.positions_to_pieces:
            piece = self.positions_to_pieces[position]
            if piece.player == BLACK:
                moves += [(piece.position, move) for move in piece.get_legal_moves(self)]
        return moves
    
    def get_all_white_legal_moves_no_check(self):
        # Legal moves ignore checked king.
        moves = []
        for position in self.positions_to_pieces:
            piece = self.positions_to_pieces[position]
            if piece.player == WHITE:
                moves += [(piece.position, move) for move in piece.get_legal_moves(self)]
        return moves
    
    def move(self, step):
        new_positions_to_pieces_dict = copy.copy(self.positions_to_pieces)
        old_pos, new_pos = step
        
        assert new_positions_to_pieces_dict[old_pos].type != EMPTY
        assert new_positions_to_pieces_dict[old_pos].player == self.turn
        assert new_positions_to_pieces_dict[new_pos].player != self.turn
        
        new_positions_to_pieces_dict[new_pos] = copy.copy(new_positions_to_pieces_dict[old_pos])
        new_positions_to_pieces_dict[new_pos].position = new_pos

        #TODO: here should handle promotion - need to split output into several boards or something...

        new_positions_to_pieces_dict[old_pos] = Empty(old_pos)
        new_state = positions_pieces_dict_to_state(new_positions_to_pieces_dict)
        
        return Board(new_state, next_turn(self.turn))
    
    def __getitem__(self, position):
        return self.positions_to_pieces[position]
    
    def __str__(self):
        return """ +-----------------+
{}
 +-----------------+
   a b c d e f g h""".format('\n'.join(["{}|{} |".format(8-i, widen(line)) for i,line in enumerate(self.state)]))
    
    def __repr__(self):
        return str(self)

def single_move_gives_mate(board, ret_step = False):
    for step1 in board.get_all_legal_moves():
        board2 = board.move(step1)
        if board2.is_mate():
            if ret_step:
                return step1
            return True
    return False

def print_working_on_step(step_string):
    print "Working on step: 1.", step_string

def print_can_handle_with_step(step2, board2):
    print "  Can handle with step: 1...", get_step_string(step2, board2)

def print_success(step_string):
    print "  Success!!!\n"
    print "  1.", step_string, "is the solution!\n"

def print_didnt_solve():
    print "Didn't solve :("
    print "Check maybe solution involves promotion, castling or en-passent."

def solve_mate_in_two(board, verbose=True):
    assert board.turn == WHITE
    if verbose:
        print board
    for step1 in board.get_all_legal_moves():
        if verbose:
            step_string = get_step_string(step1, board)
            print_working_on_step(step_string)
        board2 = board.move(step1)
        found = False
        for step2 in board2.get_all_legal_moves():
            board3 = board2.move(step2)
            if not single_move_gives_mate(board3):
                if verbose:
                    print_can_handle_with_step(step2, board2)
                found = True
                break
        if not found:
            if verbose:
                print_success(step_string)
            return step1
    
    if verbose:
        print_didnt_solve()
    
    return None

PRINT_SOLUTIONS_PREFIX = "    "

def print_solutions(solutions_dict, board_before_step2, prefix_level=1):
    threats = set(solutions_dict.values())
    for step3 in threats:
        board_after_step2 = None
        for step2 in solutions_dict:
            if solutions_dict[step2] == step3:
                if board_after_step2 == None:
                    board_after_step2 = board_before_step2.move(step2)
                print "{}{}... {}".format(PRINT_SOLUTIONS_PREFIX * prefix_level,
                                          prefix_level, get_step_string(step2, board_before_step2))

        assert board_after_step2 != None
        print "{}  =>  {}. {}".format(PRINT_SOLUTIONS_PREFIX * (prefix_level + 1), \
                                      prefix_level + 1, get_step_string(step3, board_after_step2))
        
    print

def print_solutions_doubled_dict(solutions_doubled_dict, board_before_step2, prefix_level=1):
    # Idea was to call recursively to print_solutions, but it bugs etc.
    for step2 in solutions_doubled_dict:
        
        print "{}{}... {}".format(PRINT_SOLUTIONS_PREFIX * prefix_level,
        prefix_level, get_step_string(step2, board_before_step2))
        
        board_after_step2 = board_before_step2.move(step2)
        step3 = solutions_doubled_dict[step2][0]
        
        print "{}  {}. {}".format(PRINT_SOLUTIONS_PREFIX * prefix_level,
        prefix_level + 1, get_step_string(step3, board_after_step2))
        
        board_after_step3 = board_after_step2.move(step3)
        
        for step4 in solutions_doubled_dict[step2][1]:
        
            print "{}{}... {}".format(PRINT_SOLUTIONS_PREFIX * (prefix_level + 1),
                                      prefix_level + 1, get_step_string(step4, board_after_step3))

            step5 = solutions_doubled_dict[step2][1][step4]
            board_after_step4 = board_after_step3.move(step4)
            
            print "{}  {}. {}".format(PRINT_SOLUTIONS_PREFIX * (prefix_level + 1),
                                      prefix_level + 2, get_step_string(step5, board_after_step4))
        
def solve_mate_in_three(board, verbose=True):
    assert board.turn == WHITE
    if verbose:
        print board
    for step1 in board.get_all_legal_moves():
        if verbose:
            step_string = get_step_string(step1, board)
            print_working_on_step(step_string)
        board2 = board.move(step1)
        solutions_dict = {}
        found = False
        for step2 in board2.get_all_legal_moves():
            board3 = board2.move(step2)
            step3 = solve_mate_in_two(board3, False)
            if step3 == None:
                if verbose:
                    print_can_handle_with_step(step2, board2)
                found = True
                break
            solutions_dict[step2] = step3
        if not found:
            if verbose:
                print_success(step_string)
                print_solutions(solutions_dict, board2)
            return step1, solutions_dict
    
    if verbose:
        print_didnt_solve()
    
    return None

def solve_mate_in_four(board, verbose=True):
    assert board.turn == WHITE
    if verbose:
        print board
    for step1 in board.get_all_legal_moves():
        if verbose:
            step_string = get_step_string(step1, board)
            print_working_on_step(step_string)
        board2 = board.move(step1)
        solutions_doubled_dict = {}
        found = False
        for step2 in board2.get_all_legal_moves():
            print "  Working on step2: 1...", get_step_string(step2, board2)
            board3 = board2.move(step2)
            res = solve_mate_in_three(board3, False)
            if res == None:
                if verbose:
                    print_can_handle_with_step(step2, board2)
                found = True
                break
            solutions_doubled_dict[step2] = res
        if not found:
            if verbose:
                print_success(step_string)
                print_solutions_doubled_dict(solutions_doubled_dict, board2)
            return step1, solutions_doubled_dict
    
    if verbose:
        print_didnt_solve()
    
    return None

def get_helpmate_solution_string(step1, step2, step3, step4, board):
    board2 = board.move(step1)
    board3 = board2.move(step2)
    board4 = board3.move(step3)
    return "1. {} {} 2. {} {}".format(
        get_step_string(step1, board), get_step_string(step2, board2),
        get_step_string(step3, board3), get_step_string(step4, board4))
    
def solve_helpmate_in_two(board, num_solutions=1):
    assert board.turn == BLACK
    print board
    solutions = []
    for step1 in board.get_all_legal_moves():
        print_working_on_step(get_step_string(step1, board))
        board2 = board.move(step1)
        for step2 in board2.get_all_legal_moves():
            print ("  Working on step2: 1...", get_step_string(step2, board2))
            board3 = board2.move(step2)
            for step3 in board3.get_all_legal_moves():
                board4 = board3.move(step3)
                for step4 in board4.get_all_legal_moves():
                    board5 = board4.move(step4)
                    if board5.is_mate():
                        solution = get_helpmate_solution_string(step1, step2, step3, step4, board)
                        print "  Success!!! Solution:", solution
                        solutions.append(solution)
                        if len(solutions) == num_solutions:
                            print "\nAll solutions were found!\n"
                            for i, solution in enumerate(solutions):
                                print "  Solution #{0} is: {1}".format(i+1, solution)
                            print
                            return
    
    print "\nFound following solutions:\n"
    for i, solution in enumerate(solutions):
        print "  Solution #{} is: {}".format(i+1, solution)

    print_didnt_solve()

def solve_selfmate_in_two(board):
    assert board.turn == WHITE
    print board
    for step1 in board.get_all_legal_moves(): # White move
        step_string = get_step_string(step1, board)
        print_working_on_step(step_string)
        board2 = board.move(step1)
        black_moves1 = board2.get_all_legal_moves()
        if black_moves1 == []: # We don't want mate on black.
            print "  This is a mate move. Continue."
            continue
        solutions_dict = {}
        found = False
        for step2 in black_moves1: # Black move
            board3 = board2.move(step2)
            white_moves = board3.get_all_legal_moves()
            if white_moves == []: # We don't want mate on white.
                continue
            found2 = False
            for step3 in white_moves: # White move
                board4 = board3.move(step3)
                black_moves2 = board4.get_all_legal_moves()
                if black_moves2 == []: # We don't want mate on black.
                    continue
                if [step4 for step4 in black_moves2 if not board4.move(step4).is_mate()] == []:
                    solutions_dict[step2] = step3
                    found2 = True
                    break
            if not found2:
                print_can_handle_with_step(step2, board2)
                found = True
                break
        
        if not found:
            print_success(step_string)
            print_solutions(solutions_dict, board2)
            return
    
    print_didnt_solve()

