#Conways game of life
#The idea is that the board is a function of the previous board, with the first drop of cells being the seed
#The previous state determines the next state


"""
Conway's Game of life Algorithm (psuedo-code)
=============================================
The board can just be an matrix of 0's and 1's, 0 for dead, 1 for alive"""
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


from Tkinter import *
import random
import sys
import time
import copy
DEFAULT_BOARD_WIDTH = 700
DEFAULT_BOARD_HEIGHT = 700
#--TODO--- Change GRID_SIZE to GRID_SIZE_X and GRID_SIZE_Y
GRID_SIZE_X = 75
GRID_SIZE_Y = 75

#Turns on the specified cell. Can either specify the cell by using the actual cell.
#Or by passing in the x,y coordinates of the cell. No return

def turn_alive(cell,x=-1,y=-1):
	if x == -1 or y == -1:
		loc = find_in_matrix(cell)
	else:
		loc = (x,y)
	board.itemconfigure(cell,fill='black')
	game_matrix[loc[0]][loc[1]] = 1
	board.update()
	
#Turns a cell off. Can either pass in the actual cell or pass in the x,y coordinates
#of the cell. No return	

def kill(cell,x=-1,y=-1):
	if x == -1 or y == -1:
		loc = find_in_matrix(cell)
	else:
		loc = (x,y)
	board.itemconfigure(cell,fill="white")
	game_matrix[loc[0]][loc[1]] = 0
	board.update()

#Changes the current state of the board to the state of `matrix`. Returns nothing.

def change_board(matrix):
	for r in range(GRID_SIZE_X):
		for c in range(GRID_SIZE_Y):
			game_matrix[r][c] = matrix[r][c]
			
#Updates the board `board` with the `game_matrix`. Returns nothing.
#This is the main way the board is updated. `game_matrix` represents the next state
#and update_board updates the current state to the next.

def update_board():
	for r in range(GRID_SIZE_X):
		for c in range(GRID_SIZE_Y):
			if game_matrix[r][c] == 1:
				board.itemconfig(rect_mat[r][c],fill="black")
			else:
				board.itemconfig(rect_mat[r][c],fill="white")
	board.update()
	
#Main game loop
#`board` is the actual canvas with cells on it, `rect_mat` is the internal matrix which holds numbers
#representing if the cell if alive `1` or dead `0`
#The main loop executes the main algorithm on CGOL

def game_loop():
	state_mat = copy.copy(game_matrix) #save current state in state_mat
	k = 0
	
	while True:
		for i in range(GRID_SIZE_X):
			for j in range(GRID_SIZE_Y):
				cell = rect_mat[i][j]
				
				if game_matrix[i][j] == 1:
					nbs = get_neighbors(cell)
					res = [1 for ind in nbs if is_alive(rect_mat[ind[0]][ind[1]])]
					
					if len(res) < 2:
						state_mat[i][j] = 0
						
					elif len(res) > 3:
						state_mat[i][j] = 0
						
				else:
					nbs = get_neighbors(cell)
					res = [1 for ind in nbs if is_alive(rect_mat[ind[0]][ind[1]])]
					
					if len(res) == 3 or len(res) == 4:
						state_mat[i][j] = 1
						
		change_board(state_mat)
		update_board()
		
		
#Find the i,j position of the `cell` in the matrix

def find_in_matrix(cell):
	#Because we essentially have object numbered 1 through GRID_SIZE_X*GRID_SIZE_Y,
	#We can use the numbers to find the indices quickly
	
	i = (cell-1) /GRID_SIZE_Y
	j = (cell % GRID_SIZE_X) - 1
	if j == -1:
		j = 24
	return (i,j)
	
#Returns list of i,j poistions in the matrix of all neighboring cells to `cell`

def get_neighbors(cell):
	"""need edge cases for this"""
	
	(i,j) = find_in_matrix(cell) 
	lst = []
	
	#case top row
	if i == 0:
		if j == 0: #Top left corner
			lst.append((i+1,j+1))
			lst.append((i+1,j))
			lst.append((i,j+1))
		elif j >= GRID_SIZE_X - 1: #Top right corner
			lst.append((i,j-1))
			lst.append((i-1,j-1))
			lst.append((i-1,j))
		else: #Rest of top row
			lst.append((i,j-1))
			lst.append((i,j+1))
			lst.append((i-1,j))
			lst.append((i-1,j-1))
			lst.append((i-1,j+1))
	elif i >= GRID_SIZE_Y - 1: #Bottom row
		if j >= GRID_SIZE_X - 1: #Bottom right corner
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
	elif j >= GRID_SIZE_X - 1: #Right side
		lst.append((i+1,j))
		lst.append((i+1,j-1))
		lst.append((i,j-1))
		lst.append((i-1,j-1))
		lst.append((i-1,j))
	else:
		return [(i-1,j),(i-1,j-1),(i-1,j+1),(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)]
		
	return lst
	
#Returns True if `cell` is alive, `False` if cell is not alive
	
def is_alive(cell):
	color = board.itemcget(cell,'fill')
	if color == 'black':
		return True
	else:
		return False
		
#Creates a new cell at x,y
	
def create_new_cell(x,y):
	cell = board.find_closest(x,y)[0]
	
	if not is_alive(cell):
		neighbors = get_neighbors(cell)
		
		n1 = random.choice(neighbors)
		n2 = random.choice(neighbors)
		
		board.itemconfigure(rect_mat[n1[0]][n1[1]], fill='black')
		board.itemconfigure(rect_mat[n2[0]][n2[1]], fill='black')
		board.itemconfigure(cell,fill='black')
		
		game_matrix[n1[0]][n1[1]] = 1
		game_matrix[n2[0]][n2[1]] = 1
		
		board.update()
		
#Internal function to start game

def start_game():
	game_started = True
	game_loop()

#Mouse click callback function to add cell to area and start the game

def get_click(event):
	create_new_cell(event.x,event.y)
	
	if not game_started:
		start_game()

#main() -- sets up board and calls mainloop	

def main():
	if len(sys.argv) < 2:
		width = DEFAULT_BOARD_WIDTH
		height = DEFAULT_BOARD_HEIGHT
		
	root = Tk()
	
	global board
	global game_started
	global rect_mat
	
	game_started = False
	
	board = Canvas(root,width=width,height=height, bg="white")
	board.pack()
	
	
	rect_mat = []
	rect_width = width/GRID_SIZE_X
	rect_height = height/GRID_SIZE_Y
	
	x0 = 0
	y0 = 0
	
	for i in range(GRID_SIZE_X):
		row = []
		
		for k in range(GRID_SIZE_Y):
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
	game_matrix = [[0]*GRID_SIZE_X for i in range(GRID_SIZE_Y)]
	
	# function to set a square - print board.itemconfigure(rect_mat[50][50], fill = 'black')
	#Function to get a square color - print board.itemcget(rect_mat[50][50],'fill')
	
	board.pack()
	
	board.bind('<Button-1>',get_click)
	
	
	
	root.mainloop()
	root.destroy()
	
if __name__ == "__main__":
	main()