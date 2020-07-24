from widgets.colors import *
from constants import *

# Graph function to display temp vs time
def paintTempController(pygame, screen, x_base, y_base, currentTemp, targetTemp, gasValveOn):
    
    x_length=300
    y_length=300
    line_size=10

    # Text Font
    smallFont = pygame.font.Font(None, 20)
    font = pygame.font.Font(None, 25)
    labelFont = pygame.font.Font(None, 30)
    segmentFont = pygame.font.Font(SEVEN_SEGMENT_FONT_PATH, 50)

    # Draw background of controller
    pygame.draw.rect(screen,black,[x_base,y_base,x_length,y_length])
    pygame.draw.rect(screen,grey4,[x_base,y_base,x_length,y_length],line_size)
    pygame.draw.rect(screen,grey3,[x_base+50,y_base+40,200,60])
    pygame.draw.rect(screen,grey3,[x_base+50,y_base+120,200,60])
    pygame.draw.rect(screen,grey2,[x_base+10,y_base+210,280,80])

    # Draw degree C/F leds
    pygame.draw.circle(screen,red,[x_base+265,y_base+50],6,0)
    pygame.draw.circle(screen,grey4,[x_base+265,y_base+70],6,0)

    # Draw relay output leds:
    if gasValveOn:
        pygame.draw.circle(screen,red,[x_base+95,y_base+197],6,0)
    else:
        pygame.draw.circle(screen,grey4,[x_base+95,y_base+197],6,0)
    pygame.draw.circle(screen,grey4,[x_base+198,y_base+197],6,0)

    # Draw unused buttons
    pygame.draw.circle(screen,black,[x_base+55,y_base+250],25,0)
    pygame.draw.circle(screen,black,[x_base+120,y_base+250],25,0)
    pygame.draw.circle(screen,black,[x_base+180,y_base+250],25,0)
    pygame.draw.circle(screen,black,[x_base+245,y_base+250],25,0)
    pygame.draw.polygon(screen,grey2,[(x_base+120,y_base+240),(x_base+120,y_base+260),(x_base+110,y_base+250)],0)
    pygame.draw.polygon(screen,grey2,[(x_base+170,y_base+245),(x_base+190,y_base+245),(x_base+180,y_base+255)],0)
    pygame.draw.polygon(screen,grey2,[(x_base+240,y_base+240),(x_base+240,y_base+260),(x_base+250,y_base+250)],0)

    # Draw labels
    tempLabel = font.render(str("Temperature"),True,white)
    screen.blit(tempLabel, [x_base+10,y_base+10])

    pvLabel = labelFont.render(str("PV"),True,white)
    screen.blit(pvLabel, [x_base+15,y_base+45])

    spLabel = labelFont.render(str("SP"),True,white)
    screen.blit(spLabel, [x_base+15,y_base+125])

    farenheightLabel = smallFont.render(str("F"),True,white)
    screen.blit(farenheightLabel, [x_base+275,y_base+45])

    celciusLabel = smallFont.render(str("C"),True,white)
    screen.blit(celciusLabel, [x_base+275,y_base+65])

    out1Label = smallFont.render(str("OUT1"),True,white)
    screen.blit(out1Label, [x_base+50,y_base+190])

    out2Label = smallFont.render(str("OUT2"),True,white)
    screen.blit(out2Label, [x_base+150,y_base+190])

    setLabel = font.render(str("Set"),True,white)
    screen.blit(setLabel, [x_base+42,y_base+240])

    # Draw 7 segments
    segment1 = segmentFont.render("{0:.2f}".format(currentTemp),True,red)
    screen.blit(segment1, [x_base+70,y_base+45])

    segment2 = segmentFont.render("{0:.2f}".format(targetTemp),True,green)
    screen.blit(segment2, [x_base+70,y_base+125])



