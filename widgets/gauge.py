import math
from widgets.colors import *

# Gauge Function to draw temperature gauges
def gauge_display(pygame, screen, x_init, y_init, temp):
    diameter = 350
    
    # Gauge labels font
    gauge_font = pygame.font.Font(None, 18)
    # Text Font
    font = pygame.font.Font(None, 25)

    tick_color = green
    tick_indent_long = (diameter / 2) - 15
    tick_indent_medium = (diameter / 2) - 10
    tick_indent_short = (diameter / 2) - 5
    number_indent = (diameter / 2) - 30

    # Draw background  
    pygame.draw.circle(screen,black,[int(x_init+(diameter/2)),int(y_init+(diameter/2))],int(diameter/2),0)
    pygame.draw.circle(screen,grey3,[int(x_init+(diameter/2)),int(y_init+(diameter/2))],int(diameter/2)-5,0)
    pygame.draw.circle(screen,grey2,[int(x_init+(diameter/2)),int(y_init+(diameter/2))],int(diameter/2)-15,0)

    radian_temp = math.radians(325+(10))
    x_point1 = tick_indent_medium * math.sin(radian_temp) + (x_init + (diameter/2))
    y_point1 = tick_indent_medium * math.cos(radian_temp) + (y_init + (diameter/2))
    x_point2 = (diameter/2) * math.sin(radian_temp) + (x_init + (diameter/2))
    y_point2 = (diameter/2) * math.cos(radian_temp) + (y_init + (diameter/2))
    pygame.draw.line(screen,tick_color,[x_point1,y_point1],[x_point2,y_point2],3)
    
    for temperature_num in range(15):
        scaled_temp = temperature_num*20
        temperature_text = gauge_font.render(str(scaled_temp),True,black)
        radian_temp = math.radians(325-(scaled_temp))
        screen.blit(temperature_text, [number_indent*math.sin(radian_temp)+((x_init-10)+(diameter/2)), number_indent*math.cos(radian_temp)+((y_init-5)+(diameter/2))])
        x_point1 = tick_indent_long * math.sin(radian_temp) + (x_init + (diameter/2))
        y_point1 = tick_indent_long * math.cos(radian_temp) + (y_init + (diameter/2))
        x_point2 = (diameter/2) * math.sin(radian_temp) + (x_init + (diameter/2))
        y_point2 = (diameter/2) * math.cos(radian_temp) + (y_init + (diameter/2))
        pygame.draw.line(screen,tick_color,[x_point1,y_point1],[x_point2,y_point2],4)

        scaled_temp = (temperature_num*20)+10
        radian_temp = math.radians(325-(scaled_temp))
        x_point1 = tick_indent_medium * math.sin(radian_temp) + (x_init + (diameter/2))
        y_point1 = tick_indent_medium * math.cos(radian_temp) + (y_init + (diameter/2))
        x_point2 = (diameter/2) * math.sin(radian_temp) + (x_init + (diameter/2))
        y_point2 = (diameter/2) * math.cos(radian_temp) + (y_init + (diameter/2))
        pygame.draw.line(screen,tick_color,[x_point1,y_point1],[x_point2,y_point2],3)

    
    #Draw Pointer Arrow
    radian_temp = math.radians(325 - temp + 10)
    x_point1 = -20 * math.sin(radian_temp) + (x_init + (diameter/2))
    y_point1 = -20 * math.cos(radian_temp) + (y_init + (diameter/2))
    radian_temp = math.radians(325 - temp)
    x_point2 = (diameter/2) * math.sin(radian_temp) + (x_init + (diameter/2))
    y_point2 = (diameter/2) * math.cos(radian_temp) + (y_init + (diameter/2))
    radian_temp = math.radians(325 - temp - 10)
    x_point3 = -20 * math.sin(radian_temp) + (x_init + (diameter/2))
    y_point3 = -20 * math.cos(radian_temp) + (y_init + (diameter/2))
    pygame.draw.polygon(screen,green,[(x_point1,y_point1),(x_point2,y_point2),(x_point3,y_point3)],0)
    pygame.draw.circle(screen,black,[int(x_init+(diameter/2)),int(y_init+(diameter/2))],10,0)
    
    degree_f_symbol = font.render("\B0F",True,black)
    screen.blit(degree_f_symbol, [(x_init+(diameter/2)-10),(y_init+(diameter)-40)])

    pygame.draw.rect(screen,grey1, [(x_init+(diameter/2)-40),(y_init+(diameter/2)+25),(80),(20)],0)  
    degree_temp = font.render(str("%0.4f" % temp),True,black)
    screen.blit(degree_temp, [(x_init+(diameter/2)-40),(y_init+(diameter/2)+25)])