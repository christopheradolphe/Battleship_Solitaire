from copy import deepcopy
from heapq import heappush, heappop
import heapq  
import argparse

#====================================================================================
no_hint = '0'
submarine = 'S'
water = '.'
horizontal_ship_left = '<'
horizontal_ship_right = '>'
vertical_ship_top = '^'
vertical_ship_bottom = 'v'
middle_ship = 'M'
ship_piece = 'p'

class Board:
    """
    Board class for setting up the playing board.
    """

    def __init__(self, input_filename):
        """
        :param input_filename: String that is name of document that holds the original board position
        :type input_filename: String
        """
        #Actual Code:
        puzzle_file = open(input_filename, "r")
        line_index = 0
        self.row_constraints = []
        self.column_constraints = []
        self.ship_constraints = []
        self.grid = []
        
        for line in puzzle_file:
            if line_index == 0: 
              for x, ch in enumerate(line):
                if ch != '\n':
                  self.row_constraints.append(ch)
            elif line_index == 1: 
              for x, ch in enumerate(line):
                if ch != '\n':
                  self.column_constraints.append(ch)
            elif line_index == 2:
              for x, ch in enumerate(line):
                if ch != '\n':
                  self.ship_constraints.append(ch)
            else:
              row = []
              for x, ch in enumerate(line):
                if ch != '\n':
                  row.append(ch)
              self.grid.append(row)
            line_index += 1
        self.width = len(self.column_constraints)
        self.height = len(self.row_constraints)
        self.allowable_indicies = []
        for i in range(self.width):
            self.allowable_indicies.append(i)
            self.row_constraints[i] = int(self.row_constraints[i])
            self.column_constraints[i] = int(self.column_constraints[i])
        for j in range(len(self.ship_constraints)):
            self.ship_constraints[j] = int(self.ship_constraints[j])
        self.columns_count = [0] * self.width
        self.rows_count = [0] * self.height

        self.pre_process_board()
        # self.grid is a 2-d (size * size) array automatically generated
        # using the information on the pieces when a board is being created.
        # A grid contains the symbol for representing the pieces on the board.
        (self.m_ind, self.v_ind, self.top_ind, self.right_ind, self.left_ind) = self.__modify_grid()
        self.display()

    #     #Debugging
    # def __init__(self, board, row_constraints, column_constraints, ship_constraints):
    #       """
    #       :param pieces: The list of Pieces
    #       :type pieces: List[Piece]
    #       """
    #       self.row_constraints = row_constraints
    #       self.column_constraints = column_constraints
    #       self.ship_constraints = ship_constraints
    #       self.grid = board

    #       self.width = len(self.column_constraints)
    #       self.height = len(self.row_constraints)
    #       self.allowable_indicies = []
    #       for i in range(self.width):
    #         self.allowable_indicies.append(i)
    #         self.row_constraints[i] = int(self.row_constraints[i])
    #         self.column_constraints[i] = int(self.column_constraints[i])
    #       for j in range(len(self.ship_constraints)):
    #         self.ship_constraints[j] = int(self.ship_constraints[j])
    #       self.columns_count = [0] * self.width
    #       self.rows_count = [0] * self.height
    #       self.pre_process_board()
    #       self.__modify_grid()
          



    def __modify_grid(self):
        """
        Called in __init__ to set up a 2-d grid based on the piece location information.

        """
        m_constraint_indicies = []
        v_constraint_indicies = []
        top_constraint_indicies = []
        right_constraint_indicies = []
        left_constraint_indicies = []
        for i in range(self.height):
            for j in range(self.width):
                piece = self.grid[i][j]
                if piece in [submarine, horizontal_ship_left, horizontal_ship_right, vertical_ship_top, vertical_ship_bottom, middle_ship]:
                  self.grid[i][j] = ship_piece
                  self.rows_count[i] += 1
                  self.columns_count[j] += 1
                  if piece == horizontal_ship_left:
                    left_constraint_indicies.append((i,j))
                  #   self.grid[i][j+1] = ship_piece
                  #   self.water_diag_lower_right(i,j+1)
                  #   self.water_diag_upper_right(i,j+1)
                  elif piece == horizontal_ship_right:
                    right_constraint_indicies.append((i,j))
                  #   self.grid[i][j-1] = ship_piece
                  #   self.water_diag_lower_left(i,j-1)
                  #   self.water_diag_upper_left(i,j-1)
                  elif piece == vertical_ship_bottom:
                    v_constraint_indicies.append((i,j))
                  #   self.grid[i-1][j] = ship_piece
                  #   self.water_diag_upper_left(i-1,j)
                  #   self.water_diag_upper_right(i-1,j)
                  elif piece == vertical_ship_top:
                    top_constraint_indicies.append((i,j))
                  #   self.grid[i+1][j] = ship_piece
                  #   self.water_diag_lower_left(i+1,j)
                  #   self.water_diag_lower_right(i+1,j)
                  if piece == middle_ship:
                    m_constraint_indicies.append((i,j))
                  else:
                    pass
        return (m_constraint_indicies, v_constraint_indicies, top_constraint_indicies, right_constraint_indicies, left_constraint_indicies)

    
    def water(self, coord_y, coord_x):
      if coord_y in self.allowable_indicies and coord_x in self.allowable_indicies:
        if self.grid[coord_y][coord_x] == no_hint:
          self.grid[coord_y][coord_x] = water
          return True
      return False

    def water_right(self, coord_y, coord_x):
      return self.water(coord_y, coord_x+1)
    
    def water_left(self, coord_y, coord_x):
      return self.water(coord_y, coord_x-1)

    def water_above(self, coord_y, coord_x):
      return self.water(coord_y-1, coord_x)
    
    def water_below(self, coord_y, coord_x):
      return self.water(coord_y+1, coord_x)

    def water_diag_upper_right(self, coord_y, coord_x):
      return self.water(coord_y-1, coord_x+1)
    
    def water_diag_upper_left(self, coord_y, coord_x):
      return self.water(coord_y-1, coord_x-1)
    
    def water_diag_lower_right(self, coord_y, coord_x):
      return self.water(coord_y+1, coord_x+1)
    
    def water_diag_lower_left(self, coord_y, coord_x):
      return self.water(coord_y+1, coord_x-1)
                
    def pre_process_board(self):
      for i in range(self.height):
        for j in range(self.width):
          if self.grid[i][j] == submarine:
            self.water_right(i,j)
            self.water_left(i,j)
            self.water_above(i,j)
            self.water_below(i,j)
          elif self.grid[i][j] in [horizontal_ship_left, horizontal_ship_right]:
            self.water_above(i,j)
            self.water_below(i,j)
            if self.grid[i][j] == horizontal_ship_left:
              self.water_left(i,j)
            else:
              self.water_right(i,j)
          elif self.grid[i][j] in [vertical_ship_top, vertical_ship_bottom]:
            self.water_left(i,j)
            self.water_right(i,j)
            if self.grid[i][j] == vertical_ship_top:
              self.water_above(i,j)
            else:
              self.water_below(i,j)
          else:
            pass
          if self.grid[i][j] in [submarine, horizontal_ship_left, horizontal_ship_right, vertical_ship_top, vertical_ship_bottom, middle_ship]:
            self.water_diag_upper_right(i,j)
            self.water_diag_upper_left(i,j)
            self.water_diag_lower_right(i,j)
            self.water_diag_lower_left(i,j)
      return
    

    def empty_slots(self):
        """
        Finds all empty spaces in the board. Returns list of tuples in form of [(x1,y1), (x2,y2)]

        :return: List of tuples containing coordinates of empty piecies
        :rtype: List[Tuples]
        """
        empty = []
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] == "0":
                    empty.append((i,j))
        return empty
    
    def empty_slots_row(self, row_index):
      slots_count = 0
      for i in range(self.width):
        if self.grid[row_index][i] == "0":
            slots_count += 1
      return slots_count
    
    def empty_slots_column(self, row_index):
      slots_count = 0
      for i in range(self.height):
        if self.grid[i][row_index] == "0":
            slots_count += 1
      return slots_count
  
    def display(self):
        """
        Print out the current board.

        """
        for i, line in enumerate(self.grid):
            for ch in line:
                print(ch, end='')
            print()
    
    def iterative_ship_size_finder(self, coord_y, coord_x, x_dir):
      size = 0
      while coord_y in self.allowable_indicies and coord_x in self.allowable_indicies:
        if self.grid[coord_y][coord_x] == ship_piece:
          size += 1
          if x_dir:
            coord_x += 1
          else:
            coord_y += 1
        else:
          break
      return size

    
    def vertical_ship_size_finder(self, coord_y, coord_x):
      return self.iterative_ship_size_finder(coord_y, coord_x, False)

    def horizontal_ship_size_finder(self, coord_y, coord_x):
      return self.iterative_ship_size_finder(coord_y, coord_x, True)
    
    def ship_size_finder(self, coord_y, coord_x):
      horizontal_size = self.horizontal_ship_size_finder(coord_y, coord_x)
      vertical_size = self.vertical_ship_size_finder(coord_y, coord_x)
      if horizontal_size > 1 and vertical_size > 1:
        return (0, False)
      return (max(horizontal_size, vertical_size), horizontal_size < vertical_size)
    
    def ship_counter(self):
      ship_count = [0] * 4
      explored = []
      for i in range(self.height):
        for j in range(self.width):
          if (i,j) not in explored:
            if self.grid[i][j] == ship_piece:
              (size, down) = self.ship_size_finder(i,j)
              if size == 0 or size > 4:
                return None
              ship_count[size-1] += 1
              explored.append((i,j))
              if down:
                for k in range(1, size):
                  explored.append((i+k, j))
              else:
                for k in range(1, size):
                  explored.append((i, j+k))
      return ship_count
    
    def ship_count_check(self):
      ship_numbers = self.ship_counter()
      if ship_numbers == None:
        return False
      check1 = ship_numbers[3] <= self.ship_constraints[3]
      check2 = sum(ship_numbers[2:]) <= sum(self.ship_constraints[2:])
      check3 = sum(ship_numbers[1:]) <= sum(self.ship_constraints[1:])
      check4 = sum(ship_numbers) <= sum(self.ship_constraints)
      return check1 and check2 and check3 and check4
      
    
    def row_constraint_check(self):
      for i in range(self.height):
        if self.row_constraints[i] < self.rows_count[i]:
          return False
      return True
    
    def column_constraint_check(self):
      for i in range(self.width):
        if self.column_constraints[i] < self.columns_count[i]:
          return False
      return True
    
    def ur_check(self, coord_y, coord_x):
      if (coord_y-1) in self.allowable_indicies and (coord_x+1) in self.allowable_indicies:
        return self.grid[coord_y-1][coord_x+1] in [no_hint, water]
      return True
    
    def ul_check(self, coord_y, coord_x):
      if (coord_y-1) in self.allowable_indicies and (coord_x-1) in self.allowable_indicies:
        return self.grid[coord_y-1][coord_x-1] in [no_hint, water]
      return True

    def dr_check(self, coord_y, coord_x):
      if (coord_y+1) in self.allowable_indicies and (coord_x+1) in self.allowable_indicies:
        return self.grid[coord_y+1][coord_x+1] in [no_hint, water]
      return True
    
    def dl_check(self, coord_y, coord_x):
      if (coord_y+1) in self.allowable_indicies and (coord_x-1) in self.allowable_indicies:
        return self.grid[coord_y+1][coord_x-1] in [no_hint, water]
      return True
    
    def diagonals_no_piece_check(self, coord_y, coord_x):
      return self.ur_check(coord_y, coord_x) and self.ul_check(coord_y, coord_x) and self.dr_check(coord_y, coord_x) and self.dl_check(coord_y, coord_x)
    
    def above_occupied_check(self, coord_y, coord_x):
      if (coord_y-1) in self.allowable_indicies:
        return self.grid[coord_y-1][coord_x] == ship_piece
      return False
    
    def below_occupied_check(self, coord_y, coord_x):
      if (coord_y+1) in self.allowable_indicies:
        return self.grid[coord_y+1][coord_x] == ship_piece
      return False

    def verticals_occupied_check(self, coord_y, coord_x):
      return self.above_occupied_check(coord_y, coord_x) or self.below_occupied_check(coord_y, coord_x)
    
    def right_occupied_check(self, coord_y, coord_x):
      if (coord_x+1) in self.allowable_indicies:
        return self.grid[coord_y][coord_x+1] == ship_piece
      return False
    
    def left_occupied_check(self, coord_y, coord_x):
      if (coord_x-1) in self.allowable_indicies:
        return self.grid[coord_y][coord_x-1] == ship_piece
      return False

    def horizontals_occupied_check(self, coord_y, coord_x):
      return self.right_occupied_check(coord_y, coord_x) or self.left_occupied_check(coord_y, coord_x)
    
    def check_surroundings(self, coord_y, coord_x):
      if not self.diagonals_no_piece_check(coord_y, coord_x):
        return False
      if self.verticals_occupied_check(coord_y, coord_x) and self.horizontals_occupied_check(coord_y, coord_x):
        return False
      return True
    
    def surrounded_by_water_check(self):
      for i in range(self.height):
        for j in range(self.width):
          if self.grid[i][j] == ship_piece:
            if not self.check_surroundings(i,j):
              return False
      return True
    
    def enough_ship_places_left(self):
      ships_total = sum(self.row_constraints)
      ships_on_board = sum(self.rows_count)
      potential_ship_slots = len(self.empty_slots())
      return (ships_on_board + potential_ship_slots) >= ships_total
    
    def enough_ship_places_left_columns(self):
      for i in range(self.height):
        ships_total = self.column_constraints[i]
        ships_on_board = self.columns_count[i]
        potential_ship_slots = self.empty_slots_column(i)
        if not ((ships_on_board + potential_ship_slots) >= ships_total):
          return False
      return True
    
    def enough_ship_places_left_rows(self):
      for i in range(self.width):
        ships_total = self.row_constraints[i]
        ships_on_board = self.rows_count[i]
        potential_ship_slots = self.empty_slots_row(i)
        if not ((ships_on_board + potential_ship_slots) >= ships_total):
          return False
      return True
    
    def m_surroundings(self):
      for m in self.m_ind:
        above = self.grid[m[0]-1][m[1]] in [no_hint, ship_piece]
        below = self.grid[m[0]+1][m[1]] in [no_hint, ship_piece]
        left = self.grid[m[0]][m[1]-1] in [no_hint, ship_piece]
        right = self.grid[m[0]][m[1]+1] in [no_hint, ship_piece]
        if not ((above and below) or (right and left)):
          return False
      return True
    
    def v_surroundings(self):
      for v in self.v_ind:
        above = self.grid[v[0]-1][v[1]] in [no_hint, ship_piece]
        if not above:
          return False
      return True
    
    def top_surroundings(self):
      for top in self.top_ind:
        below = self.grid[top[0]+1][top[1]] in [no_hint, ship_piece]
        if not below:
          return False
      return True
    
    def left_surroundings(self):
      for left in self.left_ind:
        right = self.grid[left[0]][left[1]+1] in [no_hint, ship_piece]
        if not right:
          return False
      return True
    
    def right_surroundings(self):
      for right in self.right_ind:
        left = self.grid[right[0]][right[1]-1] in [no_hint, ship_piece]
        if not left:
          return False
      return True
    
    def constraints_check(self):
      check1 = self.ship_count_check()
      check2 = self.row_constraint_check()
      check3 = self.column_constraint_check()
      check4 = self.surrounded_by_water_check()
      check5 = self.enough_ship_places_left()
      check6 = self.enough_ship_places_left_columns()
      check7 = self.enough_ship_places_left_rows()
      check8 = self.m_surroundings()
      check9 = self.v_surroundings()
      check10 = self.top_surroundings()
      check11 = self.left_surroundings()
      check12 = self.right_surroundings()
      return check1 and check2 and check3 and check4 and check5 and check6 and check7 and check8 and check9 and check10 and check11 and check12
    

    def row_constraint_final_check(self):
      return self.row_constraints == self.rows_count
    
    def column_constraint_final_check(self):
      return self.column_constraints == self.columns_count
    
    def ship_count_final_check(self):
      ship_numbers = self.ship_counter()
      if ship_numbers == None:
        return False
      return ship_numbers == self.ship_constraints

    
    def proper_solution(self):
      for i in range(self.width):
        for j in range(self.height):
          if self.grid[i][j] == no_hint:
            return False
      check1 = self.ship_count_final_check()
      check2 = self.row_constraint_final_check()
      check3 = self.column_constraint_final_check()
      check4 = self.surrounded_by_water_check()
      return check1 and check2 and check3 and check4
    
    def symbolize_board(self):
      explored = []
      for i in range(self.height):
        for j in range(self.width):
          if (i,j) not in explored:
            if self.grid[i][j] == ship_piece:
              (size, down) = self.ship_size_finder(i,j)
              if size == 1:
                self.grid[i][j] = submarine
              if size > 1:
                if down:
                  self.grid[i][j] = vertical_ship_top
                  self.grid[i+size-1][j] = vertical_ship_bottom
                  for k in range(1,size-1):
                      self.grid[i+k][j] = middle_ship
                else:
                  self.grid[i][j] = horizontal_ship_left
                  self.grid[i][j+size-1] = horizontal_ship_right
                  for k in range(1,size-1):
                      self.grid[i][j+k] = middle_ship
      return
    

    def output(self, file):
        """
        Prints all parents of a current state to a file.

        :param state: The current state of which we are printing its parents.
        :type filename: State class
        :param file: The name of the given file to print the moves.
        :type filename: str
        :return: Nothing
        :rtype: None
        """

        output_file = open(file, "w")
        self.symbolize_board()
        for i in range(self.height):
          for j in range(self.width):
              output_file.write(self.grid[i][j])
          output_file.write("\n")

    def place_water(self, coord_y, coord_x):
      if coord_y in self.allowable_indicies and coord_x in self.allowable_indicies:
        if self.grid[coord_y][coord_x] == ship_piece:
          return False
        else:
          self.grid[coord_y][coord_x] = water
      return True

    def place_water_ur(self, coord_y, coord_x):
      return self.place_water(coord_y-1, coord_x+1)
    
    def place_water_ul(self, coord_y, coord_x):
        return self.place_water(coord_y-1, coord_x-1)
    
    def place_water_dr(self, coord_y, coord_x):
      return self.place_water(coord_y+1, coord_x+1)
    
    def place_water_dl(self, coord_y, coord_x):
        return self.place_water(coord_y+1, coord_x-1)
      

