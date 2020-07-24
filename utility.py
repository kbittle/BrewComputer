import subprocess

def isRpiA():
    returnValue = False
    processReturnStr = subprocess.check_output(['cat', '/proc/device-tree/model'])

    modelStr = processReturnStr.split('Model')

    if modelStr[1] == 'A':
        returnValue = True

    return returnValue

def isWifiConnected():
    returnValue = False

    processReturnStr = subprocess.check_output(['iwgetid'])
    modelStr = processReturnStr.split('ESSID:')

    # If we have a SSID string, they we are considering ourselves connected to wifi.
    if modelStr[0]:
        print(">> Connected Wifi: " + modelStr[0])
        returnValue = True

    return returnValue

def doesDatabaseExist():
    # TODO
    return True

def get_ip_address():
    strIp = "0.0.0.0"
    try:
        IP = subprocess.check_output(["hostname", "-I"]).split()[0]
        strIp = str(IP)
        print(">> Ip address: " + str(IP))
    except:
        strIp = "Unknown"
    return strIp