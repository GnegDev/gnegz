from gnegzUtils import Matrix
import pygame
import pygame.freetype                         

yellowRGB = (255, 255, 0)
blackRGB = (0, 0, 0)
blueRGB = (0, 0, 255)
redRGB = (255, 0, 0)
orangeRGB = (255, 130, 0)

matrixSize = 20 # int(input("Enter a matrix size: "))
squareSize = 20 # int(input("Enter a square size: "))

margin = squareSize // 4

matrix = Matrix(matrixSize)

infoText = f"0/{matrix.winScore}"

pygame.init()
windowSize = (squareSize + margin) * matrixSize + ((squareSize * 2) + margin)
textWriter = pygame.freetype.Font("lobster.ttf", squareSize)
clock = pygame.time.Clock()
window = pygame.display.set_mode((windowSize, windowSize + squareSize + (margin * 2)))


 
runningFlag = True
lossFlag = False
gamingFlag = True
while True:
    window.fill(blueRGB)

    for yPrinter in range(1, matrixSize + 1):
        for xPrinter in range(1, matrixSize + 1):
            if matrix.getCell(xPrinter - 1, yPrinter - 1)["mode"] == "opened":
                if matrix.getCell(xPrinter - 1, yPrinter - 1)["hasMine"] == False:
                    if (mines := matrix.countMines(xPrinter - 1, yPrinter - 1)) == 0:
                        mines = ''
                    pygame.draw.rect(window,
                                 yellowRGB,
                                 (xPrinter * (squareSize + margin) , yPrinter * (squareSize + margin),
                                  squareSize, squareSize))
                    textWriter.render_to(window,
                                     ((xPrinter * (squareSize + margin)) + (squareSize // 4), (yPrinter * (squareSize + margin)) + (squareSize // 4)),
                                     str(mines),
                                     redRGB)
                else:
                    pygame.draw.rect(window,
                                    redRGB,
                                    (xPrinter * (squareSize + margin), yPrinter * (squareSize + margin),
                                    squareSize, squareSize))
                    
            elif matrix.getCell(xPrinter - 1, yPrinter - 1)["mode"] == "closed":
                pygame.draw.rect(window,
                                 blackRGB,
                                 (xPrinter * (squareSize + margin), yPrinter * (squareSize + margin),
                                  squareSize, squareSize))
                
            else:
                pygame.draw.rect(window,
                                 orangeRGB,
                                 (xPrinter * (squareSize + margin), yPrinter * (squareSize + margin),
                                  squareSize, squareSize))
            
            '''
            if matrix.getCell(xPrinter - 1, yPrinter - 1)["hasMine"] == True:
                pygame.draw.rect(window,
                                    redRGB,
                                    (xPrinter * (squareSize + margin), yPrinter * (squareSize + margin),
                                    squareSize, squareSize))
            textWriter.render_to(window,
                                     ((xPrinter * (squareSize + margin)) + (squareSize // 4), (yPrinter * (squareSize + margin)) + (squareSize // 4)),
                                     str(matrix.countMines(xPrinter - 1, yPrinter - 1)),
                                     redRGB)'''
            
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            xPos, yPos = pygame.mouse.get_pos()
 
            xMatrixPos = int((xPos / (squareSize + margin))) - 1
            yMatrixPos = int((yPos / (squareSize + margin))) - 1

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
                            matrix.revealMatrix()

                elif event.button == 3:
                    if matrix.getCell(xMatrixPos, yMatrixPos)["mode"] == "marked":
                        matrix.getCell(xMatrixPos, yMatrixPos)["mode"] = "closed"
                    else: 
                        matrix.getCell(xMatrixPos, yMatrixPos)["mode"] = "marked"

        elif event.type == pygame.QUIT:
            runningFlag = False

    pygame.draw.rect(window,
                     yellowRGB,
                     (squareSize + margin, (squareSize + margin) * (matrixSize + 1) + margin,
                      (squareSize + margin) * matrixSize - margin, squareSize))
    textWriter.render_to(window,
                         (squareSize + margin, (squareSize + margin) * (matrixSize + 1) + margin),
                         infoText,
                         blackRGB)
    infoText = f"{matrix.score} / {matrix.winScore}"


    if not runningFlag:
        pygame.display.flip()
        break

    if lossFlag == True:
        infoText = "Loss!"
        gamingFlag = False
    elif matrix.score >= matrix.winScore:
        infoText = "Win!"
        gamingFlag = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
