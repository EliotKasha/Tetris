# Tetris AI
# TODO:
# Clean up movement, it's really icky rn
# Add I piece srs
# Add tspin detection
# Add REN
# Fix glitchy ghost piece


import pygame
import random
from pieces import Orientations

# Setup
pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 32)

orientations = Orientations().orientations
kickscw = Orientations().kickscw
kicksccw = Orientations().kicksccw
combo_table = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]  # Probs an easier way to do this

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
orange = (255, 153, 0)
yellow = (255, 235, 59)
purple = (156, 39, 176)
aqua = (79, 195, 247)
grey = (155, 155, 155)

light_red = red = (255, 35, 35)

tile_colors = [black, red, green, blue, orange, yellow, purple, aqua, grey]

# Sounds
single = "../sfx/single.wav"
double = "../sfx/double.wav"
triple = "../sfx/triple.wav"
quad = "../sfx/quad.wav"
rotate = "../sfx/rotate.wav"
move = "../sfx/move.wav"
hold = "../sfx/hold.wav"

# Settings
tile_size = 30
preview = 6
auto_drop = 60

# Misc
class Pieces:
    z = 1
    s = 2
    j = 3
    l = 4
    o = 5
    t = 6
    i = 7


# Bag class to control the next piece queue, uses the 7 bag randomizer. Thus the max next piece preview should be 6
class Bag:
    def __init__(self):
        self.full_bag = [Pieces.z, Pieces.s, Pieces.j, Pieces.l, Pieces.o, Pieces.t, Pieces.i]  # Note: this gets shuffled later
        self.queue = []
        self.new_bag(2)

    def new_bag(self, n):
        for i in range(n):
            random.shuffle(self.full_bag)
            for j in self.full_bag:
                self.queue.append(j)

    def next(self):
        piece = self.queue[0]
        del(self.queue[0])

        if len(self.queue) == 7:
            self.new_bag(1)

        return piece


