# Author: YU AN PAN
# Date: 3/11/2021
# Description: Write a class named JanggiGame for playing an abstract board game called Janggi.
# A general is in check if it could be captured on the opposing player's next move.
# A player cannot make a move that puts or leaves their general in check.
# The game ends when one player **checkmates** the other's general.
# You don't actually capture a general, instead you have to put it in such a position that
# it cannot escape being in check, meaning that no matter what, it could be captured on the next move.
# Unlike chess, Janggi allows you to pass a turn and thus there is no stalemate (a scenario when no legal moves can be made).
# Your program should have Blue and Red as the competing players and Blue as the starting player.
# You do not need to implement any special mechanism for figuring out who can start the game.
# Locations on the board will be specified using "algebraic notation",
# with columns labeled a-i and rows labeled 1-10, with row 1 being the Red side and row 10 the Blue side.

class JanggiGame(object):
    """
    Represents a JanggiGame wth a board, two players:Red and Blue,
    current_state: "UNFINISHED", "RED_WON", "BLUE_WON" and multiple game's rule functions.
    """

    def __init__(self):
        """
        Constructor for JanggiGame.
        There are multiple variables in initial: board, current_state, player,
        place_pieces function and other inital variables if necessary.
        """
        self._num_rows = 10
        self._num_cols = 9
        self._board = [[None] * self._num_cols for _ in range(self._num_rows)]
        self._current_state = "UNFINISHED"             # 'UNFINISHED' or 'RED_WON' or 'BLUE_WON'
        self._players = ["B", "R"]                     # turn is even/odd, player is B/R
        self._turn = 0
        self._full_color_to_color = {"blue": "B", "red": "R"}
        self._place_pieces()

    @staticmethod
    def _get_board_position(position):
        """Get the position and transfer it to the real row and column of the board."""
        return int(position[1:]) - 1, ord(position[0]) - ord('a')

    def _get_king_position(self, color):
        """Get the position of the king and used function in the is_check method"""
        for i, row in enumerate(self._board):
            for j, piece in enumerate(row):
                if piece and piece.get_color() == color and piece.get_name() == "K":
                    return (i, j)

    def _get_player(self):
        """Get player"""
        return self._players[self._turn % 2]

    def _get_opponent(self):
        """Get opponent"""
        return self._players[(self._turn+1) % 2]

    def _is_valid_move(self, move_from, move_to):
        """Check if it is a valid move."""
        from_row, from_col = self._get_board_position(move_from)
        to_row, to_col = self._get_board_position(move_to)
        piece_from = self._board[from_row][from_col]
        piece_to = self._board[to_row][to_col]
        # if from and to are the same color, cannot move
        if piece_from and piece_to and piece_from.get_color() == piece_to.get_color(): return False
        # check if move_to is in the valid moves of the from piece
        return (to_row, to_col) in piece_from.get_valid_moves((from_row, from_col))

    def _place_pieces(self):
        """Place all pieces to initialize the board."""
        init_position_to_piece = {'a1': Chariots("R", "C", self._board),
                                  'b1': Elephants("R", "E", self._board),
                                  'c1': Horses("R", "H", self._board),
                                  'd1': Guards("R", "G", self._board),
                                  'f1': Guards("R", "G", self._board),
                                  'g1': Elephants("R", "E", self._board),
                                  'h1': Horses("R", "H", self._board),
                                  'i1': Chariots("R", "C", self._board),
                                  'e2': General("R", "K", self._board),
                                  'b3': Cannons("R", "A", self._board),
                                  'h3': Cannons("R", "A", self._board),
                                  'a4': Soldiers("R", "S", self._board),
                                  'c4': Soldiers("R", "S", self._board),
                                  'e4': Soldiers("R", "S", self._board),
                                  'g4': Soldiers("R", "S", self._board),
                                  'i4': Soldiers("R", "S", self._board),
                                  'a10': Chariots("B", "C", self._board),
                                  'b10': Elephants("B", "E", self._board),
                                  'c10': Horses("B", "H", self._board),
                                  'd10': Guards("B", "G", self._board),
                                  'f10': Guards("B", "G", self._board),
                                  'g10': Elephants("B", "E", self._board),
                                  'h10': Horses("B", "H", self._board),
                                  'i10': Chariots("B", "C", self._board),
                                  'e9': General("B", "K", self._board),
                                  'b8': Cannons("B", "A", self._board),
                                  'h8': Cannons("B", "A", self._board),
                                  'a7': Soldiers("B", "S", self._board),
                                  'c7': Soldiers("B", "S", self._board),
                                  'e7': Soldiers("B", "S", self._board),
                                  'g7': Soldiers("B", "S", self._board),
                                  'i7': Soldiers("B", "S", self._board),
                                  }

        for position in init_position_to_piece:
            row, col = self._get_board_position(position)
            self._board[row][col] = init_position_to_piece[position]

    def _update_turn(self):
        """Update turn"""
        self._turn += 1

    def _print_board(self):
        """Print board"""
        for row in self._board:
            line = [piece if piece else " " for piece in row]
            print(line)
        print("=" * 50)

    def is_in_check(self, color):
        """Check if it is in check."""
        color = self._full_color_to_color[color]
        row_id, col_id = pos = self._get_king_position(color)
        king = self._board[row_id][col_id]
        can_be_captured = king.can_be_captured(pos)
        return can_be_captured

    def get_game_state(self):
        """Get game state."""
        return self._current_state

    def make_move(self, move_from, move_to):
        """
        Get move_from and move_to parameters from user and make move. This is the public function.
        If the square being moved from does not contain a piece belonging to the player whose turn it is,
        or if the indicated move is not legal, or if the game has already been won, then it should just return False.
        Otherwise it should make the indicated move, remove any captured piece,
        update the game state if necessary, update whose turn it is, and return True.
        :param:
            move_from(str): Represents the square to move from.
            move_to(str): Represents the square to move to.
        :return:
            boolean: Return True or False. If it goes through all checks, then it returns True, otherwise it returns False.
        """

        # check game state, if the game has finished, return False
        game_state = self.get_game_state()
        if game_state == 'RED_WON' or game_state == 'BLUE_WON':
            return False

        # get board position
        from_row, from_col = pos = self._get_board_position(move_from)
        to_row, to_col = self._get_board_position(move_to)
        piece = self._board[from_row][from_col]
        # if piece is empty, move is invalid
        if not piece:
            return False

        # if it's not the right player
        if self._get_player() != piece.get_color():
            return False

        # pass the turn
        if move_from == move_to:
            # It's General and is_in_check, cannot pass
            if piece.get_name() == "K" and piece.can_be_captured(pos):
                return False
            self._update_turn()
            return True

        # not valid move
        if not self._is_valid_move(move_from, move_to):
            return False

        self._board[to_row][to_col] = self._board[from_row][from_col]
        self._board[from_row][from_col] = None

        opponent_pos = self._get_king_position(self._get_opponent())
        opponent_king = self._board[opponent_pos[0]][opponent_pos[1]]
        # If opponent is in check and the opponent's king cannot move, it's checkmate
        if opponent_king.can_be_captured(opponent_pos):
            valid_moves = []
            for next_pos in opponent_king.get_valid_moves(opponent_pos):
                tmp_piece = self._board[next_pos[0]][next_pos[1]]
                self._board[next_pos[0]][next_pos[1]] = opponent_king
                self._board[opponent_pos[0]][opponent_pos[1]] = None
                if not opponent_king.can_be_captured(next_pos):
                    valid_moves.append(next_pos)
                self._board[next_pos[0]][next_pos[1]] = tmp_piece
                self._board[opponent_pos[0]][opponent_pos[1]] = opponent_king

            if len(valid_moves) == 0:
                self._current_state = "BLUE_WON" if self._get_player() == "B" else "RED_WON"

        self._print_board()
        self._update_turn()
        return True


