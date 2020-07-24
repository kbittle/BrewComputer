from widgets.gauge import gauge_display
from widgets.graph import graph_display
import math
from widgets.colors import *
from constants import *

def guiDisplay(pygame, screen, current_time="", timer_hours=0, timer_minutes=0, 
               timer_seconds=0, target_temperature=0, current_temperature=0, 
               last_heat_counter=0, solenoid_delay_time=0, solenoid_counter=0, 
               packet_counter=0, heat_text="Off", sensor_temperature=[0,0,0],
               temperature_log=[[0,0]]):
    # Create Fonts
    font = pygame.font.Font(None, 25)

    # Information text boxes
    pygame.draw.rect(screen,grey2,[0,0,300,400])
    pygame.draw.rect(screen,black,[0,0, full_screen_width, full_screen_height],10)
    pygame.draw.rect(screen,black,[0,0,300,40],5)
    pygame.draw.rect(screen,black,[0,40,300,40],5)
    pygame.draw.rect(screen,black,[0,80,300,40],5)
    pygame.draw.rect(screen,black,[0,120,300,40],5)
    pygame.draw.rect(screen,black,[0,160,300,40],5)
    pygame.draw.rect(screen,black,[0,200,300,40],5)
    pygame.draw.rect(screen,black,[0,240,300,40],5)
    pygame.draw.rect(screen,black,[0,280,300,40],5)    
    pygame.draw.rect(screen,black,[0,320,300,40],5)
    pygame.draw.rect(screen,black,[0,360,300,40],5)

    # Heat text Box  
    pygame.draw.rect(screen,grey2,[300,0,(full_screen_width - 300),160])
    pygame.draw.rect(screen,black,[300,0,(full_screen_width - 300),160],5) 
    
    rtc_string = font.render("Time: " + current_time,True,green)
    timer_string = font.render("Timer: {0:02d}:{1:02d}:{2:02d}".format(timer_hours, timer_minutes, timer_seconds),True,green)
    target_temperature_string = font.render("Target Temperature: {0} \B0F".format(target_temperature),True,green)
    current_temperature_string = font.render("Current Temperature: {0} \B0F".format(current_temperature),True,green)
    time_to_hit_temperature_string = font.render("Time until Target Temp: {0} sec".format(0),True,green)
    last_heat_cycle_time_string = font.render("Last Heat Cycle: {0} sec".format(last_heat_counter),True,green)
    solenoid_delay_time_string = font.render("Solenoid Delay: {0} sec".format(solenoid_delay_time),True,green)
    solenoid_count_down_string = font.render("Solenoid Counter: {0} sec".format(solenoid_counter),True,green)
    display_packet_counter_string = font.render("Packet Counter: {0}".format(packet_counter),True,green)
 
    screen.blit(rtc_string, [10,10])
    screen.blit(timer_string, [10,50])
    screen.blit(target_temperature_string, [10,90])
    screen.blit(current_temperature_string, [10,130])
    screen.blit(time_to_hit_temperature_string, [10,170])
    screen.blit(last_heat_cycle_time_string, [10,210])
    screen.blit(solenoid_delay_time_string, [10,250])
    screen.blit(solenoid_count_down_string, [10,290])
    screen.blit(display_packet_counter_string, [10,330])
    
    #screen.blit(heat_text, [320,50])
    
    # Display Gauges
    #gauge_display(20,170, sensor_temperature[0])
    gauge_display(pygame, screen, 310, 170, sensor_temperature[0])
    gauge_display(pygame, screen, 670, 170, sensor_temperature[1])
    gauge_display(pygame, screen, 1030, 170, sensor_temperature[2])
    
    graph_display(pygame, screen, 10, 520, full_screen_width - 20, 380, 
        int(round(current_temperature)), target_temperature, temperature_log)

    #Parameters:           surface, color,       x,     y, length, height,width, text,  text_color
    #button_1.create_button(screen, grey3, 10,  615,    100,    100,    0, "B1", green)
    #button_2.create_button(screen, grey3, 120, 615,    100,    100,    0, "B2", green)
    #button_3.create_button(screen, grey3, 230, 615,    100,    100,    0, "B3", green)
    #button_4.create_button(screen, grey3, 340, 615,    100,    100,    0, "B4", green)

def draw_dashed_line(pygame, surf, color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(surf, color, start, end, width)

# Graph function to display temp vs time
def paintBreweryDiagram(pygame, screen, x_base, y_base):

    segmentFont = pygame.font.Font(SEVEN_SEGMENT_FONT_PATH, 50)

    # Draw image
    image = pygame.image.load(OLD_BREWERY_PNG_PATH)
    screen.blit(image, (x_base, y_base))

    # Draw border
    pygame.draw.rect(screen,black,[x_base,y_base,946,568], 5)

    # Draw temperature boxes
    pygame.draw.rect(screen,grey2,[x_base+620,y_base+70,200,60])
    pygame.draw.rect(screen,black,[x_base+620,y_base+70,200,60], 5)
    pygame.draw.rect(screen,grey2,[x_base+620,y_base+350,200,60])
    pygame.draw.rect(screen,black,[x_base+620,y_base+350,200,60], 5)

    # Draw text onto temp boxes
    postChillValue = segmentFont.render(str("125.4"),True,blue)
    screen.blit(postChillValue, [x_base+630,y_base+75])
    preChillValue = segmentFont.render(str("210.7"),True,red)
    screen.blit(preChillValue, [x_base+630,y_base+355])

    # Draw water lines
    draw_dashed_line(pygame, screen, blue, (x_base+380,y_base+155),(x_base+690,y_base+155),16, 20)
    draw_dashed_line(pygame, screen, red, [x_base+313,y_base+390],[x_base+313,y_base+435],16, 20)
    draw_dashed_line(pygame, screen, red, [x_base+313,y_base+432],[x_base+450,y_base+432],16, 20)