import copy
import random


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
        return Battleship(body, direction)

    # TODO: which param actually needed
    def __init__(self, body, direction):
        self.body = body
        self.head = head
        self.length = length
        self.direction = direction
        self.hits = [False] * len(body)

    def bodyIndex(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None

    def isDestroyed(self):
        return all(self.hits)

class Player(object):

    def __init__(self, number, shotFunction):
        self.number = number
        self.shotFunction = shotFunction

# Draw the board
def render(gameBoard, showBattleships=False):
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
            for i, (x, y) in enumerate(b.body):
                if b.direction == "N":
                    chs = ("v", "|", "^")
                elif b.direction == "S":
                    chs = ("^", "|", "v")
                elif b.direction == "E":
                    chs = ("<", "-", ">")
                elif b.direction == "W":
                    chs = (">", "-", "<")
                else:
                    raise "Unknown direction"

                if i == 0:
                    ch = chs[0]
                elif i == len(b.body) - 1:
                    ch = chs[2]
                else:
                    ch = chs[1]
                board[x][y] = ch

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


def getRandomComputerShot(gameBoard):
    x = random.randint(0, gameBoard.width - 1)
    y = random.randint(0, gameBoard.height - 1)
    return (x, y)


def getHumanShot(gameBoard):
    inp = input("Where do you want to shoot?\n")
    # TODO: input validation
    xStr, yStr = inp.split(",")
    x = int(xStr)
    y = int(yStr)

    return (x, y)


# Main
if __name__ == "__main__":

    battleships = [
        Battleship.build((1, 1), 2, "N"),
        Battleship.build((5,8), 5, "N"),
        Battleship.build((2,3), 4, "E")
    ]

    gameBoards = [
        GameBoard(battleships, 10, 10),
        GameBoard(copy.deepcopy(battleships), 10, 10)
    ]

    # Player 1 == 0 & player 2 == 1
    attackingIndex = 0

    players = [
        Player(1, getHumanShot),
        Player(2, getRandomComputerShot)
    ]

    while True:
        defendingIndex = (attackingIndex + 1) % 2

        defendingBoard = gameBoards[defendingIndex]
        attackingPlayer = players[attackingIndex]

        print("\nPLAYER " + str(attackingPlayer.number))
        shotLocation = attackingPlayer.shotFunction(defendingBoard)

        defendingBoard.takeShot(shotLocation)
        render(defendingBoard, True)

        if defendingBoard.isGameOver():
            print("PLAYER " + str(attackingPlayer.number) + " WINS!")
            break

        # Attacker now becomes defender
        attackingIndex = defendingIndex
