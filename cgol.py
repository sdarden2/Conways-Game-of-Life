#Conways game of life
#First need an outline of an algorithm
#The idea is that the board is a function of the previous board, with the first drop of cells being the seed
#The previous state determines the next state
#First, we want to write this program using sequential and function based steps, not object oriented

"""The board can just be an matrix of 0's and 1's, 0 for dead, 1 for alive"""
"""
main()
{
	init_window();
	create_grid();
	
	drop_initial_cells_on_click()
	
	while true
	{
		if cell_is_alive
		{
			if cell neighbors < 2
			{
				cell_dies()
			}
			else if neighbors > 3
			{
				cell_dies()
			}
		}
		else if cell_is_dead
		{
			if cell neighbors == 3
			{
				cell_alive()
			}
		}
	}
}

drop_initial_cells_on_click()
{
	drop a living cell - has 2 or 3 neighbors
}

cell_dies()
{
	set cell color white
}
cell_alive()
{	
	set cell color black
}
"""
#Holds the (x,y) coordinates from clicking



from Tkinter import *
import random
import sys
import time
import copy
DEFAULT_BOARD_WIDTH = 700
DEFAULT_BOARD_HEIGHT = 700
GRID_SIZE = {'x':75, 'y':75}
gx = 'x'
gy = 'y'


def turn_alive(cell,x=-1,y=-1):
	if x == -1 or y == -1:
		loc = find_in_matrix(cell)
	else:
		loc = (x,y)
	board.itemconfigure(cell,fill='black')
	game_matrix[loc[0]][loc[1]] = 1
	board.update()
def kill(cell,x=-1,y=-1):
	if x == -1 or y == -1:
		loc = find_in_matrix(cell)
	else:
		loc = (x,y)
	board.itemconfigure(cell,fill="white")
	game_matrix[loc[0]][loc[1]] = 0
	board.update()

def change_board(matrix):
	for r in range(GRID_SIZE[gx]):
		for c in range(GRID_SIZE[gy]):
			game_matrix[r][c] = matrix[r][c]
def update_board():
	for r in range(GRID_SIZE[gx]):
		for c in range(GRID_SIZE[gy]):
			if game_matrix[r][c] == 1:
				board.itemconfig(rect_mat[r][c],fill="black")
			else:
				board.itemconfig(rect_mat[r][c],fill="white")
	board.update()
def game_loop():
	state_mat = copy.copy(game_matrix)
	k = 0
	while True:
		for i in range(GRID_SIZE[gx]):
			for j in range(GRID_SIZE[gy]):
				cell = rect_mat[i][j]
				if game_matrix[i][j] == 1:
					nbs = get_neighbors(cell)
					res = [1 for ind in nbs if is_alive(rect_mat[ind[0]][ind[1]])]
					if len(res) < 2:
						state_mat[i][j] = 0
						
						#kill(cell,i,j)
					elif len(res) > 3:
						state_mat[i][j] = 0
						
						#kill(cell,i,j)
				else:
					nbs = get_neighbors(cell)
					res = [1 for ind in nbs if is_alive(rect_mat[ind[0]][ind[1]])]
					if len(res) == 3 or len(res) == 4:
						
						#print "Creating cell"
						state_mat[i][j] = 1
						#turn_alive(cell,i,j)
		change_board(state_mat)
		update_board()
		#time.sleep(.01)
		#board.update()
		#k += 1
		
		
def find_in_matrix(cell):
	#Because we essentially have object numbered 1 through GRID_SIZE[gx]*GRID_SIZE[gy],
	#We can use the numbers to find the indices quickly
	i = (cell-1) /GRID_SIZE[gy]
	j = (cell % GRID_SIZE[gx]) - 1
	if j == -1:
		j = 24
	return (i,j)
	
