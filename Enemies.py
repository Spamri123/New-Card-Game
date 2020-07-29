from random import randint
from copy import deepcopy
import pygame
from Classes import Enemy
from pathlib import Path
enemies = []
# the root of where the images are
enemyRoot = Path('Images/Enemies/')
symbolRoot = Path('Images/Symbols/')
bottomLeft = (900, 900)
sporeDetonation = pygame.image.load(str(symbolRoot / 'SporeDetonation.png'))

# enemies


def MushroomShow(self, turn, board):
    board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    number = randint(1, 4)
    if number == 1:
        board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    else:
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
    if number <= 3:
        board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    else:
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
    if turn % 3 == 0:
        self.symbols.append(sporeDetonation)
    return board


def MushroomAttack(self, turn, board, hp):
    if turn % 3 == 0 and turn != 0:
        self.symbols.remove(sporeDetonation)
        for row in board:
            for card in row:
                hp -= card['spores']
                card['spores'] = 0
    return hp, board


images = [pygame.image.load(str(enemyRoot/'Mushroom1.png')), pygame.image.load(str(enemyRoot/'Mushroom2.png')), pygame.image.load(str(enemyRoot/'Mushroom3.png')), pygame.image.load(str(enemyRoot/'Mushroom4.png'))]
enemies.append([bottomLeft[0], bottomLeft[1]-140, images, 'Mushroom', 'most basic of enemies, can apply spores at intervals', MushroomShow, MushroomAttack, 17, 140, 140])