class Piece():
    """
    Represents a Piece class with a color and name. This class is the parent class. All the other piece classes are child class.
    """
    def __init__(self, color, name, board):
        """
        Constructor for Piece. It have some initial variables: color, name, board, directions and max_step.
        """
        self._color = color
        self._name = name
        self._UP = [(-1, 0)]
        self._DOWN = [(1, 0)]
        self._RIGHT = [(0, 1)]
        self._LEFT = [(0, -1)]
        self._UP_LEFT = [(-1, -1)]
        self._UP_RIGHT = [(-1, 1)]
        self._DOWN_LEFT = [(1, -1)]
        self._DOWN_RIGHT = [(1, 1)]
        self._board = board
        self._directions = []
        self._special_directions = {}
        self._max_step = 1
        self._special_max_step = 1
        self._num_rows, self._num_cols = len(self._board), len(self._board[0])

    def __repr__(self):
        """A special method used to represent a class’s objects as a string."""
        return self._color + ":" + self._name

    def _is_valid(self, pos, top_left, bottom_right, block_colors):
        """Check if it is a valid move."""
        eat_enemy = False
        # is_valid: if pos is out of range
        top_row, left_col = top_left
        bottom_row, right_col = bottom_right
        if pos[0] < top_row or pos[0] > bottom_row or pos[1] < left_col or pos[1] > right_col:
            return False, eat_enemy
        # if it is General, check if it is in check
        if self._name == "K" and self.can_be_captured(pos):
            return False, eat_enemy

        piece = self._board[pos[0]][pos[1]]
        # pos is empty, can be moved
        if not piece: return True, eat_enemy
        # if pos is not empty, check if color in block_colors
        if piece.get_color() in block_colors:
            return False, eat_enemy
        eat_enemy = True
        return True, eat_enemy

    def get_color(self):
        """Get color"""
        return self._color

    def get_name(self):
        """Get name"""
        return self._name

    def get_valid_moves(self, pos):
        """Get individual piece's all valid moves"""
        valid_moves = []
        from_row, from_col = pos
        block_colors = ["R", "B"]

        max_steps = [self._max_step] * len(self._directions)
        bounds = [((0, 0), (self._num_rows-1, self._num_cols-1))] * len(self._directions)
        directions = self._directions[:]

        # special case in square for "K","G","S","C"
        if pos in self._special_directions:
            directions += self._special_directions[pos]
            max_steps += [self._special_max_step] * len(self._special_directions)
            if self._color == "B":
                bounds += [((7, 3), (9, 5))] * len(self._special_directions)
            else:
                bounds += [((0, 3), (2, 5))] * len(self._special_directions)

        # get all valid moves
        for i, direction in enumerate(directions):
            is_valid_move, eat_enemy = True, False
            max_step = max_steps[i]
            top_left, bottom_right = bounds[i]
            # iterate direction
            for step in range(1, max_step+1):
                for j, subdir in enumerate(direction):
                    # if i equals to last step, only piece with the same color can block itself
                    if j == len(direction) - 1:
                        block_colors = [self._color]
                    # move_from, move_to add one direction step
                    pos = (pos[0] + subdir[0], pos[1] + subdir[1])
                    # check if it is a valid move, if it's not a valid move, return false, then break
                    is_valid_move, eat_enemy = self._is_valid(pos, top_left, bottom_right, block_colors)
                    # break action when invalid or eat enemy
                    if not is_valid_move or eat_enemy:
                        break
                # break step when invalid or hit enemy
                if not is_valid_move:
                    break
                # if it is valid move, append position
                valid_moves.append(pos)
                # if eat enemy, cannot move further
                if eat_enemy:
                    break
            pos = (from_row, from_col)  # reset position
        return valid_moves

    def can_be_captured(self, pos):
        """Check if General can be captured. If the General is in opponent's valid moves, the General is in check."""
        opponent_pieces = []
        opponent_valid_moves = []
        opponent_color = "B" if self._color == "R" else "R"
        for i, row in enumerate(self._board):
            for j, piece in enumerate(row):
                if piece and piece.get_color() == opponent_color and piece.get_name() != "K":
                    opponent_pieces.append(piece)
                    opponent_valid_moves += piece.get_valid_moves((i, j))
        opponent_valid_moves = set(opponent_valid_moves)
        return pos in opponent_valid_moves