#If you're having a probelm with non-square grids, check the gx and gy params to GRID_SIZE
def get_neighbors(cell):
	"""need edge cases for this"""
	(i,j) = find_in_matrix(cell) #BIG PROBLEM HERE --- Not anymore
	lst = []
	#case top row
	if i == 0:
		if j == 0: #Top left corner
			lst.append((i+1,j+1))
			lst.append((i+1,j))
			lst.append((i,j+1))
		elif j >= GRID_SIZE[gx] - 1: #Top right corner
			lst.append((i,j-1))
			lst.append((i-1,j-1))
			lst.append((i-1,j))
		else: #Rest of top row
			lst.append((i,j-1))
			lst.append((i,j+1))
			lst.append((i-1,j))
			lst.append((i-1,j-1))
			lst.append((i-1,j+1))
	elif i >= GRID_SIZE[gy] - 1: #Bottom row
		if j >= GRID_SIZE[gx] - 1: #Bottom right corner
			lst.append((i,j-1))
			lst.append((i-1,j-1))
			lst.append((i-1,j))
		
		elif j == 0: #Bottem left corner
			lst.append((i-1,j))
			lst.append((i-1,j+1))
			lst.append((i,j+1))
		else: #Rest of bottom row
			lst.append((i,j-1))
			lst.append((i,j+1))
			lst.append((i-1,j-1))
			lst.append((i-1,j+1))
			lst.append((i-1,j))
	elif j == 0: #Left side
		lst.append((i+1,j))
		lst.append((i+1,j+1))
		lst.append((i,j+1))
		lst.append((i-1,j+1))
		lst.append((i-1,j))
	elif j >= GRID_SIZE[gx] - 1: #Right side
		lst.append((i+1,j))
		lst.append((i+1,j-1))
		lst.append((i,j-1))
		lst.append((i-1,j-1))
		lst.append((i-1,j))
	else:
		return [(i-1,j),(i-1,j-1),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
	return lst
	
def is_alive(cell):
	color = board.itemcget(cell,'fill')
	if color == 'black':
		return True
	else:
		return False
def get_cell_neighbors(nbs):
	n = []
	for loc in nbs:
		cell = rect_mat[loc[0]][loc[1]]
		n.append(cell)
	return n
	
def create_new_cell(x,y):
	cell = board.find_closest(x,y)[0]
	if not is_alive(cell):
		neighbors = get_neighbors(cell)
		print neighbors
		
		n1 = random.choice(neighbors)
		n2 = random.choice(neighbors)
		board.itemconfigure(rect_mat[n1[0]][n1[1]], fill='black')
		board.itemconfigure(rect_mat[n2[0]][n2[1]], fill='black')
		board.itemconfigure(cell,fill='black')
		game_matrix[n1[0]][n1[1]] = 1
		game_matrix[n2[0]][n2[1]] = 1
		"""glider = (i,j),(i,j+1),(i,j-1),(i-1,j+1),(i-2,j),"""
		# loc = find_in_matrix(cell) #POTENTIAL PROBLEM HERE
		# (r,c) = loc
		# lst = [(r,c+1),(r,c-1),(r-1,c+1),(r-2,c)]
		# game_matrix[r][c] = 1
		# for k in lst:
			# game_matrix[k[0]][k[1]] = 1
			# board.itemconfig(rect_mat[k[0]][k[1]],fill="black")
		board.update()

def start_game():
	game_started = True
	game_loop()
	
def get_click(event):
	create_new_cell(event.x,event.y)
	print "yo"
	if not game_started:
		start_game()

	
def main():
	if len(sys.argv) < 2:
		width = DEFAULT_BOARD_WIDTH
		height = DEFAULT_BOARD_HEIGHT
		
	root = Tk()
	global game_started
	game_started = False
	global board
	board = Canvas(root,width=width,height=height, bg="white")
	board.pack()
	
	global rect_mat
	rect_mat = []
	rect_width = width/GRID_SIZE[gx]
	rect_height = height/GRID_SIZE[gy]
	x0 = 0
	y0 = 0
	for i in range(GRID_SIZE[gx]):
		row = []
		for k in range(GRID_SIZE[gy]):
			ident = board.create_rectangle(x0,y0,x0+rect_width,y0+rect_height)
			row.append(ident)
			x0 = x0 + rect_width	
		rect_mat.append(row)
		del(row)
		x0 = 0
		y0 = y0 + rect_height
	
	#coord_mat will represent the coordinates of each box
	
	#game matrix will represent the state of the box (1) or (0)
	global game_matrix
	game_matrix = [[0]*GRID_SIZE[gx] for i in range(GRID_SIZE[gy])]
	# function to set a square - print board.itemconfigure(rect_mat[50][50], fill = 'black')
	#Function to get a square color - print board.itemcget(rect_mat[50][50],'fill')
	board.pack()
	
	board.bind('<Button-1>',get_click)
	
	
	
	root.mainloop()
	root.destroy()
	
if __name__ == "__main__":
	main()


"""glider = (i,j),(i,j+1),(i,j-1),(i-1,j+1),(i-2,j),"""