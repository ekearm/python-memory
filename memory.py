import random, pygame, sys
from pygame.locals import *

frames = 30
width = 640
hieght = 480
flip = 8
card = 40
space = 10
boardwide = 10
boardhigh = 7
assert (boardwide * boardhigh) % 2 == 0, 'Board needs an even number'
Xmarg = int ((width - (boardwide * (card + space))) / 2)
Ymarg = int ((hieght - (boardhigh * (card + space))) / 2)

gray = (100, 100, 100)
navy = (60, 60, 100)
white = ( 255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yello = (255, 255, 0)
orang = (255, 128, 0)
purpl = (255, 0, 255)
cyan = (0, 255, 255)

backgroundColo = navy
lightBGColo = gray
cardcolo = white
highLiteCol = blue

donut = 'donut'
square = 'square'
diamond = 'diamond'
lines = 'lines'
oval = 'oval'

allTheColo = (red, green, blue, yello, orang, purpl, cyan)
allTheShape = (donut, square, diamond, lines, oval)
assert len(allTheColo) * len(allTheShape) * 2 >= boardwide * boardhigh, "Board is too big for the number of shapes/colors."

def main():
	global fpsClock, displayStuff
	pygame.init()
	fpsClock = pygame.time.Clock()
	displayStuff = pygame.display.set_mode((width, hieght))

	mouseX = 0
	mouseY = 0
	pygame.display.set_caption('Memory')

	mainBoard = getRandomizedBoard()
	revealedBoxes = generateRevealedBoxesData(False)

	firstSelection = None

	displayStuff.fill(backgroundColo)
	startGameAnimation(mainBoard)

	while True:
		mouseClick = False

		displayStuff.fill(backgroundColo)
		drawBoard(mainBoard, revealedBoxes)

		for event in pygame.event.get():
			if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mouseX, mouseY = event.pos
			elif event.type == MOUSEBUTTONUP:
				mouseX, mouseY = event.pos
				mouseClick = True
		boxX, boxY = getBoxAtPixel (mouseX, mouseY)
		if boxX != None and boxY != None:
			if not revealedBoxes[boxX] [boxY]:
				drawHighlightBox(boxX, boxY)
			if not revealedBoxes [boxX] [boxY] and mouseClick:
				revealBoxesAnimation(mainBoard, [(boxX, boxY)])
				revealedBoxes[boxX] [boxY] = True

				if firstSelection == None:
					firstSelection = (boxX, boxY)
				else:
					icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
					icon2shape, icon2color = getShapeAndColor(mainBoard, boxX, boxY)

					if icon1shape != icon2shape or icon1color != icon2color:
						pygame.time.wait(1000)
						coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxX, boxY)])
						revealedBoxes[firstSelection[0]][firstSelection[1]] = False
						revealedBoxes [boxX] [boxY] = False
					elif hasWon(revealedBoxes):
						gameWonAnimation(mainBoard)
						pygame.time.wait(2000)

						mainBoard = getRandomizedBoard()
						revealedBoxes = generateRevealedBoxesData(False)

						drawBoard(mainBoard, revealedBoxes)
						pygame.display.update()
						pygame.time.wait(1000)

						startGameAnimation(mainBoard)
					firstSelection = None
		pygame.display.update()
		fpsClock.tick(frames)

def generateRevealedBoxesData(val):
	revealedBoxes = []
	for i in range(boardwide):
		revealedBoxes.append([val] * boardhigh)
	return revealedBoxes

def getRandomizedBoard():

	icons = []
	for color in allTheColo:
		for shape in allTheShape:
			icons.append( (shape, color))

	random.shuffle(icons)
	numIconsUsed = int (boardwide * boardhigh / 2)

	icons = icons[:numIconsUsed] * 2
	random.shuffle(icons)

	board = []
	for x in range(boardwide):
		column = []
		for y in range(boardhigh):
			column.append(icons[0])
			del icons[0]
		board.append(column)
	return board

def splitIntoGroupsOf(groupSize, theList):
	result = []

	for i in range(0, len(theList), groupSize):
		result.append(theList[i:i +groupSize])
	return result