class Elephants(Piece):
    """
    Represents a Elephants class with a color and name. This class is the child class. Inherits all the methods and properties from Piece class.
    It starts one point forward, backward, left or right, and then moves two points outward diagonally.
    It can be blocked anywhere along this path.
    """

    def __init__(self, color, name, game):
        """Constructor for Elephants."""
        super().__init__(color, name, game)

        # Elephants' move
        self._UP_UP_LEFT_UP_LEFT = self._UP + self._UP_LEFT + self._UP_LEFT
        self._UP_UP_RIGHT_UP_RIGHT = self._UP + self._UP_RIGHT + self._UP_RIGHT
        self._DOWN_DOWN_LEFT_DOWN_LEFT = self._DOWN + self._DOWN_LEFT + self._DOWN_LEFT
        self._DOWN_DOWN_RIGHT_DOWN_RIGHT = self._DOWN + self._DOWN_RIGHT + self._DOWN_RIGHT
        self._LEFT_UP_LEFT_UP_LEFT = self._LEFT + self._UP_LEFT + self._UP_LEFT
        self._LEFT_DOWN_LEFT_DOWN_LEFT = self._LEFT + self._DOWN_LEFT + self._DOWN_LEFT
        self._RIGHT_UP_RIGHT_UP_RIGHT = self._RIGHT + self._UP_RIGHT + self._UP_RIGHT
        self._RIGHT_DOWN_RIGHT_DOWN_RIGHT = self._RIGHT + self._DOWN_RIGHT + self._DOWN_RIGHT

        # Elephants' all valid move
        self._directions = [self._UP_UP_LEFT_UP_LEFT] + [self._UP_UP_RIGHT_UP_RIGHT] + \
                           [self._DOWN_DOWN_LEFT_DOWN_LEFT] + [self._DOWN_DOWN_RIGHT_DOWN_RIGHT] + \
                           [self._LEFT_UP_LEFT_UP_LEFT] + [self._LEFT_DOWN_LEFT_DOWN_LEFT] + \
                           [self._RIGHT_UP_RIGHT_UP_RIGHT] + [self._RIGHT_DOWN_RIGHT_DOWN_RIGHT]


