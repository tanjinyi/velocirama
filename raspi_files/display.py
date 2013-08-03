import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import gdata.calendar
import atom
import getopt
import sys
import string
import time
 
import xe 
from feed.date.rfc3339 import tf_from_timestamp 
from datetime import datetime 
from apscheduler.scheduler import Scheduler
import os, random

calendar_service = gdata.calendar.service.CalendarService()
calendar_service.email = '' #your email
calendar_service.password = '' #your password
calendar_service.source = 'Google-Calendar_Python_Sample-1.0'
calendar_service.ProgrammaticLogin()
 
def FullTextQuery(calendar_service, text_query='display'):
    print 'Full text query for events on Primary Calendar: \'%s\'' % ( text_query,)
    query = gdata.calendar.service.CalendarEventQuery('default', 'private', 'full', text_query)
    feed = calendar_service.CalendarQuery(query)
    for i, an_event in enumerate(feed.entry):
        for a_when in an_event.when:
            print "---"
            print an_event.title.text ,"Number:",i,"Event Time:",time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))),"Current Time:",time.strftime('%d-%m-%Y %H:%M')
 
            if time.strftime('%d-%m-%Y %H:%M',time.localtime(tf_from_timestamp(a_when.start_time))) == time.strftime('%d-%m-%Y %H:%M'):
                print "Comparison: Pass"
                print "---"
 
                picfile = random.choice(os.listdir("/home/pi/alarmclock/test_pics/")) #chooses the picture file
                print "File Selected:", picfile
                command ="fim -p -w /home/pi/alarmclock/test_pics/ '"+picfile+"'" #Displays an image
 
                print command
                os.system(command) #runs the bash command
            else:
                print "Comparison:Fail" #the "wake" event's start time != the system's current time
 
def callable_func():
    os.system("clear") #this is more for my benefit and is in no way necesarry
    print "------------start-----------"
    FullTextQuery(calendar_service)
    print "-------------end------------"
 
scheduler = Scheduler(standalone=True)
scheduler.add_interval_job(callable_func,seconds=5)
scheduler.start() #runs the program indefinatly on an interval of 5 seconds