def leftTopCoordOfBox(boxX, boxY):
	left = boxX * (card + space) + Xmarg
	top = boxY * (card + space) + Ymarg
	return (left, top)

def getBoxAtPixel(x, y):
	for boxX in range(boardwide):
		for boxY in range(boardhigh):
			left, top = leftTopCoordOfBox(boxX, boxY)
			boxRect = pygame.Rect(left, top, card, card)
			if boxRect.collidepoint(x, y):
				return (boxX, boxY)
	return (None, None)

def drawIcon (shape, color, boxX, boxY):
	quarter = int(card * 0.25)
	half = int(card * 0.5)

	left, top = leftTopCoordOfBox(boxX, boxY)

	if shape == donut:
		pygame.draw.circle(displayStuff, color, (left + half, top + half), half - 5)
		pygame.draw.circle(displayStuff, backgroundColo, (left + half, top + half), quarter - 5)

	elif shape == square:
		pygame.draw.rect(displayStuff, color, (left + quarter, top + quarter, card - half, card - half))
	elif shape == diamond:
		pygame.draw.polygon(displayStuff, color, ((left + half, top), (left + card - 1, top + half), (left + half, top + card - 1), (left, top + half)))
	elif shape == lines:
		for i in range(0, card, 4):
			pygame.draw.line(displayStuff, color, (left, top + i), (left + i, top))
			pygame.draw.line(displayStuff, color, (left + i, top + card - 1), (left + card - 1, top + i))

	elif shape == oval:
		pygame.draw.ellipse(displayStuff, color, (left, top + quarter, card, half))

def getShapeAndColor(board, boxX, boxY):

	return board[boxX] [boxY] [0], board[boxX] [boxY] [1]

def drawBoxCovers(board, boxes, coverage):
	for box in boxes:
		left, top = leftTopCoordOfBox(box[0], box[1])
		pygame.draw.rect(displayStuff, backgroundColo, (left, top, card, card))

		shape, color = getShapeAndColor(board, box[0], box[1])
		drawIcon(shape, color, box[0], box[1])
		if coverage > 0:
			pygame.draw.rect(displayStuff, cardcolo, (left, top, coverage, card))
	pygame.display.update()
	fpsClock.tick(frames)

def revealBoxesAnimation (board, boxesToReveal):
	for coverage in range(card, (-flip) - 1, - flip):
		drawBoxCovers(board, boxesToReveal, coverage)

def coverBoxesAnimation(board, boxesToCover):
	for coverage in range(0, card + flip, flip):
		drawBoxCovers(board, boxesToCover, coverage)

def drawBoard( board, revealed):
	for boxX in range(boardwide):
		for boxY in range(boardhigh):
			left, top = leftTopCoordOfBox(boxX, boxY)
			if not revealed[boxX] [boxY]:
				pygame.draw.rect(displayStuff, cardcolo, (left, top, card, card))
			else:
				shape, color = getShapeAndColor(board, boxX, boxY)

def drawHighlightBox (boxX, boxY):
	left, top = leftTopCoordOfBox(boxX, boxY)
	pygame.draw.rect(displayStuff, highLiteCol, (left - 5, top - 5,card + 10, card +10), 4)

def startGameAnimation(board):
	coveredBoxes = generateRevealedBoxesData(False)
	boxes = []
	for x in range(boardwide):
		for y in range(boardhigh):
			boxes.append( (x,y) )
	random.shuffle(boxes)
	boxGroups = splitIntoGroupsOf(8, boxes)

	drawBoard(board, coveredBoxes)
	for boxGroup in boxGroups:
		revealBoxesAnimation(board, boxGroup)
		coverBoxesAnimation(board, boxGroup)

def gameWonAnimation(board):
	coveredBoxes = generateRevealedBoxesData(True)
	color1 = lightBGColo
	color2 = backgroundColo

	for i in range(13):
		color1, color2 = color2, color1
		displayStuff.fill(color1)
		drawBoard(board, coveredBoxes)
		pygame.display.update()
		pygame.time.wait(300)

def hasWon(revealedBoxes):
	for i in revealedBoxes:
		if False in i:
			return False
	return True

if __name__ == '__main__':
	main()