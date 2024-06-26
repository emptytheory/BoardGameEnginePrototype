class HexHexTopology:	
	DIRECTIONS = [(0,1), (1,0), (-1,0), (0,-1), (1,-1), (-1,1)]

	def __init__(self, side_length):
		self.SIDE_LENGTH = side_length
		self.LINE_LENGTH = 2 * side_length - 1
		self.CENTER_LINE_INDEX = side_length - 1

		# Adjacency list for valid indices only
		self.adjacency_list = self._create_adjacency_list()
		self.coordinate_map = self._create_coordinate_map(self.adjacency_list.keys())

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
				new_x = self.x(i) + dx
				new_y = self.y(i) + dy
				new_i = self.index_from_xy(new_x, new_y)

				if new_i in valid_indices:
					result[i].append(new_i)
		
		return result

	def column_index(self, index):
		return index % self.LINE_LENGTH

	def row_index(self, index):
		return index // self.LINE_LENGTH
	
	def _create_coordinate_map(self, index_set):
		alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
		result = {}
		for i in index_set:
			letter_i = self.column_index(i) % len(alphabet)
			number = self.row_index(i) + 1
			result[i] = f"{alphabet[letter_i]}{number}"
		return result

	def is_off_board(self, index):
		return (abs(self.x(index)) >= self.SIDE_LENGTH or
				abs(self.y(index)) >= self.SIDE_LENGTH or
				abs(self.z(index)) >= self.SIDE_LENGTH)

	def x(self, index):
		return self.column_index(index) - self.CENTER_LINE_INDEX

	def y(self, index):
		return self.row_index(index) - self.column_index(index)

	def z(self, index):
		return -self.x(index) - self.y(index)

	def index_from_column_and_row_indices(self, column_index, row_index):
		return column_index + (self.LINE_LENGTH * row_index)

	def index_from_xy(self, x, y):
		return self.index_from_column_and_row_indices(x + self.CENTER_LINE_INDEX, y + x + self.CENTER_LINE_INDEX)
	

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
		# It would probably be faster if these weren't immutable
		self.board = [
			(self.NONE, self.NONE) if self.top.is_off_board(index) else (self.EMPTY, self.NONE) 
			for index in range(self.top.LINE_LENGTH * self.top.LINE_LENGTH)
		]
		self.mover = self.BLACK
		self.next_group_ID = 1

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
   																 len(self._friendly_adjacent_group_IDs(i, mover)) % 2 == 0])
	
	def apply_nth_move(self, n):
		# this is currently repeated in count moves and here, but should be optimized
		chosen_move = [i for i in self.top.adjacency_list.keys() if self.board[i][0] == self.EMPTY and 
   																 len(self._friendly_adjacent_group_IDs(i, self.get_mover())) % 2 == 0][n]
		self._update_group_IDs(chosen_move)
		self.mover = self.get_nonmover()

	def get_mover(self):
		return self.mover

	def get_nonmover(self):
		return (self.BLACK + self.WHITE) - self.mover

	def _friendly_adjacent_group_IDs(self, index, owner):
		unique_group_ids = set()

		# Iterate through each direction from the current position
		for neighbor in self.top.adjacency_list[index]:

				# Check if the cell belongs to the specified owner
				cell_state, group_id = self.board[neighbor]
				if cell_state == owner:
					unique_group_ids.add(group_id)

		# Return True if the count of unique group IDs is even, False otherwise
		return unique_group_ids
	
	# should only be called afer a legal placement and therefore
	# only when there are 0 or 2 friendly adjacent groups
	def _update_group_IDs(self, last_to):
		neighbor_set = self._friendly_adjacent_group_IDs(last_to, self.get_mover())

		if len(neighbor_set) == 0:
			self.board[last_to] = (self.get_mover(), self.next_group_ID)
			self.next_group_ID += 1
			return
		
		new_ID = min(neighbor_set)
		old_ID = max(neighbor_set)
		self.board[last_to] = (self.get_mover(), new_ID)
		for i, (state, ID) in enumerate(self.board):
			if ID == old_ID:
				self.board[i] = state, new_ID

	def print_all_moves(self):
		moves = [self.top.coordinate_map[i] for i in self.top.adjacency_list.keys() 
		   		    if self.board[i][0] == self.EMPTY and 
				    len(self._friendly_adjacent_group_IDs(i, self.get_mover)) % 2 == 0]
		for i, move in enumerate(moves):
			print(f"{i}: {move}")

	def print_move_n(self, n):
		moves = [i for i in self.top.adjacency_list.keys() 
		   		    if self.board[i][0] == self.EMPTY and 
				    len(self._friendly_adjacent_group_IDs(i, self.get_mover)) % 2 == 0]
		print(f"{n}: {self.top.coordinate_map[moves[n]]}")

	def __str__(self):
		result = ""

		for row_i in range(self.top.LINE_LENGTH-1, -1, -1):
			result += "   " * ((self.top.LINE_LENGTH - 1) - row_i)
			for column_i in range(self.top.LINE_LENGTH):
				i = self.top.index_from_column_and_row_indices(column_i, row_i)
				state, _ = self.board[i]
				if state == self.NONE:
					result += "      "
				else:
					result += f"{state:02d}    "
			result += "\n\n"

		return result


"""
Example of the array of a hexhex 4 board:
--  --  --  45  46  47  48
--  --  37  38  39  40  41
--  29  30  31  32  33  34
21  22  23  24  25  26  27
14  15  16  17  18  19  --
07  08  09  10  11  --  --
00  01  02  03  --  --  --





Z:
-3
-2
-1
0
1
2
3

Y: 3
      2
	     1
		    0
			   -1
			      -2
				     -3

X: -3 -2 -1 0   1  2  3

--  --  --  45  46  47  48
  --  --  37  38  39  40  41
    --  29  30  31  32  33  34
     21  22  23  24  25  26  27
       14  15  16  17  18  19  --
         07  08  09  10  11  --  --
           00  01  02  03  --  --  --
x /
z or r: |
y \
			   
x=q
y=s
z=r

+s   -r   +q
 \    |    /
-s   +r   -q

Different representation:
+s -r +q
-q +r -s


        0, 1, 2, 3, 
      7, 8, 9, 10, 11, 
   14, 15, 16, 17, 18, 19, 
21, 22, 23, 24, 25, 26, 27, 
   29, 30, 31, 32, 33, 34, 
     37, 38, 39, 40, 41, 
       45, 46, 47, 48

Here, no consecutive indices wrap around the board.
I think it can be fixed by associating x and y with the row and column indices, respectively, 
rather than the other way around. Let's see..

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
