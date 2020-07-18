import copy

class GameBoard(object):
    def __init__(self, battleships, width, height):
        self.battleships = battleships
        self.shots = []
        self.width = width
        self.height = height

    # Update battleship with any hits
    # Save a hit or miss
    def takeShot(self, shotLocation):
        isHit = False
        for b in self.battleships:
            index = b.bodyIndex(shotLocation)
            if index is not None:
                isHit = True
                b.hits[index] = True
                print("______HIT______")
                break
            else:
                print("______MISS_____")
                break
        self.shots.append(Shot(shotLocation, isHit))

    def isGameOver(self):
        return all([b.isDestroyed() for b in self.battleships])

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

    def isDestroyed(self):
        return all(self.hits)

def render(gameBoard, showBattleships = False):
    # How the top and bottom border looks
    border = " +" + "-" * gameBoard.width + "+"
    print("  0123456789")
    print(border)

    # Construct empty board
    board = []
    for _ in range(gameBoard.width):
        # List comprehension
        board.append([None for _ in range(gameBoard.height)])

    if showBattleships:
        # Add the battleships to the board
        for b in gameBoard.battleships:
            for x, y in b.body:
                board[x][y] = "0"

    # Add the shots to the board
    for sh in gameBoard.shots:
        x, y = sh.location
        if sh.isHit:
            ch = "X"
        else:
            ch = "~"
        board[x][y] = ch

    for y in range(gameBoard.height):
        row = []
        for x in range(gameBoard.width):
            row.append(board[x][y] or " ")
        print(str(y) + "|" + "".join(row) + "|")

    print(border)

# Main
if __name__ == "__main__":

    battleships = [
        Battleship.build((1,1), 2, "N"),
        # Battleship.build((5,8), 4, "N"),
        # Battleship.build((2,3), 3, "E")
    ]

    gameBoards = [
        GameBoard(battleships, 10, 10),
        GameBoard(copy.deepcopy(battleships), 10, 10)
    ]

    # Player 1 == 0 & player 2 == 1
    attackingPlayer = 0

    while True:
        defendingPlayer = (attackingPlayer + 1) % 2

        defendingBoard = gameBoards[defendingPlayer]

        print("\nPLAYER " + str(attackingPlayer + 1))
        inp = input("Where do you want to shoot?\n")
        # TODO: input validation
        xStr, yStr = inp.split(",")
        x = int(xStr)
        y = int(yStr)

        defendingBoard.takeShot((x,y))
        render(defendingBoard)

        if defendingBoard.isGameOver():
            print("PLAYER " + str(attackingPlayer + 1) + " WINS!")
            break
        
        # Attacker now becomes defender
        attackingPlayer = defendingPlayer