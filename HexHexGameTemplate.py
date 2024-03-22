class HexHexTopology:	
	DIRECTIONS = [(0,1), (1,0), (-1,0), (0,-1), (1,-1), (-1,1)]

	def __init__(self, side_length):
		self.SIDE_LENGTH = side_length
		self.LINE_LENGTH = 2 * side_length - 1
		self.CENTER_LINE_INDEX = side_length - 1

		# Adjacency list for valid indices only
		self.adjacency_list = self._create_adjacency_list()

	def _create_adjacency_list(self):
		result = {}
		# Map valid indices to empty lists initially
		for i in range(self.LINE_LENGTH * self.LINE_LENGTH):
			if not self.is_off_board(i):
				result[i] = []

		# Populate the lists with valid neighbors		
		valid_indices = result.keys()
		for i in valid_indices:
			for dx, dy in self.DIRECTIONS:
				new_column_i = self.column_index(i) + dx
				new_row_i = self.row_index(i) + dy
				new_i = self.index_from_column_and_row_indices(new_column_i, new_row_i)

				if new_i in valid_indices:
					result[i].append(new_i)
		
		return result

	def column_index(self, index):
		return index % self.LINE_LENGTH

	def row_index(self, index):
		return index // self.LINE_LENGTH

	def is_off_board(self, index):
		return (abs(self.x(index)) >= self.SIDE_LENGTH or
				abs(self.y(index)) >= self.SIDE_LENGTH or
				abs(self.z(index)) >= self.SIDE_LENGTH)

	def x(self, index):
		return self.column_index(index) - self.CENTER_LINE_INDEX

	def y(self, index):
		return self.row_index(index) - self.CENTER_LINE_INDEX

	def z(self, index):
		return -self.x(index) - self.y(index)

	def index_from_column_and_row_indices(self, column_index, row_index):
		return column_index + (self.LINE_LENGTH * row_index)

	def index_from_xy(self, x, y):
		return self.index_from_column_and_row_indices(x + self.CENTER_LINE_INDEX, y + self.CENTER_LINE_INDEX)

	def valid_line_index(self, index):
		return 0 <= index < self.LINE_LENGTH

class HexHexGameTemplate:
	NONE = -1
	EMPTY = 0
	BLACK = 1
	WHITE = 2

	# Sets the initial state and sets up the topology facts
	# Must be called only once, and not from the copies
	def init(self, side_length):
		self.top = HexHexTopology(side_length)
		# Array of cells. Each cell is a tuple (state=NONE|EMPTY|BLACK|WHITE, group_ID=NONE|nonnegative int)
		self.board = [
			(self.NONE, self.NONE) if self.top.is_off_board(index) else (self.EMPTY, self.NONE) 
			for index in range(self.top.LINE_LENGTH * self.top.LINE_LENGTH)
		]
		self.mover = self.BLACK

	# Should return a deep copy of the state and a reference to the "immutable" topology object.
	def copy(self):
		other = self.__class__()

		# copy reference only
		other.top = self.top

		# deep copy
		other.mover = self.mover
		other.board = [(state, group_ID) for (state, group_ID) in self.board]
		return other

	def count_moves(self, mover):
		return len([i for i in self.top.adjacency_list.keys() if self.board[i][0] == self.EMPTY and 
   																 self._even_neighbors(i, mover)])
	
	def apply_nth_move(self, n):
		return

	def get_mover(self):
		return self.mover

	def get_nonmover(self):
		return (self.BLACK + self.WHITE) - self.mover

	def _even_neighbors(self, index, owner):
		unique_group_ids = set()

		# Iterate through each direction from the current position
		for neighbor in self.top.adjacency_list[index]:

				# Check if the cell belongs to the specified owner
				cell_state, group_id = self.board[neighbor]
				if cell_state == owner:
					unique_group_ids.add(group_id)

		# Return True if the count of unique group IDs is even, False otherwise
		return len(unique_group_ids) % 2 == 0
	
	# def print_all_moves(self):
	## prints all legal moves for the active player in the current state

	# def print_move_n(self, n):
	## prints move number n

	# Accidentally mirrors the board, so not correctly implemented
	# Need to only flip across the horizontal axis, corrently flips across both
	# That is, I need to reverse each column individually, not the entire array
	def __str__(self):
		result = ""

		for i, (state, _) in enumerate(self.board[::-1]):
			# print row offset
			if self.top.column_index(i) == 0:
				result += "   " * self.top.row_index(i)
			# print cell state
			if state == self.NONE:
				result += "      "
			else:
				result += f"{state:02d}    "
			# line break after last column
			if self.top.column_index(i) == self.top.LINE_LENGTH - 1:
				result += "\n\n"

		return result


"""
Example of the array of a hexhex 4 board:
42  43  44  45  --  --  --
35  36  37  38  39  --  --
28  29  30  31  32  33  --
21  22  23  24  25  26  27
--  15  16  17  18  19  20
--  --  09  10  11  12  13
--  --  --  03  04  05  06

UCT interface:
- how many moves are available?
- play the Nth move
- has someone won?

Regarding keeping track of group Ids:
max number of groups: self.SIDE_LENGTH * (self.SIDE_LENGTH - 1) + 2
Could simply use self.SIDE_LENGTH * self.SIDE_LENGTH for simplicity.
But the point is that I can use the knowledge of the maximum number of digits in the group ID.


max_number_of_groups = self.SIDE_LENGTH * (self.SIDE_LENGTH - 1) + 2
self.SHIFT_MULTIPLIER = 10 * len(str(max_number_of_groups))

Could encode the state and group ID in an int or short
two bits encode
00 = OFF
01 = EMPTY
10 = BLACK
11 = WHITE

And group ID.
group_ID 0 means no stone here

Note from my 'mentor':
Precompute EVERYTHING!
So precompute neighbors and the index-coordinate map.
"""