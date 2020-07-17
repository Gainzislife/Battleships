class Battleship(object):

    @staticmethod
    def build(head, length, direction):
        body = []
        for i in range(length):
            if direction == "N":
                el = (head[0], head[1] - i)
            elif direction == "S":
                el = (head[0], head[1] + i)
            elif direction == "E":
                el = (head[0] + i, head[1])
            elif direction == "W":
                el = (head[0] - i, head[1])

            body.append(el)
        return Battleship(body)

    def __init__(self, body):
        self.body = body

# Draw the board
def renderBoard(boardWidth, boardHeight, shots):
    # How the top and bottom border looks
    border = "+" + "-" * boardWidth + "+"

    print(border)

    # Parse the shots list to a set
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

def renderBattleships(boardWidth, boardHeight, battleships):
    # How the top and bottom border looks
    border = "+" + "-" * boardWidth + "+"

    print(border)

    # Construct empty board
    board = []
    for _ in range(boardWidth):
        # List comprehension
        board.append([None for _ in range(boardHeight)])

    # Add the battleships to the board
    for b in battleships:
        for x, y in b.body:
            board[x][y] = "0"

    for y in range(boardHeight):
        row = []
        for x in range(boardWidth):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(border)

# Main
if __name__ == "__main__":
    battleships = [
        Battleship.build((1,1), 2, "N"),
        Battleship.build((5,8), 4, "N"),
        Battleship.build((2,3), 3, "E")
    ]

    for b in battleships:
        print(b.body)

    renderBattleships(10, 10, battleships)

    exit(0)


    # Empty list that will hold the shots fired
    shots = []

    while True:
        inp = input("Where do you want to shoot?\n")
        # TODO: input validation
        xStr, yStr = inp.split(",")
        x = int(xStr)
        y = int(yStr)


        shots.append((x,y))
        renderBoard(10, 10, shots)