class Horses(Piece):
    """
    Represents a Horses class with a color and name. This class is the child class. Inherits all the methods and properties from Piece class.
    It can move one point forward, backward, left or right plus one point outward diagonally. If it is blocked, it can not move.
    """

    def __init__(self, color, name, game):
        """Constructor for Horses."""
        super().__init__(color, name, game)

        # Horses' move
        self._UP_UP_LEFT = self._UP + self._UP_LEFT
        self._UP_UP_RIGHT = self._UP + self._UP_RIGHT
        self._DOWN_DOWN_LEFT = self._DOWN + self._DOWN_LEFT
        self._DOWN_DOWN_RIGHT = self._DOWN + self._DOWN_RIGHT
        self._LEFT_UP_LEFT = self._LEFT + self._UP_LEFT
        self._LEFT_DOWN_LEFT = self._LEFT + self._DOWN_LEFT
        self._RIGHT_UP_RIGHT = self._RIGHT + self._UP_RIGHT
        self._RIGHT_DOWN_RIGHT = self._RIGHT + self._DOWN_RIGHT

        # Horses' all valid move
        self._directions = [self._UP_UP_LEFT] + [self._UP_UP_RIGHT] + \
                           [self._DOWN_DOWN_LEFT] + [self._DOWN_DOWN_RIGHT] + \
                           [self._LEFT_UP_LEFT] + [self._LEFT_DOWN_LEFT] + \
                           [self._RIGHT_UP_RIGHT] + [self._RIGHT_DOWN_RIGHT]


