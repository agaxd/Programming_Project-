import random

n = 3 

def makegrid(n, grid):
    size = n * n
    hline = ("----"+"+-----"*(n-1)) 
    for i in range(0,size, n):
        print(" | ".join(grid[i:i+n]))
        if i < size-n:
            print(hline)
            
def checkwinner(n, moves):
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

def maingame(infinite, vs_computer):
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
                turn = input(f"Pick a cell from 1-{size}, with 1 being the top left and {size} being bottom right : ")
                if not turn.isdigit() or int(turn) not in range(1, size+1):
                    print(f"Incorrect entry, enter a number between 1 and {size}: ")
                elif int(turn) in player1 + player2:
                    print("That space is taken, try again: ")
                else:
                    turn = int(turn)
                    break
            
        if turns % 2 != 0:
            player1.append(turn)
        else:
            player2.append(turn)
            
        if infinite and len(player1) > n:
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
        
        makegrid(n, grid)

        if checkwinner(n, player1):
            print("Player 1 (X) wins!")
            break
        if checkwinner(n, player2):
            print("Computer (O) wins!" if vs_computer else "Player 2 (O) wins!")
            break
    else:
        print("It's a draw!")

def intro():
    
    global n 

    while True:
        gamemode = input("Enter 1 for simple game, Enter 2 for custom size game: ")

        if gamemode in ("1","2"):
            break
        print("Incorrect entry. Enter 1 for simple game or 2 for custom size game.")
     
    while True:
        infinite = input("Enter 1 for normal mode, enter 2 for infinite mode. ")
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
        
            n = input("Enter the size of the grid you would like (min: 3 - max: 100) : ")
            if not n.isdigit():
                print("Incorrect entry, try again. ")
            elif int(n)<3:
                print("Minimum grid size is 3, try again. ")
            elif int(n)> 100:
                print("Maximum grid size is 100, try again. ")
            else:
                n = int(n)
                break
        

    makegrid(n, ["   "] * (n * n))
    maingame(infinite, vs_computer)
        
intro()