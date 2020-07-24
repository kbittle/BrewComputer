from widgets.colors import *

# Graph function to display temp vs time
def graph_display(pygame, screen, x_base, y_base, x_length, y_length, temp, target_temp, temperature_log):
    #x_length = full_screen_width - 20
    #y_length = 380
    line_size = 2
    index = 0
    graph_y_min = 0
    graph_y_max = 0
    graph_font = pygame.font.Font(None, 12)
    temp_log_current_index = 0
    temp_log_target_index = 1

    # Check to make sure temp is valid
    if (temp < 0) or (temp > 280):
        return

    # Add temp to temperature list
    if (len(temperature_log) > (x_length - 10)):
        temperature_log.pop(0)
        temperature_log.append([temp,target_temp])
    else:
        temperature_log.append([temp,target_temp])

    # Draw background of graph
    pygame.draw.rect(screen,white,[x_base,y_base,x_length,y_length])
    pygame.draw.rect(screen,black,[x_base,y_base,x_length,y_length],line_size)

    # Calculate current graph offset based off new temp data
    if (temp >= 50) and (temp <= 220):
        graph_y_min = 50
        graph_y_max = 220
    elif (temp < 50):
        if (temp < 10):
            graph_y_min = 0
            graph_y_max = 170
        elif (temp < 20):
            graph_y_min = 10
            graph_y_max = 180
        elif (temp < 30):
            graph_y_min = 20
            graph_y_max = 190
        elif (temp < 40):
            graph_y_min = 30
            graph_y_max = 200
        else:
            graph_y_min = 40
            graph_y_max = 210
    elif (temp > 220):
        if (temp > 270):
            graph_y_min = 110
            graph_y_max = 280
        elif (temp > 260):
            graph_y_min = 100
            graph_y_max = 270
        elif (temp > 250):
            graph_y_min = 90
            graph_y_max = 260
        elif (temp > 240):
            graph_y_min = 80
            graph_y_max = 250
        elif (temp > 240):
            graph_y_min = 70
            graph_y_max = 240
        else:
            graph_y_min = 60
            graph_y_max = 230
        
    # Draw every point on the plot
    for temp_reading in temperature_log:
        index += 1
        if(temp_reading[temp_log_current_index] >= graph_y_min) and (temp_reading[temp_log_current_index] <= graph_y_max):
            pygame.draw.circle(screen,green,[int((x_base + 5) + index),(y_base + y_length + graph_y_min) - temp_reading[temp_log_current_index]],1)
        if(temp_reading[temp_log_target_index] >= graph_y_min) and (temp_reading[temp_log_target_index] <= graph_y_max):
            pygame.draw.circle(screen,red,[int((x_base + 5) + index),(y_base + y_length + graph_y_min) - temp_reading[temp_log_target_index]],1)

    # Draw y-azis label
    for temp_tick in range(1,int(y_length / 10)):
        pygame.draw.line(screen,black,[(x_base + line_size),(y_base + y_length) - (10 * temp_tick)],[(x_base + 3),(y_base + y_length) - (10 * temp_tick)],line_size)
        graph_label = graph_font.render(str((10 * temp_tick) + graph_y_min),True,black) 
        screen.blit(graph_label, [(x_base + 4),(y_base + y_length - line_size) - (10 * temp_tick)])
    