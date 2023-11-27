from resources.gnegzUtils import Matrix
import pygame
import pygame.freetype
import json                   

with open("config.json", "r") as config:
    config = json.load(config)

    matrixSize = config["matrixSize"]
    cellSize = config["cellSize"]

    font = config["font"]

    backgroundColour = config["colours"]["background"]
    accentColour = config["colours"]["accent"]
    textColour = config["colours"]["text"]
    disabledColour = config["colours"]["disabled"]
    errorColour = config["colours"]["error"]

margin = cellSize // 4

matrix = Matrix(matrixSize)

infoText = f"0/{matrix.winScore}"

pygame.init()
windowSize = (cellSize + margin) * matrixSize + ((cellSize * 2) + margin)
textWriter = pygame.freetype.Font("resources/" + font, cellSize)
clock = pygame.time.Clock()
window = pygame.display.set_mode((windowSize, windowSize + cellSize + (margin * 2)))


 
runningFlag = True
lossFlag = False
gamingFlag = True
while True:
    window.fill(backgroundColour)

    for yPrinter in range(1, matrixSize + 1):
        for xPrinter in range(1, matrixSize + 1):
            if matrix.getCell(xPrinter - 1, yPrinter - 1)["mode"] == "opened":
                if matrix.getCell(xPrinter - 1, yPrinter - 1)["hasMine"] == False:
                    if (mines := matrix.countMines(xPrinter - 1, yPrinter - 1)) == 0:
                        mines = ''
                    pygame.draw.rect(window,
                                 accentColour,
                                 (xPrinter * (cellSize + margin) , yPrinter * (cellSize + margin),
                                  cellSize, cellSize))
                    textWriter.render_to(window,
                                     ((xPrinter * (cellSize + margin)) + margin, (yPrinter * (cellSize + margin)) + (margin * 0.6)),
                                     str(mines),
                                     textColour)
                else:
                    pygame.draw.rect(window,
                                    errorColour,
                                    (xPrinter * (cellSize + margin), yPrinter * (cellSize + margin),
                                    cellSize, cellSize))
                    
            elif matrix.getCell(xPrinter - 1, yPrinter - 1)["mode"] == "closed":
                pygame.draw.rect(window,
                                 disabledColour,
                                 (xPrinter * (cellSize + margin), yPrinter * (cellSize + margin),
                                  cellSize, cellSize))
                
            else:
                pygame.draw.rect(window,
                                 errorColour,
                                 (xPrinter * (cellSize + margin), yPrinter * (cellSize + margin),
                                  cellSize, cellSize))
            
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            xPos, yPos = pygame.mouse.get_pos()
 
            xMatrixPos = int((xPos / (cellSize + margin))) - 1
            yMatrixPos = int((yPos / (cellSize + margin))) - 1

            if (xMatrixPos < matrixSize and yMatrixPos < matrixSize) and (xMatrixPos >= 0 and yMatrixPos >= 0) and gamingFlag:
                if event.button == 1:
                    if matrix.getCell(xMatrixPos, yMatrixPos)["mode"] != "marked":
                        matrix.getCell(xMatrixPos, yMatrixPos)["mode"] = "opened"
                        if matrix.getCell(xMatrixPos, yMatrixPos)["hasMine"] == False:
                            if matrix.countMines(xMatrixPos, yMatrixPos) == 0:
                                matrix.revealCells(xMatrixPos, yMatrixPos)
                            else:
                                matrix.gainScore(xMatrixPos, yMatrixPos)
                        else:
                            lossFlag = True

                elif event.button == 3:
                    if matrix.getCell(xMatrixPos, yMatrixPos)["mode"] == "marked":
                        matrix.getCell(xMatrixPos, yMatrixPos)["mode"] = "closed"
                    else: 
                        matrix.getCell(xMatrixPos, yMatrixPos)["mode"] = "marked"

        elif event.type == pygame.QUIT:
            runningFlag = False

    pygame.draw.rect(window,
                     accentColour,
                     (cellSize + margin, (cellSize + margin) * (matrixSize + 1) + margin,
                      (cellSize + margin) * matrixSize - margin, cellSize))
    textWriter.render_to(window,
                         (cellSize + (margin * 2), (cellSize + margin) * (matrixSize + 1) + (margin * 1.6)),
                         infoText,
                         textColour)
    infoText = f"{matrix.score} / {matrix.winScore}"


    if not runningFlag:
        pygame.display.flip()
        break

    if lossFlag == True:
        infoText = "Loss!"
        matrix.revealMatrix()
        gamingFlag = False
    elif matrix.score >= matrix.winScore:
        infoText = "Win!"
        matrix.revealMatrix()
        gamingFlag = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