class State:
    """
    State class wrapping a Board with some extra current state information.
    Note that State and Board are different. Board has the locations of the pieces. 
    State has a Board and some extra information that is relevant to the search: 
    heuristic function, f value, current depth and parent.
    """

    def __init__(self, board, empty_slots, parent=None):
        """
        :param board: The board of the state.
        :type board: Board
        :param parent: The parent of current state.
        :type parent: Optional[State]
        """
        self.board = board
        self.parent = parent
        self.cur_domain = [ship_piece, water]
        self.empty_slots = empty_slots
        self.var = None

    def backtracking_search(self):
      #Complete Backtrack Search
      if not self.board.proper_solution():
        self.var = self.empty_slots[0]
        for val in self.cur_domain:
          valid, new_board = self.assign(self.var, val)
          if new_board.constraints_check() and valid:
            state = State(new_board, new_board.empty_slots(), self)
            result = state.backtracking_search()
            if result != None:
              return result
        return None
      return self.board
    
    def assign(self, var, val):
      valid = True
      new_board = deepcopy(self.board)
      new_board.grid[var[0]][var[1]] = val
      if val == ship_piece:
        new_board.columns_count[var[1]] += 1
        new_board.rows_count[var[0]] += 1
        p1 = new_board.place_water_ur(var[0], var[1])
        p2 = new_board.place_water_ul(var[0], var[1])
        p3 = new_board.place_water_dr(var[0], var[1])
        p4 = new_board.place_water_dl(var[0], var[1])
        valid = p1 and p2 and p3 and p4
      return (valid, new_board)




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzle."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    starting_board = Board(args.inputfile)


    starting_state = State(starting_board, starting_board.empty_slots())
    final_board = starting_state.backtracking_search()
    final_board.output(args.outputfile)

    # #Debugging
    # board = [
    #             ['0', '0', '0', '.', '0', '0'],
    #             ['0', '0', '0', '0', '0', '0'],
    #             ['0', '0', '0', '0', '0', '0'],
    #             ['0', '0', '0', '0', '0', '0'],
    #             ['0', '<', '0', '0', '0', '0'],
    #             ['0', '0', '0', '0', '0', '0']]
    
    # row_constraints = ['1', '3', '3', '0', '3', '1']
    # column_constraints = ['1', '1', '2', '1', '3', '2']
    # ship_constraints = ['3', '2', '1', '0']
    # starting_board = Board(board, row_constraints, column_constraints, ship_constraints)
    
    # starting_state = State(starting_board, starting_board.empty_slots())
    # final_board = starting_state.backtracking_search()
    # final_board.output("solutions.txt")

    
    # checkers_solve(starting_state, 'output.txt')
    
