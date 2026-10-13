import random

n = 3 #default value 

def makegrid(n, grid): #creates grid in which game is played 
    size = n * n
    hline = ("----"+"+-----"*(n-1)) 
    for i in range(0,size, n):
        print(" | ".join(grid[i:i+n]))
        if i < size-n:
            print(hline)
            
def checkwinner(n, moves): #checks if there is n of the same symbol in a row in any row, column or diagonal
    cells = set(m - 1 for m in moves)
    lines = [range(r * n, r * n + n) for r in range(n)]      
    lines += [range(c, n * n, n) for c in range(n)]          
    lines += [range(0, n * n, n + 1), range(n - 1, n * n - 1, n - 1)]  
    return any(set(line) <= cells for line in lines)

def after(moves, cell, infinite):
    # the moves a player would have after playing cell (oldest drops off in infinite mode) (Needed to build the computer opponent)
    moves = moves + [cell]
    return moves[1:] if infinite and len(moves) > n else moves

def computermove(player1, player2, infinite):
    free = [c for c in range(1, n * n + 1) if c not in player1 and c not in player2]
    for c in free:                                            # 1. win if possible
        if checkwinner(n, after(player2, c, infinite)):
            return c
    for c in free:                                            # 2. block the human
        if checkwinner(n, after(player1, c, infinite)):
            return c
    center = n * n // 2 + 1
    if n % 2 == 1 and center in free:                         # 3. take the center
        return center
    corners = [c for c in (1, n, n * n - n + 1, n * n) if c in free]
    return random.choice(corners or free)                     # 4. corner, else anything

def maingame(infinite, vs_computer): #main game code, takes 
    player1 = []
    player2 = [] 
    size = n * n
    turns = 1

    while infinite or (len(player1) + len(player2)) < size:
        if vs_computer and turns % 2 == 0:
            turn = computermove(player1, player2, infinite)
            print(f"Computer picks {turn}")
        else:
            while True:
                turn = input(f"Pick a cell from 1-{size}, with 1 being the top left and {size} being bottom right: \nTo forfeit, type 'end' ")
                if turn == "end": #to end game before a winner is declared - useful in the larger custom games or infinite mode as they can take long time 
                    if turns %2 != 0:
                        print("Player 1 (X) has forfeited the game. Player 2 (O) wins!")
                    else:
                        print("Player 2 (O) has forfeited the game. Player 1 (X) wins!")
                    return
                elif not turn.isdigit() or int(turn) not in range(1, size+1): #if anything other than a number in the range of spaces is entered, asks again for correct input
                    print(f"Incorrect entry, enter a number between 1 and {size}: ")
                elif int(turn) in player1 + player2: #if space is already taken, try again 
                    print("That space is taken, try again: ")
                else:
                    turn = int(turn)
                    break
            
        if turns % 2 != 0: #stores the turns taken
            player1.append(turn)
        else:
            player2.append(turn)
            
        if infinite and len(player1) > n: #removes the first object in list when number of turns exceeds n
            player1.pop(0)
        if infinite and len(player2) > n:
            player2.pop(0)
            
        turns += 1
        
        grid = ["   "] * size
        for moves, symbol in ((player1, "X"), (player2, "O")):
            for move in moves:
                grid[move - 1] = f" {symbol} "
            if infinite and len(moves) == n:                  # highlights the oldest mark that will disappear
                grid[moves[0] - 1] = f"[{symbol}]"
        
        makegrid(n, grid) #reprints the grid with latest moves 

        if checkwinner(n, player1):
            print("Player 1 (X) wins!")
            break
        if checkwinner(n, player2):
            print("Computer (O) wins!" if vs_computer else "Player 2 (O) wins!")
            break
    else:
        print("It's a draw!")

def intro():
    
    global n #needed for multiple functions to use the same n instead of creating a new one or passing it to every function that uses it 

    while True:
        gamemode = input("Enter 1 for classic 3x3 game, Enter 2 for custom size game: ")

        if gamemode in ("1","2"):
            break
        print("Incorrect entry. Enter 1 for classic 3x3 game or 2 for custom size game.")
     
    while True:
        infinite = input("Normal mode: Players make moves until the board is full or there is a winner. \nInfinite mode: Players can only have 3 (or your custom number) of moves on the board at any time. The oldest move is deleted first. \nEnter 1 for normal mode, enter 2 for infinite mode. ")
        if infinite in ("1","2"):
            break
        print("Incorrect entry. Enter 1 for normal mode, enter 2 for infinite mode. ")
    infinite = infinite == "2"
        
    while True:
        vs_computer = input("Enter 1 for two players, enter 2 to play against the computer. ")
        if vs_computer in ("1","2"):
            break
        print("Incorrect entry. ")
    vs_computer = vs_computer == "2"

    if gamemode in ("1"):
        n = 3
    else:
        while True:
        
            n = input("Enter the size of the grid you would like, eg: enter 4 for a 4x4 grid (min: 3 - max: 10) ")
            if not n.isdigit():
                print("Incorrect entry, try again. ")
            elif int(n)<3:
                print("Minimum grid size is 3x3, try again. ")
            elif int(n)> 10:
                print("Maximum grid size is 10x10, try again. ")
            else:
                n = int(n)
                break
        

    makegrid(n, ["   "] * (n * n))
    maingame(infinite, vs_computer)
        
intro()