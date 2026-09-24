n = 3 #default value

def makegrid(n, grid):
    size = n * n
    hline = ("----"+"+-----"*(n-1)) 
    for i in range(0,size, n):
        print(" | ".join(grid[i:i+n]))
        if i < size-n:
            print(hline)
            
gamemode = int(input("Enter 1 for simple game, Enter 2 for custom size game: "))

while gamemode != 1 and gamemode !=2:
    gamemode = int(input("Incorrect entry. Enter 1 for simple game or 2 for custom size game."))

if gamemode == 1:
    n = 3
    grid = ["   "]*(n*n)
    makegrid(n, grid)
else:
    n = int(input("Enter the size of the grid you would like: "))
    grid = ["   "]*(n*n)
    makegrid(n, grid)
    #tcurrent progress: the grid prints, but no values are saved as right now input is only working for 3x3 grid 

player1 = []
player2 = [] 
size = n * n
turns = 1

while (len(player1) + len(player2)) < size:
    grid = [" "] * size
    for move in player1:
        grid[move - 1] = "X"
    for move in player2:
        grid[move - 1] = "O"
    
    
    turn = int(input("Pick a cell from 1-9, with 1 being the top left and 9 being bottom right"))
    
    if turn not in range(0,10):
        turn = int(input("Incorrect entry, enter a number between 1 and 9"))
        
    if turn in player1 or turn in player2:
        turn = int(input("That space is taken, try again."))
        
    if turns %2 != 0:
        player1.append(turn)
    else:
        player2.append(turn)
        
    turns +=1
    
    grid = ["   "] * size
    for move in player1:
        grid[move - 1] = " X "
    for move in player2:
        grid[move -1] = " O "
    
    makegrid(n, grid)