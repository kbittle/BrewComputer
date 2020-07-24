import sqlite3

# webBrewData database layout: deviceIndex, rom, description, timestamp, temperature
class sql_database_lib:

    def __init__(self):
        print(">> Before sqlite3 connect")
        #conn = sqlite3.connect('/var/www/temperatureLog.db')
        self.conn = sqlite3.connect('/var/www/homebrewWebDataLog.db')
        self.curs = self.conn.cursor()

        self.curs.execute("SELECT SQLITE_VERSION()")
        print(">> SQLite version: {0}".format(self.curs.fetchone()))

    def add_sensor_to_db(self, deviceRom, deviceDescription):
        # Device ROM id is in the form of an 8 byte array, convert it to a string
        deviceRomStr = '-'.join(map(str,deviceRom))

        # Build select call to look for devices with the same ROM
        selectCmd = "SELECT * FROM brewWebData WHERE rom='{0}'".format(deviceRomStr)
        self.curs.execute(selectCmd)

        deviceWithSameRom = self.curs.fetchone()

        # If a device with that ROM does not exist, create it
        if deviceWithSameRom is None:
            # Find the number of entries in our database
            self.curs.execute("SELECT Count(*) FROM brewWebData")

            # Convert (XX,) into X. Then add 1 since sql doesnt have a zero index
            numberOfRows = int(str(self.curs.fetchone()).replace("(","").replace(",","").replace(")","")) + 1

            # Create the add command
            addCmd = "INSERT INTO brewWebData VALUES({0}, '{1}', '{2}', date('now'), 0)".format(numberOfRows, deviceRomStr, deviceDescription)
            self.curs.execute(addCmd)
            self.conn.commit()
        else:
            print "Sensor Already Exists, re-initializing data"
            
            # Zero out the specified temp sensor
            updateCmd = "UPDATE brewWebData SET temperature=0, timestamp=date('now') WHERE rom=" + deviceRomStr
            self.curs.execute(updateCmd)
            self.conn.commit()

    def update_temperature(self, index, temp):
        # Build update command, were updating based off database indexes
        # might switch to ROM checks later, this is easier
        updateCmd = "UPDATE brewWebData SET temperature={0}, timestamp=date('now') WHERE deviceIndex={1}".format(temp, index)
        self.curs.execute(updateCmd)
        self.conn.commit()

    def print_everything(self):
        for row in self.curs.execute("SELECT * FROM brewWebData"):
            print row

    def close(self):
        self.conn.close()
