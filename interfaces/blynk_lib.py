import blynklib

# Blynk Virtual Pin layout
#
# V0 - Gauge(Current Temp)
# V1 - Number Box(Wort Chiller In)
# V2 - Number Box(Wort Chiller Out)
# V3 - LED(Gas)
# V4 - LED(Pump)
# V5 - Number Box(Target Temp)
# V6 - Button(Start Timer)
# V7 - Button(Start HopDropper)
# V8 - Terminal
# V9 - Number Box(Time Remaining)
#

BLYNK_AUTH = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXx'
appConnected = False
blynkDisconnectRcvd = False

# GUI Input Vars
timerActive = False
timerValueSeconds = 0

class blynk_lib:    
    global appConnected
    try:
        blynk = blynklib.Blynk(BLYNK_AUTH,
                                server='blynk-cloud.com', # set server address
                                port=80,                # set server port
                                heartbeat=10)
        appConnected = True
    
        @blynk.handle_event("connected")
        def blynk_connected(ping):
            global appConnected
            print('Blynk ready. Ping:', ping, 'ms')
            appConnected = True

        @blynk.handle_event("disconnected")    
        def blynk_disconnected():
            global appConnected, blynkDisconnectRcvd
            print('Blynk disconnected')
            appConnected = False
            blynkDisconnectRcvd = True

        # register handler for virtual pin V6 reading
        @blynk.handle_event("write V6")
        def read_virtual_pin_handler(pin, value):
            global timerActive
            print(">> Timer Button state: {}".format(value))
            if value[0] == "1":
                print(">> Timer Button Pressed")
                timerActive = True
            else:
                print(">> Timer Button Released")
                timerActive = False

        # register handler for virtual pin V6 terminal reading
        @blynk.handle_event("write V8")
        def write_handler(pin, values):
            global timerValueSeconds
            if values:
                cmd_params = values[0].split(' ')
                if cmd_params[0] == "set":
                    if cmd_params[1] == "timer":
                        print(">> Recieved Timer Set Cmd: {0}".format(cmd_params[2]))
                        timerValueSeconds = cmd_params[2]
                    else:
                        print("Unknown Set Cmd: {}".format(cmd_params[0]))
                else:
                    print("Unknown Cmd: {}".format(cmd_params[0]))

    except Exception as e:
        print("Failed to connect to Blynk, trying again...")

    def __init__(self):
        self.reConnectTimer = 60

    def isAppConnected(self):
        global appConnected
        return appConnected

    def getTimerData(self):
        global timerActive, timerValueSeconds
        return [timerActive, timerValueSeconds]

    def writeDataToServer(self, brewPotTemp=0, chillerInTemp=0, chillerOutTemp=0,
                          gasOn=False, pumpOn=False, targetTemp=0, timeRemaining=0):
        global appConnected
        if appConnected:
            self.blynk.virtual_write(0, brewPotTemp)
            self.blynk.virtual_write(1, chillerInTemp)
            self.blynk.virtual_write(2, chillerOutTemp)
            if gasOn:
                self.blynk.virtual_write(3, 255)
            else:
                self.blynk.virtual_write(3, 0)
            if pumpOn:
                self.blynk.virtual_write(4, 255)
            else:
                self.blynk.virtual_write(4, 0)
            self.blynk.virtual_write(5, targetTemp)
            self.blynk.virtual_write(9, timeRemaining)

    def run(self):
        global appConnected, blynkDisconnectRcvd
        if appConnected:
            # Blynk needs this in main loop 
            self.blynk.run()

            # Clear reconnect timer
            self.reConnectTimer = 0

        # Disconnect received, close socket
        if blynkDisconnectRcvd:
            blynkDisconnectRcvd = False
            self.blynk.disconnect()
            self.blynk.close()
            self.reConnectTimer = 30

        # Try to connect again
        if self.reConnectTimer > 0:
            self.reConnectTimer -= 1
            if self.reConnectTimer == 0:                
                try:
                    self.blynk.disconnect()
                    self.blynk.connect()
                    appConnected = True
                except Exception as e:
                    print("Failed to connect to Blynk, trying again...")
                    self.reConnectTimer = 30
                

