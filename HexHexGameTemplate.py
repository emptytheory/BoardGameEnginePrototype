class HexHexGameTemplate:
	NONE = -1
	EMPTY = 0
	BLACK = 1
	WHITE = 2
	DIRECTIONS = [(0,1), (1,0), (-1,0), (0,-1), (1,-1), (-1,1)]

	def __init__(self, side_length):
		self.SIDE_LENGTH = side_length
		self.LINE_LENGTH = 2 * side_length - 1
		self.CENTER_LINE_INDEX = side_length - 1
		# Array of cells. Each cell is a tuple (state=NONE|EMPTY|BLACK|WHITE, group_ID=NONE|nonnegative int)
		self.board = [
			(self.NONE, self.NONE) if self._is_off_board(index) else (self.EMPTY, self.NONE) 
			for index in range(self.LINE_LENGTH * self.LINE_LENGTH)
		]

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
		return 0 < index < self.LINE_LENGTH

	def even_neighbors(self, row_index, column_index, owner):
		unique_group_ids = set()

		# Iterate through each direction from the current position
		for dx, dy in self.DIRECTIONS:
			new_row_index = row_index + dx
			new_column_index = column_index + dy

			# Check if the new position is valid
			if self._valid_line_index(new_row_index) and self._valid_line_index(new_column_index):
				# Calculate the index for the new position
				index = self._index_from_column_and_row_indices(new_row_index, new_column_index)

				# Check if the cell belongs to the specified owner
				cell_state, group_id = board[index]
				if cell_state == owner:
					unique_group_ids.add(group_id)

		# Return True if the count of unique group IDs is even, False otherwise
		return len(unique_group_ids) % 2 == 0

	def _group_IDs_around(self, index, group_owner):


"""
42  43  44  45  --  --  --
35  36  37  38  39  --  --
28  29  30  31  32  33  --
21  22  23  24  25  26  27
--  15  16  17  18  19  20
--  --  09  10  11  12  13
--  --  --  03  04  05  06

sideLength = 4
lineLength = 2*sideLength-1
array = [0]*lineLength*lineLength
centerIndex = sideLength-1

columnIndex = lambda index: index%lineLength
rowIndex = lambda index: index // lineLength

x = lambda index: columnIndex(index)-centerIndex
y = lambda index: rowIndex(index)-centerIndex
z = lambda index: -x(index)-y(index)

indexFromColumnAndRowIndex = lambda columnIndex, rowIndex: columnIndex + (lineLength * rowIndex)

indexFromXY = lambda x, y: indexFromColumnAndRowIndex(x+centerIndex, y+centerIndex)

# Tests:
for (index, _) in enumerate(array):
    print(f"{index}: ({x(index)}, {y(index)},{z(index)}), sum: {x(index) + y(index) + z(index)}\n")

for (index, _) in enumerate(array):                                         
    print(f"{index}: ({x(index)}, {y(index)},{z(index)}), indexCheck: {indexFromXY(x(index), y(index))}\n")

# Additional:
OFF = -1
EMPTY = 0
BLACK = 1
WHITE = 2

def cutCorners(array):
    top-i = lineLength - 1
    for row-i in range(lineLength):
        for offset in range(centerIndex):
            

# Fill the following indexes with OFF:
# 3 last  from the 0th row from the top
# 2 last  from the 1st row from the top
# 1 last  from the 2nd row from the top
# 0 last  from the 3rd row from the top
# 1 first from the 2nd row from the bottom
# 2 first from the 1st row from the bottom
# 3 first from the 0th row from the bottom


def isOff(i):
    return (columnIndex(i) > centerIndex+rowIndex(i) or
            rowIndex(i) > centerIndex+columnIndex(i))


def hexhex(size):
	return [-1 if isOff(i) else 0 in range()]

moving along the x axis is changing x by 0 and y and z by 1 and -1. 
The two different possibilities (y by 1 and z by -1 or y by -1 and z by 1)
correspond to two directions along the x axis – moving to a higher y line and lower z line (always the same when moving along x),
or moving to a lower y line and higer z line.
So you don't need all three coordinates.
Let's find out how to move in the six directions without cube coordinates.
Oh, I haven't made sure that I cut the right corners.
So let's try to see if the three cube coordinates correspond to the correct directions.

Note that for UCT based AIs, all you really need is a very simple interface:
- how many moves are available?
- play the Nth move
- has someone won?

Paintbucket
Solder

Counting moves in Single-Placement Solder:
I need to track group ids, so one only needs to check the surrounding stones.
You can always place if there is 0 stones.
And one can never place if there is 1, 5 or 6 stones.
So you need to check when there are 2, 3 or 4 stones.
There is a complication: The restriction for P2.
The counting should be lazy. 
Return as soon as a legal Black move is found that is not the current White move.
But this makes counting quadratic.. O(n^2).
We can calculate how many moves it takes before it is possible that black has no moves.
Or we can calculate how many moves Black can lose per move, 
so we can use the previous move count (memoized) to rule out a check.
That is, if you call on numMoves again with the same position (so it would need to have a parameter),
the number is returned without calculation. Or just have a different function that returns the recorded number for the last move.


Regarding tracking groups:
I need to be able to look up the group id of an index.
And I need to be able to count the number of groups.

The first can be achieved with an array that maps index to group id.
The second can be achieved by keeping track as stones are placed.
There are 2 kinds of placements, corresponding to 2 different ways a player's group count can change.
Adjacent to 0 groups: +1.
Adjacent to 2 groups: -1.

And +1 only happens when you place adjacent to 0 friendly stones.
All other legal moves are -1.

Check all friendly stones surrounding the placement.
(0,1) (1,0) (-1,0) (0,-1) (1,-1) (-1,1)

def _apply_direction((x, y), (d1, d2)):
	return (self._row_index(x) + d1, self.column_index(y) + d2))


I could have a function that simply returns true iff an index has 0 or 2 neighboring groups of a given owner.

def _has_even_neighbors(index, owner):
	for direction in self.directions:

How do I turn on all hte bits around a given bit?
How do I even target a bit with an index? Answer: Left-shift 1 n times to get the nth bit from the right.
(To get the value of the nth bit, apply the mask and right shift n times.)

if num ids = 2, for all stones, with the larger of the two, change to the smaller of the two
if num ids = 0, pick a new.

I need to store owner and group id for each cell, that's two numbers. 
The first number is always -1, 0, 1 or 2, though. And that part can only change from 0.
That's add 1 or 2.
Changing the number behind that is adding 200-the I don't know what the largest number of groups are.

max number of groups: self.SIDE_LENGTH * (self.SIDE_LENGTH - 1) + 2
Could simply use self.SIDE_LENGTH * self.SIDE_LENGTH for simplicity.
But the point is that I need to know how many digits there are.


max_number_of_groups = self.SIDE_LENGTH * (self.SIDE_LENGTH - 1) + 2
self.SHIFT_MULTIPLIER = 10 * len(str(max_number_of_groups))

a column or row must be higher than 0 and lower than self.LINE_LENGTH

def neighbor_at_direction
def _count_adjacent_groups(index):
	

two bits encode
00 = OFF
01 = EMPTY
10 = BLACK
11 = WHITE

group_ID 0 means no stone here

select the row and column and correct diagonal of the index and take their intersection
filter for the ones by the correct owner

Precompute neighbors!
Precompute EVERYTHING! (mrraow)
So precompute the index-coordinate map as well, then.


"""