# Main Tetris game
class Game:
    def __init__(self, w=1280, h=720):
        self.window = pygame.display.set_mode((w, h))

        # Calculating the top left corner of the board for centering purposes
        self.top = (h / 2) - (tile_size * 10)
        self.left = (w / 2) - (tile_size * 5)

        self.w, self.h = w, h

        self.board = [[0 for j in range(10)] for i in range(20)]
        self.bag = Bag()
        self.hold = None
        self.has_held = False

        self.inc_garb = []
        self.inc_garb_total = 0

        self.ren = -1

        self.get_next_piece()

    # Sets up [n] lines of garbage
    def add_garbage(self, n):
        self.inc_garb_total += n
        self.inc_garb.append(n)

    # Gets the next piece in queue, and resets all respective data
    def get_next_piece(self):
        self.current = self.bag.next()
        self.rotation = 0
        self.position = [-1, 3]  # Spawn position is the same for all
        self.ad = 0  # Cooldown for auto falling

        if not self.legal_position(self.position):
            quit("Game Over!")

    # Check collision
    def legal_position(self, pos):
        for i in range(4):
            for j in range(4):
                if orientations[self.current][self.rotation][i][j] != 0:
                    if (i + pos[0]) > 19 or (j + pos[1]) < 0 or (j + pos[1]) > 9:
                        return False

                    elif (i + self.position[0]) > -1:
                        if self.board[i + pos[0]][j + pos[1]] != 0:
                            return False

        return True

    def get_ghost(self):
        temp = [self.position[0], self.position[1]]
        while self.legal_position(temp):
            temp[0] += 1

        temp[0] -= 1

        return temp

    # Lock piece in
    def lock(self):
        for i in range(4):
            for j in range(4):
                if orientations[self.current][self.rotation][i][j] != 0:
                    self.board[i + self.position[0]][j + self.position[1]] = orientations[self.current][self.rotation][i][j]

        self.get_next_piece()
        self.has_held = False

        clears = 0
        for i in range(20):
            if 0 not in self.board[i]:
                del(self.board[i])
                self.board.insert(0, [0 for j in range(10)])
                clears += 1

        if clears > 0:
            # +1 REN
            self.ren += 1

            if clears == 1:
                pygame.mixer.music.load(single)
                self.add_garbage(combo_table[self.ren])

            elif clears == 2:
                pygame.mixer.music.load(double)
                self.add_garbage(1 + combo_table[self.ren])

            elif clears == 3:
                pygame.mixer.music.load(triple)
                self.add_garbage(2 + combo_table[self.ren])

            elif clears == 4:
                pygame.mixer.music.load(quad)
                self.add_garbage(4 + combo_table[self.ren])

            # PC
            pc = True
            for i in range(20):
                for j in range(10):
                    if self.board[i][j] != 0:
                        pc = False

            if pc:
                self.add_garbage(10)

            pygame.mixer.music.play(1)

        else:
            self.ren = -1

            # Send Garbage
            if self.inc_garb_total > 0:
                for garb in self.inc_garb:
                    open_col = random.randint(0, 9)
                    for j in range(garb):
                        del(self.board[0])
                        self.board.append([])
                        for k in range(10):
                            if k != open_col:
                                self.board[19].append(8)

                            else:
                                self.board[19].append(0)

                self.inc_garb = []
                self.inc_garb_total = 0


    # Run every frame; accepts user input
    def take_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    while self.legal_position(self.position):
                        self.position[0] += 1

                    self.position[0] -= 1

                    self.lock()

                if event.key == pygame.K_DOWN:
                    while self.legal_position(self.position):
                        self.position[0] += 1

                    self.position[0] -= 1

                    self.ad = 0

                if event.key == pygame.K_x:
                    self.rotation = (self.rotation + 1) % 4

                    if not self.legal_position(self.position):

                        # Kicks Test
                        for i in range(4):
                            self.position = [self.position[0] + kickscw[self.rotation][i][0], self.position[1] + kickscw[self.rotation][i][1]]
                            if self.legal_position(self.position):
                                return
                            else:
                                self.position = [self.position[0] - kickscw[self.rotation][i][0], self.position[1] - kickscw[self.rotation][i][1]]

                        self.rotation = (self.rotation - 1) % 4

                    '''
                    else:
                        pygame.mixer.music.load(rotate)
                        pygame.mixer.music.play(1)
                    '''

                if event.key == pygame.K_z:
                    self.rotation = (self.rotation - 1) % 4

                    if not self.legal_position(self.position):

                        # Kicks Test
                        for i in range(4):
                            self.position = [self.position[0] + kicksccw[self.rotation][i][0],
                                             self.position[1] + kicksccw[self.rotation][i][1]]
                            if self.legal_position(self.position):
                                return
                            else:
                                self.position = [self.position[0] - kicksccw[self.rotation][i][0],
                                                 self.position[1] - kicksccw[self.rotation][i][1]]

                        self.rotation = (self.rotation + 1) % 4

                    '''
                    else:
                        pygame.mixer.music.load(rotate)
                        pygame.mixer.music.play(1)
                    '''

                if event.key == pygame.K_LEFT:
                    self.position[1] -= 1

                    if not self.legal_position(self.position):
                        self.position[1] += 1

                    '''
                    else:
                        pygame.mixer.music.load(move)
                        pygame.mixer.music.play(1)
                    '''

                if event.key == pygame.K_RIGHT:
                    self.position[1] += 1

                    if not self.legal_position(self.position):
                        self.position[1] -= 1

                    '''
                    else:
                        pygame.mixer.music.load(move)
                        pygame.mixer.music.play(1)
                    '''

                if event.key == pygame.K_c:
                    if not self.has_held:
                        if self.hold is None:
                            self.hold = self.current
                            self.get_next_piece()

                        else:
                            temp = self.current
                            self.current = self.hold
                            self.hold = temp

                            self.rotation = 0
                            self.position = [-1, 3]  # Spawn position is the same for all
                            self.ad = 0  # Cooldown for auto falling

                        self.has_held = True
                        pygame.mixer.music.load(hold)
                        pygame.mixer.music.play(1)

                if event.key == pygame.K_F2:
                    self.__init__()


    # Run every frame; renders the game
    def render(self):
        self.window.fill(black)

        # Draw grid
        for i in range(21):
            pygame.draw.line(self.window, white, (self.left, self.top + (i * tile_size)),
                             (self.left + (10 * tile_size), self.top + (i * tile_size)), 1)

        for j in range(11):
            pygame.draw.line(self.window, white, (self.left + (j * tile_size), self.top),
                             (self.left + (j * tile_size), self.top + (20 * tile_size)), 1)

        # Draw tiles
        for i in range(20):
            for j in range(10):
                pygame.draw.rect(self.window, tile_colors[self.board[i][j]], (self.left + j * tile_size + 1, self.top + i * tile_size + 1, tile_size - 1, tile_size - 1))

        # Draw Queue
        for p in range(preview):
            for i in range(4):
                for j in range(4):
                    if orientations[self.bag.queue[p]][0][i][j] != 0:
                        pygame.draw.rect(self.window, tile_colors[orientations[self.bag.queue[p]][0][i][j]],
                                         (self.left + (11 * tile_size) + (j * tile_size) + 1, self.top + (3 * p * tile_size) + (i * tile_size) + 1, tile_size - 1, tile_size - 1))

        # Draw Ghost Piece
        ghost_position = self.get_ghost()

        for i in range(4):
            for j in range(4):
                if -1 < (i + ghost_position[0]) < 20 and -1 < (j + ghost_position[1]) < 10:
                    if orientations[self.current][self.rotation][i][j] != 0:
                        pygame.draw.rect(self.window,
                                         tile_colors[orientations[self.current][self.rotation][i][j]],
                                         (
                                         self.left + (j * tile_size) + (ghost_position[1] * tile_size) + 1,
                                         self.top + (i * tile_size) + (ghost_position[0] * tile_size) + 1,
                                         tile_size - 1,
                                         tile_size - 1))

                        pygame.draw.rect(self.window,
                                         black,
                                         (self.left + (j * tile_size) + (ghost_position[1] * tile_size) + (
                                                     tile_size * 0.1) + 1,
                                          self.top + (i * tile_size) + (ghost_position[0] * tile_size) + (
                                                      tile_size * 0.1) + 1,
                                          (tile_size * 0.8) - 1,
                                          (tile_size * 0.8) - 1))

        # Draw Active Piece
        for i in range(4):
            for j in range(4):
                if -1 < (i + self.position[0]) < 20 and -1 < (j + self.position[1]) < 10:
                    if orientations[self.current][self.rotation][i][j] != 0:
                        pygame.draw.rect(self.window, tile_colors[orientations[self.current][self.rotation][i][j]],
                                             (self.left + (j * tile_size) + (self.position[1] * tile_size) + 1,
                                              self.top + (i * tile_size) + (self.position[0] * tile_size) + 1, tile_size - 1,
                                              tile_size - 1))

        # Draw Held Piece
        if self.hold is not None:
            if self.has_held:
                for i in range(4):
                    for j in range(4):
                        if orientations[self.hold][0][i][j] != 0:
                            pygame.draw.rect(self.window, grey,
                                             (self.left - (5 * tile_size) + (j * tile_size) + 1,
                                              self.top + (i * tile_size) + 1, tile_size - 1,
                                              tile_size - 1))

            else:
                for i in range(4):
                    for j in range(4):
                        if orientations[self.hold][0][i][j] != 0:
                            pygame.draw.rect(self.window, tile_colors[orientations[self.hold][0][i][j]],
                                             (self.left - (5 * tile_size) + (j * tile_size) + 1,
                                              self.top + (i * tile_size) + 1, tile_size - 1,
                                              tile_size - 1))

        # Draw Garbage Meter
        if self.inc_garb_total > 0:
            pygame.draw.rect(self.window, light_red, (self.left - 10, self.top + ((20 - self.inc_garb_total) * tile_size) + 1, 10, self.inc_garb_total * tile_size))

        # Text
        if self.ren > 1:
            ren = font.render(f"{self.ren} Combo!", 1, white)
            self.window.blit(ren, (self.w / 2 - ren.get_width() / 2, self.top + tile_size * 20 + 10))

        clock.tick(60)
        self.ad += 1

        # Move to take_input
        if self.ad % auto_drop == 0:
            self.position[0] += 1

            if not self.legal_position(self.position):
                self.position[0] -= 1
                self.lock()

        pygame.display.update()


def main():
    game = Game()

    while True:
        game.take_input()
        game.render()


if __name__ == "__main__":
    main()