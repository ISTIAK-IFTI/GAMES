# minesweeper game

emoji = [ '💣', '1️⃣ ', '2️⃣ ', '3️⃣ ', '4️⃣ ', '5️⃣ ', '6️⃣ ', '7️⃣ ', '8️⃣ ', '9️⃣ ', '🚩', '󠀠󠀠󠀠⬛', '⬜']

import os
import random
from collections import defaultdict

# To clean the window 
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# This is the element of each block in the board 
# value = {
#     f"{i}{j}" : emoji[11]
#     for i in range(1,10) 
#     for j in range(1,10)
# }
value = defaultdict(str)

# Hidden element of the board like bomb 
val = defaultdict(str)

# To print the board 
def printBoard():
    print(f"    Minesweeper Game ")
    print(f"    1 |  2 |  3 |  4 |  5 |  6 |  7 |  8 |  9")
    print(f"   ------------------------------------------")
    for i in range(1, 10):
        row = []
        for j in range(1, 10):
            row.append(value[f"{i}{j}"])
        print(f"{i}  " + " | ".join(row))
        if i != 9:
            print(f"   ------------------------------------------")
    return


# Show all the blank space adjacent to the current blank space 
def spacePrint(choice):
    if val[choice] == emoji[12]:
        value[choice] = emoji[12]
        val[choice] = 'alreadyOpen'
        x, y = int(choice[0]), int(choice[1])
        directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 1 <= nx <= 9 and 1 <= ny <= 9:
                if val[f"{nx}{ny}"] == emoji[12]:
                    spacePrint(f"{nx}{ny}")
                elif val[f"{nx}{ny}"] in emoji[1:10]:
                    value[f"{nx}{ny}"] = val[f"{nx}{ny}"]
    return


# SetUp function of this game 
def setUpGame(choice):
    global placeableBomb
    placeableBomb = 10
    xy = [str(i) for i in range(1, 10)]
    while placeableBomb > 0:
        key = random.choice(xy) + random.choice(xy)
        if val[key] != emoji[0] and key != choice:
            val[key] = emoji[0]
            placeableBomb -= 1
    directions = [(-1,0),(1,0),(0,-1),(0,1),
                  (-1,-1),(-1,1),(1,-1),(1,1)]
    for i in range(1, 10):
        for j in range(1, 10):
            key = f"{i}{j}"
            if val[key] == emoji[0]:
                continue
            count = 0
            for dx, dy in directions:
                ni, nj = i + dx, j + dy
                if 1 <= ni <= 9 and 1 <= nj <= 9 and val[f"{ni}{nj}"] == emoji[0]:
                    count += 1
            val[key] = emoji[count] if count > 0 else emoji[12]
    if val[choice] != emoji[12]:
        value[choice] = val[choice]
    else:
        spacePrint(choice)
    return


# If game is over then it shows all the hidden bomb and terminate the game 
def gameOver():
    print(f"!!!!😔 You lost the Game 😔!!!!!")
    xy = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    for x in xy:
        for y in xy:
            if val[x+y] == emoji[0]: value[x+y] = emoji[0]
    printBoard()
    return 


# If you won the game then it celebrate it 
def checkWin():
    hidden = [key for key in value if value[key] == emoji[11]]
    flags = [key for key in value if value[key] == emoji[10]]
    bombs = [key for key in val if val[key] == emoji[0]]

    if set(flags) == set(bombs) and len(hidden) == 0:
        print("🎉 Congratulations! You flagged all bombs correctly! 🎉")
        return True
    if len(hidden) + len(flags) == len(bombs):
        # Alternative win condition: all non-bomb cells revealed
        print("🎉 Congratulations! You cleared the board! 🎉")
        return True
    return False



# To start the game
def startGame():
    clear()     # To clear the window 
    for i in range(1,10):
        for j in range(1,10):
            value[f"{i}{j}"] = emoji[11]
    printBoard()
    choice = input("\nEnter your choice (rowcol like 23): ")
    if choice in value:
        setUpGame(choice)
    else:
        startGame()
    
    while True:
        clear()
        printBoard()
        choice = input("\nEnter your choice (rowcol like 23 or 23f for flag): ")

        if len(choice) == 3 and choice[2] == 'f':
            pos = choice[:2]
            if value[pos] == emoji[11]:   # hidden ⬛
                value[pos] = emoji[10]    # set 🚩
            elif value[pos] == emoji[10]: # toggle flag back to ⬛
                value[pos] = emoji[11]
            continue

        if choice not in value: 
            continue

        # ignore flagged cells
        if value[choice] == emoji[10]:
            continue

        if val[choice] == emoji[0]:
            gameOver()
            break

        if val[choice] == emoji[12]: 
            spacePrint(choice)
        elif val[choice] in emoji[1:10]:
            value[choice] = val[choice]

        if checkWin():
            break
    
    again = input("Play again? (y/n): ")
    if again.lower() == 'y':
        startGame()

    return


if __name__ == "__main__":
    startGame()