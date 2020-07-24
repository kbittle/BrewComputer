from widgets.colors import *
import os, datetime
from datetime import datetime, timedelta
from constants import *

def drawMenuStrip(pygame, screen, x_base, y_base, menuHeight, curDateTime=datetime.now(), showBlynkIcon=True, 
    showDatabaseIcon=True, showWifiIcon=True, timerSeconds=0, mmiComm=False, 
    waterLevelComm=False, rtcComm=False, i2cError=False, indicatorFlashState=[0]):

    # Create fonts
    font = pygame.font.Font(None, 25)
    timeDateFont = pygame.font.Font(None, 35)
    titleFont = pygame.font.Font(None, 60)
    segmentFont = pygame.font.Font(SEVEN_SEGMENT_FONT_PATH, 60)

    # Draw top menu bar
    pygame.draw.rect(screen,grey1,[x_base, y_base, full_screen_width, menuHeight])
    pygame.draw.rect(screen,black,[x_base, y_base, full_screen_width, menuHeight], 2)

    # Draw Icons
    varShrinkage = 3

    if showBlynkIcon:
        image = pygame.image.load(BLYNK_ICON_PATH)
        image = pygame.transform.scale(image, (menuHeight-varShrinkage, menuHeight-varShrinkage))
        screen.blit(image, (x_base+1030, y_base+2))

    if showWifiIcon:
        image = pygame.image.load(WIFI_ICON_PATH)
        image = pygame.transform.scale(image, (menuHeight-varShrinkage, menuHeight-varShrinkage))
        screen.blit(image, (x_base+1030+menuHeight, y_base+2))

    if showDatabaseIcon:
        image = pygame.image.load(DATABASE_ICON_PATH)
        image = pygame.transform.scale(image, (menuHeight-varShrinkage, menuHeight-varShrinkage))
        screen.blit(image, (x_base+1030+menuHeight*2, y_base+2))

    # Draw American Flag
    image = pygame.image.load(AMERICAN_FLAG_PATH)
    image = pygame.transform.scale(image, (int((menuHeight-varShrinkage)*3.5/2), menuHeight-varShrinkage) )
    screen.blit(image, (x_base+2, y_base+2))

    # Draw Time and date
    timeStr = curDateTime.strftime("%H:%M:%S")
    timeRendered = timeDateFont.render(timeStr, True, black) 
    screen.blit(timeRendered, [x_base+full_screen_width-150, int(menuHeight/3)-10])
    dateStr = curDateTime.strftime("%m/%d/%Y")
    dateRendered = timeDateFont.render(dateStr, True, black) 
    screen.blit(dateRendered, [x_base+full_screen_width-150, int(menuHeight/3*2)-10])

    # Create timer str
    if timerSeconds > 0:
        delta = timedelta(seconds=timerSeconds)
        timestamp = datetime(1,1,1) + delta
        timeString = "{:02d}:{:02d}:{:02d}".format(timestamp.hour, timestamp.minute, timestamp.second)
    else:
        timeString = "00:00:00"

    # Draw timer
    pygame.draw.rect(screen,black,[x_base+800, y_base+2, 200, menuHeight])
    timerStr = segmentFont.render( timeString,True, green) 
    screen.blit(timerStr, [x_base+805, y_base+4])

    # Draw Title
    timeStr = titleFont.render("Bittle's Brewery",True, black) 
    screen.blit(timeStr, [x_base+310, y_base+15])

    # Set flash rate based on OS
    if os.name == 'nt':
        flashRate = 30
    else:
        flashRate = 1

    # Comm indicator logic
    if indicatorFlashState[0] == '1':
        indicatorFlashState[1] += 1

        if indicatorFlashState[1] > flashRate:
            indicatorFlashState[0] = '0'
            indicatorFlashState[1] = 0

        # Indicators are cleared by the repainting of this widget
    else:
        indicatorFlashState[1] += 1

        if indicatorFlashState[1] > flashRate:
            indicatorFlashState[0] = '1'
            indicatorFlashState[1] = 0

        # Draw indicators
        if mmiComm:
            pygame.draw.rect(screen, red,[x_base+120, y_base+10, 80, 20])
            errorText = font.render(str("MMI Error"), True, white)
            screen.blit(errorText, [x_base+120,y_base+10])

        if waterLevelComm:
            pygame.draw.rect(screen, red,[x_base+120, y_base+35, 80, 20])
            errorText = font.render(str("WLS Error"), True, white)
            screen.blit(errorText, [x_base+120,y_base+35])

        if rtcComm:
            pygame.draw.rect(screen, red,[x_base+215, y_base+10, 80, 20])
            errorText = font.render(str("RTC Error"), True, white)
            screen.blit(errorText, [x_base+215,y_base+10])

        if i2cError:
            pygame.draw.rect(screen, red,[x_base+215, y_base+35, 80, 20])
            errorText = font.render(str("I2C Error"), True, white)
            screen.blit(errorText, [x_base+215,y_base+35])
