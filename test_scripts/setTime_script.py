import hw_lib.ds1307_lib as ds1307_lib
from time import *

# Load Library
real_time = ds1307_lib.ds1307(0)

print "Current Time = " + real_time.getDateDs1307()

input_hours = input ("Enter Hours: ")
print ("Hours = " + str(input_hours))

input_minutes = input ("Enter Minutes: ")
print ("Minutes = " + str(input_minutes))

input_seconds = input ("Enter Seconds: ")
print ("Seconds = " + str(input_seconds))

input_dayOfWeek = input ("Enter Day Of Week: ")
print ("Day Of Week = " + str(input_dayOfWeek))

input_dayOfMonth = input ("Enter Day Of Month: ")
print ("Day Of Month = " + str(input_dayOfMonth))

input_months = input ("Enter Month: ")
print ("Months = " + str(input_months))

input_years = input ("Enter Year: ")
input_years = (input_years & 255)
print ("Years = " + str(input_years))

real_time.setDateDs1307(input_seconds,input_minutes,input_hours,input_dayOfWeek,input_dayOfMonth,input_months,input_years)

sleep(1)

print "New Time = " + real_time.getDateDs1307Str()
