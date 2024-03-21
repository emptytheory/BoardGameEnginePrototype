class HexHexGameTemplate:
	NONE = -1
	EMPTY = 0
	BLACK = 1
	WHITE = 2
	DIRECTIONS = [(0,1), (1,0), (-1,0), (0,-1), (1,-1), (-1,1)]

	# As it stands, all of this happens every time an instance of this class is made.
	# It is not possible to overload methods in Python.
	# One solution is to make it conditional on the arguments passed.
	# Another is to make a separate initialization method that must be called manually
	def __init__(self, side_length):
		self.SIDE_LENGTH = side_length
		self.LINE_LENGTH = 2 * side_length - 1
		self.CENTER_LINE_INDEX = side_length - 1
		# Array of cells. Each cell is a tuple (state=NONE|EMPTY|BLACK|WHITE, group_ID=NONE|nonnegative int)
		self.board = [
			(self.NONE, self.NONE) if self._is_off_board(index) else (self.EMPTY, self.NONE) 
			for index in range(self.LINE_LENGTH * self.LINE_LENGTH)
		]
		# Adjacency list for valid indices only. Should never be deep copied.
		self.adjacency_list = self._create_adjacency_list()

	def _create_adjacency_list(self):
		result = {}
		# Map valid indices to empty lists initially
		for i, (state, _) in enumerate(self.board):
			if state != self.NONE:
				result[i] = []

		# Populate the lists with valid neighbors		
		valid_indices = result.keys()
		for i in valid_indices:
			for dx, dy in self.DIRECTIONS:
				new_column_i = self._column_index(i) + dx
				new_row_i = self._row_index(i) + dy
				new_i = self._index_from_column_and_row_indices(new_column_i, new_row_i)

				if new_i in valid_indices:
					result[i].append(new_i)
		
		return result

	def _column_index(self, index):
		return index % self.LINE_LENGTH

	def _row_index(self, index):
		return index // self.LINE_LENGTH

	def _is_off_board(self, index):
		return (abs(self._x(index)) >= self.SIDE_LENGTH or
				abs(self._y(index)) >= self.SIDE_LENGTH or
				abs(self._z(index)) >= self.SIDE_LENGTH)

	def _x(self, index):
		return self._column_index(index) - self.CENTER_LINE_INDEX

	def _y(self, index):
		return self._row_index(index) - self.CENTER_LINE_INDEX

	def _z(self, index):
		return -self._x(index) - self._y(index)

	def _index_from_column_and_row_indices(self, column_index, row_index):
		return column_index + (self.LINE_LENGTH * row_index)

	def _index_from_xy(self, x, y):
		return self._index_from_column_and_row_indices(x + self.CENTER_LINE_INDEX, y + self.CENTER_LINE_INDEX)

	def _valid_line_index(self, index):
		return 0 <= index < self.LINE_LENGTH

	def even_neighbors(self, index, owner):
		unique_group_ids = set()

		# Iterate through each direction from the current position
		for neighbor in self.adjacency_list[index]:

				# Check if the cell belongs to the specified owner
				cell_state, group_id = board[neighbor]
				if cell_state == owner:
					unique_group_ids.add(group_id)

		# Return True if the count of unique group IDs is even, False otherwise
		return len(unique_group_ids) % 2 == 0

	def __str__(self):
		result = ""

		for i, (state, _) in enumerate(self.board[::-1]):
			# print row offset
			if self._column_index(i) == 0:
				result += "   " * self._row_index(i)
			# print cell state
			if state == self.NONE:
				result += "      "
			else:
				result += f"{state:02d}    "
			# line break after last column
			if self._column_index(i) == self.LINE_LENGTH - 1:
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