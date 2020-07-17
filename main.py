class GameBoard(object):
    def __init__(self, battleships, boardWidth, boardHeight):
        self.battleships = battleships
        self.shots = []
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight

    # Update battleship with any hits
    # Save a hit or miss
    def takeShot(self, shotLocation):
        isHit = False
        for b in self.battleships:
            index = b.bodyIndex(shotLocation)
            if index is not None:
                isHit = True
                b.hits[index] = True
                break
        self.shots.append(Shot(shotLocation, isHit))

class Shot(object):
    def __init__(self, location, isHit):
        self.location = location
        self.isHit = isHit

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
        self.hits = [False] * len(body)

    def bodyIndex(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None

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

    gameBoard = GameBoard(battleships, 10, 10)
    shots = [(1,1), (0,0), (5,7)]
    for sh in shots:
        gameBoard.takeShot(sh)

    for sh in gameBoard.shots:
        print(sh.location)
        print(sh.isHit)
        print("========")
    for b in gameBoard.battleships:
        print(b.body)
        print(b.hits)
        print("========")

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