class Soldiers(Piece):
    """
    Represents a Soldiers class with a color and name. This class is the child class. Inherits all the methods and properties from Piece class.
    It can move one step, either forward of sideways. Within the fortress, the solider may also move forward along the diagonal lines.
    """
    def __init__(self, color, name, game):
        """Constructor for Soldiers."""
        super().__init__(color, name, game)
        if color == "B":
            self._directions = [self._UP] + [self._RIGHT] + [self._LEFT]
            # self.pos_to_additional_directions = {(2, 3): ["UP_RIGHT"], (2, 5): ["UP_LEFT"], (1, 4): ["UP_RIGHT", "UP_LEFT"]}
        if color == "R":
            self._directions = [self._DOWN] + [self._RIGHT] + [self._LEFT]
            # self.pos_to_additional_directions = {(7, 3): ["DOWN_RIGHT"], (7, 5): ["DOWN_LEFT"], (8, 4): ["DOWN_RIGHT", "DOWN_LEFT"]}

        # Soldier's special move
        if color == "B":
            self._special_directions = {
                (1, 4): [self._UP_RIGHT, self._UP_LEFT],
                (2, 3): [self._UP_RIGHT],
                (2, 5): [self._UP_LEFT],

            }
        else:
            self._special_directions = {
               (7, 3): [self._DOWN_RIGHT],
               (7, 5): [self._DOWN_LEFT],
               (8, 4): [self._DOWN_RIGHT, self._DOWN_LEFT],
            }


class FortressPiece(Piece):
    """
    Represents a FortressPiece class with a color and name. This class is the child class. Inherits all the methods and properties from Piece class.
    It is also the parent class of the General and Guards class which have the same moving rule and range.
    Must stay within the fortress. It moves one point along any printed line in the fortress. It can moves diagonally along the printed lines.
    """
    def __init__(self, color, name, game):
        """Constructor for General."""
        super().__init__(color, name, game)
        if color == "B":
            self._special_directions = {(7, 3): [self._RIGHT, self._DOWN, self._DOWN_RIGHT],
                               (7, 4): [self._LEFT, self._RIGHT, self._DOWN],
                               (7, 5): [self._LEFT, self._DOWN, self._DOWN_LEFT],
                               (8, 3): [self._UP, self._DOWN, self._RIGHT],
                               (8, 4): [self._UP, self._DOWN, self._RIGHT, self._LEFT,
                                        self._UP_RIGHT, self._UP_LEFT, self._DOWN_RIGHT, self._DOWN_LEFT],
                               (8, 5): [self._UP, self._DOWN, self._LEFT],
                               (9, 3): [self._UP, self._RIGHT, self._UP_RIGHT],
                               (9, 4): [self._UP, self._LEFT, self._RIGHT],
                               (9, 5): [self._UP, self._LEFT, self._UP_LEFT],
                               }
        else:
            self._special_directions = {(0, 3): [self._DOWN, self._RIGHT, self._DOWN_RIGHT],
                               (0, 4): [self._LEFT, self._DOWN, self._RIGHT],
                               (0, 5): [self._LEFT, self._DOWN, self._DOWN_LEFT],
                               (1, 3): [self._UP, self._DOWN, self._RIGHT],
                               (1, 4): [self._UP, self._DOWN, self._RIGHT, self._LEFT,
                                        self._DOWN_RIGHT, self._DOWN_LEFT, self._UP_RIGHT, self._UP_LEFT],
                               (1, 5): [self._UP, self._DOWN, self._LEFT],
                               (2, 3): [self._UP, self._RIGHT, self._UP_RIGHT],
                               (2, 4): [self._LEFT, self._UP, self._RIGHT],
                               (2, 5): [self._LEFT, self._UP, self._UP_LEFT],
                               }


class General(FortressPiece):
    """
    Represents a General class with a color and name. This class is the child class. Inherits all the methods and properties from FortressPiece class.
    Must stay within the fortress. It moves one point along any printed line in the fortress. It can moves diagonally along the printed lines.
    """
    def __init__(self, color, name, game):
        """Constructor for General."""
        super().__init__(color, name, game)


class Guards(FortressPiece):
    """
    Represents a Guard class with a color and name. This class is the child class. Inherits all the methods and properties from FortressPiece class.
    It moves exactly the same as the general, and is also confined to the fortress.
    """
    def __init__(self, color, name, game):
        """Constructor for Guards."""
        super().__init__(color, name, game)


