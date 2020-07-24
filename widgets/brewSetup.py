from widgets.colors import *
from constants import *

def paintBreweryDiagram(pygame, screen, x_base, y_base, wortTempIn=0, wortTempOut=0, 
    pumpOn=False, valve1=False, valve2=False, waterLevel=5):

    font = pygame.font.Font(None, 25)
    tempFont = pygame.font.Font(None, 35)
    segmentFont = pygame.font.Font(SEVEN_SEGMENT_FONT_PATH, 50)

    # Draw image
    image = pygame.image.load(BREWERY_PNG_PATH)
    screen.blit(image, (x_base, y_base))

    # Erase wort chiller temps
    pygame.draw.rect(screen, black, [x_base+834, y_base+73, 109, 36])
    pygame.draw.rect(screen, black, [x_base+834, y_base+249, 109, 36])

    # Repaint temperature text
    wortTempOutStr = tempFont.render("{0:.2f}".format(wortTempOut), True, green) 
    screen.blit(wortTempOutStr, [x_base+838, y_base+80])
    wortTempInStr = tempFont.render("{0:.2f}".format(wortTempIn), True, green) 
    screen.blit(wortTempInStr, [x_base+838, y_base+256])
    
    # Draw Led's
    if pumpOn:
        pygame.draw.circle(screen, red, [x_base+639,y_base+326], 9, 0)
    else:
        pygame.draw.circle(screen, grey3, [x_base+639,y_base+326], 9, 0)
    pygame.draw.circle(screen, black, [x_base+638,y_base+326], 10, 1)

    if valve1:
        pygame.draw.circle(screen, red, [x_base+514,y_base+402], 9, 0)
    else:
        pygame.draw.circle(screen, grey3, [x_base+514,y_base+402], 9, 0)
    pygame.draw.circle(screen, black, [x_base+513,y_base+402], 10, 1)

    if valve2:
        pygame.draw.circle(screen, red, [x_base+779,y_base+401], 9, 0)
    else:
        pygame.draw.circle(screen, grey3, [x_base+779,y_base+401], 9, 0)
    pygame.draw.circle(screen, black, [x_base+778,y_base+401], 10, 1)

    # Draw water level
    if waterLevel >= 75:
        pygame.draw.line(screen, blue, [x_base+103, y_base+75], [x_base+103, y_base+408], 10)
    elif waterLevel >= 50:
        pygame.draw.line(screen, grey3, [x_base+103, y_base+75], [x_base+103, y_base+408], 10)
        pygame.draw.line(screen, blue, [x_base+103, y_base+155], [x_base+103, y_base+408], 10)
    elif waterLevel >= 25:
        pygame.draw.line(screen, grey3, [x_base+103, y_base+75], [x_base+103, y_base+408], 10)
        pygame.draw.line(screen, blue, [x_base+103, y_base+235], [x_base+103, y_base+408], 10)
    elif waterLevel >= 5:
        pygame.draw.line(screen, grey3, [x_base+103, y_base+75], [x_base+103, y_base+408], 10)
        pygame.draw.line(screen, blue, [x_base+103, y_base+340], [x_base+103, y_base+408], 10)
    else:
        pygame.draw.line(screen, grey3, [x_base+103, y_base+75], [x_base+103, y_base+408], 10)

