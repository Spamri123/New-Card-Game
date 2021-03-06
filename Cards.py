from Relics import *
from Classes import *
from Definitions import *
from copy import deepcopy
from pathlib import Path
# sets up some variables
cards = {}
cardRoot = Path("Images/Cards/")

# some extra definitions


def Blank(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    return targets, board, player

# cards


def LuckOfTheDice(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # sets up some variables
        newBoard = deepcopy(blankBoard)
        counter1 = 0

        # makes a order which goes from (0,0) to (4,4)
        order = []

        for x in range(5):
            for y in range(5):
                order.append((x, y))
        # copies this order and shuffles it into different sections
        blankOrder = {'card': shuffle(deepcopy(order)), 'playable': shuffle(deepcopy(order)), 'attacked': shuffle(deepcopy(order)), 'spores': shuffle(deepcopy(order)), 'block': shuffle(deepcopy(order))}

        # loops through all cards
        for row in board:
            counter2 = 0
            for card in row:
                # loops through each type of the card
                for type in card:
                    # finds new places for the card's type to go based on the order for its type
                    cordsX = blankOrder[type][counter1*5+counter2][0]
                    cordsY = blankOrder[type][counter1*5+counter2][1]

                    # moves it to these ne places
                    newBoard[cordsX][cordsY][type] = card[type]

                    # checks if the type is the card class and if so resizes and adds the new co-ordinates for the card
                    if type == 'card' and newBoard[cordsX][cordsY][type] != False:
                        newBoard[cordsX][cordsY][type].x, newBoard[cordsX][cordsY][type].y, newBoard[cordsX][cordsY][type].screenX, newBoard[cordsX][cordsY][type].screenY = cordsX, cordsY, cardGapWIDTH * cordsX + cardSpaceWIDTH, cardGapHEIGHT * cordsY + cardSpaceHEIGHT
                        newBoard[cordsX][cordsY][type].resize(scaleWidth=scaleWidth, scaleHeight=scaleHeight)
                counter2 += 1
            counter1 += 1
        # returns saying that it was played
        return True, targets, newBoard, player
    # returns saying it wasn't able to be played
    return False, targets, board, player


cards['luck of the dice'] = [LuckOfTheDice, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'luck of the dice', 'Randomize all cards positions, attacks positions and playable card position ', 0, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def StrikeAtTheHeart(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # applies its effects to the target
        targets['enemy'][0].crippled += 2
        targets['enemy'][0].hit(15, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['strike at the heart'] = [StrikeAtTheHeart, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'strike at the heart', 'High cost, medium damage, status effect, single target', 3, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def SneakAttack(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile or if its turn 1
    if board[self.x][self.y]['playable'] or turn == 1:
        # applies damage to the target
        targets['enemy'][0].hit(5, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['sneak attack'] = [SneakAttack, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'sneak attack', 'low cost, low damage, single target', 1, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def Execute(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile or the target is able to be one shot by the card
    if board[self.x][self.y]['playable'] or targets['enemy'][0].hp <= 10:
        # applies damage to the target
        targets['enemy'][0].hit(10, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['execute'] = [Execute, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'execute', 'medium cost with medium damage, single target', 2, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def IchorSurge(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile or the player has no ichor left
    if board[self.x][self.y]['playable'] or player.ichorLeft == 0:
        # increases the ichor left by 1
        player.ichorLeft += 1

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['ichor surge'] = [IchorSurge, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'ichor surge', 'no cost, small ichor increase', 0, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Fireball(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # hits the target for 20
        targets['enemy'][0].hit(20, player, False)
        # hits all the other enemies for 3
        for enemy in targets['enemies']:
            if enemy.id != targets['enemy'][0].id:
                enemy.hit(3, player)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['fireball'] = [Fireball, Blank, pygame.image.load(str(cardRoot / 'Fireball.png')), 'fireball', 'High cost, high damage to single target, low damage to other targets', 4, True, {'enemy': 1, 'card': 0, 'enemies': 1, 'spot': 0}]


def Mechanise(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.relics.append(Relic(relics['mechanise relic'][0], relics['mechanise relic'][1], relics['mechanise relic'][2], relics['mechanise relic'][3], relics['mechanise relic'][4], relics['mechanise relic'][5]))
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['mechanise passive'] = [Mechanise, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'mechanise passive', 'Large Ichor cost, massive armour, legendary spell', 3, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def VirulentPlague(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for enemy1 in targets['enemies']:
            for enemy2 in targets['enemies']:
                enemy2.poison += 3

        for enemy in targets['enemies']:
            enemy.hp -= enemy.poison
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['virulent plague'] = [VirulentPlague, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'virulent plague', 'Medium Ichor, Large AOE, legendary spell', 2, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def FinalStand(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # totals damage
    total = 0
    for row in board:
        for card in row:
            for id in card['attacked']:
                total += card['attacked'][str(id)]

    # checks if the card is on a playable tile or if this card prevents death
    if board[self.x][self.y]['playable'] or player.hp <= total <= player.hp + 50:
        player.totalBlock += 50
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['final stand'] = [FinalStand, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'final stand', 'small ichor cost, massive armour', 1, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def DemonicSeal(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # totals the number of demonic seals on the board
    screen = 0
    for row in board:
        for card in row:
            if card['card']:
                if card['card'].name == 'demonic seal':
                    screen += 1

    # totals the number of demonic seals in the deck
    deck = 0
    for card in player.stackCards:
        if card['card'].name == 'demonic seal':
            deck += 1

    # checks if the card is on a playable tile, there are more than one demonic seal on the board or if its the last demonic seal
    if board[self.x][self.y]['playable'] or screen > 1 or deck + screen == 1:
        # checks if its the last demonic seal and if so adds demonfire relic
        if screen + deck == 1:
            player.relics.append(Relic(relics['demonfire'][0], relics['demonfire'][1], relics['demonfire'][2], relics['demonfire'][3], relics['demonfire'][4], relics['demonfire'][5]))

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['demonic seal'] = [DemonicSeal, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'demonic seal', 'Medium cost, Does nothing until all are played', 1, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def TheWorldTree(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile or if this card prevents death
    if board[self.x][self.y]['playable']:
        # adds block to the card
        board[self.x][self.y]['block'] += 15

        # goes through each card, removes its block and adds it to the player's hp
        for row in board:
            for card in row:
                player.hp += card['block']
                card['block'] = 0

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['the world tree'] = [TheWorldTree, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'the world tree', 'Large Cost, Massive Heal', 3, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def CurrencyExchange(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # totals up all the co-ordinates of where cards are
        Cards = []
        for row in board:
            for card in row:
                if card['card']:
                    Cards.append((card['card'].x, card['card'].y))

        # replaces two cards with two random cards
        for x in range(2):
            card = Cards[randint(0, len(Cards) - 1)]
            board[card[0]][card[1]]['card'] = cards[player.allCards[randint(0, len(cards) - 1)]]
            board[cordsX][cordsY]['card'].x, board[cordsX][cordsY]['card'].y, board[cordsX][cordsY]['card'].screenX, board[cordsX][cordsY]['card'].screenY = cordsX, cordsY, cardGapWIDTH * cordsX + cardSpaceWIDTH, cardGapHEIGHT * cordsY + cardSpaceHEIGHT
            board[cordsX][cordsY]['card'].resize(scaleWidth=scaleWidth, scaleHeight=scaleHeight)
            board[card[0]][card[1]].used(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player)
            player.discard += 1

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['currency exchange'] = [CurrencyExchange, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'currency exchange', 'Discards two random cards from the board. Generate two random cards.', 0, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def LeBureauDeChange(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for x in range(3):
            board, player.stackCards = drawCard(board, player.stackCards, targets, blankBoard, scaleWidth, scaleHeight, turn, player)

        for card in targets['card']:
            board[card.x][card.y]['card'] = False
            player.discard += 1

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['le bureau de change'] = [LeBureauDeChange, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'le bureau de change', 'Draw 3 cards. Discard 3 cards from the board.', 0, True, {'enemy': 0, 'card': 3, 'enemies': 0, 'spot': 0}]


def Bank(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        PLAYABLE = []
        counter1 = 0
        for row in board:
            counter2 = 0
            for card in row:
                if card['card']:
                    player.gold += 3
                    player.stackCards.append(card['card'])
                    card['card'] = False
                    player.discard += 1
                if card['playable']:
                    PLAYABLE.append((counter1, counter2))
                counter2 += 1
            counter1 += 1
        player.stackCards = shuffle(player.stackCards)
        card = PLAYABLE[randint(0, len(PLAYABLE) - 1)]
        board[card[0]][card[1]]['card'] = player.stackCards[0]

        player.stackCards.pop(0)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['bank'] = [Bank, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'bank', 'Discard all of the cards on the grid. Gain 3 currency (non-meta) per card that you discard. Draw 1 card and place it on a random active space which is empty.', 2, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Gamble(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # sets up some variables
        available = []
        attacked = []
        counter1 = 0
        blank = {}

        # gets a blank template for a non-attacking spot
        for id in board[0][0]:
            blank[id] = 0

        # loops through each card with counters
        for row in board:
            counter2 = 0
            for card in row:
                # if theres a card in the spot then add it to the deck and remove from board
                if card['card']:
                    player.stackCards.append(card['card'])
                    card['card'] = False
                    player.discard += 1

                # adds to available if the card is not on an active spot
                if not card['playable']:
                    available.append((counter1, counter2))

                # adds to the attacked square list if the card does not equal the blank template
                if board[counter1][counter2]['attacked'] == blank:
                    attacked.append((counter1, counter2))
                counter2 += 1
            counter1 += 1

        # goes through and adds 5 cards to spots that aren't active
        total = 0
        for x in range(5):
            card = available[randint(0, len(available) - 1)]
            board[card[0]][card[1]]['card'] = player.stackCards[0]
            player.stackCards.pop(0)
            board[card[0]][card[1]]['card'].x, board[card[0]][card[1]]['card'].y, board[card[0]][card[1]]['card'].screenX, board[card[0]][card[1]]['card'].screenY = card[0], card[1], cardGapWIDTH * card[0] + cardSpaceWIDTH, cardGapHEIGHT * card[1] + cardSpaceHEIGHT
            board[card[0]][card[1]]['card'].resize(scaleWidth=scaleWidth, scaleHeight=scaleHeight)
            board[card[0]][card[1]]['card'].used(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player)

            # checks if the spot is attacked if so increasing total count
            if board[card[0]][card[1]]['attacked'] != blank:
                total += 1

        # for how many spots where attacked it adds 5 block to a random attacked square
        for x in range(total):
            spot = available[randint(0, len(available) - 1)]
            board[spot[0]][spot[1]]['block'] += 5
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['gamble'] = [Gamble, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'gamble', 'Discard all cards on the grid. Draw 5 cards and place them on a random non-active space. Gain 5 Block on a random threatened space for each card drawn which lands on a threatened space.', 2, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def ShieldSlam(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # totals up block
        damage = 0
        for row in board:
            for card in row:
                damage += card['block']

        # deals damage equal to that total to the enemy
        targets['enemy'][0].hit(damage, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['shield slam'] = [ShieldSlam, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'shield slam', 'low cost, deal damage equal to armour', 1, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def ShieldStorm(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # totals up block
        damage = 0
        for row in board:
            for card in row:
                damage += card['block']
                card['block'] = 0

        # deals total damage to each enemy
        for enemy in targets['enemies']:
            enemy.hit(damage, player, False)

        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['shield storm'] = [ShieldStorm, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'shield storm', 'Medium cost, deal damage to all enemies with your armour', 2, False, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def TimeSwipe(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.ichorLeft += 2
        player.nextMana = player.maxIchor - 3
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['time swipe'] = [TimeSwipe, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'time swipe', 'Low cost, gain energy with downside', 0, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Taunt(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # gives the card 30 block
        board[self.x][self.y]['block'] += 30

        # totals all damage from each enemy
        totalDamage = {}
        for row in board:
            for card in row:
                for id in card['attacked']:
                    totalDamage[str(id)] += card['attacked'][str(id)]

        # adds that damage
        board[self.x][self.y]['attacked'] = totalDamage
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['taunt'] = [Taunt, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'taunt', 'Low cost gain armour, all attacks target that square', 1, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def ShieldBash(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        enemyHP = targets['enemy'][0].hp
        targets['enemy'][0].hit(10, player, False)
        board[self.x][self.y]['block'] += enemyHP - targets['enemy'][0].hp
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['shield bash'] = [ShieldBash, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'shield bash', 'Medium cost, deal a bunch of damage, gain a bunch of armour', 2, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def ClumsySlash(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable'] or player.discard:
        targets['enemy'][0].hit(3, player)
        Cards = []
        for row in board:
            for card in row:
                if card['card']:
                    Cards.append((card['card'].x, card['card'].y))

        card = Cards[randint(0, len(Cards) - 1)]
        player.stackCards.append(board[card[0]][card[1]]['card'])
        board[card[0]][card[1]]['card'] = False
        player.discard += 1
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['clumsy slash'] = [ClumsySlash, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'clumsy slash', 'Part of the money money bucket', 0, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def WildLeap(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        blockCards = []
        total = 0
        counter1 = 0
        for row in board:
            counter2 = 0
            for card in row:
                if card['block'] > 0:
                    card['block'] *= 3
                    total += card['block']
                    blockCards.append([counter1, counter2, card['block']])
                counter2 += 1
            counter1 += 1

        if total > 40:
            total = 40
        while total != 0:
            random = blockCards[randint(0, len(blockCards) - 1)]
            board[random[0]][random[1]]['block'] -= 1
            random[2] -= 1
            if board[random[0]][random[1]]['block'] == 0:
                blockCards.remove(random)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['wild leap'] = [WildLeap, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'wild leap', 'Part of the dodge bucket', 2, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def MicroDodge(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the target is on an attacked tile
    total = 0
    for id in targets['spot'][0][2]['attacked']:
        total += targets['spot'][0][2]['attacked'][str(id)]
    if total > 0:
        board[targets['spot'][0]][targets['spot'][1]]['block'] += 3
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['micro dodge'] = [MicroDodge, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'micro dodge', 'Part of the 0-cost bucket and the block bucket', 0, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 1}]


def ThrowingDagger(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if not board[self.x][self.y]['playable']:
        for enemy in targets['enemies']:
            enemy.hit(3, player, False)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['throwing dagger'] = [ThrowingDagger, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'throwing dagger', 'Part of the 0-cost bucket and the multi strike damage', 0, False, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def DefenciveStance(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.relics.append(Relic(relics['storm of shields relic'][0], relics['storm of shields relic'][1], relics['storm of shields relic'][2], relics['storm of shields relic'][3], relics['storm of shields relic'][4], relics['storm of shields relic'][5]))
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['defencive stance passive'] = [DefenciveStance, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'defencive stance passive', 'Part of the block bucket', 3, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def EnhancedDNA(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        try:
            self.block
        except AttributeError:
            self.block = 1

        totalAttacked = 0
        for row in board:
            for card in row:
                for id in card['attacked']:
                    totalAttacked += card['attacked'][id]
                card['block'] += 1

        if totalAttacked == 0:
            self.block += 1
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['enhanced dna'] = [EnhancedDNA, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'enhanced dna', 'Part of the block bucket', 1, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def EvolvingParasite(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        increaseDamage = False
        for enemy in targets['enemies']:
            enemy.hit(self.attack, player, True)
            if enemy.hp < 1:
                increaseDamage = True

        if increaseDamage:
            player.evolvingParasite += 2
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['evolving parasite'] = [EvolvingParasite, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'evolving parasite', 'an archetype of its own and part of the multistrike bucket', 1, True, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def Slash(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    try:
        self.damage
    except AttributeError:
        self.damage = 7
    targets['enemy'][0].hit(self.damage, player)
    self.damage += 5
    # returns saying that it was played
    return True, targets, board, player


cards['slash'] = [Slash, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'slash', 'An archetype of its own', 1, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def JungleHarmony(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.hp += 5
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['jungle harmony'] = [JungleHarmony, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'jungle harmony', 'An event card - its supposed to be just a really good card if youre not playing an overly defensive build or youre just taking a ton of damage', 0, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Brace(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.relics.append(Relic(relics['brace relic'][0], relics['brace relic'][1], relics['brace relic'][2], relics['brace relic'][3], relics['brace relic'][4], relics['brace relic'][5]))
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['brace passive'] = [Brace, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'brace passive', 'Someone crouching behind a shield', 1, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def LivingOnTheEdge(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for space in targets['spot']:
            board[space[0]][space[1]]['block'] += player.maxHP - player.hp
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['living on the edge'] = [LivingOnTheEdge, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'living on the edge', 'Block bucket', 2, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 3}]


def Bolt(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    targets['enemies'][randint(0, len(targets['enemies']))].hit(4, player, False)
    return True, targets, board, player


cards['bolt'] = [Bolt, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'bolt', 'a basic tool', 0, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Volley(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for x in range(player.ichorLeft):
            for y in range(3):
                none, targets, board, player = player.fires['bolt'][0](self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player)
        player.ichorLeft = 0
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['volley'] = [Volley, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'volley', 'Fire 3X bolts', 0, True, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def Pincushion(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for x in range(5):
            targets['enemy'][0].hit(10, player, False)
        player.nextMana += 1
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['pincushion'] = [Pincushion, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'pincushion', 'Deal 10 damage 5 times. Gain 1 energy next turn', 5, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def Enraged(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.relics.append(Relic(relics['enraged relic'][0], relics['enraged relic'][1], relics['enraged relic'][2], relics['enraged relic'][3], relics['enraged relic'][4], relics['enraged relic'][5]))
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['enraged passive'] = [Enraged, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'enraged passive', 'Gain 1 energy every time you take unblocked attack damage', 2, True, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def GrondV2(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for x in range(2):
            for enemy in targets['enemies']:
                enemy.hit(5, player, True)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['grond v2'] = [GrondV2, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'grond v2', 'Can only get from playing Morgoth', 0, False, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def Morgoth(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        card = cards['grond v2']
        for x in range(0, player.ichorLeft):
            player.stackCards.append(Card(0, 0, 0, 0, card[0], card[1], card[2], card[3], card[4], card[5], card[6], card[7]))
        player.stackCards = shuffle(player.stackCards)
        player.ichorLeft = 0
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['morgoth'] = [Morgoth, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'morgoth', 'Kind of archetype of its own', 0, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def KnowTheEnemy(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        board, player.stackCards = drawCard(board, player.stackCards, targets['enemies'], blankBoard, scaleWidth, scaleHeight, turn, player)
        for enemy in targets['enemies']:
            board, player.stackCards = drawCard(board, player.stackCards, targets['enemies'], blankBoard, scaleWidth, scaleHeight, turn, player)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['know the enemy'] = [KnowTheEnemy, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'know the enemy', 'medium cost draw cards', 2, False, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def PotionOfWisdom(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for x in range(2):
            board, player.stackCards = drawCard(board, player.stackCards, targets['enemies'], blankBoard, scaleWidth, scaleHeight, turn, player)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['potion of wisdom'] = [PotionOfWisdom, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'potion of wisdom', 'Potions are mini theme, cheap thing + exhaust', 0, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def PotionOfFire(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        targets['enemy'][0].hit(15, player, False)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['potion of fire'] = [PotionOfFire, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'potion of fire', '/\\', 0, True, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def Wind(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    totalMove = [0, 0]
    totalMove[0] = targets['spot'][0][0] - self.x
    totalMove[1] = targets['spot'][0][1] - self.y
    spot = []
    for x in range(5):
        add = []
        for y in range(5):
            add.append(totalMove)
        spot.append(add)
    board = move(board, spot, blankBoard)
    # returns saying that it was played
    return True, targets, board, player


cards['wind'] = [Wind, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'wind', 'like the fourth iteration of wind and moves all tiles, part of the move bucket', 1, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 1}]


def Swap(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        board[targets['card'][0]['card'].x][targets['card'][0]['card'].y]['card'] = targets['card'][1]['card']
        board[targets['card'][1]['card'].x][targets['card'][1]['card'].y]['card'] = targets['card'][0]['card']
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['swap'] = [Swap, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'swap', 'part of the move bucket', 0, False, {'enemy': 0, 'card': 2, 'enemies': 0, 'spot': 0}]


def Move(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # makes sure the target spot is blank
    if not board[targets['spot'][0][0]][targets['spot'][0][1]]['card']:
        board[targets['spot'][0][0]][targets['spot'][0][1]]['card'] = targets['card'][0]['card']
        board[targets['card'][0]['card'].x][targets['card'][0]['card'].y]['card'] = False
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['move'] = [Move, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'move', 'part of the move bucket', 0, False, {'enemy': 0, 'card': 1, 'enemies': 0, 'spot': 1}]


def PoisonousSpider(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        targets['enemy'][0].hit(5, player, False)
        targets['enemy'][0].poison += round(3 * player.poisonMultiplier)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['poisonous spider'] = [PoisonousSpider, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'poisonous spider', 'part of the poison bucket', 1, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def UnoReverseCard(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        crippled, fragile, poison = targets['enemy'][0].crippled, targets['enemy'][0].fragile, targets['enemy'][0].poison
        targets['enemy'][0].crippled, targets['enemy'][0].fragile, targets['enemy'][0].poison = player.crippled, player.fragile, player.poison
        player.crippled, player.fragile, player.poison = crippled, fragile, poison
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['uno reverse card'] = [UnoReverseCard, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'uno reverse card', 'a reference to uno', 0, True, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def DejaVu(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        total = 2
        for row in board:
            for card in row:
                if card.name == 'deja vu':
                    total -= 1
        if total < 0:
            total = 0
        if player.ichorLeft >= total:
            try:
                self.damage
            except AttributeError:
                self.damage = 5
            oldBoard = deepcopy(board)
            targets['enemy'][0].hit(self.damage, player, False)
            board, player.stackCards = drawCard(board, player.stackCards, targets, blankBoard, scaleWidth, scaleHeight, turn, player)
            counter1 = 0
            for row in board:
                counter2 = 0
                for card in row:
                    if card != oldBoard[counter1][counter2]:
                        if card['card'].name == 'deja vu':
                            self.damage += 1
                        board[counter1][counter2]['playable'] = True
                        player.relics.append(relics['deja vu relic'][0], relics['deja vu relic'][1], relics['deja vu relic'][2], relics['deja vu relic'][3], relics['deja vu relic'][4], relics['deja vu relic'][5])
                        player.relics[len(player.relics) - 1].spot = (counter1, counter2)
                        break
                    counter2 += 1
                counter1 += 1
            player.ichorLeft -= total
            # returns saying that it was played
            return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['deja vu'] = [DejaVu, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'deja vu', 'Basic damage card, Flavour text: I’ve just been in this place before', 0, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def Pride(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.relics.append(relics['pride relic'][0], relics['pride relic'][1], relics['pride relic'][2], relics['pride relic'][3], relics['pride relic'][4], relics['pride relic'][5])
        card = cards['downfall']
        player.stackCards.append(Card(0, 0, 0, 0, card[0], card[1], card[2], card[3], card[4], card[5], card[6], card[7]))
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['pride'] = [Pride, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'pride', 'hex bucket probs', 2, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Downfall(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for row in board:
            for card in row:
                card['block'] = 0
        player.relics.append(relics['downfall relic'][0], relics['downfall relic'][1], relics['downfall relic'][2], relics['downfall relic'][3], relics['downfall relic'][4], relics['downfall relic'][5])
        card = cards['pride']
        player.stackCards.append(Card(0, 0, 0, 0, card[0], card[1], card[2], card[3], card[4], card[5], card[6], card[7]))
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['downfall'] = [Downfall, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'downfall', 'uncollectable', 2, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def SealedFate(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        total = 0
        for row in board:
            for card in row:
                if card['card']:
                    total += 1

        if total > 1:
            targets['enemy'][0].hp = 0
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['sealed fate'] = [SealedFate, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'sealed fate', '0 cost bucket', 0, True, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


def Balance(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    if targets['card'][0]['card'].ichorCost != 0:
        targets['card'][0]['card'].ichorCost -= 1
    while True:
        num = (randint(0, 4), randint(0, 4))
        if num != (targets['card'][0]['card'].x, targets['card'][0]['card'].y):
            board[num[0]][num[1]]['card'].ichorCost += 1
            break
    # returns saying that it was played
    return True, targets, board, player


cards['balance'] = [Balance, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'balance', 'Part of the 0 cost bucket, flavour text: like all things should be', 0, True, {'enemy': 0, 'card': 1, 'enemies': 0, 'spot': 0}]


def StoreRoom(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.nextMana += player.ichorLeft - 1
        player.ichorLeft = 1
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player

cards['store room'] = [StoreRoom, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'store room', 'Store all your remaining energy until next turn', 1, False, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def SelfImmolation(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        for enemy in targets['enemies']:
            enemy.hit(12, player, False)
        player.hit(12)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['self immolation'] = [SelfImmolation, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'self immolation', 'self damage', 0, False, {'enemy': 0, 'card': 0, 'enemies': 1, 'spot': 0}]


def VampiricBite(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        player.relics.append(relics['vampiric bite relic'][0], relics['vampiric bite relic'][1], relics['vampiric bite relic'][2], relics['vampiric bite relic'][3], relics['vampiric bite relic'][4], relics['vampiric bite relic'][5])
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['vampiric bite'] = [VampiricBite, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'vampiric bite', 'self damage', 1, True, {'enemy': 0, 'card': 0, 'enemies': 0, 'spot': 0}]


def Dishabilitate(self, targets, board, blankBoard, scaleWidth, scaleHeight, turn, player):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        targets['enemy'][0].hit(35, player, False)
        # returns saying that it was played
        return True, targets, board, player
    # returns saying that it wasn't able to be played
    return False, targets, board, player


cards['dishabilitate'] = [Dishabilitate, Blank, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'dishabilitate', 'a sword?', 3, False, {'enemy': 1, 'card': 0, 'enemies': 0, 'spot': 0}]


print(len(cards))
for card2 in cards:
    card = cards[card2]
    print(card[3], len(card))
