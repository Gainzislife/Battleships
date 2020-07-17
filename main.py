

def renderBoard(boardWidth, boardHeight, shots):
    border = "+" + "-" * boardWidth + "+"
    print(border)

    shots_set = set(shots)
    for y in range(boardHeight):
        row = []
        for x in range(boardWidth):
            if (x,y) in shots_set:
                ch = "X"
            else:
                ch = " "
            row.append(ch)
        print("|" + "".join(row) + "|")

    print(border)

if __name__ == "__main__":
    shots = []

    while True:
        inp = input("Where do you want to shoot?\n")
        # TODO: input validation
        xStr, yStr = inp.split(",")
        x = int(xStr)
        y = int(yStr)


        shots.append((x,y))
        renderBoard(10, 10, shots)