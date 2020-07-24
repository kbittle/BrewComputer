from widgets.colors import *

# Graph function to display temp vs time
def paintSwitch(pygame, screen, x_base, y_base, title="", position=0):
    
    x_length=300
    y_length=200
    line_size=4

    # Text Font
    smallFont = pygame.font.Font(None, 20)
    font = pygame.font.Font(None, 25)
    labelFont = pygame.font.Font(None, 30)

    # Draw background of controller
    pygame.draw.rect(screen,grey1,[x_base,y_base,x_length,y_length])
    pygame.draw.rect(screen,black,[x_base,y_base,x_length,y_length],line_size)

    # Draw 3 pos switch
    pygame.draw.circle(screen, black, [x_base+int(x_length/2), y_base+int(y_length/2)+20], 60,0)
    pygame.draw.circle(screen, grey2, [x_base+int(x_length/2), y_base+int(y_length/2)+20], 60,8)

    if position == 0:        
        xPoint1 = x_base+int(x_length/3) + 6
        yPoint1 = y_base+int(y_length/3) + 6
        xPoint2 = x_base+int(x_length/2) - 10
        yPoint2 = y_base+int(y_length/2) + 10
        pygame.draw.circle(screen, grey3, [xPoint1, yPoint1], 8,0)
        pygame.draw.polygon(screen, grey3,[(xPoint1+5,yPoint1-5),(xPoint1-5,yPoint1+5),(xPoint2-5,yPoint2+5),(xPoint2+5,yPoint2-5)]) 
        pygame.draw.circle(screen, grey3, [xPoint2, yPoint2], 8,0)   

        xPoint1 = x_base+int(x_length/3) + 7
        yPoint1 = y_base+int(y_length/3) + 7
        xPoint2 = x_base+int(x_length/2) - 32
        yPoint2 = y_base+int(y_length/2) - 16
        pygame.draw.circle(screen, white, [xPoint1, yPoint1], 4,0)
        pygame.draw.polygon(screen, white,[(xPoint1+3,yPoint1-3),(xPoint1-3,yPoint1+3),(xPoint2-3,yPoint2+3),(xPoint2+3,yPoint2-3)]) 
        pygame.draw.circle(screen, white, [xPoint2, yPoint2], 4,0)
    elif position == 1:
        pygame.draw.circle(screen, grey3, [x_base+int(x_length/2), y_base+int(y_length/2)-40], 8,0)
        pygame.draw.rect(screen, grey3,[x_base+int(x_length/2)-8,y_base+int(y_length/2)-40,16, 50]) 
        pygame.draw.circle(screen, grey3, [x_base+int(x_length/2), y_base+int(y_length/2)+10], 8,0)   

        pygame.draw.circle(screen, white, [x_base+int(x_length/2), y_base+int(y_length/2)-40], 4,0)
        pygame.draw.rect(screen, white,[x_base+int(x_length/2)-4,y_base+int(y_length/2)-40, 8, 20]) 
        pygame.draw.circle(screen, white, [x_base+int(x_length/2), y_base+int(y_length/2)-20], 4,0)
    elif position == 2:
        xPoint1 = x_base+int(x_length/3*2) - 6
        yPoint1 = y_base+int(y_length/3) + 6
        xPoint2 = x_base+int(x_length/2) + 10
        yPoint2 = y_base+int(y_length/2) + 10
        pygame.draw.circle(screen, grey3, [xPoint1, yPoint1], 8,0)
        pygame.draw.polygon(screen, grey3,[(xPoint1-5,yPoint1-5),(xPoint1+5,yPoint1+5),(xPoint2+5,yPoint2+5),(xPoint2-5,yPoint2-5)]) 
        pygame.draw.circle(screen, grey3, [xPoint2, yPoint2], 8,0)   

        xPoint1 = x_base+int(x_length/3*2) - 7
        yPoint1 = y_base+int(y_length/3) + 7
        xPoint2 = x_base+int(x_length/2) + 32
        yPoint2 = y_base+int(y_length/2) - 16
        pygame.draw.circle(screen, white, [xPoint1, yPoint1], 4,0)
        pygame.draw.polygon(screen, white,[(xPoint1-3,yPoint1-3),(xPoint1+3,yPoint1+3),(xPoint2+3,yPoint2+3),(xPoint2-3,yPoint2-3)]) 
        pygame.draw.circle(screen, white, [xPoint2, yPoint2], 4,0)

    # Draw switch title
    titleStr = labelFont.render(title,True, black) 
    screen.blit(titleStr, [x_base+20, y_base+y_length-30])

    # Draw switch position text labels
    pygame.draw.rect(screen,black,[x_base+int(x_length/2)-35, y_base+10, 70, 40])
    pygame.draw.rect(screen,black,[x_base+20, y_base+40, 70, 40])
    pygame.draw.rect(screen,black,[x_base+x_length-90, y_base+40, 70, 40])

    labelStr = labelFont.render("Off",True, white) 
    screen.blit(labelStr, [x_base+40, y_base+50])
    labelStr = labelFont.render("Auto",True, white) 
    screen.blit(labelStr, [x_base+int(x_length/2)-25, y_base+20])
    labelStr = labelFont.render("On",True, white) 
    screen.blit(labelStr, [x_base+x_length-70, y_base+50])