class Chariots(Piece):
    """
    Represents a Chariots class with a color and name. This class is the child class. Inherits all the methods and properties from Piece class.
    Moves as many points as the max step in board. It can also move along the diagonal lines in the fortress.
    """
    def __init__(self, color, name, game):
        """Constructor for Chariots."""
        super().__init__(color, name, game)

        # Chariots' all possible directions
        self._directions = [self._UP] + [self._DOWN] + [self._LEFT] + [self._RIGHT]

        # Chariots' special move
        self._special_directions = {
            (7, 3): [self._DOWN_RIGHT],
            (7, 5): [self._DOWN_LEFT],
            (8, 4): [self._UP_RIGHT, self._UP_LEFT, self._DOWN_RIGHT, self._DOWN_LEFT],
            (9, 3): [self._UP_RIGHT],
            (9, 5): [self._UP_LEFT],
            (0, 3): [self._DOWN_RIGHT],
            (0, 5): [self._DOWN_LEFT],
            (1, 4): [self._DOWN_RIGHT, self._DOWN_LEFT, self._UP_RIGHT, self._UP_LEFT],
            (2, 3): [self._UP_RIGHT],
            (2, 5): [self._UP_LEFT],

        }

        # Chariots' max step
        self._max_step = 9
        self._special_max_step = 2


class Cannons(Piece):
    """
    Represents a Cannons class with a color and name. This class is the child class. Inherits all the methods and properties from Piece class.
    The cannon moves along any straight line, including the lines within the fortress, but must have one piece to jump over.
    It may not move without jumping. Also, it may not leap over another cannon, and may never capture another cannon.
    """
    def __init__(self, color, name, board):
        """Constructor for Cannons."""
        super().__init__(color, name, board)
        self._directions = [self._UP] + [self._DOWN] + [self._LEFT] + [self._RIGHT]

        # Cannons' special move
        self._special_directions = {
            (7, 3): [self._DOWN_RIGHT],
            (7, 5): [self._DOWN_LEFT],
            (9, 3): [self._UP_RIGHT],
            (9, 5): [self._UP_LEFT],
            (0, 3): [self._DOWN_RIGHT],
            (0, 5): [self._DOWN_LEFT],
            (2, 3): [self._UP_RIGHT],
            (2, 5): [self._UP_LEFT],
        }
        self._max_step = max(self._num_rows, self._num_cols)
        self._special_max_step = 2

    def get_valid_moves(self, pos):
        """Get all valid moves."""
        valid_moves = []
        from_row, from_col = pos
        piece_from = self._board[from_row][from_col]

        max_steps = [self._max_step] * len(self._directions)
        bounds = [((0, 0), (self._num_rows-1, self._num_cols-1))] * len(self._directions)
        directions = self._directions[:]

        if pos in self._special_directions:
            directions += self._special_directions[pos]
            max_steps += [self._special_max_step] * len(self._special_directions)
            if self._color == "B":
                bounds += [((7, 3), (9, 5))] * len(self._special_directions)
            else:
                bounds += [((0, 3), (2, 5))] * len(self._special_directions)

        # start to check every move is invalid or not
        for i, direction in enumerate(directions):
            has_encountered = False
            max_step = max_steps[i]
            top_left, bottom_right = bounds[i]
            top_row, left_col = top_left
            bottom_row, right_col = bottom_right
            for step in range(1, max_step+1):
                pos = (pos[0] + direction[0][0], pos[1] + direction[0][1])
                # if it is out of range
                if pos[0] < top_row or pos[0] >= bottom_row or pos[1] < left_col or pos[1] >= right_col:
                    break

                piece = self._board[pos[0]][pos[1]]
                if not has_encountered:
                    if piece:
                        # if the first encountered piece is Cannon, cannot jump
                        if piece.get_name() == "A":
                            break
                        has_encountered = True
                else:
                    if not piece:
                        valid_moves.append(pos)
                    else:
                        if not (piece.get_color() == piece_from.get_color() or piece.get_name() == "A"):
                            valid_moves.append(pos)
                        break
            pos = (from_row, from_col)  # reset position
        return valid_moves
